# -*- coding: utf-8 -*-
"""pi-zh-apply.py — Pi (@earendil-works/pi-coding-agent) 一键中文汉化 / 升级后恢复

用法:
    python pi-zh-apply.py                 # 自动探测安装位置
    python pi-zh-apply.py --dist <路径>   # 指定 dist 目录(升级后重跑用)
    python pi-zh-apply.py --check         # 只检查当前汉化状态,不修改

原理:
    读取同目录 patches.json(由 generate-patches.py 从「英文原版 + 已汉化版」提取),
    把每个文件的英文字符串替换为中文。幂等:重复运行安全。
    补丁只影响本机安装副本,pi 升级后会被覆盖,重跑本脚本即可恢复。
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATCHES_FILE = HERE / "patches.json"
CJK = re.compile(r"[\u4e00-\u9fff]")

CANDIDATE_DISTS = [
    # 常见安装位置(Windows 优先,按可能性排序)
    r"C:/Users/super/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/dist",
    r"C:/Users/super/AppData/Local/pi-agent-web/node_modules/@earendil-works/pi-coding-agent/dist",
    r"C:/Users/super/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/dist",
    "/usr/local/lib/node_modules/@earendil-works/pi-coding-agent/dist",
    "/usr/lib/node_modules/@earendil-works/pi-coding-agent/dist",
    "/opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent/dist",
]


def find_dist(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if (p / "core").is_dir() and (p / "modes").is_dir() else None
    for cand in CANDIDATE_DISTS:
        p = Path(cand)
        if (p / "core").is_dir() and (p / "modes").is_dir():
            return p
    # 兜底:扫描 pi 可执行文件所在位置
    return None


def check_status(dist: Path, patches: dict) -> tuple[int, int]:
    """返回 (已汉化文件数, 待汉化文件数)"""
    done = todo = 0
    for rel, pairs in patches.items():
        target = dist / rel
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        # 检查每个文件第一组替换是否已生效
        old, new = pairs[0]
        if old in text:
            todo += 1
        else:
            done += 1
    return done, todo


def apply(dist: Path, patches: dict) -> tuple[int, int, int]:
    """应用全部补丁,返回 (文件数, 替换条数, 失败条数)"""
    files_ok = pairs_ok = pairs_fail = 0
    skipped = 0
    for rel, pairs in patches.items():
        target = dist / rel
        if not target.exists():
            print(f"  ✗ 缺失: {rel}")
            continue
        text = target.read_text(encoding="utf-8")
        if CJK.search(text):
            skipped += 1
            print(f"  = {rel} (已汉化,跳过)")
            continue
        changed = False
        file_ok = True
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new)
                pairs_ok += 1
                changed = True
            else:
                pairs_fail += 1
                file_ok = False
        if changed:
            target.write_text(text, encoding="utf-8")
            files_ok += 1
            print(f"  ✓ {rel}")
        elif file_ok:
            print(f"  ✓ {rel} (新补丁)")
        else:
            print(f"  ~ {rel} (部分未匹配,可能版本已变化)")
    return files_ok, pairs_ok, pairs_fail, skipped


def main():
    ap = argparse.ArgumentParser(description="Pi 中文汉化 / 升级后恢复")
    ap.add_argument("--dist", help="pi-coding-agent 的 dist 目录(默认自动探测)")
    ap.add_argument("--check", action="store_true", help="只检查状态,不修改")
    args = ap.parse_args()

    if not PATCHES_FILE.exists():
        print(f"✗ 找不到 {PATCHES_FILE},请确认与脚本同目录")
        return 1
    patches = json.loads(PATCHES_FILE.read_text(encoding="utf-8"))

    dist = find_dist(args.dist)
    if not dist:
        print("✗ 未找到 pi-coding-agent 安装目录,请用 --dist 指定")
        return 1
    print(f"目标: {dist}")

    done, todo = check_status(dist, patches)
    print(f"状态: {done} 个文件已汉化, {todo} 个文件待处理")

    if args.check:
        return 0

    files_ok, pairs_ok, pairs_fail, skipped = apply(dist, patches)
    print(f"\n完成: 应用 {files_ok} 个文件, {pairs_ok} 条替换生效, {pairs_fail} 条未匹配, 跳过已汉化 {skipped} 个文件")
    print("提示: 完全退出并重启 pi 后生效;升级后重跑本脚本即可恢复汉化。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
