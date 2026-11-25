
import ollama

response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "What is artificial intelligence? Explain in 3 sentences."
        }
    ]
)

answer = response["message"]["content"]

print("\n--- GENAI OUTPUT ---")
print(answer)
