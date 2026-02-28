import os
import time
import re
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from huggingface_hub.utils import HfHubHTTPError

try:
    from json_repair import repair_json
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False

load_dotenv()

MAX_HTTP_RETRIES = 3
BASE_BACKOFF_DELAY = 1.5


class LLMTransportError(Exception):
    """Raised when LLM transport repeatedly fails."""
    pass


def extract_and_clean_json(text: str) -> str:
    """
    Extract and clean JSON from LLM response.
    Handles markdown code blocks, escape sequences, and other formatting.
    """
    text = text.strip()
    
    # Remove markdown code blocks (```json ... ``` or just ``` ... ```)
    text = re.sub(r'^```(?:json)?\s*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```$', '', text, flags=re.MULTILINE)
    
    text = text.strip()
    
    # Find the first { and last } to extract JSON object
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        text = text[start_idx:end_idx + 1]
    else:
        # If we can't find braces, it might not be valid JSON
        raise ValueError("No JSON object found in response")
    
    # Fix common JSON issues
    # Remove trailing commas in arrays and objects
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Try to fix unescaped newlines in strings by replacing with space
    # This is a multi-line replace that's careful not to destroy valid JSON
    lines = text.split('\n')
    
    # Reconstruct, being careful about string boundaries
    in_string = False
    escape_next = False
    result = []
    
    for char in text:
        if escape_next:
            result.append(char)
            escape_next = False
            continue
            
        if char == '\\':
            result.append(char)
            escape_next = True
            continue
            
        if char == '"':
            in_string = not in_string
            result.append(char)
            continue
            
        if char == '\n' and in_string:
            # Replace newline with space inside strings
            result.append(' ')
            continue
            
        result.append(char)
    
    text = ''.join(result)
    return text


class LLMClient:

    def __init__(self):
        token = os.getenv("HF_API_KEY")
        if not token:
            raise ValueError("HF_API_KEY not found in environment")

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

                raw_response = response.choices[0].message.content.strip()
                
                # Clean and extract JSON from response
                cleaned_json = extract_and_clean_json(raw_response)
                
                # Try to repair JSON if json-repair is available
                if HAS_JSON_REPAIR:
                    try:
                        cleaned_json = repair_json(cleaned_json)
                    except Exception as repair_error:
                        # If repair fails, continue with original
                        pass
                
                # Validate that it's actually JSON by trying to parse it
                try:
                    json.loads(cleaned_json)
                except json.JSONDecodeError as e:
                    # Show more details about the error
                    error_pos = e.pos if hasattr(e, 'pos') else 0
                    preview = cleaned_json[max(0, error_pos - 50):min(len(cleaned_json), error_pos + 50)]
                    print(f"      JSON Error at position {error_pos}: {preview}")
                    raise ValueError(f"Invalid JSON at char {error_pos}: {str(e)}")
                
                return cleaned_json

            except HfHubHTTPError as e:
                last_error = e
                error_msg = str(e)
                print(f"    HF API Error (attempt {attempt + 1}/{MAX_HTTP_RETRIES}): {error_msg}")

                if attempt == MAX_HTTP_RETRIES - 1:
                    break

                # Exponential backoff
                delay = BASE_BACKOFF_DELAY * (2 ** attempt)
                print(f"    Retrying in {delay}s...")
                time.sleep(delay)
                
            except Exception as e:
                last_error = e
                error_msg = str(e)
                print(f"    Unexpected Error (attempt {attempt + 1}/{MAX_HTTP_RETRIES}): {type(e).__name__}: {error_msg}")

                if attempt == MAX_HTTP_RETRIES - 1:
                    break

                # Back off on any error
                delay = BASE_BACKOFF_DELAY * (2 ** attempt)
                print(f"    Retrying in {delay}s...")
                time.sleep(delay)

        raise LLMTransportError(
            f"LLM transport failed after {MAX_HTTP_RETRIES} attempts: {last_error}"
        )