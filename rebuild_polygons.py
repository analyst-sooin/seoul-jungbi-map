#!/usr/bin/env python3
"""면적 기반 사각형 폴리곤 생성"""

import json
import math
import pandas as pd

def create_rect_polygon(lat, lng, area_m2):
    """면적 기반 사각형 폴리곤 생성"""
    # 면적에서 한 변의 길이 계산 (정사각형 가정)
    side = math.sqrt(area_m2) if area_m2 > 0 else 200
    half_side = side / 2

    # 위도/경도 변환 (미터 -> 도)
    lat_diff = half_side / 110540
    lng_diff = half_side / (111320 * math.cos(math.radians(lat)))

    # 사각형 좌표 (시계방향)
    coords = [
        [lng - lng_diff, lat + lat_diff],  # 좌상
        [lng + lng_diff, lat + lat_diff],  # 우상
        [lng + lng_diff, lat - lat_diff],  # 우하
        [lng - lng_diff, lat - lat_diff],  # 좌하
        [lng - lng_diff, lat + lat_diff],  # 닫기
    ]
    return coords

# 3080+ 데이터 재생성
data_3080 = [
    {"자치구": "도봉구", "구역명": "3080+방학역", "위치": "도봉2동 622번지", "면적": 8428, "세대수": 420, "단계": "이주중", "lat": 37.6686, "lng": 127.0466},
    {"자치구": "도봉구", "구역명": "3080+쌍문역동측", "위치": "창1동 663-2번지", "면적": 15902, "세대수": 639, "단계": "이주중", "lat": 37.6529, "lng": 127.0349},
    {"자치구": "도봉구", "구역명": "3080+쌍문역서측", "위치": "쌍문3동 138-1번지", "면적": 41325, "세대수": 1404, "단계": "보상준비", "lat": 37.6529, "lng": 127.0249},
    {"자치구": "도봉구", "구역명": "3080+창2동주민센터", "위치": "창2동 585-90번지", "면적": 15412, "세대수": 584, "단계": "설계준비", "lat": 37.6560, "lng": 127.0380},
    {"자치구": "금천구", "구역명": "3080+독산역", "위치": "독산동", "면적": 25000, "세대수": 800, "단계": "추진중", "lat": 37.4673, "lng": 126.8955},
    {"자치구": "금천구", "구역명": "3080+시흥대로", "위치": "시흥동", "면적": 30000, "세대수": 950, "단계": "추진중", "lat": 37.4507, "lng": 126.9085},
    {"자치구": "영등포구", "구역명": "3080+신길역", "위치": "신길동", "면적": 28000, "세대수": 900, "단계": "추진중", "lat": 37.5065, "lng": 126.9119},
    {"자치구": "은평구", "구역명": "3080+불광역", "위치": "불광동", "면적": 35000, "세대수": 1100, "단계": "추진중", "lat": 37.6194, "lng": 126.9354},
    {"자치구": "은평구", "구역명": "3080+응암역", "위치": "응암동", "면적": 22000, "세대수": 700, "단계": "추진중", "lat": 37.5926, "lng": 126.9216},
    {"자치구": "강북구", "구역명": "3080+미아역", "위치": "미아동", "면적": 32000, "세대수": 1000, "단계": "추진중", "lat": 37.6220, "lng": 127.0209},
    {"자치구": "강북구", "구역명": "3080+수유역", "위치": "수유동", "면적": 28000, "세대수": 880, "단계": "추진중", "lat": 37.6365, "lng": 127.0043},
    {"자치구": "동대문구", "구역명": "3080+청량리역", "위치": "전농동", "면적": 45000, "세대수": 1500, "단계": "추진중", "lat": 37.5806, "lng": 127.0554},
    {"자치구": "동대문구", "구역명": "3080+답십리역", "위치": "답십리동", "면적": 38000, "세대수": 1200, "단계": "추진중", "lat": 37.5700, "lng": 127.0546},
    {"자치구": "용산구", "구역명": "3080+효창공원앞역", "위치": "효창동", "면적": 52000, "세대수": 2483, "단계": "추진중", "lat": 37.5389, "lng": 126.9611},
    {"자치구": "서대문구", "구역명": "3080+홍제역", "위치": "홍제동", "면적": 25000, "세대수": 800, "단계": "추진중", "lat": 37.5871, "lng": 126.9467},
    {"자치구": "강서구", "구역명": "3080+화곡2동주민센터", "위치": "화곡동", "면적": 240310, "세대수": 5973, "단계": "예정지구지정", "lat": 37.5421, "lng": 126.8441},
    {"자치구": "중랑구", "구역명": "3080+망우역", "위치": "망우동", "면적": 30000, "세대수": 950, "단계": "추진중", "lat": 37.6008, "lng": 127.1076},
    {"자치구": "중랑구", "구역명": "3080+상봉역", "위치": "상봉동", "면적": 35000, "세대수": 1100, "단계": "추진중", "lat": 37.5963, "lng": 127.0854},
    {"자치구": "관악구", "구역명": "3080+신림역", "위치": "신림동", "면적": 42000, "세대수": 1350, "단계": "추진중", "lat": 37.4782, "lng": 126.9518},
    {"자치구": "구로구", "구역명": "3080+개봉역", "위치": "개봉동", "면적": 28000, "세대수": 900, "단계": "추진중", "lat": 37.4946, "lng": 126.8562},
]

