#!/usr/bin/env python3
"""매물-정비구역/모아타운/신통기획 재매칭 스크립트"""

import pandas as pd
import json
import math

# 데이터 로드
print("데이터 로딩...")
maemul = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/vl_full_matched.csv', encoding='utf-8-sig')
sintong = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/sintong_geocoded.csv', encoding='utf-8-sig')
moatown = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/moatown_expanded_geo.csv', encoding='utf-8-sig')

print(f"매물: {len(maemul)}건")
print(f"신통기획: {len(sintong)}개")
print(f"모아타운: {len(moatown)}개")

# 좌표 컬럼 확인
print(f"매물 좌표 컬럼: '위도', '경도'")
valid_coords = maemul['위도'].notna() & maemul['경도'].notna()
print(f"좌표 있는 매물: {valid_coords.sum()}건")

# 거리 계산 함수 (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    """두 지점 간 거리 (미터)"""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

# 신통기획 매칭 (반경 500m 내)
print("\n신통기획 매칭 중...")
sintong_matches = []
sintong_stages = []

for idx, row in maemul.iterrows():
    if pd.isna(row.get('위도')) or pd.isna(row.get('경도')):
        sintong_matches.append('')
        sintong_stages.append('')
        continue

    best_match = ''
    best_stage = ''
    min_dist = float('inf')

    for _, s in sintong.iterrows():
        if pd.isna(s['lat']) or pd.isna(s['lng']):
            continue
        dist = haversine(row['위도'], row['경도'], s['lat'], s['lng'])
        if dist < 500 and dist < min_dist:  # 500m 반경
            min_dist = dist
            best_match = f"{s['자치구']} {s['구역명']}"
            best_stage = s['추진단계']

    sintong_matches.append(best_match)
    sintong_stages.append(best_stage)

maemul['신통구역'] = sintong_matches
maemul['신통단계'] = sintong_stages

sintong_count = sum(1 for x in sintong_matches if x)
print(f"신통기획 내 매물: {sintong_count}건")

# 모아타운 재매칭 (반경 300m 내)
print("\n모아타운 재매칭 중...")
moatown_matches = []
moatown_stages = []

for idx, row in maemul.iterrows():
    if pd.isna(row.get('위도')) or pd.isna(row.get('경도')):
        moatown_matches.append('')
        moatown_stages.append('')
        continue

    best_match = ''
    best_stage = ''
    min_dist = float('inf')

    for _, m in moatown.iterrows():
        if pd.isna(m['lat']) or pd.isna(m['lng']):
            continue
        dist = haversine(row['위도'], row['경도'], m['lat'], m['lng'])
        if dist < 300 and dist < min_dist:  # 300m 반경
            min_dist = dist
            best_match = f"{m['자치구']} {m['위치']}"
            best_stage = m['현황']

    moatown_matches.append(best_match)
    moatown_stages.append(best_stage)

maemul['모아타운'] = moatown_matches
maemul['모아현황'] = moatown_stages

moatown_count = sum(1 for x in moatown_matches if x)
print(f"모아타운 내 매물: {moatown_count}건")

# 결과 저장
maemul.to_csv('/Users/kimwaterman/Desktop/dev/정비구역/vl_full_matched.csv', index=False, encoding='utf-8-sig')
print(f"\nCSV 저장 완료: vl_full_matched.csv")

# 매물 GeoJSON 업데이트
print("\n매물 GeoJSON 업데이트 중...")
features = []
for _, row in maemul.iterrows():
    if pd.isna(row.get('위도')) or pd.isna(row.get('경도')):
        continue

    # 매칭 여부 확인
    in_jungbi = bool(row.get('정비구역명_매칭')) and str(row.get('정비구역명_매칭')) != 'nan'
    in_moatown = bool(row.get('모아타운')) and str(row.get('모아타운')) != ''
    in_sintong = bool(row.get('신통구역')) and str(row.get('신통구역')) != ''

    feature = {
        "type": "Feature",
        "properties": {
            "물건명": str(row.get('나머지주소', '')),
            "매물가": str(row.get('최저가', '')),
            "전용면적": str(row.get('전용면적', '')),
            "정비구역": str(row.get('정비구역명_매칭', '')) if pd.notna(row.get('정비구역명_매칭')) else '',
            "정비단계": str(row.get('정비단계', '')) if pd.notna(row.get('정비단계')) else '',
            "모아타운": str(row.get('모아타운', '')) if row.get('모아타운') else '',
            "모아현황": str(row.get('모아현황', '')) if row.get('모아현황') else '',
            "신통구역": str(row.get('신통구역', '')) if row.get('신통구역') else '',
            "신통단계": str(row.get('신통단계', '')) if row.get('신통단계') else '',
            "in_jungbi": in_jungbi,
            "in_moatown": in_moatown,
            "in_sintong": in_sintong
        },
        "geometry": {
            "type": "Point",
            "coordinates": [row['경도'], row['위도']]
        }
    }
    features.append(feature)

geojson = {"type": "FeatureCollection", "features": features}
with open('/Users/kimwaterman/Desktop/dev/정비구역/maemul.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False)

print(f"매물 GeoJSON 저장 완료: {len(features)}개")

# 최종 통계
print("\n=== 최종 매칭 현황 ===")
jungbi_count = sum(1 for x in maemul['정비구역명_매칭'] if pd.notna(x) and str(x) != '')
print(f"정비구역 내 매물: {jungbi_count}건")
print(f"모아타운 내 매물: {moatown_count}건")
print(f"신통기획 내 매물: {sintong_count}건")
