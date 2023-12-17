import pandas as pd
import sys
sys.path.append('../')
from tasks_configure import TaskReader
from vllm import LLM, SamplingParams
from collections.abc import Iterable


def messages_to_string(prompts: Iterable[str]):
    return [f"### 질문: {instruction}\n\n### 답변:" for instruction in prompts]


taskReader = TaskReader("../../TaskManager")

if taskReader.get_input_data_dirs == []:
    exit

MAX_TOKENS = 1024
MAX_BATCH_SIZE = 128
sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=MAX_TOKENS)
llm = LLM(model="qwopqwop/KoAlpaca-Polyglot-12.8B-GPTQ", tensor_parallel_size=4)
MODEL_NAME = "koalpaca-12.8b"
FILE_NAME = "result.csv"

result_data = pd.DataFrame()
rerun = False
try:
    result_data = pd.read_csv(FILE_NAME, engine="python")
    rerun = True
except Exception as e:
    print("failed to load result file")
    print(e)
    pass


total_len = len(taskReader.get_input_data_dirs())


for ind, input_data_dir in enumerate(taskReader.get_input_data_dirs()):
    data = None
    try:
        data = pd.read_csv(input_data_dir)
    except:
        print(f"[{ind+1}/{total_len}]: Error occures while reading {input_data_dir}. Skikped.")
        continue


    # data filtering that is not in result file
    remain_indexes = []
    if rerun is True:
        for i in range(len(data)):
            ret1 = result_data.query(f"task_name == '{data['task_name'][i]}' and index == {data['index'][i]}")
            ret2 = result_data.query(f"task_name == '{data['task_name'][i]}' and index == '{data['index'][i]}'")
            # if result is empty
            if len(ret1) == 0 and len(ret2) == 0:
                remain_indexes.append(i)
                print(f"task_name == '{data['task_name'][i]}' and index == {data['index'][i]}")
    else:
        remain_indexes = list(range(len(data)))

    if remain_indexes == []:
        print(f"[{ind+1}/{total_len}]: {input_data_dir} is already processed. Skipped.")
        continue
    
    print(f"[{ind+1}/{total_len}]: {input_data_dir} processing needed {len(remain_indexes)}/{len(data)}.")

    data = data.iloc[remain_indexes]

    # restart processing
    bs = MAX_BATCH_SIZE # initial batch size
    st_pos = 0 # processing starting position
    success_cnt = 0
    while bs > 0 and st_pos < len(data):
        try:
            end_pos = min(len(data), st_pos + bs)
            subdata = data.iloc[st_pos:end_pos].copy()
            prompts = subdata["prompt"].to_list()

            prompts = messages_to_string(prompts) # generate prompts

            outputs = llm.generate(prompts, sampling_params) # generate data

            outputs = [output.outputs[0].text for output in outputs] # 결과 텍스트만 가져옴
            outputs = [output.replace("\n", " ") for output in outputs] # 개행문자를 공백으로 대체.

            subdata["result"] = outputs
            subdata["model_name"] = MODEL_NAME
            result_data = pd.concat([result_data, subdata[["task_name", "index", "result", "model_name"]]], ignore_index=True)
            st_pos += bs # go to next position
            success_cnt = success_cnt + 1
            if bs < MAX_BATCH_SIZE and success_cnt > 1: # 두번 연속으로 성공하면 배치크기를 두배로 늘려봄
                bs *= 2
        except Exception as e:
            print(f"[{ind+1}/{total_len}]: {input_data_dir} 처리 중 에러 발생. bath size = {bs}, pos = {st_pos}")
            print(e)
            bs=bs//2
            success_cnt = 0
    
    print(f"[{ind+1}/{total_len}]: {input_data_dir} 에서 새롭게 {min(st_pos, len(data))}개 처리.")
    result_data.sort_values(by=['task_name', 'index'], inplace=True)
    result_data.to_csv(FILE_NAME, encoding = 'utf-8-sig', index=False) # 중간중간 저장

result_data.sort_values(by=['task_name', 'index'], inplace=True)
result_data.to_csv(FILE_NAME, encoding = 'utf-8-sig', index=False) # 최종저장