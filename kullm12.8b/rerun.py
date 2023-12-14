import pandas as pd
import sys
sys.path.append('../')
from tasks_configure import TaskReader

result_data = pd.DataFrame()
rerun = False

try:
    result_data = pd.read_csv("result.csv")
    rerun = True
except:
    pass

taskReader = TaskReader("../../TaskManager")

if taskReader.get_input_data_dirs == []:
    exit

MAX_TOKENS = 256
MAX_BATCH_SIZE = 128
#sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=MAX_TOKENS)
#llm = LLM(model="nlpai-lab/kullm-polyglot-12.8b-v2", tensor_parallel_size=4)


total_len = len(taskReader.get_input_data_dirs())


for ind, input_data_dir in enumerate(taskReader.get_input_data_dirs()):
    data = None
    try:
        data = pd.read_csv(input_data_dir)
    except:
        print(f"[{ind}/{total_len}]: Error occures while reading {input_data_dir}. Skikped.")
        continue

    # data filtering that is not in result.csv
    remain_indexes = []
    if rerun is True:
        for i in range(len(data)):
            ret = result_data.query(f"task_name == '{data['task_name'][i]}' and index == {data['index'][i]}")
            # if result is empty
            if len(ret) == 0:
                remain_indexes.append(i)
    else:
        remain_indexes = list(range(len(data)))

    if remain_indexes == []:
        print(f"[{ind}/{total_len}]: {input_data_dir} is already processed. Skipped.")
        continue
    
    print(f"[{ind}/{total_len}]: {input_data_dir} processing needed {len(remain_indexes)}/{len(data)}.")

    data = data.iloc[remain_indexes]

    # restart processing
    bs = MAX_BATCH_SIZE # initial batch size
    st_pos = 0 # processing starting position

    while bs > 0 and st_pos < len(data):
        try:
            end_pos = min(len(data), st_pos + bs)
            subdata = data.iloc[st_pos:end_pos].copy()
            prompts = subdata["prompt"].to_list()

            outputs = prompts # generate data

            subdata["result"] = outputs
            subdata["model_name"] = "kullm12.8b"
            result_data = pd.concat([result_data, subdata[["task_name","index", "result", "model_name"]]], ignore_index=True)
            st_pos += bs # go to next position
        except Exception as e:
            print(f"[{ind}/{total_len}]: {input_data_dir} 처리 중 에러 발생. bath size = {bs}, pos = {st_pos}")
            print(e)
            bs=bs//2
    
    print(f"[{ind}/{total_len}]: {input_data_dir} 에서 새롭게 {min(st_pos, len(data))}개 처리.")
    result_data.sort_values(by=['task_name', 'index'], inplace=True)
    result_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False) # 중간중간 저장

result_data.sort_values(by=['task_name', 'index'], inplace=True)
result_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False) # 최종저장