# 3080+ GeoJSON 생성
features_3080 = []
for row in data_3080:
    coords = create_rect_polygon(row['lat'], row['lng'], row['면적'])
    feature = {
        "type": "Feature",
        "properties": {
            "DGM_NM": row['구역명'],
            "자치구": row['자치구'],
            "위치": row['위치'],
            "면적": row['면적'],
            "세대수": row['세대수'],
            "진행단계": row['단계'],
            "구역유형": "도심공공주택복합사업"
        },
        "geometry": {"type": "Polygon", "coordinates": [coords]}
    }
    features_3080.append(feature)

with open('/Users/kimwaterman/Desktop/dev/정비구역/dosim3080_polygon.geojson', 'w', encoding='utf-8') as f:
    json.dump({"type": "FeatureCollection", "features": features_3080}, f, ensure_ascii=False)
print(f"3080+ GeoJSON: {len(features_3080)}개 (사각형 폴리곤)")

# 신통기획 GeoJSON 재생성
sintong = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/sintong_geocoded.csv', encoding='utf-8-sig')
features_sintong = []
for _, row in sintong.iterrows():
    if pd.isna(row['lat']) or pd.isna(row['lng']):
        continue
    area = row['면적'] if pd.notna(row['면적']) else 50000
    coords = create_rect_polygon(row['lat'], row['lng'], area)
    feature = {
        "type": "Feature",
        "properties": {
            "구역명": row['구역명'],
            "자치구": row['자치구'],
            "면적": str(int(area)) if area else "-",
            "세대수": str(int(row['세대수'])) if pd.notna(row['세대수']) else "-",
            "추진단계": row['추진단계'] if pd.notna(row['추진단계']) else "-"
        },
        "geometry": {"type": "Polygon", "coordinates": [coords]}
    }
    features_sintong.append(feature)

with open('/Users/kimwaterman/Desktop/dev/정비구역/sintong_polygon.geojson', 'w', encoding='utf-8') as f:
    json.dump({"type": "FeatureCollection", "features": features_sintong}, f, ensure_ascii=False)
print(f"신통기획 GeoJSON: {len(features_sintong)}개 (사각형 폴리곤)")

# 모아타운 GeoJSON 재생성
moatown = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/moatown_expanded_geo.csv', encoding='utf-8-sig')
features_moatown = []
for _, row in moatown.iterrows():
    if pd.isna(row['lat']) or pd.isna(row['lng']):
        continue
    area = row['면적'] if pd.notna(row['면적']) and row['면적'] > 0 else 30000
    coords = create_rect_polygon(row['lat'], row['lng'], area)
    feature = {
        "type": "Feature",
        "properties": {
            "위치": row['위치'],
            "자치구": row['자치구'],
            "면적": str(int(area)) if area else "-",
            "세대수": str(int(row['세대수'])) if pd.notna(row['세대수']) and row['세대수'] > 0 else "-",
            "현황": row['현황'] if pd.notna(row['현황']) else "-"
        },
        "geometry": {"type": "Polygon", "coordinates": [coords]}
    }
    features_moatown.append(feature)

with open('/Users/kimwaterman/Desktop/dev/정비구역/moatown_polygon.geojson', 'w', encoding='utf-8') as f:
    json.dump({"type": "FeatureCollection", "features": features_moatown}, f, ensure_ascii=False)
print(f"모아타운 GeoJSON: {len(features_moatown)}개 (사각형 폴리곤)")

# jungbi_active.geojson에서 3080+ 제거 (별도 레이어로 관리)
with open('/Users/kimwaterman/Desktop/dev/정비구역/jungbi_area.geojson') as f:
    jungbi = json.load(f)

# 활성 구역만 필터링 (기존 로직 유지)
active_features = [f for f in jungbi['features'] if '해제' not in str(f['properties'].get('DGM_NM', '')) and '직권해제' not in str(f['properties'].get('DGM_NM', ''))]
print(f"정비구역: {len(active_features)}개")

with open('/Users/kimwaterman/Desktop/dev/정비구역/jungbi_active.geojson', 'w', encoding='utf-8') as f:
    json.dump({"type": "FeatureCollection", "features": active_features}, f, ensure_ascii=False)
