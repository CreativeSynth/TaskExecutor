import requests

API_URL = "https://api-inference.huggingface.co/models/skt/ko-gpt-trinity-1.2B-v0.5"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers = headers, json = payload)
    return response.json()

output = query(
    {
        "inputs": '"우겨넣다"와 "욱여넣다" 중 맞는 말은 ',
    }
)

print(output[0]['generated_text'])

for i in range(999):
    text = input("\n입력:")
    if text == "그만":
        break
    output = query({"inputs": text})
    print(output[0]['generated_text'])