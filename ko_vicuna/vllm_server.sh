CUDA_VISIBLE_DEVICES=1,2 python -m vllm.entrypoints.openai.api_server --model junelee/ko_vicuna_7b --host 147.46.219.237 --port 8124 --tensor-parallel-size 2
