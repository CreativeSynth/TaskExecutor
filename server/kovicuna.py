import torch
from transformers import pipeline, AutoModelForCausalLM
from peft import IA3Config

MODEL = 'junelee/ko_vicuna_7b'

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    # load_in_8bit = True,
    torch_dtype=torch.float16,
    # device_map = device_map,
)

config = IA3Config(
    peft_type = "IA3",
    task_type = "CAUSAL_LM",
    target_modules = ['q_proj', 'k_proj', 'down_prog'],
    feedforward_modules = ["down_proj"],
)

model = get_peft_model(model, config)
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
    print(ans[0]['generated_text'])

ask("딥러닝이 뭐야?")
