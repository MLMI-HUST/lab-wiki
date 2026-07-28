#!/usr/bin/env python3
"""stale_check.py — 过期笔记提醒

检查笔记的 updated 日期，为过期笔记插入 warning callout。

用法: python3 stale_check.py <content_dir> [--threshold 180]
退出码: 0=无变更或完成, 1=出错
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# 匹配整段 stale-warning 块（含注释标记）
STALE_RE = re.compile(
    r"<!-- stale-warning -->.*?<!-- /stale-warning -->\n?",
    re.DOTALL,
)


def should_exclude(path: Path) -> bool:
    name = path.name
    if name.startswith("「"):
        return True
    if name.startswith("_"):
        return True
    if "模板" in path.parts:
        return True
    return False


def parse_frontmatter_bounds(text: str) -> tuple[int, int] | None:
    """返回 frontmatter 的行索引范围 (start_line, end_line_exclusive)。
    end_line 指向第二个 --- 所在行的下一行。无 frontmatter 返回 None。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (0, i + 1)
    return None


def get_updated_date(text: str) -> str | None:
    """从 frontmatter 提取 updated 字段值。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None
    for line in lines[1:end_idx]:
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m and m.group(1) == "updated":
            return m.group(2).strip().strip('"').strip("'")
    return None


def build_callout(days: int, last_date: str) -> str:
    """构造 stale-warning callout 块。"""
    return (
        "<!-- stale-warning -->\n"
        f"> [!warning] 此笔记已超过 {days} 天未更新\n"
        f"> 最后更新：{last_date}。内容可能已过时，请有经验的组员复核后移除此提示。\n"
        "> 复核后将 frontmatter 的 `updated` 字段更新为今天即可自动移除。\n"
        "<!-- /stale-warning -->\n"
    )


def process_note(path: Path, threshold: int, today: date) -> tuple[bool, str]:
    """处理单篇笔记，返回 (是否修改, 说明)。"""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"读取失败: {e}"

    bounds = parse_frontmatter_bounds(text)
    if bounds is None:
        return False, "无 frontmatter，跳过"

    updated_str = get_updated_date(text)
    if not updated_str or not DATE_RE.match(updated_str):
        return False, f"updated 日期格式无效: {updated_str!r}，跳过"

    try:
        updated_date = datetime.strptime(updated_str, "%Y-%m-%d").date()
    except ValueError:
        return False, f"updated 日期无效: {updated_str!r}，跳过"

    days = (today - updated_date).days
    fm_end_line = bounds[1]  # frontmatter 之后的起始行索引
    lines = text.splitlines(keepends=True)

    existing_block = STALE_RE.search(text)

    if days > threshold:
        # 需要插入或更新 callout
        new_callout = build_callout(days, updated_str)
        if existing_block:
            # 已有标记：替换为最新日期信息
            new_text = STALE_RE.sub(new_callout, text, count=1)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                return True, f"已更新 stale-warning（{days} 天未更新）"
            return False, "callout 已是最新"
        else:
            # 无标记：在 frontmatter 之后、正文之前插入
            head = "".join(lines[:fm_end_line])
            if head and not head.endswith("\n"):
                head += "\n"
            tail = "".join(lines[fm_end_line:])
            new_text = head + "\n" + new_callout + "\n" + tail.lstrip("\n")
            path.write_text(new_text, encoding="utf-8")
            return True, f"已插入 stale-warning（{days} 天未更新）"
    else:
        # 未过期：若有标记则移除（说明已复核）
        if existing_block:
            new_text = STALE_RE.sub("", text, count=1)
            new_text = re.sub(r"\n{3,}", "\n\n", new_text)
            path.write_text(new_text, encoding="utf-8")
            return True, "已移除 stale-warning（笔记已复核）"
        return False, f"正常（{days} 天）"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查笔记的 updated 日期，为过期笔记插入 warning callout"
    )
    parser.add_argument("content_dir", help="content 目录路径")
    parser.add_argument(
        "--threshold",
        type=int,
        default=180,
        help="过期阈值天数（默认 180）",
    )
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    if not content_dir.is_dir():
        print(f"错误: {content_dir} 不是目录", file=sys.stderr)
        return 1

    today = date.today()
    changed = 0
    checked = 0

    for md_file in sorted(content_dir.rglob("*.md")):
        if should_exclude(md_file):
            continue
        checked += 1
        modified, msg = process_note(md_file, args.threshold, today)
        rel = md_file.relative_to(content_dir)
        mark = "✎" if modified else "·"
        print(f"{mark} {rel}: {msg}")
        if modified:
            changed += 1

    print(f"\n完成：扫描 {checked} 篇，修改 {changed} 篇")
    return 0


if __name__ == "__main__":
    sys.exit(main())
