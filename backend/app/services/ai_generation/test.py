from llm_client import LLMClient

client = LLMClient()

print(
    client.generate_json(
        "You are a JSON generator.",
        'Return {"hello": "world"} and nothing else.'
    )
)