import os
from openai import OpenAI
from tqdm import tqdm
import pandas as pd 

input_data_dirs = ["../../TaskManager/ko_quiz/ko_quiz_1.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_2.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_8.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_4.csv",
                   ]
# "../../TaskManager/ko_quiz/ko_quiz_3.csv",
# "../../TaskManager/ko_quiz/ko_quiz_5.csv",
# "../../TaskManager/ko_quiz/ko_quiz_6.csv",
# "../../TaskManager/ko_quiz/ko_quiz_7.csv",
# "../../TaskManager/nli/nli.csv",
# "../../TaskManager/number_1/number_1.csv",
# "../../TaskManager/number_2/number_2.csv",
# "../../TaskManager/number_3/number_3.csv",
# "../../TaskManager/Reasoning/data.csv",
# "../../TaskManager/spelling_correct/spelling_correct.csv",
# "../../TaskManager/summarization/data.csv",

def apiCall(): 
    max_context_length = 50
    createdMessages = []
    prompts = []
    for input_data_dir in tqdm(input_data_dirs):
        try:
            data = pd.read_csv(input_data_dir)
            data_prompts = data["prompt"].to_list()
            prompts.extend(data_prompts)
            for prompt in data_prompts:
                createdMessages.append({"role": "user", "content": prompt})
        except Exception as e:
            print(input_data_dir+" 처리 중 에러 발생")
            print(e)
    
    chunked_messages = [
        createdMessages[i:i + max_context_length - 1] 
        for i in range(0, len(createdMessages), max_context_length-1)
    ]
    
    responseList = []
    for chunk in chunked_messages:
        openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chunk,        
        )
        for choice in response.choices:
            responseList.append(choice.message)
    return responseList

def main():
    responses = apiCall()
    output_data = pd.DataFrame()
    # retrive input data
    for input_data_dir in tqdm(input_data_dirs):
        try:
            data = pd.read_csv(input_data_dir)
        except Exception as e:
            print(input_data_dir+" 처리 중 에러 발생")
            print(e)
    # retrive outputs from model  
    idx = 0
    for response in tqdm(responses):
        print(f'response: {response}/n')
        if response and response.role == 'assistant':
            output = response.content
            print(f'output: {output}/n')
            current_data = data.iloc[idx].copy()
            current_data["result"] = output
            current_data["model_name"] = "gpt-4-1106-preview"
            output_data = pd.concat([output_data, current_data[["task_name", "index", "result", "model_name"]]], ignore_index=True)
            idx += 1
        else:
            print("Response structure might have changed. Check the response object attributes.")
    
    output_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False)

if __name__ == "__main__":
    main()
