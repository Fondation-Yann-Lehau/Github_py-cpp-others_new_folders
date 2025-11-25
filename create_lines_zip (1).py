#!/usr/bin/env python3
# create_lines_zip.py
# Usage:
#   python3 create_lines_zip.py [-s|--skip-empty] [-t|--text] output.zip file1 [file2 ...]
#
# Options:
#   -s, --skip-empty   : Ne pas créer de fichier pour les lignes composées uniquement d'un saut de ligne.
#   -t, --text         : Mode texte UTF-8 — lit et écrit les lignes en texte (préserve les terminaisons).
#
# Comportement :
# - Par défaut (mode binaire) : lit chaque fichier en bytes et splitlines(keepends=True), écrit chaque segment
#   dans line_XXXX.<ext> en bytes (préserve exactement les octets et les terminaisons).
# - En mode texte (--text) : lit en UTF-8 (défaut d'encodage), splitlines(keepends=True) et écrit chaque ligne
#   dans un fichier texte UTF-8, en préservant les terminaisons (ouvert en newline='').
# - Avec --skip-empty : les lignes qui sont strictement un saut de ligne (b'\n', b'\r\n', b'\r' en binaire
#   ou '\n','\r\n','\r' en texte) ne génèrent PAS de fichier.
# - Si un fichier source est vide (0 octet) :
#     - si --skip-empty : aucun fichier créé pour ce source;
#     - sinon : on crée line_0001.<ext> vide (comme représentation).
#
# Exemple :
#   python3 create_lines_zip.py -s -t lines_archive.zip unified_robot_system.cpp unified_hybrid_system.py

import argparse
import sys
import os
import tempfile
import zipfile
import shutil
from pathlib import Path
from typing import List

EMPTY_BYTES = {b"\n", b"\r\n", b"\r"}
EMPTY_STRS = {"\n", "\r\n", "\r"}

def process_file_binary(src_path: Path, out_dir: Path, skip_empty: bool, ext: str) -> None:
    content = src_path.read_bytes()
    lines = content.splitlines(keepends=True)
    # If file completely empty
    if not lines and len(content) == 0:
        if not skip_empty:
            (out_dir / f"line_{1:04d}.{ext}").write_bytes(b"")
        return

    for idx, line_bytes in enumerate(lines, start=1):
        if skip_empty and line_bytes in EMPTY_BYTES:
            # Skip creating a file for purely newline-only lines
            continue
        target = out_dir / f"line_{idx:04d}.{ext}"
        target.write_bytes(line_bytes)


def process_file_text(src_path: Path, out_dir: Path, skip_empty: bool, ext: str) -> None:
    # Read as text preserving newline chars
    text = src_path.read_text(encoding="utf-8", errors="surrogateescape")
    # splitlines(keepends=True) keeps newline characters
    lines = text.splitlines(keepends=True)
    if not lines and len(text) == 0:
        if not skip_empty:
            (out_dir / f"line_{1:04d}.{ext}").write_text("", encoding="utf-8", newline="")
        return

    for idx, line in enumerate(lines, start=1):
        if skip_empty and line in EMPTY_STRS:
            continue
        target = out_dir / f"line_{idx:04d}.{ext}"
        # open with newline='' to avoid Python altering newline bytes on Windows
        with target.open("w", encoding="utf-8", newline="") as f:
            f.write(line)


def create_lines_zip(output_zip: str, sources: List[str], skip_empty: bool, text_mode: bool) -> None:
    tmpdir = Path(tempfile.mkdtemp(prefix="lines_zip_"))
    try:
        for src in sources:
            src_path = Path(src)
            if not src_path.is_file():
                print(f"File not found: {src}", file=sys.stderr)
                continue

            name_without_ext = src_path.stem
            ext = src_path.suffix.lstrip('.') or "txt"
            out_dir = tmpdir / name_without_ext
            out_dir.mkdir(parents=True, exist_ok=True)

            if text_mode:
                process_file_text(src_path, out_dir, skip_empty, ext)
            else:
                process_file_binary(src_path, out_dir, skip_empty, ext)

        # Create ZIP archive
        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(tmpdir):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, tmpdir)
                    zf.write(abs_path, rel_path)

        print(f"Archive created: {output_zip}")
    finally:
        # cleanup
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass


def parse_args():
    parser = argparse.ArgumentParser(description="Create ZIP where each source line is a separate file.")
    parser.add_argument("-s", "--skip-empty", action="store_true",
                        help="Skip files for lines that are only a newline.")
    parser.add_argument("-t", "--text", action="store_true",
                        help="Text UTF-8 mode: read/write lines as UTF-8 text (preserve newlines).")
    parser.add_argument("output_zip", help="Output ZIP archive path")
    parser.add_argument("sources", nargs="+", help="Source files to split")
    return parser.parse_args()


def main():
    args = parse_args()
    create_lines_zip(args.output_zip, args.sources, args.skip_empty, args.text)


if __name__ == "__main__":
    main()