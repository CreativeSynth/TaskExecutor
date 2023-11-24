import asyncio
import os
from openai import OpenAI

def apiCall():
    openai = OpenAI()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
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
    print(completion.data.choices[0].text)
if __name__ == "__main__":
    asyncio.run(main())