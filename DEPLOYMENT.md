# 🚀 TradeGuard 배포 가이드

## GitHub & Streamlit Cloud 배포 완벽 가이드

### 📦 준비된 파일들

✅ `trade_guard_app.py` - 메인 애플리케이션  
✅ `requirements.txt` - 패키지 의존성  
✅ `README.md` - 프로젝트 문서  
✅ `.gitignore` - Git 제외 파일  
✅ `.streamlit/config.toml` - Streamlit 설정  
✅ `logo.png` - 애플리케이션 로고  

---

## 🔧 1단계: Git 저장소 초기화

### PowerShell에서 실행:

```powershell
# 현재 디렉토리에서 Git 초기화
git init

# Git 사용자 설정 (최초 1회만)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: TradeGuard v1.0"
```

---

## 🌐 2단계: GitHub 저장소 생성 및 연결

### A. GitHub에서 새 저장소 생성

1. https://github.com 접속 및 로그인
2. 우측 상단 `+` 버튼 → `New repository` 클릭
3. 저장소 정보 입력:
   - **Repository name**: `tradeguard` (또는 원하는 이름)
   - **Description**: "지능형 수입신고 리스크 분석 솔루션"
   - **Public** 또는 **Private** 선택
   - ⚠️ **"Initialize this repository with a README" 체크 해제** (이미 있음)
4. `Create repository` 클릭

### B. 로컬 저장소와 GitHub 연결

```powershell
# GitHub 저장소 URL로 원격 저장소 추가
# (GitHub에서 보여주는 URL로 교체)
git remote add origin https://github.com/YOUR_USERNAME/tradeguard.git

# 메인 브랜치로 변경 (최신 Git 기본값)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

**인증 방법:**
- **HTTPS 사용 시**: Personal Access Token (PAT) 필요
  - GitHub Settings → Developer settings → Personal access tokens → Generate new token
  - `repo` 권한 선택
  - 생성된 토큰을 비밀번호 대신 사용

- **SSH 사용 시**: SSH 키 등록 필요
  - https://docs.github.com/ko/authentication/connecting-to-github-with-ssh

---

## ☁️ 3단계: Streamlit Cloud 배포

### A. Streamlit Cloud 계정 생성

1. https://streamlit.io/cloud 접속
2. `Sign up` 클릭
3. **GitHub 계정으로 로그인** (권장)

### B. 앱 배포

1. Streamlit Cloud 대시보드에서 `New app` 클릭
2. 배포 정보 입력:
   - **Repository**: `YOUR_USERNAME/tradeguard` 선택
   - **Branch**: `main`
   - **Main file path**: `trade_guard_app.py`
   - **App URL** (optional): 원하는 URL 설정 (예: `tradeguard-app`)
3. `Deploy!` 클릭
4. 🎉 약 2-3분 후 앱이 자동으로 배포됩니다!

### C. 배포 URL

배포가 완료되면 다음과 같은 URL로 접속할 수 있습니다:
```
https://YOUR_APP_NAME.streamlit.app
```

---

## 🔄 4단계: 코드 업데이트 시 재배포

코드를 수정한 후 GitHub에 푸시하면 **자동으로 재배포**됩니다:

```powershell
# 파일 수정 후
git add .
git commit -m "Update: 새로운 기능 추가"
git push
```

Streamlit Cloud가 자동으로 변경사항을 감지하고 앱을 재시작합니다.

---

## ⚙️ 추가 설정 (선택사항)

### Streamlit Cloud에서 설정 변경

1. Streamlit Cloud 대시보드에서 앱 선택
2. `Settings` → `Advanced settings` 클릭
3. 설정 가능 옵션:
   - **Python version**: 기본값 사용 (3.11)
   - **Environment variables**: 필요 시 추가

### 비밀 정보 관리 (Secrets)

만약 API 키나 비밀번호가 필요하다면:

1. Streamlit Cloud 앱 설정 → `Secrets` 클릭
2. TOML 형식으로 입력:
```toml
[secrets]
api_key = "your-api-key-here"
```
3. 코드에서 사용:
```python
import streamlit as st
api_key = st.secrets["secrets"]["api_key"]
```

---

## 🐛 문제 해결

### 배포 실패 시 체크리스트

✅ `requirements.txt` 파일이 올바른지 확인  
✅ Python 버전 호환성 확인 (Python 3.8-3.11 권장)  
✅ GitHub 저장소가 Public이거나 Streamlit Cloud에 접근 권한이 있는지 확인  
✅ `trade_guard_app.py` 파일명이 정확한지 확인  

### 로그 확인

Streamlit Cloud 앱 우측 하단 `Manage app` → `Logs`에서 오류 확인 가능

### 로컬 테스트

배포 전 로컬에서 테스트:
```powershell
pip install -r requirements.txt
streamlit run trade_guard_app.py
```

---

## 📞 지원

문제가 있거나 도움이 필요하시면:
- Streamlit 문서: https://docs.streamlit.io
- Streamlit 커뮤니티: https://discuss.streamlit.io

---

**Made by 전자동 | 관세법인 우신**

