# 정비구역 프로젝트 핸드오프

## 현재 상태 (2026.03.09 최신)

### 완성된 데이터 파일

| 파일 | 설명 | 건수 |
|------|------|------|
| `jungbi_active.geojson` | 정비구역 폴리곤 (활성만) | 876개 |
| `sintong_polygon.geojson` | 신통기획 원형 폴리곤 | 83개 |
| `moatown_polygon.geojson` | 모아타운 원형 폴리곤 | 61개 |
| `maemul.geojson` | 매물 포인트 | 6,630개 |
| `vl_full_matched.csv` | 매물 + 정비구역/모아타운/신통기획 매칭 | 6,686건 |
| `viewer.html` | Leaflet 지도 뷰어 | - |

### 매물 매칭 현황

| 구분 | 매물 수 |
|------|---------|
| 정비구역 내 | 42건 |
| 모아타운 내 | 72건 |
| 신통기획 내 | 48건 |

### vl_full_matched.csv 컬럼

원본 컬럼 + 추가된 컬럼:
- `정비구역명_매칭`: 폴리곤 기반 정비구역명
- `정비단계`: 해당 구역 진행단계
- `구역유형_매칭`: 재개발/재건축/촉진 등
- `모아타운`: 모아타운 위치 (자치구 + 동)
- `모아현황`: 모아타운 추진현황
- `신통구역`: 신통기획 구역명 (자치구 + 구역명)
- `신통단계`: 신통기획 추진단계

### 뷰어 기능

```bash
cd /Users/kimwaterman/Desktop/dev/정비구역
python3 -m http.server 8888
# http://localhost:8888/viewer.html
```

**체크박스 레이어:**
- 정비구역 (876개) - 단계별 색상
- 신통기획 (83개) - 청록색 점선
- 모아타운 (61개) - 연두색 점선
- 매물 (6,630개) - 색상별 구분
  - 녹색: 정비구역 내 (42건)
  - 청록: 신통기획 내 (48건)
  - 연두: 모아타운 내 (72건)
  - 핑크: 일반 매물

---

## 완료된 작업 (2026.03.09)

### 1. 모아타운 데이터 확장
- 기존: 50개소
- 현재: 61개소
- 추가 출처: 서울시 미디어허브, 공공기관 참여 모아타운, SH참여 모아타운

### 2. 신통기획 매물 매칭 추가
- sintong_geocoded.csv 기반 500m 반경 매칭
- 48건 매칭 완료
- vl_full_matched.csv에 `신통구역`, `신통단계` 컬럼 추가

### 3. 모아타운 매물 재매칭
- 확장된 61개소 기준 재매칭
- 46건 → 72건으로 증가

---

## 미완료 작업

### 1. 모아타운 추가 확장 가능
- 현재: 61개소
- 전체: 122개소 (서울시 공식)
- **다운로드 필요**: https://news.seoul.go.kr/citybuild/archives/516139
  - "모아타운 관리계획 추진현황.hwp" 파일

### 2. GitHub Pages 배포
- `gh auth login` 필요
- 그 후 gh-pages 브랜치 생성 및 배포

---

## 주요 파일 경로

```
/Users/kimwaterman/Desktop/dev/정비구역/
├── viewer.html                 # 지도 뷰어
├── jungbi_active.geojson       # 정비구역 폴리곤
├── sintong_polygon.geojson     # 신통기획 폴리곤
├── moatown_polygon.geojson     # 모아타운 폴리곤
├── maemul.geojson              # 매물 포인트
├── vl_full_matched.csv         # 매물 + 매칭 데이터
├── sintong_geocoded.csv        # 신통기획 좌표
├── moatown_expanded_geo.csv    # 모아타운 좌표
├── update_moatown.py           # 모아타운 업데이트 스크립트
├── rematch_all.py              # 매물 매칭 스크립트
└── HANDOFF.md                  # 이 파일
```

## DB 정보

- PostgreSQL: 172.31.3.129:5432 / skykey_db
- 좌표계: WGS84 (EPSG:4326)

---

## 재시작 후 이어서 할 작업

```
"HANDOFF.md 읽고 이어서 진행해줘. 모아타운 122개소 전체 확보하거나 GitHub Pages 배포해줘"
```
