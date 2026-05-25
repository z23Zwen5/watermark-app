#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 命名模块 - 移植自「星核OC 拦截款命名工具」core.py
无 GUI 依赖，仅标准库。
"""

import os
import re
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

# ============================================================
# 常量
# ============================================================

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
}
TONE_OPTIONS = ["中文（古风/仙侠/鬼怪）", "英文（西方/现代/赛博）", "日文（和风/日式）"]
TONE_KEY = {
    "中文（古风/仙侠/鬼怪）": "中文",
    "英文（西方/现代/赛博）": "英文",
    "日文（和风/日式）": "日文",
}

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
]

OPENAI_MODELS = [
    "gpt-4.1-mini",
    "gpt-4.1",
    "gpt-4.1-nano",
    "gpt-4o-mini",
    "o4-mini",
]

CLAUDE_MODELS = [
    "claude-sonnet-4-6",
    "claude-opus-4-6",
    "claude-haiku-4-5-20251001",
    "claude-sonnet-4-5-20250514",
]

DOUBAO_MODELS = [
    "doubao-seed-2-0-lite-260215",
    "doubao-seed-2-0-pro-260215",
    "doubao-seed-2-0-mini-260215",
]

QWEN_MODELS = [
    "qwen3-vl-plus",
    "qwen3-vl-flash",
    "qwen-vl-max-latest",
    "qwen-vl-plus-latest",
]

# 文案模板。占位符（大小写敏感）：
#   {date} - 日期(MMDD)   {series} - 系列名   {emoji} - 表情
#   {atmosphere} - AI 生成的氛围文案   {tags} - 标签字符串（含 # 前缀，空格分隔）
# 用户可在 Rename 面板里覆盖此模板；未识别的占位符会原样保留。
DEFAULT_POST_TEMPLATE = """星核档案 NO.{date}｜{series} {emoji}

{atmosphere}

📌 可蹲可拦截
———
⚠️ AI生成图像设子｜AI tag已标
📎 设子仅供参考，禁描图/二改/垫图/融图

