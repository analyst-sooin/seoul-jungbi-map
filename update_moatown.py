#!/usr/bin/env python3
"""모아타운 데이터 확장 및 업데이트 스크립트"""

import pandas as pd
import json
import requests
import math
import time

# 기존 데이터 로드
df = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/moatown_expanded_geo.csv', encoding='utf-8-sig')
print(f"기존 모아타운 데이터: {len(df)}개")

# 새로 발견한 모아타운 데이터
new_data = [
    # 최근 확정된 4곳
    {"자치구": "중랑구", "위치": "신내1동493-13", "면적": 0, "세대수": 878, "현황": "확정"},
    {"자치구": "중랑구", "위치": "묵2동243-7", "면적": 0, "세대수": 1826, "현황": "확정"},
    {"자치구": "광진구", "위치": "자양2동649", "면적": 95353, "세대수": 2325, "현황": "확정"},
    # SH참여 모아타운 7곳
    {"자치구": "동작구", "위치": "사당동449", "면적": 0, "세대수": 0, "현황": "SH참여"},
    {"자치구": "송파구", "위치": "잠실동329", "면적": 0, "세대수": 0, "현황": "SH참여"},
    {"자치구": "양천구", "위치": "신월동480-1", "면적": 0, "세대수": 0, "현황": "SH참여"},
    {"자치구": "강남구", "위치": "삼성동84", "면적": 0, "세대수": 0, "현황": "SH참여"},
    {"자치구": "구로구", "위치": "개봉동20", "면적": 0, "세대수": 0, "현황": "SH참여"},
    {"자치구": "구로구", "위치": "개봉2동304", "면적": 0, "세대수": 0, "현황": "SH참여"},
    {"자치구": "구로구", "위치": "개봉2동305", "면적": 0, "세대수": 0, "현황": "SH참여"},
    # 공공기관 참여 10곳 중 추가
    {"자치구": "종로구", "위치": "구기동100-48", "면적": 0, "세대수": 0, "현황": "공공참여"},
    {"자치구": "서대문구", "위치": "홍제동322", "면적": 0, "세대수": 0, "현황": "공공참여"},
    {"자치구": "강서구", "위치": "등촌동520-3", "면적": 0, "세대수": 0, "현황": "공공참여"},
    {"자치구": "동작구", "위치": "노량진동221-24", "면적": 0, "세대수": 0, "현황": "공공참여"},
    {"자치구": "성동구", "위치": "응봉동265", "면적": 0, "세대수": 0, "현황": "공공참여"},
]

# 중복 체크 함수
def is_duplicate(row, df):
    """기존 데이터에 비슷한 위치가 있는지 확인"""
    dong = row["위치"].replace("-", "").replace("동", "")[:3]  # 동 이름 추출
    for _, existing in df.iterrows():
        if row["자치구"] == existing["자치구"]:
            existing_dong = str(existing["위치"]).replace("-", "").replace("동", "")[:3]
            if dong == existing_dong:
                return True
    return False

# 지오코딩 함수 (네이버/카카오 API 없이 동 이름 기반 좌표 사용)
dong_coords = {
    "신내": (37.6107, 127.0931),
    "묵": (37.6102, 127.0778),
    "자양": (37.5360, 127.0936),
    "사당": (37.4850, 126.9704),
    "잠실": (37.5133, 127.1001),
    "삼성": (37.5140, 127.0565),
    "개봉": (37.4946, 126.8562),
    "구기": (37.6090, 126.9573),
    "홍제": (37.5871, 126.9467),
    "등촌": (37.5520, 126.8615),
    "노량진": (37.5126, 126.9421),
    "응봉": (37.5523, 127.0335),
}

def get_coords(row):
    """동 이름에서 좌표 추출"""
    for dong, coords in dong_coords.items():
        if dong in row["위치"]:
            return coords
    return (None, None)

# 새 데이터 추가
added = 0
for row in new_data:
    if not is_duplicate(row, df):
        lat, lng = get_coords(row)
        if lat and lng:
            new_row = {
                "연번": len(df) + 1,
                "자치구": row["자치구"],
                "위치": row["위치"],
                "면적": row["면적"],
                "세대수": row["세대수"],
                "현황": row["현황"],
                "lat": lat,
                "lng": lng
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            added += 1
            print(f"추가: {row['자치구']} {row['위치']}")
        else:
            print(f"좌표 없음: {row['자치구']} {row['위치']}")
    else:
        print(f"중복: {row['자치구']} {row['위치']}")

print(f"\n추가된 모아타운: {added}개")
print(f"최종 모아타운 데이터: {len(df)}개")

# CSV 저장
df.to_csv('/Users/kimwaterman/Desktop/dev/정비구역/moatown_expanded_geo.csv', index=False, encoding='utf-8-sig')
print("CSV 저장 완료")

# GeoJSON 생성 (원형 폴리곤)
def create_circle_polygon(lat, lng, radius_m=200, num_points=32):
    """원형 폴리곤 생성"""
    coords = []
    for i in range(num_points + 1):
        angle = 2 * math.pi * i / num_points
        dx = radius_m * math.cos(angle) / (111320 * math.cos(math.radians(lat)))
        dy = radius_m * math.sin(angle) / 110540
        coords.append([lng + dx, lat + dy])
    return coords

features = []
for _, row in df.iterrows():
    if pd.notna(row['lat']) and pd.notna(row['lng']):
        coords = create_circle_polygon(row['lat'], row['lng'])
        feature = {
            "type": "Feature",
            "properties": {
                "위치": row['위치'],
                "자치구": row['자치구'],
                "면적": str(row['면적']) if pd.notna(row['면적']) and row['면적'] != 0 else "-",
                "세대수": str(int(row['세대수'])) if pd.notna(row['세대수']) and row['세대수'] != 0 else "-",
                "현황": row['현황'],
                "사업유형": "모아타운"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            }
        }
        features.append(feature)

geojson = {"type": "FeatureCollection", "features": features}

with open('/Users/kimwaterman/Desktop/dev/정비구역/moatown_polygon.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False)

print(f"GeoJSON 저장 완료: {len(features)}개 폴리곤")
