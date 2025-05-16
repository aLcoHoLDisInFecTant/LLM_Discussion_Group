# utils/llm_utils.py

from openai_client import call_llm
import ast, re

def llm_generate_options(topic: str, model: str = "gpt-4.1") -> list[str]:
    prompt = f"""
For the following discussion topic, generate 3 to 5 distinct and mutually exclusive voting options that represent different positions.

Topic: "{topic}"

Please return them as a Python list of quoted strings.
For example: ["Option A", "Option B", "Option C"]
"""
    raw = call_llm(prompt, model=model)
    return _parse_ranked_list(raw)

def _parse_ranked_list(raw: str) -> list[str]:
    try:
        match = re.findall(r'\[(.*?)\]', raw)
        if match:
            items = ast.literal_eval(f"[{match[0]}]")
            return [item.strip().strip('"').strip("'") for item in items]
        else:
            return []
    except Exception:
        return []
