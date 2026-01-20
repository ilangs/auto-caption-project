from pathlib import Path
from dotenv import load_dotenv

from youtube_audio import download_audio
from whisper_stt import transcribe

def transcribe_in_chunks(chunk_dir: Path) -> str:
    parts = sorted(chunk_dir.glob("part_*.mp3"))
    if not parts:
        raise FileNotFoundError("분할된 오디오(part_*.mp3)가 없습니다.")

    texts = []
    for i, p in enumerate(parts, start=1):
        print(f"[{i}/{len(parts)}] STT 처리 중: {p.name}")
        texts.append(transcribe(str(p)))
    return "\n".join(texts)

def main():
    load_dotenv()

    youtube_url = input("유튜브 URL을 입력하세요: ").strip()
    audio_path = Path(download_audio(youtube_url))

    out_dir = Path("output") / "subtitles"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_file = out_dir / "result.txt"

    # 1) 먼저 파일이 너무 크면 분할 처리 안내(자동화는 다음 단계에서)
    size_mb = audio_path.stat().st_size / 1024 / 1024
    print(f"오디오 파일 크기: {size_mb:.2f} MB")

    # 2) 분할 파일이 존재하면 분할 기반 STT
    chunk_dir = Path("input") / "audio" / "chunks"
    if chunk_dir.exists():
        text = transcribe_in_chunks(chunk_dir)
    else:
        # 분할 폴더가 없으면 단일 파일 STT 시도
        result = transcribe(str(audio_path))

    output_file.write_text(result.text, encoding="utf-8")
    print("자막 파일 생성 완료:", output_file)

if __name__ == "__main__":
    main()
