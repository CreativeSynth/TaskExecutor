import os
from openai import OpenAI

def apiCall():
    openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
             "content": "욱여넣다와 우겨넣다 중 맞는 말은?",
            },
        ]
    )
    return completion

def main():
    completion = apiCall()
    if completion.choices and completion.choices[0].message.role == 'assistant':
        print(completion.choices[0].message.content)
    else:
        print("Response structure might have changed. Check the response object attributes.")

if __name__ == "__main__":
    main()
