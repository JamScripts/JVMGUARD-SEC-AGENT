from ollama import chat 

response = chat(
    model="qwen3.5:2b",
    messages=[
        {
            "role": "user",
            "content": "Reply only with: JVMGuard connection successful."
        }
    ],
    think=False,
)

print(response.message.content)
