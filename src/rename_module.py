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

POST_TEMPLATE = """{emoji} 灵感分享 {date}｜{series}

{atmosphere}

今日灵感：{series} {emoji}
———
📌 可蹲可拦截
———
❗以上为AI生成图像设子，AI tag已标，触雷请左滑勿ky
———
📎设子仅供参考，不可描图、二改、垫图、融图❗
———
{tags}"""

PAN_GREETING = "您的拦截款已送到✨ 请妈咪及时查收喔~\n感谢妈咪一直的耐心等待(/ω＼)♡"


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

    # 按圆圈编号排序
    parsed.sort(key=lambda x: x["circled_idx"] if x["circled_idx"] >= 0 else 999)

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

def build_prompt(date: str, series: str, tone: str, auto_series: bool = False) -> str:
    lang_desc = {
        "中文": "中文2字（适用于中式古风/仙侠/鬼怪系列）。示例：啖花、冥录、折枝",
        "英文": "英文1个单词（适用于西方/现代/赛博/潮流系列）。示例：Prism、Rust、Veil",
        "日文": "日文2-3字（适用于和风/日式系列）。示例：面影、花散里、残響",
    }.get(tone, "中文2字")

    if auto_series:
        series_block = "- 系列名：由你根据所有角色的整体视觉风格和调性来命名（2-4个字，有辨识度）"
        if series:
            series_block += f"\n- 用户参考方向：{series}（仅供参考，可采纳可另取）"
    else:
        series_block = f"- 系列名：{series}"

    series_name_field = '\n  "series_name": "你取的系列名",' if auto_series else ""

    return f"""你是星核OC店铺的创意命名助手。请根据以下角色图片为每个角色生成命名和文案。

## 系列信息
- 日期：{date}
{series_block}
- 副题语言：{lang_desc}

## 副题规则
- 从角色最突出的视觉特征中提取意象
- 禁止直白描述外观（❌ 红衣男、蓝发女、白裙、黑翼）
- 同系列内每个副题从不同维度切入，避免同质化
- 要有意象感和诗意，但不能空洞

## 释义文案规则
- 视觉元素 + 概念延伸，1-3句
- 语感匹配系列调性（暗黑要鬼气、甜系要毒性、潮流要冲击感）
- 简洁有力

## 氛围文案规则（整个系列共用一段）
- 2-4句，诗意，有画面感
- 符合系列调性
- 适合小红书发文

## 输出
请严格按以下JSON格式输出，不要输出任何其他内容：
{{{series_name_field}
  "characters": [
    {{"index": 1, "subtitle": "副题", "explanation": "释义文案"}}
  ],
  "atmosphere": "氛围文案",
  "emoji": "一个最匹配主题的emoji",
  "tags": ["主题标签1", "主题标签2"]
}}

图片按顺序编号，第1张图 = index 1。"""


# ============================================================
# Gemini API（纯标准库，零依赖）
# ============================================================

def call_gemini(api_key: str, model: str, prompt: str, image_paths: list) -> dict:
    """同步调用 Gemini API，返回解析后的 JSON dict。"""
    parts = [{"text": prompt}]
    for p in image_paths:
        ext = Path(p).suffix.lower()
        mime = MIME_MAP.get(ext, "image/png")
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"temperature": 0.75, "responseMimeType": "application/json"},
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body[:500]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected response: {json.dumps(result, ensure_ascii=False)[:500]}")
    return json.loads(text)


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
) -> dict:
    """根据 Gemini 返回数据构建全部输出。"""
    tags = tags or []
    use_num = len(characters) > 1

    file_names = []
    display_names = []
    explanations = []

    for i, ch in enumerate(characters):
        sub = ch.get("subtitle", "")
        expl = ch.get("explanation", "")
        num = CIRCLED[i] if use_num and i < len(CIRCLED) else ""

        ext = Path(image_paths[i]).suffix if i < len(image_paths) else ".png"
        fn = sanitize(f"{date}-{series}・{num}{sub}{ext}")
        dn = f"{num} {date} | {series}・{sub}【买断有赠图】" if num else f"{date} | {series}・{sub}【买断有赠图】"
        ep = f"> **{num}{sub}**——{expl}"

        file_names.append(fn)
        display_names.append(dn)
        explanations.append(ep)

    tag_str = " ".join(f"#{t}" for t in ["oc", "aigc", "设子", "空壳设"] + tags)
    post = POST_TEMPLATE.format(
        emoji=emoji, date=date, series=series, atmosphere=atmosphere, tags=tag_str
    )

    combined = ""
    combined += "=== 文件命名 ===\n" + "\n".join(file_names) + "\n\n"
    combined += "=== 规格名/展示命名 ===\n" + "\n".join(display_names) + "\n\n"
    combined += "=== 释义 ===\n" + "\n".join(explanations) + "\n\n"
    combined += "=== 小红书文案 ===\n" + post

    return {
        "file_names": file_names,
        "display_names": display_names,
        "explanations": explanations,
        "post": post,
        "combined": combined,
    }


def save_rename_outputs(
    folder: str,
    image_paths: list,
    outputs: dict,
    rename_images: bool = True,
    save_explanation: bool = True,
) -> dict:
    """写入 txt 文件并重命名图片。返回 {txt_files, renamed}。"""
    txt_files = []

    with open(os.path.join(folder, "文案.txt"), "w", encoding="utf-8") as f:
        f.write(outputs["post"])
    txt_files.append("文案.txt")

    with open(os.path.join(folder, "规格清单.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(outputs["display_names"]))
    txt_files.append("规格清单.txt")

    if save_explanation:
        with open(os.path.join(folder, "释义.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(outputs["explanations"]))
        txt_files.append("释义.txt")

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
) -> dict:
    """调 Gemini API + 构建输出，不执行文件操作。
    返回: {series_name, characters, outputs, gemini_raw}
    """
    prompt = build_prompt(date, series, tone, auto_series)
    data = call_gemini(api_key, model, prompt, image_paths)

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


def build_pan_message(file_names: list, pan_text: str) -> tuple:
    """匹配网盘链接到已命名文件，生成发货信息。
    返回 (完整消息文本, [未匹配的文件名])。
    """
    blocks = parse_pan_links(pan_text)
    link_map = {b["filename"]: b["link_line"] for b in blocks}

    entries = []
    matched_files = set()
    for fn in file_names:
        if fn in link_map:
            matched_files.add(fn)
            stem = Path(fn).stem
            parts = stem.split("・", 1)
            subtitle = parts[1] if len(parts) > 1 else stem
            idx = _circled_index(subtitle)
            entries.append({
                "subtitle": subtitle,
                "link_line": link_map[fn],
                "sort_idx": idx if idx >= 0 else 999,
            })

    entries.sort(key=lambda e: e["sort_idx"])
    unmatched = [fn for fn in file_names if fn not in matched_files]

    lines = []
    for e in entries:
        lines.append(PAN_GREETING)
        lines.append("")
        lines.append(e["subtitle"])
        lines.append(e["link_line"])
        lines.append("")

    return "\n".join(lines).rstrip(), unmatched
