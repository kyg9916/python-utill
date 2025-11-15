# 🐍 Python 스크립트 모음: 유틸리티 및 AI 기반 자동화

이 저장소는 동영상 처리, 시뮬레이션, 디스코드 챗봇 등 일상 및 개발 보조에 유용한 다양한 파이썬 스크립트들을 모아 놓은 컬렉션입니다.

---

### 1. 🎬 동영상 파일 병합 및 셔플 (`combine.py`)

*   **파일명:** `combine.py`
*   **핵심 기술:** Python, FFmpeg
*   **주요 기능:** 지정 폴더 내 동영상을 무작위 셔플 후 단일 파일로 빠르게 병합합니다 (`-c copy` 사용).
*   **준비 사항:**
    *   Python 3 설치
    *   FFmpeg 설치 및 `PATH` 환경 변수 설정
*   **사용 방법:**
    1.  `combine.py`와 같은 경로에 `videos` 폴더를 생성하고 병합할 동영상 파일을 넣습니다.
    2.  스크립트 내 `video_folder`, `output_filename`, `shuffle_videos` 변수를 필요에 따라 수정합니다.
    3.  터미널에서 `python combine.py` 실행.

---

### 2. 💰 로또 시뮬레이션 및 통계 기반 번호 추천 (`lotto.py`)

*   **파일명:** `lotto_simulator.py`
*   **핵심 기술:** Python, `collections.Counter`
*   **주요 기능:** 가상 자금으로 로또를 구매하고 당첨 결과를 시뮬레이션하며, 누적된 당첨 데이터를 기반으로 번호를 예측 추천합니다.
*   **작동 방식:** 시뮬레이션 당첨 번호가 `PAST_WINNING_NUMBERS_ACCUMULATED`에 누적되며, 'B' 모드 선택 시 이 데이터를 분석하여 가장 자주 나온 상위 숫자 풀에서 6개의 번호를 추천합니다. `INITIAL_PAST_WINNING_NUMBERS`를 실제 당첨 번호로 교체하여 정확도를 높일 수 있습니다.
*   **사용 방법:**
    1.  터미널에서 `python lotto_simulator.py` 실행.
    2.  프롬프트에 따라 구매 수량, 'P'(수동), 'S'(반자동), 'B'(예측), 'X'(종료) 중 선택.
    3.  **배포용 파일 생성:** `pip install pyinstaller` 후 `pyinstaller --onefile lotto_simulator.py` 명령으로 단일 실행 파일 생성 가능.

---

### 3. 🤖 Gemini 기반 디스코드 AI 챗봇 (`my_chat_bot.py`)

*   **파일명:** `discord_bot.py`
*   **핵심 기술:** Python, `discord.py`, Google Gemini API
*   **주요 기능:** 디스코드 봇으로 Gemini AI를 연동하여 질의응답을 수행합니다. 지수 백오프(Exponential Backoff) 로직으로 안정적인 API 재시도를 지원합니다.
*   **준비 사항:**
    *   라이브러리 설치: `pip install discord google-genai`
    *   **API 키 준비:**
        *   `MY_DISCORD_TOKEN`: 디스코드 개발자 포털에서 획득
        *   `MY_GEMINI_KEY`: Google AI Studio에서 획득
        *   (권장) 보안을 위해 환경 변수로 설정 (예: 파이참의 'Run Configuration'에서 `MY_DISCORD_TOKEN=YOUR_TOKEN`, `MY_GEMINI_KEY=YOUR_KEY` 추가).
*   **사용 방법:**
    1.  `python discord_bot.py` 실행.
    2.  디스코드 채널에서 `!캬루야 [질문 내용]` 형식으로 봇을 호출하여 사용.

---

### 4. 🔗 마크다운 링크 제목 추출기 (`notion_link_remove.py`)

*   **파일명:** `notion_link_remove.py`
*   **핵심 기술:** Python, `re` (정규표현식)
*   **주요 기능:** 마크다운 링크 형식 `[번호. 제목](링크)`에서 제목 부분만 추출하고 번호를 다시 매겨 출력합니다. 노션 등에서 링크 목록 정리 시 유용합니다.
*   **작동 원리 (예시):**
    *   입력: `[2. 🐶💸 악동 도지쉑 - 다 잃었소](https://...)`
    *   출력: `1. 🐶💸 악동 도지쉑 - 다 잃었소`
*   **사용 방법:**
    1.  스크립트 내 `input_text` 변수에 처리할 마크다운 링크 텍스트를 수정합니다.
    2.  `python notion_link_remove.py` 실행.

---

### 5. 🎬 Whisper 기반 자동 자막 생성기 (`video.py`)

*   **파일명:** `video.py`
*   **핵심 기술:** Python, `ffmpeg-python`, `openai-whisper`
*   **주요 기능:** 로컬 동영상 파일에서 오디오를 추출하고, OpenAI Whisper 모델을 이용하여 SRT 자막 파일을 자동으로 생성합니다.
*   **준비 사항:**
    *   라이브러리 설치: `pip install ffmpeg-python openai-whisper`
    *   FFmpeg 설치 및 `PATH` 환경 변수 설정 (시스템 전역).
*   **사용 방법:**
    1.  자막을 생성할 동영상 파일 (예: `audioTwo.mp4`)을 스크립트와 같은 경로에 둡니다.
    2.  스크립트 내부의 `video_path` 변수에 동영상 파일명을 지정합니다.
    3.  `python video.py` 실행.
    4.  실행 완료 후, 프로젝트 폴더에 `output.srt` 파일이 생성됩니다.
*   **Whisper 모델 변경:** `model = whisper.load_model("small")` (기본값 'base')에서 'small', 'medium', 'large' 등으로 변경하여 정확도 및 처리 속도 조절 가능.

---
