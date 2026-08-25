# -*- coding: utf-8 -*-
"""从「英文原版 + 已汉化版本」自动提取替换对,生成 patches.json (v2 块级 diff)

用法:
    python generate-patches.py --pristine <英文原版dist> --localized <已汉化dist> [-o patches.json]

v2 改进:
    - 使用 SequenceMatcher opcodes,按 replace 块(可多行)配对英文原文块 -> 中文译文块
    - 应用时按块长度降序替换,避免子串互相覆盖
    - 输出前做「原版+补丁 == 汉化版」完整性校验,不一致文件列出供人工处理
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u4e00-\u9fff]")
MAX_BLOCK = 4000  # 单块最大字符数,防止误匹配超大块


def collect_files(root: Path):
    return sorted(p for p in root.rglob("*.js") if p.is_file())


def extract_pairs(p_text: str, l_text: str):
    p_lines = p_text.splitlines(keepends=True)
    l_lines = l_text.splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(None, p_lines, l_lines, autojunk=False)
    pairs = []
    for tag, ai, aj, bi, bj in matcher.get_opcodes():
        if tag != "replace":
            continue
        a_block = "".join(p_lines[ai:aj])
        b_block = "".join(l_lines[bi:bj])
        if len(a_block) > MAX_BLOCK or len(b_block) > MAX_BLOCK:
            continue
        if a_block and b_block and a_block != b_block and CJK.search(b_block):
            if a_block.strip() != b_block.strip():  # 过滤纯空白/格式差异
                pairs.append((a_block, b_block))
    # 长块优先,避免短替换破坏长块原文
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pristine", required=True)
    ap.add_argument("--localized", required=True)
    ap.add_argument("-o", "--output", default="patches.json")
    args = ap.parse_args()

    pristine_root = Path(args.pristine)
    localized_root = Path(args.localized)
    all_patches = {}
    verified_ok = 0
    problems = []

    for pf in collect_files(pristine_root):
        rel = pf.relative_to(pristine_root)
        lf = localized_root / rel
        if not lf.exists():
            continue
        p_text = pf.read_text(encoding="utf-8")
        l_text = lf.read_text(encoding="utf-8")
        if not CJK.search(l_text):
            continue
        pairs = extract_pairs(p_text, l_text)
        if not pairs:
            continue
        applied = p_text
        for old, new in pairs:
            applied = applied.replace(old, new)
        # 容忍结尾换行差异(脚本写入时常带多余换行,不影响内容)
        if applied == l_text or applied.rstrip("\n") == l_text.rstrip("\n"):
            verified_ok += 1
            # JSON 中始终使用 POSIX 分隔符，保证补丁可跨 Windows/macOS/Linux 使用。
            all_patches[rel.as_posix()] = pairs
        else:
            problems.append(rel.as_posix())

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(all_patches, fh, ensure_ascii=False, indent=1)

    total = sum(len(v) for v in all_patches.values())
    print(f"[OK] 完整校验通过文件: {verified_ok}")
    print(f"[TODO] 校验失败文件: {problems}")
    print(f"共提取替换对: {total} 条, 覆盖 {len(all_patches)} 个文件 -> {args.output}")


if __name__ == "__main__":
    sys.exit(main())
