# 모델 현황

* KoAlpaca
    * torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 128.00 MiB
* KoVicuna
    * ModuleNotFoundError: No module named 'peft'
* Polyglot-Ko
    * torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 32.00 MiB
* KULLM
    * ModuleNotFoundError: No module named 'utils.prompter'; 'utils' is not a package
* XGML
    * ModuleNotFoundError: No module named 'sagemaker'
* Ko-GPT-Trinity
    * "우겨넣다"와 "욱여넣다" 중 맞는 말은 욱여넣는 것이다.
    * **성공**
* KoGPT
    * ???
* GPT
    * ImportError: cannot import name 'OpenAI' from 'openai'
    * openai의 버전 문제로 추정.