
from transformers import AutoTokenizer, AutoModelForCausalLM

input_data_dirs = [
        "../../TaskManager/ko_quiz/ko_quiz_1.csv",
]


tokenizer = AutoTokenizer.from_pretrained("EleutherAI/polyglot-ko-12.8b")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/polyglot-ko-12.8b")

prompt = "따분하다는 무슨 뜻이야?"
max_new_tokens = 100
temperature = 0.7
outputs = model.generate(tokenizer(prompt, return_tensors="pt").input_ids, max_new_tokens=max_new_tokens, temperature=temperature)
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
