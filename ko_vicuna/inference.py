import requests

API_URL = "https://api-inference.huggingface.co/models/junelee/ko_vicuna_7b"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Can you please let us know more details about your ",
})
print(output)