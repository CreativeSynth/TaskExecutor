from asyncio import sleep
import pathlib
import textwrap
import google.generativeai as genai
import os
from tqdm import tqdm
import pandas as pd 

input_data_dirs = []


GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def apiCall(input_data): 
    createdMessages = []
    for prompt in input_data['prompt']:
        createdMessages.append(prompt)
    
    responseList = []
    model = genai.GenerativeModel('gemini-pro')
    for message in tqdm(createdMessages):
        try:
            response = model.generate_content(message, stream=True)
            responseChunks = ""
            for chunk in response:
                responseChunks += chunk.text
            responseList.append(responseChunks)
        except Exception as e:
            print("API 요청 중 에러 발생")
            print(e)
    return responseList

def process_file(input_data_dir):
    try:
        data = pd.read_csv(input_data_dir)
        responses = apiCall(data)
        rows = []
        for idx, response in enumerate(responses):
            if idx < len(data) and response:
                current_index = idx
                current_data = data.iloc[current_index].copy()
                row = {
                    "task_name": current_data["task_name"],
                    "index": current_data["index"],
                    "result": response,
                    "model_name": "gemini-pro"
                }
                rows.append(row)
            else:
                print("Response structure might have changed. Check the response object attributes.")
        output_data = pd.DataFrame(rows)
        output_file = input_data_dir.split('/')[-1].replace('.csv', '_result.csv')
        output_data.to_csv(output_file, encoding='utf-8-sig', index=False)

    except Exception as e:
        print(input_data_dir + " 처리 중 에러 발생")
        print(e)

def main():
    for input_data_dir in input_data_dirs:
        print("Processing %s", input_data_dir)
        process_file(input_data_dir)

if __name__ == "__main__":
    main()