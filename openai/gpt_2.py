import os
from openai import OpenAI
from tqdm import tqdm
import pandas as pd 

input_data_dirs = [
        # "../../TaskManager/number_1/number_1.csv",
        # "../../TaskManager/number_2/number_2.csv",
        # "../../TaskManager/number_3/number_3.csv",
        "../../TaskManager/reasoning/reasoning.csv",
        # "../../TaskManager/spelling_correct/spelling_correct.csv",
        # "../../TaskManager/summarization/summarization.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_1.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_2.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_8.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_4.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_3.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_5.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_6.csv",
        # "../../TaskManager/ko_quiz/ko_quiz_7.csv",
        # "../../TaskManager/nli/nli.csv",
        
]

def apiCall(input_data): 
    createdMessages = []
    for prompt in input_data['prompt']:
        createdMessages.append({"role": "user", "content": prompt})
    
    responseList = []
    openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    for message in tqdm(createdMessages):
        try: 
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[message,],        
            )
            for choice in response.choices:
                responseList.append(choice.message.content)
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
                    "model_name": "gpt-3.5-turbo"
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