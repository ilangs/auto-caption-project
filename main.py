from pathlib import Path
from dotenv import load_dotenv

from youtube_audio import download_audio
from whisper_stt import transcribe
from subtitle_utils import save_srt, translate_srt, srt_to_tts

def main():
    # 1) .env 로드(OPENAI_API_KEY)
    load_dotenv()

    # 2) 입력
    youtube_url = input("유튜브 URL을 입력하세요: ").strip()
    if not youtube_url:
        raise ValueError("유튜브 URL이 비어 있습니다.")

    # 3) 음성 추출(다운로드) → audio_path 반환
    audio_path = download_audio(youtube_url)
    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"음성 파일이 생성되지 않았습니다: {audio_path}")

    # 4) Whisper STT
    result = transcribe(str(audio_path))

    # 5) 출력 폴더 생성 + 저장
    out_dir = Path("output") / "subtitles"
    out_dir.mkdir(parents=True, exist_ok=True)

    output_file = out_dir / "result.txt"
    output_file.write_text(result.text, encoding="utf-8")
  
    print("자막 파일 생성 완료:", output_file)

if __name__ == "__main__":
    main()
