import asyncio
from openai import OpenAI, Configuration

async def apiCall():
    configuration = Configuration(api_key = 'your-api-key')
    openai = OpenAI(configuration)

    completion = await openai.create_completion(
        model = "gpt-3.5",
        prompt = '"우겨넣다"와 "욱여넣다" 중 맞는 말은 '
    )

    return completion

async def main():
    completion = await apiCall()
    print(completion.data.choices[0].text)

if __name__ == "__main__":
    asyncio.run(main())