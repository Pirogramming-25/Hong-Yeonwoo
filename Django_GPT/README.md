# Django GPT - Hugging Face AI 웹 서비스

Django와 Hugging Face Transformers `pipeline()`을 사용한 AI 웹 서비스입니다.  
사용자는 웹 페이지에서 영어 텍스트를 입력하고 감정 분석, 문서 요약, 유해 표현 분석 기능을 실행할 수 있습니다.

## 주요 기능

- 감정 분석: `/sentiment/`
- 문서 요약: `/summarize/`
- 유해 표현 분석: `/moderate/`
- 복합 분석: `/combo/`
- Django Authentication 기반 로그인
- 로그인 사용자 실행 기록 DB 저장
- 각 기능별 최근 실행 기록 5개 출력
- CSRF 보호 적용
- 입력값 검증 적용
- Hugging Face 모델 Lazy Loading 적용

## 사용 모델

| 기능           | URL           | 모델                                               | Task                  | 접근 권한     |
| -------------- | ------------- | -------------------------------------------------- | --------------------- | ------------- |
| 감정 분석      | `/sentiment/` | `cardiffnlp/twitter-roberta-base-sentiment-latest` | `text-classification` | 비로그인 허용 |
| 문서 요약      | `/summarize/` | `sshleifer/distilbart-cnn-6-6`                     | `summarization`       | 로그인 필요   |
| 유해 표현 분석 | `/moderate/`  | `unitary/toxic-bert`                               | `text-classification` | 로그인 필요   |
| 복합 분석      | `/combo/`     | 여러 모델 연결                                     | Pipeline Chaining     | 로그인 필요   |

## 실행 방법

프로젝트 폴더에서 가상환경을 활성화한 뒤 필요한 패키지를 설치하고 DB 마이그레이션을 실행합니다. 이후 관리자 계정을 생성하고 개발 서버를 실행하면 됩니다.

```powershell
cd C:\Users\wepe\Desktop\Hong-Yeonwoo\Django_GPT
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
