#!/usr/bin/env python3
"""check_notes.py — Frontmatter 校验

检查 content/ 目录下 .md 笔记的 frontmatter 是否完整。

用法: python3 check_notes.py <content_dir>
退出码: 0=全部通过, 1=有错误
"""

import argparse
import re
import sys
from pathlib import Path


def should_exclude(path: Path) -> bool:
    """判断文件是否应被排除检查。"""
    name = path.name
    if name.startswith("「"):  # 归档标记
        return True
    if name.startswith("_"):  # 整理报告等
        return True
    if "模板" in path.parts:  # 模板目录
        return True
    return False


def parse_frontmatter(text: str) -> dict | None:
    """解析 YAML frontmatter，返回字段字典；无 frontmatter 返回 None。"""
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None

    fields: dict = {}
    current_key = None
    for line in lines[1:end_idx]:
        if not line.strip():
            continue
        # 缩进的列表项: "  - xxx"
        if re.match(r"^\s+-\s+", line):
            if current_key and isinstance(fields.get(current_key), list):
                val = re.sub(r"^\s+-\s+", "", line).strip().strip('"').strip("'")
                fields[current_key].append(val)
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                fields[key] = []
                current_key = key
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                fields[key] = (
                    [x.strip().strip('"').strip("'") for x in inner.split(",")]
                    if inner
                    else []
                )
                current_key = key
            else:
                fields[key] = val.strip('"').strip("'")
                current_key = key
    return fields


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_note(path: Path) -> list[str]:
    """检查单篇笔记，返回错误信息列表。"""
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"读取失败: {e}"]

    fields = parse_frontmatter(text)
    if fields is None:
        return ["缺少 frontmatter（文件未以 --- 开头或格式不完整）"]

    title = fields.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("title 字段缺失或为空")

    tags = fields.get("tags")
    if not isinstance(tags, list) or len(tags) == 0:
        errors.append("tags 字段缺失或非列表")

    created = fields.get("created")
    if not isinstance(created, str) or not DATE_RE.match(created):
        errors.append(f"created 字段格式错误: {created!r}（应为 YYYY-MM-DD）")

    updated = fields.get("updated")
    if not isinstance(updated, str) or not DATE_RE.match(updated):
        errors.append(f"updated 字段格式错误: {updated!r}（应为 YYYY-MM-DD）")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查 .md 笔记的 frontmatter 是否完整"
    )
    parser.add_argument("content_dir", help="content 目录路径")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    if not content_dir.is_dir():
        print(f"错误: {content_dir} 不是目录", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    note_count = 0

    for md_file in sorted(content_dir.rglob("*.md")):
        if should_exclude(md_file):
            continue
        note_count += 1
        for err in check_note(md_file):
            rel = md_file.relative_to(content_dir)
            all_errors.append(f"{rel}: {err}")

    if all_errors:
        print(f"发现 {len(all_errors)} 个问题（共扫描 {note_count} 篇笔记）:\n")
        for e in all_errors:
            print(f"  ✗ {e}")
        return 1
    print(f"✓ 全部通过（共扫描 {note_count} 篇笔记）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
