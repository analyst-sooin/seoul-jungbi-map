#!/usr/bin/env python3
"""
매물 CSV를 GeoJSON으로 변환
"""

import pandas as pd
import json

# CSV 로드 (cp949 인코딩)
df = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/vl_202603091443.csv', encoding='cp949')

print(f"총 {len(df)}건")
print(f"컬럼: {list(df.columns)}")

# 좌표 있는 데이터만 필터
df_valid = df[df['위도'].notna() & df['경도'].notna()].copy()
print(f"좌표 있는 데이터: {len(df_valid)}건")

# GeoJSON 변환
features = []
for _, row in df_valid.iterrows():
    try:
        lat = float(row['위도'])
        lng = float(row['경도'])

        # 유효한 좌표인지 확인
        if lat < 33 or lat > 43 or lng < 124 or lng > 132:
            continue

        # 가격 포맷
        def format_price(val):
            if pd.isna(val):
                return '-'
            try:
                v = float(val)
                if v >= 10000:
                    return f"{v/10000:.1f}억"
                else:
                    return f"{v:.0f}만"
            except:
                return str(val)

        feature = {
            "type": "Feature",
            "properties": {
                "매물번호": str(row.get('매물번호', '')),
                "주소": str(row.get('주소', '')),
                "감정가": format_price(row.get('감정가', '')),
                "최저가": format_price(row.get('최저가', '')),
                "비율": f"{row.get('비율', 0):.0f}%" if pd.notna(row.get('비율')) else '-',
                "전용평수": f"{row.get('전용평수', 0):.1f}평" if pd.notna(row.get('전용평수')) else '-',
                "매각기일": str(row.get('매각기일', ''))[:10] if pd.notna(row.get('매각기일')) else '-',
                "유찰횟수": int(row.get('유찰횟수', 0)) if pd.notna(row.get('유찰횟수')) else 0,
                "정비구역명": str(row.get('정비구역명', '')) if pd.notna(row.get('정비구역명')) else '',
                "용도": str(row.get('주용도군', '')) if pd.notna(row.get('주용도군')) else '',
                "시도": str(row.get('시도', '')) if pd.notna(row.get('시도')) else ''
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]
            }
        }
        features.append(feature)
    except Exception as e:
        continue

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# 저장
with open('/Users/kimwaterman/Desktop/dev/정비구역/maemul.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False)

print(f"\nGeoJSON 저장 완료: {len(features)}건")

# 정비구역 내 매물 통계
in_jungbi = [f for f in features if f['properties']['정비구역명']]
print(f"정비구역 내 매물: {len(in_jungbi)}건")

# 시도별 통계
sido_count = {}
for f in features:
    sido = f['properties']['시도']
    sido_count[sido] = sido_count.get(sido, 0) + 1

print("\n시도별 현황:")
for k, v in sorted(sido_count.items(), key=lambda x: -x[1])[:10]:
    print(f"  {k}: {v}건")
