# Vercel + Supabase 배포 가이드

## 1. Supabase 설정

### 1.1 프로젝트 생성
1. [Supabase](https://supabase.com)에 로그인
2. "New Project" 클릭
3. 프로젝트 이름과 데이터베이스 비밀번호 설정
4. Region: Northeast Asia (Seoul) 선택 권장

### 1.2 데이터베이스 스키마 생성
1. Supabase Dashboard에서 "SQL Editor" 클릭
2. `supabase/schema.sql` 파일 내용 복사하여 실행
3. `supabase/data.sql` 파일 내용 복사하여 실행

> **data.sql 생성 방법:**
> ```bash
> python supabase/migrate_data.py
> ```

### 1.3 연결 문자열 확인
1. Settings > Database > Connection string
2. "URI" 탭에서 연결 문자열 복사
3. `[YOUR-PASSWORD]`를 실제 비밀번호로 교체

## 2. Vercel 배포

### 2.1 GitHub 연결
1. 프로젝트를 GitHub에 푸시
2. [Vercel](https://vercel.com)에 로그인
3. "Import Project" → GitHub 저장소 선택

### 2.2 환경 변수 설정
Vercel 프로젝트 Settings > Environment Variables에서 추가:

| Name | Value |
|------|-------|
| `DATABASE_URL` | `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres` |

### 2.3 배포
1. "Deploy" 클릭
2. 빌드 완료까지 대기 (약 2-3분)
3. 배포된 URL 확인

## 3. 로컬 개발

### 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env
# DATABASE_URL을 Supabase 연결 문자열로 수정
```

### 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

## 4. 이미지 URL 수정 (중요!)

현재 의원 사진은 로컬 경로(`/images/members/`)로 저장되어 있습니다.
Vercel 배포 시 이미지도 함께 배포됩니다.

만약 외부 이미지 호스팅을 사용하려면:
1. 이미지를 Supabase Storage 또는 Cloudinary에 업로드
2. `backend/data/members.json`의 `photo_url` 수정
3. 데이터베이스에 새 URL로 업데이트

## 5. 트러블슈팅

### "Module not found" 에러
- `requirements.txt`에 필요한 패키지가 있는지 확인
- Vercel 빌드 로그에서 Python 버전 확인

### 데이터베이스 연결 실패
- Supabase 연결 문자열이 올바른지 확인
- `postgres://`를 `postgresql://`로 변경했는지 확인
- Supabase Dashboard에서 IP 허용 설정 확인

### API 404 에러
- `vercel.json`의 rewrites 설정 확인
- `/api/*` 경로가 올바르게 라우팅되는지 확인
