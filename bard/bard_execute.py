from bardapi import BardCookies
from tqdm import tqdm
import pandas as pd 

input_data_dirs = [
        "../../TaskManager/ko_quiz/ko_quiz_1.csv",
        "../../TaskManager/ko_quiz/ko_quiz_2.csv",
        "../../TaskManager/ko_quiz/ko_quiz_8.csv",
        "../../TaskManager/ko_quiz/ko_quiz_4.csv",
        "../../TaskManager/ko_quiz/ko_quiz_3.csv",
        "../../TaskManager/ko_quiz/ko_quiz_5.csv",
        "../../TaskManager/ko_quiz/ko_quiz_6.csv",
        "../../TaskManager/ko_quiz/ko_quiz_7.csv",
        "../../TaskManager/nli/nli.csv",
        "../../TaskManager/number_1/number_1.csv",
        "../../TaskManager/number_2/number_2.csv",
        "../../TaskManager/number_3/number_3.csv",
        "../../TaskManager/Reasoning/data.csv",
        "../../TaskManager/spelling_correct/spelling_correct.csv",
        "../../TaskManager/summarization/data.csv",
]

cookie_dict = {
    "__Secure-1PSID": "dQi_vJlmz64BV4q_B0DI7-1985Wx9BTs7CLpiUpCY6VaG4HJuwhFef3ZyejEpw79uq946Q.",
    "__Secure-1PSIDTS": "sidts-CjEBPVxjSgwME7JQkkpHoYkY5hf6x3Brg_KZyOs11LVdb2ZsAHdDoyJhM31F0_xkBmrqEAA",
    "__Secure-1PSIDCC": "ACA-OxOIbLQro40a57hOWy67BpzoPZwwumFn0QSZv6N8u3s4poi3wQtjHtr-2OenC0lJAMLWTw",
}

bard = BardCookies(cookie_dict=cookie_dict)


def apiCall(input_data):
    responseList = []
    for message in tqdm(input_data["prompt"]):
        try: 
            response = bard.get_answer(message)
            responseList.append(response['content'])
        except Exception as e:
            print("API 요청 중 에러 발생")
            print(e)
    return responseList

def process_file(input_data_dir):
    try:
        data = pd.read_csv(input_data_dir)
        responses = apiCall(data)
        output_data = pd.DataFrame()
        for idx, response in enumerate(responses):
            if response:
                current_data = data.iloc[idx].copy()
                current_data["result"] = response
                current_data["model_name"] = "bard"
                output_data = pd.concat([output_data, current_data], ignore_index=True)
            else:
                print("Response structure might have changed. Check the response object attributes.")
        # Save the output data
        output_file = input_data_dir.split('/')[-1].replace('.csv', '_result.csv')
        output_data.to_csv(output_file, encoding='utf-8-sig', index=False)
    except Exception as e:
        print(input_data_dir + " 처리 중 에러 발생")
        print(e)

def main():
    for input_data_dir in input_data_dirs:
        process_file(input_data_dir)

if __name__ == "__main__":
    main()