from openai import OpenAI
from dotenv import load_dotenv
import os


def main():
    
    load_dotenv()
    client = OpenAI(api_key= os.getenv("OPEN_API_KEY"))

    response = client.chat.completions.create (
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content" : "너는 친절한 상담사"},
            {"role": "user","content" : "AI는 무엇인가? 한줄로 답해 줘"}
        ],
        temperature=0.5
    )
        
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
