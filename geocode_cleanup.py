#!/usr/bin/env python3
"""
클린업 데이터의 주소를 좌표로 변환 (Nominatim 사용)
"""

import pandas as pd
import requests
import time
import json

def geocode_nominatim(address):
    """Nominatim (OpenStreetMap) 지오코딩"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "kr"
    }
    headers = {"User-Agent": "JungbiProject/1.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        pass

    return None, None

def main():
    print("클린업 데이터 지오코딩 시작 (Nominatim)...")
    print("※ API 제한으로 인해 약 20분 소요됩니다.\n")

    # 데이터 로드
    df = pd.read_csv('/Users/kimwaterman/Desktop/dev/정비구역/cleanup_status.csv', encoding='utf-8-sig')
    print(f"총 {len(df)}건 처리 예정\n")

    # 결과 저장용
    results = []
    success_count = 0
    fail_count = 0

    for idx, row in df.iterrows():
        gu = row['자치구']
        address = str(row['대표지번']).strip()
        name = row['사업장명']
        biz_type = row['사업구분']
        stage = row['진행단계']

        # 주소 구성: "서울 마포구 아현동 613-10"
        full_address = f"서울 {gu} {address}"

        # 지오코딩
        lat, lng = geocode_nominatim(full_address)

        # 실패시 동 이름만으로 재시도
        if lat is None and address:
            dong = address.split()[0] if ' ' in address else address.split('-')[0]
            simple_address = f"서울 {gu} {dong}"
            lat, lng = geocode_nominatim(simple_address)
            time.sleep(1)

        if lat:
            success_count += 1
        else:
            fail_count += 1

        results.append({
            '자치구': gu,
            '사업구분': biz_type,
            '사업장명': name,
            '대표지번': address,
            '진행단계': stage,
            'lat': lat,
            'lng': lng
        })

        # 진행상황 출력
        if (idx + 1) % 100 == 0:
            print(f"  {idx + 1}/{len(df)} 완료 (성공: {success_count}, 실패: {fail_count})")

        # API 제한 방지 (1초 대기)
        time.sleep(1)

    # 결과 저장
    result_df = pd.DataFrame(results)
    result_df.to_csv('/Users/kimwaterman/Desktop/dev/정비구역/cleanup_geocoded.csv', index=False, encoding='utf-8-sig')

    # 통계
    success = result_df[result_df['lat'].notna()]
    failed = result_df[result_df['lat'].isna()]

    print(f"\n=== 지오코딩 결과 ===")
    print(f"성공: {len(success)}건")
    print(f"실패: {len(failed)}건")

    # GeoJSON 생성
    features = []
    for _, row in success.iterrows():
        feature = {
            "type": "Feature",
            "properties": {
                "자치구": row['자치구'],
                "사업구분": row['사업구분'],
                "사업장명": row['사업장명'],
                "대표지번": row['대표지번'],
                "진행단계": row['진행단계'],
                "data_type": "point"  # 폴리곤이 아닌 점 데이터
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row['lng'], row['lat']]
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('/Users/kimwaterman/Desktop/dev/정비구역/cleanup_points.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"\nGeoJSON 저장: cleanup_points.geojson ({len(features)}개)")

    # 사업구분별 통계
    print("\n=== 사업구분별 현황 ===")
    for biz_type in sorted(success['사업구분'].unique()):
        count = len(success[success['사업구분'] == biz_type])
        print(f"  {biz_type}: {count}건")

    print("\n완료!")

if __name__ == '__main__':
    main()
