import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# API URL
llm_api_url = os.getenv("LLM_BASE_URL")
# api_url = "http://localhost:11434"

# 设置请求头
headers = {
    "Content-Type": "application/json",
}

# 设置请求数据
data = {
    'model': 'llama3',  # 指定要使用的模型
    'prompt': '用中文帮我安排一个7天的北京旅行行程。',  # 问题
    'max_tokens': 10000,  # 生成回答的最大token数
    'stream': False  # 是否流式回答
}

# 发送POST请求
response = requests.post(f"{llm_api_url}/api/generate", headers=headers, data=json.dumps(data))
# 检查响应状态码
if response.status_code == 200:
    # 解析响应内容
    result = response.text
    print("模型回答:", json.loads(result)['response'])
else:
    print("请求失败，状态码:", response.status_code)