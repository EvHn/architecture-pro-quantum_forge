from openai import OpenAI

client = OpenAI(
    api_key="test", 
    base_url="http://localhost:9090/v1"
)

try:
    chat_completion = client.chat.completions.create(
        model="gemma-3-1b-it",
        messages=[
            {"role": "system", "content": "You are emotionless robot. Be logical, helpfull and give short answers"},
            {"role": "user", "content": "Hello, world!"}
            ]
    )
    print(chat_completion.choices)
except Exception as e:
    print(f"An error occurred: {e}")
