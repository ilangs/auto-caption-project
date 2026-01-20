import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")

client = OpenAI()


# Whisper를 단 1회만 호출하여 text + segments(자막) 모두 반환
def transcribe(audio_path: str):
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json"  # text + segments 모두 제공
        )
    return result  # 객체 반환
