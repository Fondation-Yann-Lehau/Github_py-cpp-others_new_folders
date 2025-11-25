#!/usr/bin/env python3
# create_lines_zip. py
# Usage:
#   python3 create_lines_zip.py [options] output.zip file1 [file2 ...]
#
# Options:
#   -s, --skip-empty       : Ne pas inclure les lignes composées uniquement d'un saut de ligne.
#   -t, --text             : Mode texte UTF-8 (lit/écrit en UTF-8, préserve terminaisons).
#   -n, --lines-per-file N : Nombre de lignes par fichier de sortie (défaut: 1). 
#
# Comportement :
# - Regroupe N lignes par fichier de sortie (défaut 1 = une ligne par fichier).
# - Crée un répertoire par fichier source (nom = nom_sans_extension).
# - Fichiers nommés chunk_0001. <ext>, chunk_0002.<ext>, ... 
# - Avec --skip-empty : les lignes purement saut de ligne ne sont pas comptées ni écrites.
# - Mode binaire (défaut) : préserve exactement les octets. 
# - Mode texte (--text) : lit/écrit en UTF-8, préserve les terminaisons de ligne.
#
# Exemples :
#   # 1000 lignes par fichier, mode texte UTF-8, ignorer lignes vides
#   python3 create_lines_zip.py -s -t -n 1000 archive. zip unified_robot_system.cpp unified_hybrid_system.py
#
#   # 500 lignes par fichier, mode binaire, garder toutes les lignes
#   python3 create_lines_zip.py -n 500 archive.zip unified_robot_system.cpp unified_hybrid_system.py
#
# Résultat dans le ZIP :
#   unified_robot_system/
#       chunk_0001.cpp   (lignes 1-1000)
#       chunk_0002.cpp   (lignes 1001-2000, si applicable)
#   unified_hybrid_system/
#       chunk_0001.py    (lignes 1-1000)

import argparse
import sys
import os
import tempfile
import zipfile
import shutil
from pathlib import Path
from typing import List, Generator, Tuple, Any

EMPTY_BYTES = {b"\n", b"\r\n", b"\r"}
EMPTY_STRS = {"\n", "\r\n", "\r"}


def chunk_lines(
    lines: List[Any],
    lines_per_file: int,
    skip_empty: bool,
    empty_set: set
) -> Generator[Tuple[int, List[Any]], None, None]:
    """
    Génère des chunks de lignes regroupées par lines_per_file.
    Si skip_empty, ignore les lignes dans empty_set.
    Retourne un générateur de (chunk_index, list_of_lines).
    """
    buffer = []
    chunk_idx = 1
    for line in lines:
        if skip_empty and line in empty_set:
            continue
        buffer.append(line)
        if len(buffer) >= lines_per_file:
            yield chunk_idx, buffer
            buffer = []
            chunk_idx += 1
    # Dernier chunk s'il reste des lignes
    if buffer:
        yield chunk_idx, buffer


def process_file_binary(
    src_path: Path,
    out_dir: Path,
    skip_empty: bool,
    ext: str,
    lines_per_file: int
) -> None:
    content = src_path.read_bytes()
    lines = content.splitlines(keepends=True)

    # Si fichier complètement vide
    if not lines and len(content) == 0:
        if not skip_empty:
            (out_dir / f"chunk_0001. {ext}").write_bytes(b"")
        return

    for chunk_idx, chunk_lines_list in chunk_lines(lines, lines_per_file, skip_empty, EMPTY_BYTES):
        target = out_dir / f"chunk_{chunk_idx:04d}.{ext}"
        target.write_bytes(b"".join(chunk_lines_list))


def process_file_text(
    src_path: Path,
    out_dir: Path,
    skip_empty: bool,
    ext: str,
    lines_per_file: int
) -> None:
    text = src_path.read_text(encoding="utf-8", errors="surrogateescape")
    lines = text.splitlines(keepends=True)

    # Si fichier complètement vide
    if not lines and len(text) == 0:
        if not skip_empty:
            (out_dir / f"chunk_0001.{ext}").write_text("", encoding="utf-8", newline="")
        return

    for chunk_idx, chunk_lines_list in chunk_lines(lines, lines_per_file, skip_empty, EMPTY_STRS):
        target = out_dir / f"chunk_{chunk_idx:04d}. {ext}"
        with target.open("w", encoding="utf-8", newline="") as f:
            f.write("".join(chunk_lines_list))


def create_lines_zip(
    output_zip: str,
    sources: List[str],
    skip_empty: bool,
    text_mode: bool,
    lines_per_file: int
) -> None:
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
                process_file_text(src_path, out_dir, skip_empty, ext, lines_per_file)
            else:
                process_file_binary(src_path, out_dir, skip_empty, ext, lines_per_file)

        # Créer l'archive ZIP
        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(tmpdir):
                for file in sorted(files):
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, tmpdir)
                    zf.write(abs_path, rel_path)

        print(f"Archive created: {output_zip}")
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create ZIP where source files are split into chunks of N lines each."
    )
    parser.add_argument("-s", "--skip-empty", action="store_true",
                        help="Skip lines that are only a newline.")
    parser.add_argument("-t", "--text", action="store_true",
                        help="Text UTF-8 mode: read/write lines as UTF-8 text.")
    parser.add_argument("-n", "--lines-per-file", type=int, default=1000,
                        help="Number of lines per output file (default: 1000).")
    parser. add_argument("output_zip", help="Output ZIP archive path")
    parser.add_argument("sources", nargs="+", help="Source files to split")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.lines_per_file < 1:
        print("Error: --lines-per-file must be >= 1", file=sys.stderr)
        sys.exit(1)
    create_lines_zip(
        args.output_zip,
        args.sources,
        args.skip_empty,
        args.text,
        args. lines_per_file
    )


if __name__ == "__main__":
    main()