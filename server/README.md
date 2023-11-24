# 모델 현황

* KoAlpaca
    * torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 128.00 MiB (GPU 0; 23.65 GiB total capacity; 368.56 MiB already allocated; 125.44 MiB free; 386.00 MiB reserved in total by PyTorch)
* KoVicuna
    * ModuleNotFoundError: No module named 'peft'
* Polyglot-Ko
    * torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 32.00 MiB (GPU 0; 23.65 GiB total capacity; 488.20 MiB already allocated; 9.44 MiB free; 502.00 MiB reserved in total by PyTorch)
* KULLM
    * ModuleNotFoundError: No module named 'utils.prompter'; 'utils' is not a package
* XGML
    * botocore.exceptions.NoCredentialsError: Unable to locate credentials
* Ko-GPT-Trinity
    * "우겨넣다"와 "욱여넣다" 중 맞는 말은 욱여넣는 것이다.
    * **성공**
* KoGPT
    * ???
* GPT
    * ImportError: cannot import name 'OpenAI' from 'openai'
    * openai의 버전 문제로 추정.