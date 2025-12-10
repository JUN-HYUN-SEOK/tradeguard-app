# 🛡️ TradeGuard (트레이드가드)

## 지능형 수입신고 리스크 분석 솔루션

TradeGuard는 **관세법인 우신**에서 개발한 수입신고 데이터의 리스크를 분석하는 스트림릿 기반 웹 애플리케이션입니다.

### ✨ 주요 기능

#### 📊 14가지 리스크 분석
1. **8% 환급 검토** - 관세율 8% 이상 A세율 적용 건
2. **0% 세율 위험** - 저율 적용 건 중 특수세율 미적용 건
3. **세율 위험** - 동일 규격에 다른 HS코드 적용 건
4. **단가 위험** - Z-Score 기반 통계적 이상치 탐지
5. **내국세구분 누락** - 주류(세번 22) 수입 시 내국세부호 누락
6. **수입요건 불일치** - 동일 규격에 상이한 수입요건 적용
7. **F세율 적용** - FTA 협정세율 적용 건 선별
8. **FTA 기회 발굴** - FTA 미적용 건 중 적용 가능 건
9. **저가신고 의심** - 단가 $10 이하 저가 신고 건
10. **통화단위 불일치** - 거래처별 통화단위 혼용 건
11. **국가별 통화단위 불일치** - 희귀 통화 사용 건 (빈도 기반)
12. **특수거래 구분** - 재수출·감면 등 특수 거래 건
13. **무상운임 누락** - GN(무상) 거래 시 운임 누락 건
14. **용도세율 적용** - C세율(용도세율) 적용 건

#### 📈 데이터 시각화
- **대시보드** - 주요 지표를 한눈에 확인
- **파이차트** - Risk 유형별 분포
- **라인차트** - 월별 수입신고 추이
- **산점도** - 단가 이상치 분포

#### 📥 다중 포맷 보고서
- **Excel** - 분석 결과 + 검증방법 시트
- **Word** - 요약 보고서
- **HTML** - 웹 기반 인터랙티브 보고서

### 🚀 로컬 실행 방법

1. **저장소 클론**
```bash
git clone https://github.com/[your-username]/[your-repo-name].git
cd [your-repo-name]
```

2. **패키지 설치**
```bash
pip install -r requirements.txt
```

3. **앱 실행**
```bash
streamlit run trade_guard_app.py
```

4. 브라우저에서 `http://localhost:8501` 접속

### 🌐 Streamlit Cloud 배포

1. GitHub에 코드 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud) 접속
3. `New app` 클릭
4. 저장소 선택 및 `trade_guard_app.py` 지정
5. `Deploy!` 클릭

### 📋 사용 방법

1. **파일 업로드**: Excel 또는 CSV 형식의 수입신고 데이터 업로드
2. **분석 옵션 선택**: 왼쪽 사이드바에서 원하는 분석 항목 선택
3. **분석 시작**: "🔍 분석 시작" 버튼 클릭
4. **결과 확인**: 탭별로 분석 결과 확인
5. **보고서 다운로드**: Excel, Word, HTML 형식으로 다운로드

### 📊 지원 데이터 형식

- **파일 형식**: Excel (.xlsx, .xls), CSV (.csv)
- **필수 컬럼**: 
  - 수입신고번호
  - 세율구분
  - 관세실행세율
  - 수리일자
  - HS코드(세번부호)
- **권장 컬럼**: 규격1, 단가, 금액, 거래처, 통화단위 등

### 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Export**: OpenPyXL, python-docx, xlsxwriter

### 👨‍💻 개발자

**Made by Mr.jeon**  
관세법인 우신

### 📄 라이선스

This project is proprietary software developed by 관세법인 우신.

### 🤝 지원 및 문의

문의사항이 있으시면 관세법인 우신으로 연락 주시기 바랍니다.

---

© 2024 관세법인 우신. All rights reserved.
