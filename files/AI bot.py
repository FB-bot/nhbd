import requests

API_KEY = "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"

messages = [
    {
        "role": "system",
        "content": "Answer briefly and clearly. Only give correct answer. No extra explanation. No emojis."
    }
]

while True:
    user = input("তুমি: ")

    if user.lower() == "bye":
        print("AI: Goodbye")
        break

    messages.append({"role": "user", "content": user})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "My AI App"
        },
        json={
            "model": "openrouter/auto",
            "messages": messages,
            "max_tokens": 50   # 👉 ছোট reply
        }
    )

    data = response.json()

    if "choices" in data:
        reply = data["choices"][0]["message"]["content"].strip()
        print("AI:", reply)
        messages.append({"role": "assistant", "content": reply})
    else:
        print("Error:", data)