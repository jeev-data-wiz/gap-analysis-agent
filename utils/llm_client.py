from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, TEMPERATURE

client = OpenAI(api_key=OPENAI_API_KEY)

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are a precise, structured AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
