import ffmpeg
import whisper
import os


# 1. 오디오 추출 함수
def extract_audio(video_path, output_audio="audio.wav"):
    """
    로컬 동영상 파일에서 오디오만 추출
    """
    (
        ffmpeg
        .input(video_path)
        .output(output_audio, acodec='pcm_s16le', ac=1, ar='16000')  # Whisper가 좋아하는 설정
        .overwrite_output()
        .run(quiet=True)
    )
    return output_audio


# SRT 타임포맷 변환 함수
def format_timestamp(seconds):
    import math

    millisec = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02},{millisec:03}"


# 2. Whisper로 텍스트 전사 + SRT 만들기
def create_subtitles(audio_file, output_srt="output.srt"):
    """
    오디오 파일을 Whisper로 텍스트 전사하고 SRT 자막 생성
    """
    model = whisper.load_model("base")  # "small", "medium", "large"로 변경 가능 (정확도↑)

    print("🕒 Whisper가 오디오를 분석하는 중...")
    result = model.transcribe(audio_file, language='en')

    # ➜ 전체 텍스트 출력
    print("\n=== 전체 텍스트 ===")
    print(result["text"])
    print("==================\n")

    # ➜ SRT 파일 저장
    with open(output_srt, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], start=1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            text = seg["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

    print(f"🎉 SRT 파일 생성 완료: {output_srt}")

    return result["text"]


# 3. 전체 파이프라인 실행 함수
def process_video(video_path):
    print(f"🎬 입력 파일: {video_path}")

    audio_file = "temp_audio.wav"

    # 오디오 추출
    print("🎧 오디오 추출 중…")
    extract_audio(video_path, audio_file)

    # Whisper로 텍스트 변환 + 자막 생성
    create_subtitles(audio_file, "output.srt")

    # 임시 오디오 파일 삭제
    os.remove(audio_file)

    print("✅ 완료되었습니다.")


# 단독 실행 시
if __name__ == "__main__":
    # 동영상 파일 경로 입력
    video_path = "audioTwo.mp4"  # ★ 여기에 로컬 영상 파일 이름을 적으면 됨
    process_video(video_path)
