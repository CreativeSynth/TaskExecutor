import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel

try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName = 'sagemaker_execution_role')['Role']['Arn']

hub = {
    'HF_MODEL_ID': 'facebook/xglm-7.5B',
    'HF_TASK': 'text-generation'
}

huggingface_model = HuggingFaceModel(
    transformers_version = '4.26.0',
    pytorch_version = '1.13.1',
    py_version = 'py39',
    env = hub,
    role = role,
)

predictor = huggingface_model.deploy(
    initial_instance_count = 1,
    instance_type = 'ml.m5.xlarge'
)

predictor.predict({
    "inputs": '"우겨넣다"와 "욱여넣다" 중 맞는 말은 ',
})