{tags}"""

# 默认标签（输出为 #oc #AIGC #设子 #空壳设）。AI 返回的 tags 会追加在后面。
DEFAULT_POST_TAGS = ["oc", "AIGC", "设子", "空壳设"]

# 向后兼容旧引用名
POST_TEMPLATE = DEFAULT_POST_TEMPLATE

PAN_GREETING = "您的拦截款已送到✨ 请妈咪及时查收喔~\n感谢妈咪一直的耐心等待(/ω＼)♡"


def parse_tag_list(raw: str) -> list:
    """把用户输入的标签字符串解析为列表。
    支持空格、逗号（中英文）、井号、换行任意混用作分隔符。
    空串返回空列表（调用方应回退到 DEFAULT_POST_TAGS）。
    """
    if not raw or not raw.strip():
        return []
    cleaned = raw.replace("#", " ").replace("，", " ").replace(",", " ").replace("\n", " ")
    return [t for t in cleaned.split() if t]


def format_post(
    *, date: str, series: str, emoji: str, atmosphere: str,
    extra_tags: list = None,
    template: str | None = None,
    default_tags: list | None = None,
) -> str:
    """根据模板和标签生成小红书文案。

    template:     None/空串 → 使用 DEFAULT_POST_TEMPLATE
    default_tags: None → 使用 DEFAULT_POST_TAGS；空列表也视为「无默认」
    extra_tags:   AI 返回的额外标签，追加在默认标签之后
    未识别的占位符会原样保留（safe_format）。
    """
    tpl = template if (template and template.strip()) else DEFAULT_POST_TEMPLATE
    base_tags = list(default_tags) if default_tags is not None else list(DEFAULT_POST_TAGS)
    all_tags = base_tags + list(extra_tags or [])
    tag_str = " ".join(f"#{t}" for t in all_tags)

    fields = {
        "date": date, "series": series, "emoji": emoji,
        "atmosphere": atmosphere, "tags": tag_str,
    }
    try:
        return tpl.format(**fields)
    except KeyError:
        # 用户写了未知占位符 → 用安全替换避免崩溃
        out = tpl
        for k, v in fields.items():
            out = out.replace("{" + k + "}", str(v))
        return out


# ============================================================
# 文件工具
# ============================================================

_NAMED_RE = re.compile(r'^\d{4}-.+・.+$')


def is_named_file(path: str) -> bool:
    """判断文件名是否已符合 MMDD-系列名・副题 的命名格式。"""
    return bool(_NAMED_RE.match(Path(path).stem))


def parse_named_file(path: str) -> dict | None:
    """从已命名文件中解析出 date, series, subtitle, circled_num。
    返回 None 表示文件名不符合格式。
    """
    stem = Path(path).stem
    if not _NAMED_RE.match(stem):
        return None
    date = stem[:4]
    rest = stem[5:]  # 跳过 "MMDD-"
    parts = rest.split("・", 1)
    if len(parts) != 2:
        return None
    series = parts[0]
    subtitle_raw = parts[1]
    # 提取圆圈编号
    circled_idx = _circled_index(subtitle_raw)
    if circled_idx >= 0:
        circled_char = CIRCLED[circled_idx]
        subtitle = subtitle_raw.replace(circled_char, "", 1)
    else:
        circled_char = ""
        subtitle = subtitle_raw
    return {
        "date": date,
        "series": series,
        "subtitle": subtitle,
        "circled_num": circled_char,
        "circled_idx": circled_idx,
    }


def build_spec_from_named_files(image_paths: list) -> dict | None:
    """从已命名的图片文件列表生成规格清单内容。
    返回 {display_names: list, date, series} 或 None（无可解析文件）。
    """
    parsed = []
    for p in image_paths:
        info = parse_named_file(p)
        if info:
            parsed.append(info)
    if not parsed:
        return None

    # 按日期优先，再按圆圈编号排序
    parsed.sort(key=lambda x: (x["date"], x["circled_idx"] if x["circled_idx"] >= 0 else 999))

    date = parsed[0]["date"]
    series = parsed[0]["series"]
    use_num = len(parsed) > 1

    display_names = []
    for info in parsed:
        num = info["circled_num"]
        sub = info["subtitle"]
        s = info["series"]
        d = info["date"]
        if num:
            dn = f"{num} {d} | {s}・{sub}【买断有赠图】"
        else:
            dn = f"{d} | {s}・{sub}【买断有赠图】"
        display_names.append(dn)

    return {"display_names": display_names, "date": date, "series": series}


def sanitize(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name)


def _extract_number(path: str) -> tuple:
    """从文件名中提取数字用于排序。"""
    nums = re.findall(r'\d+', Path(path).stem)
    if nums:
        return (0, int(nums[0]), Path(path).stem.lower())
    return (1, 0, Path(path).stem.lower())


def find_images(folder: str) -> list:
    files = [os.path.join(folder, f) for f in os.listdir(folder)
             if Path(f).suffix.lower() in IMAGE_EXTS]
    return sorted(files, key=_extract_number)


def sort_paths(paths: list) -> list:
    return sorted(paths, key=_extract_number)


# ============================================================
# Prompt 构建
# ============================================================

# 默认 Prompt 模板。占位符（大小写敏感）：
#   {theme_block}, {date}, {series_block}, {lang_desc}, {count_line}, {series_name_field}
# 用户可自定义此模板；未使用的占位符会被保留原样显示。
DEFAULT_PROMPT_TEMPLATE = """你是星核OC店铺的创意命名助手。请根据以下角色图片为每个角色生成命名和文案。
{theme_block}
## 系列信息
- 日期：{date}
{series_block}
- 副题语言：{lang_desc}
{count_line}

## 副题规则
- 从角色最突出的视觉特征中提取意象
- 禁止直白描述外观（❌ 红衣男、蓝发女、白裙、黑翼）
- 同系列内每个副题从不同维度切入，避免同质化
- 要有意象感和诗意，但不能空洞

## 氛围文案规则（整个系列共用一段）
- 2-4句，诗意，有画面感
- 符合系列调性
- 适合小红书发文

