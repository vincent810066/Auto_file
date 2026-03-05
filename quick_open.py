#!/usr/bin/env python3
"""Quick file opener.

Manage a preset list of files and open them in one command.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List

DEFAULT_CONFIG = Path(__file__).with_name("quick_open_files.json")


def load_config(path: Path) -> List[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("設定檔格式錯誤：應為 JSON 陣列")
    return [str(Path(p).expanduser()) for p in data]


def save_config(path: Path, files: List[str]) -> None:
    normalized = sorted(dict.fromkeys(files))
    with path.open("w", encoding="utf-8") as f:
        json.dump(normalized, f, indent=2, ensure_ascii=False)
        f.write("\n")


def open_file(path: Path, dry_run: bool = False) -> None:
    if dry_run:
        print(f"[DRY RUN] would open: {path}")
        return

    if sys.platform.startswith("win"):
        os.startfile(str(path))  # type: ignore[attr-defined]
        return
    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=True)
        return

    subprocess.run(["xdg-open", str(path)], check=True)


def cmd_init(args: argparse.Namespace) -> int:
    config = Path(args.config)
    if config.exists() and not args.force:
        print(f"設定檔已存在：{config}（使用 --force 可覆蓋）")
        return 1
    save_config(config, [])
    print(f"已建立設定檔：{config}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    config = Path(args.config)
    files = load_config(config)

    for file_arg in args.files:
        full_path = str(Path(file_arg).expanduser().resolve())
        files.append(full_path)
        print(f"已加入：{full_path}")

    save_config(config, files)
    print(f"已儲存至：{config}")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    config = Path(args.config)
    files = load_config(config)
    remove_set = {str(Path(p).expanduser().resolve()) for p in args.files}

    remaining = [p for p in files if str(Path(p).resolve()) not in remove_set]
    removed = [p for p in files if str(Path(p).resolve()) in remove_set]

    for p in removed:
        print(f"已刪除：{p}")

    if not removed:
        print("沒有符合的項目可刪除")

    save_config(config, remaining)
    print(f"已儲存至：{config}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    config = Path(args.config)
    files = load_config(config)

    if not files:
        print("目前沒有任何預設檔案。")
        return 0

    print("預設檔案清單：")
    for idx, p in enumerate(files, 1):
        status = "存在" if Path(p).exists() else "不存在"
        print(f"{idx:>2}. {p} [{status}]")
    return 0


def cmd_open(args: argparse.Namespace) -> int:
    config = Path(args.config)
    files = load_config(config)

    if not files:
        print("目前沒有任何預設檔案，請先使用 add 加入。")
        return 1

    failed = 0
    for p in files:
        path = Path(p)
        if not path.exists():
            print(f"找不到檔案：{path}")
            failed += 1
            continue
        try:
            open_file(path, dry_run=args.dry_run)
            print(f"已開啟：{path}")
        except Exception as exc:
            print(f"開啟失敗：{path} ({exc})")
            failed += 1

    return 0 if failed == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="一鍵開啟預設檔案工具")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help=f"設定檔路徑（預設：{DEFAULT_CONFIG}）",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init", help="初始化設定檔")
    p_init.add_argument("--force", action="store_true", help="覆蓋既有設定檔")
    p_init.set_defaults(func=cmd_init)

    p_add = subparsers.add_parser("add", help="加入要一鍵開啟的檔案")
    p_add.add_argument("files", nargs="+", help="檔案路徑，可同時加入多個")
    p_add.set_defaults(func=cmd_add)

    p_remove = subparsers.add_parser("remove", help="刪除預設檔案")
    p_remove.add_argument("files", nargs="+", help="要刪除的檔案路徑")
    p_remove.set_defaults(func=cmd_remove)

    p_list = subparsers.add_parser("list", help="列出目前預設檔案")
    p_list.set_defaults(func=cmd_list)

    p_open = subparsers.add_parser("open", help="一鍵開啟所有預設檔案")
    p_open.add_argument("--dry-run", action="store_true", help="僅顯示將開啟哪些檔案")
    p_open.set_defaults(func=cmd_open)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"錯誤：{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
