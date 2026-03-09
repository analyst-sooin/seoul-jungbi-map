#!/usr/bin/env python3
"""
아실(asil.kr) 정비사업 데이터 수집 스크립트
네트워크 요청을 가로채서 데이터 수집
"""

import json
import time
from playwright.sync_api import sync_playwright

def scrape_asil():
    print("아실 데이터 수집 시작...")

    all_data = []

    def handle_response(response):
        """네트워크 응답 가로채기"""
        if 'data_redevelop.jsp' in response.url:
            try:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    print(f"  API 응답 캡처: {len(data)}건")
                    all_data.extend(data)
            except:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()

        # 네트워크 응답 가로채기 설정
        page.on('response', handle_response)

        # 아실 지도 페이지 접속
        print("아실 지도 페이지 접속 중...")
        page.goto('https://asil.kr/map', wait_until='networkidle', timeout=60000)
        time.sleep(5)

        print(f"현재까지 수집: {len(all_data)}건")

        # 지도 이동하며 데이터 수집
        print("지도 이동하며 추가 데이터 수집 중...")

        # 서울 각 지역 좌표
        regions = [
            (37.57, 126.98),  # 종로/중구
            (37.52, 126.92),  # 마포/용산
            (37.50, 127.03),  # 강남/서초
            (37.55, 127.08),  # 광진/성동
            (37.60, 127.02),  # 성북/동대문
            (37.64, 126.92),  # 은평/서대문
            (37.48, 126.88),  # 금천/관악
            (37.53, 126.85),  # 양천/강서
            (37.50, 126.95),  # 동작/영등포
            (37.58, 127.08),  # 중랑/노원
            (37.65, 127.05),  # 노원/도봉
            (37.47, 127.05),  # 송파/강동
            (37.45, 126.90),  # 구로/금천
        ]

        for lat, lng in regions:
            # JavaScript로 지도 이동
            try:
                page.evaluate(f'''
                    if (typeof kakao !== 'undefined' && kakao.maps) {{
                        var map = document.querySelector('#map');
                        if (map && map.__map__) {{
                            map.__map__.setCenter(new kakao.maps.LatLng({lat}, {lng}));
                        }}
                    }}
                ''')
            except:
                pass

            # 마우스로 지도 드래그 시뮬레이션
            page.mouse.move(960, 540)
            page.mouse.down()
            page.mouse.move(960 + (lng - 126.98) * 1000, 540 + (37.55 - lat) * 1000)
            page.mouse.up()

            time.sleep(2)
            print(f"  위치 ({lat:.2f}, {lng:.2f}) - 현재 {len(all_data)}건")

        # 추가 대기
        time.sleep(3)

        browser.close()

    # 중복 제거
    unique_data = {}
    for item in all_data:
        key = item.get('key', '')
        if key and key not in unique_data:
            unique_data[key] = item

    result = list(unique_data.values())
    print(f"\n총 {len(result)}건 수집 완료")

    if len(result) == 0:
        print("\n데이터 수집 실패. 직접 캡처가 필요합니다.")
        return []

    # 저장
    output_path = '/Users/kimwaterman/Desktop/dev/정비구역/asil_full.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {output_path}")

    # 통계
    print("\n=== 수집 데이터 통계 ===")
    types = {}
    for item in result:
        title = item.get('title', '')
        if '재개발' in title:
            t = '재개발'
        elif '재건축' in title:
            t = '재건축'
        elif '모아타운' in title:
            t = '모아타운'
        elif '가로주택' in title:
            t = '가로주택'
        else:
            t = '기타'
        types[t] = types.get(t, 0) + 1

    for k, v in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}건")

    return result

if __name__ == '__main__':
    scrape_asil()
