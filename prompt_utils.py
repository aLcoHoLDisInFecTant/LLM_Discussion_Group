# utils/prompt_utils.py

import os
from jinja2 import Template

def load_prompt(path: str, context: dict) -> str:
    """
    加载并填充 prompt 模板

    参数：
        path: 模板文件路径（.txt）
        context: 字典，用于替换 {{key}} 的值

    返回：
        渲染后的字符串
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(**context)
