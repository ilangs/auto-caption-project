from datetime import timedelta
from gtts import gTTS
from openai import OpenAI

# OpenAI 클라이언트
client = OpenAI()


# --------------------------
# 타임스탬프 변환 (SRT 포맷)
# --------------------------
def format_timestamp(seconds):
    td = timedelta(seconds=seconds)
    total = str(td)

    if "." in total:
        time, ms = total.split(".")
        ms = ms[:3]
    else:
        time = total
        ms = "000"

    if len(time.split(":")) == 2:
        time = "0:" + time

    return f"{time.replace('.', ',')},{ms}"


# --------------------------
# Whisper segments → SRT 저장
# --------------------------
def save_srt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = format_timestamp(seg.start)
            end = format_timestamp(seg.end)
            text = seg.text.strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(text + "\n\n")


# --------------------------
# OpenAI 번역
# --------------------------
def translate_line(text: str, target: str = "ko") -> str:
    # GPT-4o-mini 기반 번역
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate the following text into {target}."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()


# --------------------------
# 영어 SRT → 한국어 SRT 번역
# --------------------------
def translate_srt(input_srt, output_srt, target_lang="ko"):
    out_lines = []

    with open(input_srt, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        # 숫자(line 번호), 시간코드, 공백 줄은 번역 금지
        if line.strip().isdigit() or "-->" in line or line.strip() == "":
            out_lines.append(line)
        else:
            translated = translate_line(line.strip(), target_lang)
            out_lines.append(translated + "\n")

    with open(output_srt, "w", encoding="utf-8") as f:
        f.writelines(out_lines)


# --------------------------
# 한국어 SRT → 한국어 음성(mp3) 생성
# --------------------------
def srt_to_tts(input_srt, output_audio):
    text_list = []

    with open(input_srt, "r", encoding="utf-8") as f:
        for line in f:
            if "-->" in line or line.strip().isdigit():
                continue
            if line.strip():
                text_list.append(line.strip())

    full_text = " ".join(text_list)

    tts = gTTS(full_text, lang="ko")
    tts.save(output_audio)