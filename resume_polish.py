"""resume-polish-lite：把大白话经历改写为「动作动词 + 量化结果」的简历 bullet。

无 LLM 时的规则：
- 识别并替换弱开头（负责 / 参与 / 协助 -> 强动作动词）；
- 抽取其中的量化数字（百分比、倍数、金额、数量）；
- 套模板输出 "动词 + 做了什么 + 量化结果" 的简洁 bullet。
可选 LLM 进一步润色。
"""

from __future__ import annotations

import json
import os
import re
import urllib.request

WEAK_TO_STRONG = {
    "负责": "主导",
    "参与": "参与落地",
    "协助": "支持推进",
    "帮忙": "配合完成",
    "做了": "完成",
    "搞了": "搭建",
    "弄了": "实现",
    "主管": "统筹",
    "打理": "运营",
}

ACTION_VERBS = [
    "主导", "搭建", "设计", "实现", "优化", "推动", "统筹", "落地",
    "重构", "提升", "拓展", "建立", "自动化", "牵头",
]

NUMBER_RE = re.compile(
    r"(\d+(?:\.\d+)?\s*(?:%|％|倍|万|亿|w|W|k|K|个|条|人|次|天|月|年)?)")


def polish_one(line: str) -> str:
    """把一条大白话经历润色为简历 bullet。"""
    line = line.strip().rstrip("。.")
    if not line:
        return ""

    for weak, strong in WEAK_TO_STRONG.items():
        if line.startswith(weak):
            line = strong + line[len(weak):]
            break

    nums = NUMBER_RE.findall(line)
    line = re.sub(r"了(?=[，,])", "", line)

    bullet = line if line.endswith(("。", ".")) else line
    if nums:
        bullet = re.sub(r"\s+", "", bullet)
    else:
        bullet = bullet + "（可补充量化结果，如提升 X%）"
    return bullet


def polish(lines: list[str], use_llm: bool = False) -> list[str]:
    """批量润色；可选 LLM。"""
    result = [b for b in (polish_one(l) for l in lines) if b]
    if use_llm and os.environ.get("OPENAI_API_KEY"):
        try:
            return polish_llm(result)
        except Exception as exc:
            print(f"[warn] LLM 润色失败，使用规则结果：{exc}")
    return result


def polish_llm(bullets: list[str], api_key: str | None = None,
               base_url: str | None = None, model: str | None = None) -> list[str]:
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                or "https://api.openai.com/v1").rstrip("/")
    model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        raise RuntimeError("未设置 OPENAI_API_KEY")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是简历润色专家，把每条经历改写为动作动词开头、尽量量化的 bullet，输出 JSON 字符串数组，不要解释。"},
            {"role": "user", "content": "请润色以下简历条目：\n" + "\n".join(f"- {b}" for b in bullets)},
        ],
        "temperature": 0.4,
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"].strip().strip("`")
    if content.startswith("json"):
        content = content[4:].strip()
    return [str(x) for x in json.loads(content)]
