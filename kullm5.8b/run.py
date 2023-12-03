from collections.abc import Iterable
import pandas as pd
from vllm import LLM, SamplingParams
from tqdm import tqdm

def messages_to_string(prompts: Iterable[str]):
    return [f"아래는 작업을 설명하는 명령어입니다. 요청을 적절히 완료하는 응답을 작성하세요.\n\n### 명령어:\n{instruction}\n\n### 응답:\n" for instruction in prompts]


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
                   "../../TaskManager/translation/기술과학/en-ko/data.csv",
                   "../../TaskManager/translation/기술과학/ko-en/data.csv",
                   "../../TaskManager/translation/기초과학/en-ko/data.csv",
                   "../../TaskManager/translation/기초과학/ko-en/data.csv",
                   "../../TaskManager/translation/방송콘텐츠/en-ko/data.csv",
                   "../../TaskManager/translation/방송콘텐츠/ko-en/data.csv",
                   "../../TaskManager/translation/사회과학/en-ko/data.csv",
                   "../../TaskManager/translation/사회과학/ko-en/data.csv",
                   "../../TaskManager/translation/인문학/en-ko/data.csv",
                   "../../TaskManager/translation/인문학/ko-en/data.csv",
                   "../../TaskManager/translation/일상생활 및 구어체/en-ko/data.csv",
                   "../../TaskManager/translation/일상생활 및 구어체/ko-en/data.csv",
                   ]


output_data = pd.DataFrame()

for input_data_dir in tqdm(input_data_dirs):
    try:
        data = pd.read_csv(input_data_dir)
        prompts = data["prompt"].to_list()
        prompts = messages_to_string(prompts)
        outputs = llm.generate(prompts, sampling_params)
        outputs = [output.outputs[0].text for output in outputs] # 결과 텍스트만 가져옴
        data["result"] = outputs
        data["model_name"] = "kullm5.8b"
        output_data = pd.concat([output_data, data[["task_name","index", "result", "model_name"]]], ignore_index=True)

        # 디버깅 목적으로 상위 10개 확인
        print(outputs[:min(10, len(outputs))])
    except Exception as e:
        print(input_data_dir+" 처리 중 에러 발생")
        print(e)

output_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False) # 한글 호환되는 포맷
    