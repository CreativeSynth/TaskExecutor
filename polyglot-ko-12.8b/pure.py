import torch
from transformers import pipeline, AutoModelForCausalLM

MODEL = 'etri-xainlp/polyglot-ko-12.8b-instruct'

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
pipe.model.config.pad_token_id = pipe.model.config.eos_token_id

def ask(x, context='', is_input_full=False):
    ans = pipe(
        f"### 질문: {x}\n\n### 맥락: {context}\n\n### 답변:" if context else f"### 질문: {x}\n\n### 답변:", 
        do_sample=True, 
        max_new_tokens=2048,
        temperature=0.9,
        top_p=0.9,
        return_full_text=False,
        eos_token_id=2,
    )
    return ans[0]['generated_text']

while True:
    quit = input('prompt?: ')
    if quit == 'q':
        break
    else:
        generation = ask(quit)
        print("etri_ai:", generation)
