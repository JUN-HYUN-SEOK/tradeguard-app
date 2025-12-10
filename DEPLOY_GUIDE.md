# 🚀 TradeGuard GitHub & Streamlit Cloud 배포 가이드

## 📋 배포 전 체크리스트

### 필수 파일 (✅ 이미 있음)
- ✅ `trade_guard_app.py` - 메인 앱
- ✅ `requirements.txt` - 패키지 목록
- ✅ `usage_rate_hsk.csv` - 용도세율 HSK 데이터
- ✅ `logo.png` - 로고 이미지
- ✅ `.gitignore` - Git 제외 파일
- ✅ `README.md` - 프로젝트 설명

### 제외할 파일
- ❌ `fix_file.py`, `fix_complete.py` - 수정용 스크립트
- ❌ `trade_guard_app_backup.py` - 백업 파일
- ❌ `__pycache__/` - 파이썬 캐시
- ❌ `SHEETS_SUMMARY.md` - 내부 문서 (선택)

---

## 1️⃣ GitHub 레포지토리 생성

### 1-1. GitHub 접속
1. https://github.com 접속
2. 로그인
3. 우측 상단 **+** 버튼 → **New repository** 클릭

### 1-2. 레포지토리 설정
```
Repository name: tradeguard-app
Description: 지능형 수입신고 리스크 분석 솔루션
[ ] Public ← 선택 (Streamlit Cloud 무료 배포는 Public만 가능)
[✓] Add a README file ← 체크 해제 (이미 있음)
```

**Create repository** 클릭!

---

## 2️⃣ Git 초기화 및 커밋

### 2-1. PowerShell에서 프로젝트 폴더로 이동
```powershell
cd "C:\Users\PC\OneDrive\Desktop\python\01.report\안티그래피티v2"
```

### 2-2. Git 초기화
```powershell
git init
```

### 2-3. 불필요한 파일 삭제 (선택사항)
```powershell
Remove-Item fix_file.py, fix_complete.py, trade_guard_app_backup.py
```

### 2-4. Git 설정 (처음 한 번만)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2-5. 파일 추가 및 커밋
```powershell
# 모든 파일 스테이징
git add .

# 커밋
git commit -m "Initial commit: TradeGuard 수입신고 분석 앱"
```

---

## 3️⃣ GitHub에 푸시

### 3-1. 원격 저장소 연결
GitHub에서 생성한 레포지토리 URL을 사용:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/tradeguard-app.git
```

**YOUR_USERNAME**을 본인의 GitHub 사용자명으로 변경!

### 3-2. 메인 브랜치 이름 변경
```powershell
git branch -M main
```

### 3-3. GitHub에 푸시
```powershell
git push -u origin main
```

**인증 요청 시:**
- GitHub 사용자명 입력
- **비밀번호 대신 Personal Access Token 사용**

### 3-4. Personal Access Token 생성 (필요시)
1. GitHub → 우측 상단 프로필 → **Settings**
2. 좌측 맨 아래 **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Note: "tradeguard-deploy"
6. Expiration: 90 days
7. Scopes: ✅ **repo** 체크
8. **Generate token** 클릭
9. 생성된 토큰 복사 (한 번만 표시됨!)

---

## 4️⃣ Streamlit Cloud 배포

### 4-1. Streamlit Cloud 접속
1. https://share.streamlit.io 접속
2. **Sign up** 또는 **Log in**
3. **GitHub 계정으로 로그인** 선택

### 4-2. 앱 배포
1. 우측 상단 **New app** 클릭
2. 설정:
   ```
   Repository: YOUR_USERNAME/tradeguard-app
   Branch: main
   Main file path: trade_guard_app.py
   App URL (optional): tradeguard (또는 원하는 이름)
   ```
3. **Advanced settings** (선택사항):
   - Python version: 3.11
   - Secrets: 필요시 추가

4. **Deploy!** 클릭

### 4-3. 배포 완료
- 배포 시간: 약 2-5분
- 상태 확인: 로그 창에서 진행 상황 확인
- 완료 시 자동으로 앱 실행

**앱 URL**: `https://tradeguard.streamlit.app`

---

## 🔧 배포 후 수정사항

### 코드 수정 시
```powershell
# 수정 후 커밋
git add .
git commit -m "설명 메시지"
git push

# Streamlit Cloud가 자동으로 재배포함 (약 1-2분)
```

### 앱 재시작
Streamlit Cloud → 앱 선택 → **⋮** → **Reboot app**

---

## ❗ 자주 발생하는 문제

### 1. 로고가 안 보임
**해결:** `logo.png` 파일이 GitHub에 올라갔는지 확인

### 2. CSV 파일 오류
**해결:** `usage_rate_hsk.csv` UTF-8 인코딩 확인
```python
# trade_guard_app.py에서 encoding 명시
pd.read_csv('usage_rate_hsk.csv', encoding='utf-8')
```

### 3. 메모리 부족
**해결:** Streamlit Cloud 무료 플랜은 1GB 제한
- 큰 데이터 처리 시 주의
- 캐싱 활용 (`@st.cache_data`)

### 4. Git 푸시 인증 실패
**해결:** Personal Access Token 재생성 및 사용

---

## 📚 다음 단계

### 선택사항
1. **커스텀 도메인** 설정 (유료 플랜)
2. **비밀번호 보호** 추가
3. **데이터베이스** 연결
4. **Analytics** 추가

### 현재 구성 (무료)
- ✅ GitHub Public Repository: 무료
- ✅ Streamlit Cloud Community: 무료
- ✅ 제한: 1 app, 1GB RAM, Public only

**배포 성공하면 전세계 어디서나 접속 가능! 🎉**
