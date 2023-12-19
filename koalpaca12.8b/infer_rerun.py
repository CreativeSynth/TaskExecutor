import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

import pandas as pd
import sys
sys.path.append('../')
from tasks_configure import TaskReader
from collections.abc import Iterable
import torch
from tqdm import tqdm

MODEL = 'beomi/KoAlpaca-Polyglot-12.8B'
MODEL_NAME = "KoAlpaca-Polyglot-12.8B"

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
).to(device=f"cuda", non_blocking=True)
model.eval()

pipe = pipeline(
    'text-generation', 
    model=model,
    tokenizer=MODEL,
    device=0
)

def ask(x, context='', is_input_full=False):
    ans = pipe(
        f"### 질문: {x}\n\n### 맥락: {context}\n\n### 답변:" if context else f"### 질문: {x}\n\n### 답변:", 
        do_sample=True, 
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        return_full_text=False,
        eos_token_id=2,
    )
    return ans[0]['generated_text']


result_data = pd.DataFrame()
rerun = False
try:
    result_data = pd.read_csv("result.csv", engine="python")
    rerun = True
except Exception as e:
    print("failed to load result file")
    print(e)
    pass

taskReader = TaskReader("../../TaskManager")

if taskReader.get_input_data_dirs == []:
    exit

total_len = len(taskReader.get_input_data_dirs())


for ind, input_data_dir in enumerate(taskReader.get_input_data_dirs()):
    data = None
    try:
        data = pd.read_csv(input_data_dir)
    except:
        print(f"[{ind+1}/{total_len}]: Error occures while reading {input_data_dir}. Skikped.")
        continue

    # data filtering that is not in result.csv
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
    cnt = 0

    for i in tqdm(range(len(data))):
        try:
            prompt = data["prompt"][i]
            ret = ask(prompt)
            ret = ret.replace("\n", " ")
            new_data = pd.DataFrame(
                {"task_name": data["task_name"][i],
                "index": data["index"][i],
                "result": ret,
                "model_name": MODEL_NAME
                }
                , index=[0])
            result_data = pd.concat([result_data,  new_data], ignore_index=True)
            cnt += 1
        except Exception as e:
            print(f"[{ind+1}/{total_len}]: {input_data_dir} 처리 중 에러 발생. i = {i}")
            print(e)
    
    print(f"[{ind+1}/{total_len}]: {input_data_dir} 에서 새롭게 {cnt}개 처리.")
    result_data.sort_values(by=['task_name', 'index'], inplace=True)
    result_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False) # 중간중간 저장

result_data.sort_values(by=['task_name', 'index'], inplace=True)
result_data.to_csv("result.csv", encoding = 'utf-8-sig', index=False) # 최종저장