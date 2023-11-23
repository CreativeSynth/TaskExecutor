import asyncio
import os
from openai import OpenAI

async def apiCall():
    openai = OpenAI()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    
    completion = await openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"promt":"욱여넣다와 우겨넣다 중 맞는 말은?"},
        ]
    )
    return completion

async def main():
    completion = await apiCall()
    print(completion.data.choices[0].text)

if __name__ == "__main__":
    asyncio.run(main())