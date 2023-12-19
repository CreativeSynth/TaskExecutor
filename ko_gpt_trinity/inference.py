import requests

API_URL = "https://api-inference.huggingface.co/models/skt/ko-gpt-trinity-1.2B-v0.5"
headers = {"Authorization": "Bearer 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"}

def messages_to_string(prompt: str):
    return f"### 질문: {prompt}\n\n### 답변:"



def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


# input: 미완성된 문장 ex) 1919년 일어난 3.1운동은
# output: 문장을 이어서 완성시킨 문장 ex) 1919년 일어난 3.1운동은 독립신문을 통해 전국적으로 알려지게 되었다. 3.1'
output = query(
    {
	"inputs": messages_to_string("AI에 대해 설명해줘"),
    }
)

print(output)
