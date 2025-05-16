# llm_api/openai_client.py

from openai import OpenAI

# 模型 1（默认）：gpt-4.1 via zhizengzeng
API_SECRET_KEY_1 = "sk-zk2ce785dbb50e420728c1e1e8cf55a13be682676a2b006b"
BASE_URL_1 = "https://api.zhizengzeng.com/v1/"

# 模型 2：gemini-2.0-flash-thinking-exp（同样使用 BASE_URL_1）
# 模型 3：DeepSeek-R1 via siliconflow
API_SECRET_KEY_2 = "sk-twrjsuuzwysueciikxfimexrliahbnrnqpefzoxugzbdjjcp"
BASE_URL_2 = "https://api.siliconflow.cn/v1/"


def call_llm(prompt: str, model: str = "gpt-4.1") -> str:
    """
    统一调用 LLM 模型（支持 gpt-4.1、gemini-2.0-flash-thinking-exp、DeepSeek-R1）
    """
    if model == "Pro/deepseek-ai/DeepSeek-R1":
        client = OpenAI(api_key=API_SECRET_KEY_2, base_url=BASE_URL_2)
    else:
        client = OpenAI(api_key=API_SECRET_KEY_1, base_url=BASE_URL_1)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] LLM API 调用失败：{e}"
