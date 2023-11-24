import pandas as pd
from vllm import LLM, SamplingParams
from tqdm import tqdm

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
llm = LLM(model="nlpai-lab/kullm-polyglot-5.8b-v2", tensor_parallel_size=4)


input_data_dirs = ["../../TaskManager/ko_quiz/ko_quiz_1.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_2.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_3.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_4.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_5.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_6.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_7.csv",
                   "../../TaskManager/ko_quiz/ko_quiz_8.csv",
                   "../../TaskManager/nli/nli.csv",
                   "../../TaskManager/number_1/number_1.csv",
                   "../../TaskManager/number_2/number_2.csv",
                   "../../TaskManager/number_3/number_3.csv",
                   "../../TaskManager/Reasoning/data.csv",
                   "../../TaskManager/spelling_correct/spelling_correct.csv",
                   "../../TaskManager/summarization/data.csv",
                   ]


output_data = pd.DataFrame()

for input_data_dir in tqdm(input_data_dirs):
    try:
        data = pd.read_csv(input_data_dir)
        prompts = data["prompt"].to_list()
        outputs = llm.generate(prompts, sampling_params)
        outputs = [output.outputs[0].text for output in outputs] # 결과 텍스트만 가져옴
        data["result"] = outputs
        data["model_name"] = "kullm5.8b"
        output_data = pd.concat([output_data, data[["task_name","index", "result", "model_name"]]], ignore_index=True)
    except Exception as e:
        print(input_data_dir+" 처리 중 에러 발생")
        print(e)

output_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False) # 한글 호환되는 포맷
    