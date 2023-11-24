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
    max_context_length = 120
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
    
    completionList = []
    for chunk in chunked_messages:
        openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chunk,        
        )
        print(f'completion: {completion}')
        if completionList == []:
            completionList = completion
        else:
            completionList = completionList.append(completion)
    return completionList

def main():
    completion = apiCall()
    output_data = pd.DataFrame()
    # retrive input data
    for input_data_dir in tqdm(input_data_dirs):
        try:
            data = pd.read_csv(input_data_dir)
        except Exception as e:
            print(input_data_dir+" 처리 중 에러 발생")
            print(e)
    # retrive outputs from model  
    for choice in completion.choices:
        print(f'choice: {choice.message.content}')
        if choice and choice.message.role == 'assistant':
            output = choice.message.content
            data["result"] = output
            data["model_name"] = "gpt-4-1106-preview"
            output_data = pd.concat([output_data, data[["task_name","index", "result", "model_name"]]], ignore_index=True)
        else:
            print("Response structure might have changed. Check the response object attributes.")
    
    output_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False)

if __name__ == "__main__":
    main()
