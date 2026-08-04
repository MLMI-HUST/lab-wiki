#!/usr/bin/env python3
"""check_wikilinks.py — 双向链接校验

检查 [[笔记名]] 链接的目标文件是否存在。

用法: python3 check_wikilinks.py <content_dir>
退出码: 0=全部通过, 1=有断链
"""

import argparse
import re
import sys
from pathlib import Path

# 匹配 [[xxx]] 或 [[xxx|显示名]]，不匹配 ![[xxx]]（附件嵌入）
WIKILINK_RE = re.compile(r"(?<!\!)\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def should_exclude(path: Path) -> bool:
    name = path.name
    if name.startswith("「"):
        return True
    if name.startswith("_"):
        return True
    return False


def extract_wikilinks(text: str) -> list[str]:
    """提取所有 [[xxx]] 和 [[xxx|显示名]] 中的目标名 xxx。"""
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(text)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查 [[笔记名]] 双向链接的目标是否存在"
    )
    parser.add_argument("content_dir", help="content 目录路径")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    if not content_dir.is_dir():
        print(f"错误: {content_dir} 不是目录", file=sys.stderr)
        return 1

    # 预先建立文件名索引（stem，不含扩展名）
    all_stems = {md.stem for md in content_dir.rglob("*.md")}

    all_errors: list[str] = []
    checked = 0

    for md_file in sorted(content_dir.rglob("*.md")):
        if should_exclude(md_file):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"警告: 无法读取 {md_file}: {e}", file=sys.stderr)
            continue
        checked += 1
        rel = md_file.relative_to(content_dir)
        for link in extract_wikilinks(text):
            target = link.split("/")[-1]  # 处理 子目录/笔记 形式
            # 处理 Obsidian 锚点链接 [[笔记名#锚点|显示名]]
            target = target.split("#")[0].strip()
            if target and target not in all_stems:
                all_errors.append(f"{rel}: 断链 [[{link}]]")

    if all_errors:
        print(f"发现 {len(all_errors)} 个断链（扫描 {checked} 篇笔记）:\n")
        for e in all_errors:
            print(f"  ✗ {e}")
        return 1
    print(f"✓ 全部链接有效（扫描 {checked} 篇笔记）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
