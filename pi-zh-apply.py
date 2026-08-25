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
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath

HERE = Path(__file__).resolve().parent
PATCHES_FILE = HERE / "patches.json"
DEPENDENCY_PATCHES_FILE = HERE / "dependency-patches.json"
PATCHSET_PI_VERSION = "0.84.3"
BUNDLE_PROXY = '#!/usr/bin/env node\nimport "../cli.js";\n'

CANDIDATE_DISTS = [
    # 常见安装位置(Windows 优先,按可能性排序)
    r"C:/Users/super/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/dist",
    r"C:/Users/super/AppData/Local/pi-agent-web/node_modules/@earendil-works/pi-coding-agent/dist",
    r"C:/Users/super/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/dist",
    "/usr/local/lib/node_modules/@earendil-works/pi-coding-agent/dist",
    "/usr/lib/node_modules/@earendil-works/pi-coding-agent/dist",
    "/opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent/dist",
]


def is_dist(path: Path) -> bool:
    return (path / "core").is_dir() and (path / "modes").is_dir() and (path / "cli.js").is_file()


def npm_global_dist() -> Path | None:
    """通过当前 npm 配置发现自定义 prefix 下的全局安装目录。"""
    try:
        result = subprocess.run(
            ["npm", "root", "-g"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    root = result.stdout.strip()
    if not root:
        return None
    return Path(root) / "@earendil-works" / "pi-coding-agent" / "dist"


def dist_from_pi_executable() -> Path | None:
    """从 PATH 中 pi 的真实入口反向定位 dist，兼容 npm 自定义 prefix。"""
    executable = shutil.which("pi")
    if not executable:
        return None
    resolved = Path(executable).resolve()
    for parent in (resolved.parent, *resolved.parents):
        if parent.name == "dist" and is_dist(parent):
            return parent
    return None


def find_dist(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        return p if is_dist(p) else None

    candidates = [
        dist_from_pi_executable(),
        npm_global_dist(),
        *(Path(cand) for cand in CANDIDATE_DISTS),
    ]
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate is None:
            continue
        p = candidate.expanduser().resolve()
        if p in seen:
            continue
        seen.add(p)
        if is_dist(p):
            return p
    return None


def target_path(dist: Path, rel: str) -> Path:
    """将补丁路径统一为平台无关路径，并拒绝跳出 dist 的路径。"""
    portable = PurePosixPath(rel.replace("\\", "/"))
    if portable.is_absolute() or ".." in portable.parts:
        raise ValueError(f"非法补丁路径: {rel}")
    return dist.joinpath(*portable.parts)


@dataclass
class PatchStats:
    applied: int = 0
    localized: int = 0
    unmatched: int = 0
    missing_files: int = 0
    changed_files: int = 0

    def add(self, other: "PatchStats") -> None:
        self.applied += other.applied
        self.localized += other.localized
        self.unmatched += other.unmatched
        self.missing_files += other.missing_files
        self.changed_files += other.changed_files


def check_status(dist: Path, patches: dict) -> PatchStats:
    """逐条检查补丁，正确识别未处理、已处理和版本不匹配。"""
    stats = PatchStats()
    for rel, pairs in patches.items():
        target = target_path(dist, rel)
        if not target.exists():
            stats.missing_files += 1
            continue
        text = target.read_text(encoding="utf-8")
        for old, new in pairs:
            if old in text:
                stats.applied += 1  # check 模式下表示待应用
            elif new in text:
                stats.localized += 1
            else:
                stats.unmatched += 1
    return stats


def apply(dist: Path, patches: dict) -> PatchStats:
    """逐条应用补丁；支持幂等运行，也能继续处理部分汉化文件。"""
    stats = PatchStats()
    for rel, pairs in patches.items():
        target = target_path(dist, rel)
        if not target.exists():
            print(f"  ✗ 缺失: {rel}")
            stats.missing_files += 1
            continue
        text = target.read_text(encoding="utf-8")
        changed = False
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new)
                stats.applied += 1
                changed = True
            elif new in text:
                stats.localized += 1
            else:
                stats.unmatched += 1
        if changed:
            target.write_text(text, encoding="utf-8")
            stats.changed_files += 1
            print(f"  ✓ {rel}")
        elif all(new in text for _, new in pairs):
            print(f"  = {rel} (已汉化)")
        else:
            print(f"  ~ {rel} (部分未匹配,可能版本已变化)")
    return stats


def package_version(dist: Path) -> str | None:
    package_json = dist.parent / "package.json"
    try:
        return json.loads(package_json.read_text(encoding="utf-8")).get("version")
    except (OSError, json.JSONDecodeError):
        return None


def dependency_dist(dist: Path, package_name: str, relative_root: str = "dist") -> Path:
    """解析 coding-agent 内安装的依赖目录，不允许路径逃逸。"""
    package_parts = package_name.split("/")
    if (
        len(package_parts) != 2
        or not package_parts[0].startswith("@")
        or not package_parts[0][1:]
        or not package_parts[1]
        or any(part in {".", ".."} for part in package_parts)
    ):
        raise ValueError(f"非法依赖包名: {package_name}")
    package_root = dist.parent / "node_modules" / package_parts[0] / package_parts[1]
    return target_path(package_root, relative_root)


def dependency_version(root: Path, relative_root: str) -> str | None:
    package_root = root
    for _ in PurePosixPath(relative_root.replace("\\", "/")).parts:
        package_root = package_root.parent
    try:
        return json.loads((package_root / "package.json").read_text(encoding="utf-8")).get("version")
    except (OSError, json.JSONDecodeError):
        return None


def load_dependency_patchsets() -> dict:
    if not DEPENDENCY_PATCHES_FILE.exists():
        return {}
    return json.loads(DEPENDENCY_PATCHES_FILE.read_text(encoding="utf-8"))


def check_dependencies(dist: Path, patchsets: dict) -> PatchStats:
    total = PatchStats()
    for package_name, config in patchsets.items():
        relative_root = config.get("root", "dist")
        root = dependency_dist(dist, package_name, relative_root)
        expected = config.get("version")
        actual = dependency_version(root, relative_root)
        status = check_status(root, config.get("files", {}))
        total.add(status)
        version_text = actual or "未知"
        print(
            f"依赖 {package_name}: {version_text} (补丁集: {expected or '未指定'}) · "
            f"{status.localized} 条已汉化, {status.applied} 条待处理, "
            f"{status.unmatched} 条未匹配, {status.missing_files} 个文件缺失"
        )
    return total


def apply_dependencies(dist: Path, patchsets: dict) -> PatchStats:
    total = PatchStats()
    for package_name, config in patchsets.items():
        root = dependency_dist(dist, package_name, config.get("root", "dist"))
        print(f"依赖 {package_name}:")
        status = apply(root, config.get("files", {}))
        total.add(status)
    return total


def uses_bundled_entry(dist: Path) -> bool:
    package_json = dist.parent / "package.json"
    try:
        package = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return package.get("bin", {}).get("pi") == "dist/bundle/cli.js"


def bundle_entry_status(dist: Path) -> str:
    """新版 npm 包从 bundle 启动；入口需转到已汉化的未打包模块。"""
    if not uses_bundled_entry(dist):
        return "无需切换"
    entry = dist / "bundle" / "cli.js"
    if not entry.is_file():
        return "入口缺失"
    return "已切换" if entry.read_text(encoding="utf-8") == BUNDLE_PROXY else "待切换"


def redirect_bundle_entry(dist: Path) -> bool:
    if not uses_bundled_entry(dist):
        return False
    entry = dist / "bundle" / "cli.js"
    if not entry.is_file() or entry.read_text(encoding="utf-8") == BUNDLE_PROXY:
        return False
    entry.write_text(BUNDLE_PROXY, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="Pi 中文汉化 / 升级后恢复")
    ap.add_argument("--dist", help="pi-coding-agent 的 dist 目录(默认自动探测)")
    ap.add_argument("--check", action="store_true", help="只检查状态,不修改")
    ap.add_argument("--no-dependencies", action="store_true", help="跳过 pi-tui 等依赖补丁")
    args = ap.parse_args()

    if not PATCHES_FILE.exists():
        print(f"✗ 找不到 {PATCHES_FILE},请确认与脚本同目录")
        return 1
    patches = json.loads(PATCHES_FILE.read_text(encoding="utf-8"))
    try:
        dependency_patchsets = load_dependency_patchsets()
    except (OSError, json.JSONDecodeError) as error:
        print(f"✗ 无法读取 {DEPENDENCY_PATCHES_FILE}: {error}")
        return 1

    dist = find_dist(args.dist)
    if not dist:
        print("✗ 未找到 pi-coding-agent 安装目录,请用 --dist 指定")
        return 1
    print(f"目标: {dist}")
    version = package_version(dist)
    if version:
        print(f"Pi 版本: {version} (补丁集: {PATCHSET_PI_VERSION})")
        if version != PATCHSET_PI_VERSION:
            print("⚠ 当前 Pi 版本与补丁集版本不同，可能出现未匹配条目")

    status = check_status(dist, patches)
    print(
        f"状态: {status.localized} 条已汉化, {status.applied} 条待处理, "
        f"{status.unmatched} 条未匹配, {status.missing_files} 个文件缺失"
    )
    if not args.no_dependencies:
        check_dependencies(dist, dependency_patchsets)
    print(f"运行入口: {bundle_entry_status(dist)}")

    if args.check:
        return 0

    result = apply(dist, patches)
    dependency_result = PatchStats()
    if not args.no_dependencies:
        dependency_result = apply_dependencies(dist, dependency_patchsets)
    entry_changed = redirect_bundle_entry(dist)
    result.add(dependency_result)
    print(
        f"\n完成: 修改 {result.changed_files} 个文件, {result.applied} 条替换生效, "
        f"{result.localized} 条原已汉化, {result.unmatched} 条未匹配, "
        f"{result.missing_files} 个文件缺失"
    )
    if entry_changed:
        print("  ✓ bundle/cli.js (已切换到汉化后的未打包入口)")
    print("提示: 完全退出并重启 pi 后生效;升级后重跑本脚本即可恢复汉化。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
