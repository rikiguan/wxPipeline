from zhipuai import ZhipuAI
from conf import *

client = ZhipuAI(api_key=apiKey)
response = client.chat.completions.create(
    model="glm-4-0520",  # 填写需要调用的模型编码
    messages=[
        {"role": "user", "content": "你是一名高情商的感情大师，你会把我发给女朋友的句子优化的更加活泼得体[要求：直接返回句子内容]句子内容是：你是不是傻"}
    ],
)
print(response.choices[0].message.content.replace('"',''))