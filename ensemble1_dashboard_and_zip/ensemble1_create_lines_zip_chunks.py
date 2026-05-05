#!/usr/bin/env python3
"""
create_lines_zip_chunks.py

Unifie/fiabilise les variantes:
- Create_line_zip_bis-1
- Create_line_zip_bis-2.py
- create_lines_zip*.py

Fonction:
- Découpe chaque fichier source en fichiers "chunk_0001.<ext>", etc.
- Chaque chunk contient ~N lignes (N configurable).
- Crée un répertoire par fichier source dans un ZIP.

Modes:
- Binaire par défaut: préserve exactement les octets (terminaisons de lignes incluses).
- Texte (--text): lit/écrit en UTF-8, en préservant les terminaisons via splitlines(keepends=True).
Options:
- --skip-empty: ignore les lignes constituées uniquement d'un saut de ligne.
- --lines-per-file N: nombre de lignes par chunk (défaut 1000).
"""

import argparse
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, List, Set, Tuple, Union

EMPTY_BYTES: Set[bytes] = {b"\n", b"\r\n", b"\r"}
EMPTY_STRS: Set[str] = {"\n", "\r\n", "\r"}


def chunk_lines(
    lines: List[Union[str, bytes]],
    lines_per_file: int,
    skip_empty: bool,
    empty_set: Set[Union[str, bytes]],
) -> Iterable[Tuple[int, List[Union[str, bytes]]]]:
    buf: List[Union[str, bytes]] = []
    idx = 1
    for line in lines:
        if skip_empty and line in empty_set:
            continue
        buf.append(line)
        if len(buf) >= lines_per_file:
            yield idx, buf
            buf = []
            idx += 1
    if buf:
        yield idx, buf


def process_binary(src: Path, out_dir: Path, ext: str, skip_empty: bool, lines_per_file: int) -> None:
    content = src.read_bytes()
    lines = content.splitlines(keepends=True)

    if len(content) == 0 and not lines:
        if not skip_empty:
            (out_dir / f"chunk_{1:04d}.{ext}").write_bytes(b"")
        return

    for i, chunk in chunk_lines(lines, lines_per_file, skip_empty, EMPTY_BYTES):
        (out_dir / f"chunk_{i:04d}.{ext}").write_bytes(b"".join(chunk))


def process_text(src: Path, out_dir: Path, ext: str, skip_empty: bool, lines_per_file: int) -> None:
    text = src.read_text(encoding="utf-8", errors="surrogateescape")
    lines = text.splitlines(keepends=True)

    if len(text) == 0 and not lines:
        if not skip_empty:
            (out_dir / f"chunk_{1:04d}.{ext}").write_text("", encoding="utf-8", newline="")
        return

    for i, chunk in chunk_lines(lines, lines_per_file, skip_empty, EMPTY_STRS):
        with (out_dir / f"chunk_{i:04d}.{ext}").open("w", encoding="utf-8", newline="") as f:
            f.write("".join(chunk))


def create_zip(output_zip: Path, sources: List[Path], skip_empty: bool, text_mode: bool, lines_per_file: int) -> None:
    tmpdir = Path(tempfile.mkdtemp(prefix="lines_zip_"))
    try:
        for src in sources:
            if not src.is_file():
                print(f"File not found: {src}", file=sys.stderr)
                continue

            out_dir = tmpdir / src.stem
            out_dir.mkdir(parents=True, exist_ok=True)
            ext = src.suffix.lstrip(".") or "txt"

            if text_mode:
                process_text(src, out_dir, ext, skip_empty, lines_per_file)
            else:
                process_binary(src, out_dir, ext, skip_empty, lines_per_file)

        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(tmpdir):
                for fn in sorted(files):
                    abs_path = Path(root) / fn
                    rel_path = abs_path.relative_to(tmpdir)
                    zf.write(abs_path, rel_path.as_posix())

        print(f"Archive created: {output_zip}")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def parse_args():
    p = argparse.ArgumentParser(description="Split source files into chunks of N lines and pack into a ZIP.")
    p.add_argument("-s", "--skip-empty", action="store_true", help="Skip lines that are only a newline.")
    p.add_argument("-t", "--text", action="store_true", help="Text UTF-8 mode (preserve line endings).")
    p.add_argument("-n", "--lines-per-file", type=int, default=1000, help="Number of lines per chunk file.")
    p.add_argument("output_zip", help="Output ZIP archive path")
    p.add_argument("sources", nargs="+", help="Source files to split")
    return p.parse_args()


def main():
    args = parse_args()
    if args.lines_per_file < 1:
        print("Error: --lines-per-file must be >= 1", file=sys.stderr)
        sys.exit(1)

    create_zip(
        Path(args.output_zip),
        [Path(s) for s in args.sources],
        skip_empty=args.skip_empty,
        text_mode=args.text,
        lines_per_file=args.lines_per_file,
    )


if __name__ == "__main__":
    main()
