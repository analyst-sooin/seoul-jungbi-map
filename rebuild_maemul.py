#!/usr/bin/env python3
"""매물 GeoJSON 재생성 - 상세 정보 포함"""

import pandas as pd
import json

# 데이터 로드
maemul = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/vl_full_matched.csv', encoding='utf-8-sig')
print(f"매물: {len(maemul)}건")

# 매물 GeoJSON 생성
features = []
for _, row in maemul.iterrows():
    if pd.isna(row.get('위도')) or pd.isna(row.get('경도')):
        continue

    # 매칭 여부 확인
    in_jungbi = bool(row.get('정비구역명_매칭')) and str(row.get('정비구역명_매칭')) not in ['', 'nan']
    in_moatown = bool(row.get('모아타운')) and str(row.get('모아타운')) not in ['', 'nan']
    in_sintong = bool(row.get('신통구역')) and str(row.get('신통구역')) not in ['', 'nan']

    def safe_str(val, default=''):
        if pd.isna(val) or str(val) in ['nan', 'None']:
            return default
        return str(val)

    def safe_num(val, default=''):
        if pd.isna(val):
            return default
        try:
            return f"{float(val):,.0f}"
        except:
            return str(val)

    feature = {
        "type": "Feature",
        "properties": {
            "매물번호": safe_str(row.get('매물번호')),
            "주소": safe_str(row.get('나머지주소')),
            "시구": safe_str(row.get('시구')),
            "동": safe_str(row.get('동1')),
            "감정가": safe_num(row.get('감정가')),
            "최저가": safe_num(row.get('최저가')),
            "비율": safe_str(row.get('비율')),
            "전용면적": safe_str(row.get('전용면적')),
            "전용평수": safe_str(row.get('전용평수')),
            "유찰횟수": safe_str(row.get('유찰횟수')),
            "매각기일": safe_str(row.get('매각기일')),
            "이용상태": safe_str(row.get('이용상태')),
            "공시가격": safe_num(row.get('공시가격')),
            "최근실거래가": safe_num(row.get('최근실거래가')),
            "정비구역": safe_str(row.get('정비구역명_매칭')),
            "정비단계": safe_str(row.get('정비단계')),
            "구역유형": safe_str(row.get('구역유형_매칭')),
            "모아타운": safe_str(row.get('모아타운')),
            "모아현황": safe_str(row.get('모아현황')),
            "신통구역": safe_str(row.get('신통구역')),
            "신통단계": safe_str(row.get('신통단계')),
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

# 통계
jungbi = sum(1 for f in features if f['properties']['in_jungbi'])
moatown = sum(1 for f in features if f['properties']['in_moatown'])
sintong = sum(1 for f in features if f['properties']['in_sintong'])
print(f"정비구역 내: {jungbi}건")
print(f"모아타운 내: {moatown}건")
print(f"신통기획 내: {sintong}건")
