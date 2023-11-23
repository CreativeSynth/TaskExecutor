from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
    "대한민국의 수도는?",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

llm = LLM(model="nlpai-lab/kullm-polyglot-12.8b-v2", tensor_parallel_size=4)

outputs = llm.generate(prompts, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