## 输出
请严格按以下JSON格式输出，不要输出任何其他内容：
{{series_name_field}
  "characters": [
    {"index": 1, "subtitle": "副题"}
  ],
  "atmosphere": "氛围文案",
  "emoji": "一个最匹配主题的emoji",
  "tags": ["主题标签1", "主题标签2"]
}

图片按顺序编号，第1张图 = index 1。"""


def build_prompt(
    date: str,
    series: str,
    tone: str,
    auto_series: bool = False,
    theme_hint: str = "",
    image_count: int = 0,
    template: str | None = None,
) -> str:
    lang_desc = {
        "中文": "中文2字（适用于中式古风/仙侠/鬼怪系列）",
        "英文": "英文1个单词（适用于西方/现代/赛博/潮流系列）",
        "日文": "日文2-3字（适用于和风/日式系列）",
    }.get(tone, "中文2字")

    if auto_series:
        series_block = "- 系列名：由你根据所有角色的整体视觉风格和调性来命名（2-4个字，有辨识度）"
        if series:
            series_block += f"\n- 用户参考方向：{series}（仅供参考，可采纳可另取）"
    else:
        series_block = f"- 系列名：{series}"

    series_name_field = '\n  "series_name": "你取的系列名",' if auto_series else ""
    theme_block = f"\n## 主题背景\n{theme_hint}\n" if theme_hint.strip() else ""
    count_line = f"- 图片总数：**{image_count} 张**，characters 数组必须包含且仅包含 {image_count} 个条目\n" if image_count > 0 else ""

    tpl = template if (template and template.strip()) else DEFAULT_PROMPT_TEMPLATE
    substitutions = {
        "{theme_block}": theme_block,
        "{date}": date,
        "{series_block}": series_block,
        "{lang_desc}": lang_desc,
        "{count_line}": count_line,
        "{series_name_field}": series_name_field,
    }
    out = tpl
    for k, v in substitutions.items():
        out = out.replace(k, v)
    return out


# ============================================================
# Provider 调用：内部共用工具
# ============================================================

def _encode_image_b64(path: str) -> tuple:
    """读取图片返回 (mime, base64_data)。"""
    ext = Path(path).suffix.lower()
    mime = MIME_MAP.get(ext, "image/png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return mime, b64


def _http_post_json(url: str, payload: dict, headers: dict,
                    *, timeout: int = 180, http_error_hint_fn=None) -> dict:
    """POST JSON 并解析响应。HTTP / 网络错误统一抛 RuntimeError。
    http_error_hint_fn(code, body) -> str  在 HTTPError 时追加提示。
    """
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        hint = http_error_hint_fn(e.code, body) if http_error_hint_fn else ""
        raise RuntimeError(f"HTTP {e.code}: {body[:500]}{hint or ''}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e


def _extract_json_block(text: str) -> str:
    """从模型自由文本里抽出 {...} JSON 区段。
    剥离 markdown ```json``` 围栏，截取首个 { 到最后一个 } 之间的内容。
    输入若已是干净 JSON 则等价于 strip()。
    """
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1] if "\n" in text else text
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        text = text[start:end]
    return text


def _call_openai_compatible(
    api_key: str, model: str, prompt: str, image_paths: list,
    *,
    url: str,
    response_format: dict = None,
    http_error_hint_fn=None,
    json_decode_error_fn=None,
) -> dict:
    """OpenAI Chat Completions 兼容协议的统一调用（openai / doubao / qwen 共用）。

    response_format:        传 {"type": "json_object"} 启用 JSON 模式；不支持的 provider 传 None。
    json_decode_error_fn:   (raw_text, JSONDecodeError) -> str；返回 None 则按原异常抛。
    """
    content = [{"type": "text", "text": prompt}]
    for p in image_paths:
        mime, b64 = _encode_image_b64(p)
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"},
        })

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0.75,
        "max_tokens": 8192,
    }
    if response_format is not None:
        payload["response_format"] = response_format

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    result = _http_post_json(url, payload, headers, http_error_hint_fn=http_error_hint_fn)

    try:
        text = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected response: {json.dumps(result, ensure_ascii=False)[:500]}")

    raw = text
    cleaned = _extract_json_block(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        if json_decode_error_fn:
            raise RuntimeError(json_decode_error_fn(raw, e)) from e
        raise


# ============================================================
# Gemini API（纯标准库，零依赖）
# ============================================================

def call_gemini(api_key: str, model: str, prompt: str, image_paths: list) -> dict:
    """同步调用 Gemini API，返回解析后的 JSON dict。"""
    parts = [{"text": prompt}]
    for p in image_paths:
        mime, b64 = _encode_image_b64(p)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.75,
            "responseMimeType": "application/json",
            "maxOutputTokens": 8192,
        },
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    result = _http_post_json(url, payload, {"Content-Type": "application/json"})

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected response: {json.dumps(result, ensure_ascii=False)[:500]}")
    return json.loads(text)


# ============================================================
# OpenAI API
# ============================================================

def call_openai(api_key: str, model: str, prompt: str, image_paths: list) -> dict:
    """同步调用 OpenAI Chat Completions API（含视觉）。"""
    return _call_openai_compatible(
        api_key, model, prompt, image_paths,
        url="https://api.openai.com/v1/chat/completions",
        response_format={"type": "json_object"},
    )


# ============================================================
# Claude (Anthropic) API
# ============================================================

def call_claude(api_key: str, model: str, prompt: str, image_paths: list) -> dict:
    """同步调用 Anthropic Messages API（含视觉）。"""
    content = []
    for p in image_paths:
        mime, b64 = _encode_image_b64(p)
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": mime, "data": b64},
        })
    content.append({"type": "text", "text": prompt})

    payload = {
        "model": model,
        "max_tokens": 8192,
        "messages": [{"role": "user", "content": content}],
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    result = _http_post_json("https://api.anthropic.com/v1/messages", payload, headers)

    try:
        text = result["content"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected response: {json.dumps(result, ensure_ascii=False)[:500]}")
    # Claude 可能会在 JSON 前后输出额外文本
    return json.loads(_extract_json_block(text))


# ============================================================
# Doubao / 火山引擎 Ark API（OpenAI 兼容）
# ============================================================

def _doubao_http_hint(code: int, _body: str) -> str:
    if code != 404:
        return ""
    return (
        "\n\n提示：Ark 404 通常表示 model 字段对不上。请去火山控制台「在线推理 / 开通管理」"
        "确认该模型已开通；或创建「推理接入点」，把 ep-xxxxxxxxxxxx-xxxxx "
        "粘到 Model 下拉框里（可编辑）。"
    )


def call_doubao(api_key: str, model: str, prompt: str, image_paths: list) -> dict:
    """同步调用火山引擎 Ark（豆包）Chat Completions API。
    model 可填豆包模型 ID 或用户在控制台创建的 endpoint ID（ep-xxx）。
    """
    return _call_openai_compatible(
        api_key, model, prompt, image_paths,
        url="https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        http_error_hint_fn=_doubao_http_hint,
    )


# ============================================================
# Qwen / 阿里云百炼 DashScope API（OpenAI 兼容）
# ============================================================

def _qwen_json_decode_msg(raw: str, exc: json.JSONDecodeError) -> str:
    snippet = raw[:400] + ("…" if len(raw) > 400 else "")
    return (
        f"Qwen 返回内容无法解析为 JSON ({exc.msg} @ char {exc.pos})。\n"
        f"原始响应开头:\n{snippet}"
    )


def call_qwen(api_key: str, model: str, prompt: str, image_paths: list) -> dict:
    """同步调用阿里云百炼（通义千问）DashScope OpenAI 兼容接口。"""
    return _call_openai_compatible(
        api_key, model, prompt, image_paths,
        url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        response_format={"type": "json_object"},
        json_decode_error_fn=_qwen_json_decode_msg,
    )


# ============================================================
# Provider 注册表 - 新增供应商在此处加一行即可
# ============================================================

PROVIDERS = {
    "gemini": {
        "display_name": "Gemini",
        "models": GEMINI_MODELS,
        "key_attr": "gemini_api_key",
        "key_label": "Gemini Key:",
        "key_placeholder": "AIza…",
        "model_editable": False,
        "call": call_gemini,
    },
    "openai": {
        "display_name": "OpenAI",
        "models": OPENAI_MODELS,
        "key_attr": "openai_api_key",
        "key_label": "OpenAI Key:",
        "key_placeholder": "sk-…",
        "model_editable": False,
        "call": call_openai,
    },
    "claude": {
        "display_name": "Claude",
        "models": CLAUDE_MODELS,
        "key_attr": "claude_api_key",
        "key_label": "Claude Key:",
        "key_placeholder": "sk-ant-…",
        "model_editable": False,
        "call": call_claude,
    },
    "doubao": {
        "display_name": "Doubao",
        "models": DOUBAO_MODELS,
        "key_attr": "doubao_api_key",
        "key_label": "Doubao Key:",
        "key_placeholder": "火山 API Key（model 下拉可手填 ep-xxx endpoint ID 或完整模型 ID）",
        "model_editable": True,
        "call": call_doubao,
    },
    "qwen": {
        "display_name": "Qwen",
        "models": QWEN_MODELS,
        "key_attr": "qwen_api_key",
        "key_label": "Qwen Key:",
        "key_placeholder": "阿里云百炼 sk-… (DashScope API Key)",
        "model_editable": True,
        "call": call_qwen,
    },
}

PROVIDER_ORDER = ["gemini", "openai", "claude", "doubao", "qwen"]


# ============================================================
# 输出构建
# ============================================================

def build_outputs(
    date: str,
    series: str,
    characters: list,
    image_paths: list,
    atmosphere: str = "",
    emoji: str = "✨",
    tags: list = None,
    post_template: str | None = None,
    default_tags: list | None = None,
) -> dict:
    """根据 Gemini 返回数据构建全部输出。

    post_template / default_tags: 见 format_post。空 / None 则回退到内置默认。
    """
    use_num = len(characters) > 1

    file_names = []
    display_names = []

    for i, ch in enumerate(characters):
        sub = ch.get("subtitle", "")
        num = CIRCLED[i] if use_num and i < len(CIRCLED) else ""

        ext = Path(image_paths[i]).suffix if i < len(image_paths) else ".png"
        fn = sanitize(f"{date}-{series}・{num}{sub}{ext}")
        dn = f"{num} {date} | {series}・{sub}【买断有赠图】" if num else f"{date} | {series}・{sub}【买断有赠图】"

        file_names.append(fn)
        display_names.append(dn)

    post = format_post(
        date=date, series=series, emoji=emoji, atmosphere=atmosphere,
        extra_tags=tags or [],
        template=post_template,
        default_tags=default_tags,
    )

    combined = ""
    combined += "=== 文件命名 ===\n" + "\n".join(file_names) + "\n\n"
    combined += "=== 规格名/展示命名 ===\n" + "\n".join(display_names) + "\n\n"
    combined += "=== 小红书文案 ===\n" + post

    return {
        "file_names": file_names,
        "display_names": display_names,
        "post": post,
        "combined": combined,
    }


def save_rename_outputs(
    folder: str,
    image_paths: list,
    outputs: dict,
    save_txts: bool = True,
    rename_images: bool = True,
) -> dict:
    """按需写入 txt 文件 / 重命名图片。返回 {txt_files, renamed}。

    save_txts:    True 时写 文案.txt + 规格清单.txt
    rename_images: True 时按 outputs['file_names'] 改名
    两个开关相互独立，避免 Rename Files 顺手覆盖已编辑过的 txt。
    """
    txt_files = []

    if save_txts:
        with open(os.path.join(folder, "文案.txt"), "w", encoding="utf-8") as f:
            f.write(outputs["post"])
        txt_files.append("文案.txt")

        with open(os.path.join(folder, "规格清单.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(outputs["display_names"]))
        txt_files.append("规格清单.txt")

    renamed = []
    if rename_images:
        for i, path in enumerate(image_paths):
            if i < len(outputs["file_names"]):
                new_path = os.path.join(folder, outputs["file_names"][i])
                if path != new_path:
                    if os.path.exists(new_path):
                        base, ext = os.path.splitext(new_path)
                        new_path = f"{base}_1{ext}"
                    os.rename(path, new_path)
                    renamed.append((os.path.basename(path), os.path.basename(new_path)))

    return {"txt_files": txt_files, "renamed": renamed}


# ============================================================
# 一体化接口
# ============================================================

def generate_and_build(
    api_key: str,
    image_paths: list,
    date: str,
    series: str = "",
    tone: str = "中文",
    auto_series: bool = False,
    model: str = "gemini-2.5-flash",
    provider: str = "gemini",
    theme_hint: str = "",
    prompt_template: str | None = None,
    post_template: str | None = None,
    default_tags: list | None = None,
) -> dict:
    """调 API + 构建输出，不执行文件操作。
    provider: 'gemini' | 'openai'
    prompt_template: 可选自定义 AI 命名 Prompt 模板（空 → 默认）
    post_template:   可选自定义小红书文案模板（空 → DEFAULT_POST_TEMPLATE）
    default_tags:    可选自定义默认标签列表（None → DEFAULT_POST_TAGS）
    返回: {series_name, characters, outputs, raw}
    """
    prompt = build_prompt(
        date, series, tone, auto_series, theme_hint,
        image_count=len(image_paths),
        template=prompt_template,
    )
    spec = PROVIDERS.get(provider) or PROVIDERS["gemini"]
    data = spec["call"](api_key, model, prompt, image_paths)

    final_series = data.get("series_name", series) if auto_series else series
    characters = data.get("characters", [])

    outputs = build_outputs(
        date=date,
        series=final_series,
        characters=characters,
        image_paths=image_paths,
        atmosphere=data.get("atmosphere", ""),
        emoji=data.get("emoji", "✨"),
        tags=data.get("tags", []),
        post_template=post_template,
        default_tags=default_tags,
    )

    return {
        "series_name": final_series,
        "characters": characters,
        "outputs": outputs,
        "gemini_raw": data,
    }


# ============================================================
# 网盘发货
# ============================================================

def parse_pan_links(text: str) -> list:
    """解析百度网盘分享文本，返回 [{filename, link_line}, ...]。"""
    lines = [l.strip() for l in text.strip().splitlines()]
    blocks = []
    last_filename = None

    for line in lines:
        if not line:
            continue
        if line.startswith("链接:") or line.startswith("链接："):
            if last_filename:
                blocks.append({"filename": last_filename, "link_line": line})
                last_filename = None
        elif (line.startswith("提取码") or line.startswith("--来自")
              or line.startswith("http")):
            continue
        else:
            m = re.search(r'[\w\-・①②③④⑤⑥⑦⑧⑨⑩⑪⑫]+\.\w{2,5}$', line)
            if m:
                last_filename = m.group(0)

    return blocks


def _circled_index(s: str) -> int:
    """从字符串中提取圆圈编号索引，无编号返回 -1。"""
    for i, c in enumerate(CIRCLED):
        if c in s:
            return i
    return -1


def build_pan_message(file_names: list, pan_text: str, greeting: str = "") -> tuple:
    """匹配网盘链接到已命名文件，生成发货信息。
    返回 (完整消息文本, [未匹配的文件名])。
    """
    greeting = greeting.strip() or PAN_GREETING
    blocks = parse_pan_links(pan_text)
    link_map = {b["filename"]: b["link_line"] for b in blocks}

    entries = []
    matched_files = set()
    for fn in file_names:
        if fn in link_map:
            matched_files.add(fn)
            stem = Path(fn).stem
            idx = _circled_index(stem)
            # 提取日期用于排序
            date_part = stem[:4] if len(stem) >= 4 else ""
            entries.append({
                "filename": stem,
                "date": date_part,
                "link_line": link_map[fn],
                "sort_idx": idx if idx >= 0 else 999,
            })

    entries.sort(key=lambda e: (e["date"], e["sort_idx"]))
    unmatched = [fn for fn in file_names if fn not in matched_files]

    lines = []
    for e in entries:
        lines.append(greeting)
        lines.append("")
        lines.append(e["filename"])
        lines.append(e["link_line"])
        lines.append("")

    return "\n".join(lines).rstrip(), unmatched
