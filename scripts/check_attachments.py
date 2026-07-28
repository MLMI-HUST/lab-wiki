#!/usr/bin/env python3
"""check_attachments.py — 附件校验

检查 ![[图片名]] 引用的附件文件是否存在。

用法: python3 check_attachments.py <content_dir>
退出码: 0=全部通过, 1=有缺失附件
"""

import argparse
import re
import sys
from pathlib import Path

# 匹配 ![[xxx]] 或 ![[xxx|显示名]]
EMBED_RE = re.compile(r"!\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def should_exclude(path: Path) -> bool:
    name = path.name
    if name.startswith("「"):
        return True
    return False


def extract_embeds(text: str) -> list[str]:
    """提取所有 ![[xxx]] 中的附件名 xxx。"""
    return [m.group(1).strip() for m in EMBED_RE.finditer(text)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查 ![[图片名]] 引用的附件是否存在"
    )
    parser.add_argument("content_dir", help="content 目录路径")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    if not content_dir.is_dir():
        print(f"错误: {content_dir} 不是目录", file=sys.stderr)
        return 1

    # 建立附件名索引（所有非 .md 文件，按文件名索引）
    attachment_names: set[str] = set()
    for f in content_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() != ".md":
            attachment_names.add(f.name)

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
        for emb in extract_embeds(text):
            # 去掉可能的子路径、参数、显示名
            name = emb.split("/")[-1].split("|")[0].split("?")[0].strip()
            if name and name not in attachment_names:
                all_errors.append(f"{rel}: 缺失附件 ![[{emb}]]")

    if all_errors:
        print(f"发现 {len(all_errors)} 个缺失附件（扫描 {checked} 篇笔记）:\n")
        for e in all_errors:
            print(f"  ✗ {e}")
        return 1
    print(f"✓ 全部附件存在（扫描 {checked} 篇笔记）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
