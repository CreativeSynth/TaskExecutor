CUDA_VISIBLE_DEVICES=0,1,2,3 python -m vllm.entrypoints.openai.api_server --model nlpai-lab/kullm-polyglot-5.8b-v2 --host 147.46.219.237 --port 8123 --tensor-parallel-size 4
