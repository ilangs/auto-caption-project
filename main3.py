from pathlib import Path
from dotenv import load_dotenv

from youtube_audio import download_audio
from whisper_stt import transcribe
from subtitle_utils import save_srt, translate_srt, srt_to_tts


def main():
    load_dotenv()

    youtube_url = input("유튜브 URL을 입력하세요: ").strip()
    if not youtube_url:
        raise ValueError("유튜브 URL이 비어 있습니다.")

    # 1) 오디오 다운로드
    audio_path = download_audio(youtube_url)
    audio_path = Path(audio_path)

    out_dir = Path("output")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 2) Whisper STT (한 번만 호출)
    print("Whisper STT 실행 중...")
    result = transcribe(str(audio_path))

    # 영어 TXT 저장
    txt_path = out_dir / "subtitle_en.txt"
    txt_path.write_text(result.text, encoding="utf-8")
    print("영어 TXT 저장 완료:", txt_path)

    # 영어 SRT 저장
    srt_en_path = out_dir / "subtitle_en.srt"
    save_srt(result.segments, srt_en_path)
    print("영어 SRT 저장 완료:", srt_en_path)

    # 3) 한국어 번역 SRT 생성
    srt_ko_path = out_dir / "subtitle_ko.srt"
    translate_srt(srt_en_path, srt_ko_path)
    print("한국어 SRT 생성 완료:", srt_ko_path)

    # 4) 한국어 TTS 생성
    mp3_path = out_dir / "subtitle_ko.mp3"
    srt_to_tts(srt_ko_path, mp3_path)
    print("한국어 음성(mp3) 생성 완료:", mp3_path)

    print("\n=== 전체 작업 완료 ===")
    print("영어 TXT :", txt_path)
    print("영어 SRT :", srt_en_path)
    print("한국어 SRT :", srt_ko_path)
    print("한국어 TTS :", mp3_path)


if __name__ == "__main__":
    main()
