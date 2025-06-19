
import groq


GROQ_API_KEY = "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"
client = groq.Client(api_key=GROQ_API_KEY)
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": "Ping"}]
)

print(response.choices[0].message.content)