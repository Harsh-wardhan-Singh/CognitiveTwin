import os
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from huggingface_hub.utils import HfHubHTTPError

load_dotenv()

MAX_HTTP_RETRIES = 3
BASE_BACKOFF_DELAY = 1.5


class LLMTransportError(Exception):
    """Raised when LLM transport repeatedly fails."""
    pass


class LLMClient:

    def __init__(self):
        token = os.getenv("HF_API_KEY")
        if not token:
            raise ValueError("HF_API_KEY not found")

        self.client = InferenceClient(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            token=token
        )

    def generate_json(self, system_prompt: str, user_prompt: str) -> str:

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        last_error = None

        for attempt in range(MAX_HTTP_RETRIES):
            try:
                response = self.client.chat_completion(
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                )

                return response.choices[0].message.content.strip()

            except HfHubHTTPError as e:
                last_error = e

                if attempt == MAX_HTTP_RETRIES - 1:
                    break

                # Exponential backoff
                delay = BASE_BACKOFF_DELAY * (2 ** attempt)
                time.sleep(delay)

        raise LLMTransportError(
            f"LLM transport failed after {MAX_HTTP_RETRIES} attempts: {last_error}"
        )