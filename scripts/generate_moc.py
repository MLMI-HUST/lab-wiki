#!/usr/bin/env python3
"""generate_moc.py — MOC 自动生成

扫描各子目录，自动生成 _索引.md MOC 文件。

用法: python3 generate_moc.py <content_dir>
"""

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

EXCLUDE_DIRS = {".obsidian", "模板", "插入的图片", "附件"}


def parse_frontmatter(text: str) -> dict:
    """简单解析 frontmatter，返回字段字典。"""
    fields: dict = {}
    if not text.startswith("---"):
        return fields
    lines = text.splitlines()
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return fields

    current_key = None
    for line in lines[1:end_idx]:
        if not line.strip():
            continue
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


def get_first_paragraph(text: str) -> str:
    """取正文第一段非空、非标题行作为摘要。"""
    lines = text.splitlines()
    fm_end = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i + 1
                break
    for line in lines[fm_end:]:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("<!--"):
            continue
        if s.startswith(">"):
            continue
        if s.startswith("|"):
            continue
        # 清理 markdown 符号，保留可读文字
        summary = re.sub(r"[\[\]#!|>`*_~]", "", s)
        summary = re.sub(r"\s+", " ", summary).strip()
        return summary[:60]
    return ""


def is_draft(fields: dict) -> bool:
    d = fields.get("draft")
    if isinstance(d, str):
        return d.lower() in ("true", "yes", "1")
    return False


def generate_index_for_dir(dir_path: Path) -> str:
    """为单个子目录生成 _索引.md 内容。"""
    notes = []  # list of (stem, title, tags, updated, summary)
    for md_file in sorted(dir_path.glob("*.md")):
        name = md_file.name
        if name.startswith("「") or name.startswith("_"):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        fields = parse_frontmatter(text)
        if is_draft(fields):
            continue
        stem = md_file.stem
        title = fields.get("title", stem)
        if not isinstance(title, str):
            title = stem
        tags = fields.get("tags", [])
        if not isinstance(tags, list):
            tags = []
        updated = fields.get("updated", "")
        if not isinstance(updated, str):
            updated = ""
        summary = get_first_paragraph(text)
        notes.append((stem, title, tags, updated, summary))

    # 按第一个 tag 分组
    groups: dict[str, list] = defaultdict(list)
    for stem, title, tags, updated, summary in notes:
        key = tags[0] if tags else "未分类"
        groups[key].append((stem, title, updated, summary))

    today = date.today().isoformat()
    dir_name = dir_path.name

    out: list[str] = []
    out.append("---")
    out.append(f'title: "{dir_name}索引"')
    out.append("tags:")
    out.append("  - 索引")
    out.append("unlisted: true")
    out.append(f"created: {today}")
    out.append(f"updated: {today}")
    out.append("---")
    out.append("")
    out.append("<!-- AUTO-GENERATED: 请勿手动编辑，运行 generate_moc.py 重新生成 -->")
    out.append("")
    out.append("[[index|🏠 返回主页]]")
    out.append("")
    out.append(f"# {dir_name}索引")
    out.append("")

    for tag, items in sorted(groups.items()):
        out.append(f"## {tag}")
        out.append("")
        for stem, title, updated, summary in items:
            line = f"- [[{stem}|{title}]]"
            if updated:
                line += f" | {updated}"
            if summary:
                line += f" | {summary}"
            out.append(line)
        out.append("")

    return "\n".join(out)


def generate_homepage(content_dir: Path) -> bool:
    """如果 index.md 不存在，生成首页.md。返回是否生成。"""
    if (content_dir / "index.md").exists():
        return False
    today = date.today().isoformat()
    home = content_dir / "首页.md"
    out: list[str] = []
    out.append("<!-- AUTO-GENERATED: 请勿手动编辑 -->")
    out.append("---")
    out.append('title: "Wiki 首页"')
    out.append("tags:")
    out.append("  - 索引")
    out.append("  - 主页")
    out.append(f"created: {today}")
    out.append(f"updated: {today}")
    out.append("---")
    out.append("")
    out.append("# Wiki 首页")
    out.append("")
    out.append("## 目录导航")
    out.append("")
    for sub in sorted(content_dir.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name in EXCLUDE_DIRS or sub.name.startswith("."):
            continue
        out.append(f"- [[{sub.name}/_索引|{sub.name}]]")
    out.append("")
    home.write_text("\n".join(out), encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="扫描子目录自动生成 _索引.md MOC 文件"
    )
    parser.add_argument("content_dir", help="content 目录路径")
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    if not content_dir.is_dir():
        print(f"错误: {content_dir} 不是目录", file=sys.stderr)
        return 1

    generated = 0
    for sub in sorted(content_dir.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name in EXCLUDE_DIRS or sub.name.startswith("."):
            continue
        content = generate_index_for_dir(sub)
        index_path = sub / "_索引.md"
        index_path.write_text(content, encoding="utf-8")
        print(f"✓ 生成 {index_path.relative_to(content_dir)}")
        generated += 1

    if generate_homepage(content_dir):
        print("✓ 生成 首页.md")
        generated += 1
    else:
        print("· index.md 已存在，跳过首页生成")

    print(f"\n完成：共生成 {generated} 个文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
