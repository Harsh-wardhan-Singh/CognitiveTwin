import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_json(self, system_prompt: str, user_prompt: str):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        return response.choices[0].message.content