#!/usr/bin/env python3
# create_lines_zip.py
# Usage: python3 create_lines_zip.py output.zip file1 [file2 ...]
# Example: python3 create_lines_zip.py lines_archive.zip unified_robot_system.cpp unified_hybrid_system.py
#
# Comportement :
# - Lit chaque fichier en binaire et découpe en "lignes" via splitlines(keepends=True).
# - Crée un répertoire par fichier source (nom = nom_sans_extension).
# - Chaque segment de ligne devient line_0001.<ext>, line_0002.<ext>, ... et contient exactement les octets lus.
# - Produit un ZIP contenant tous les répertoires.
import sys
import os
import tempfile
import zipfile
from pathlib import Path

def create_lines_zip(output_zip: str, sources):
    tmpdir = tempfile.mkdtemp(prefix="lines_zip_")
    try:
        for src in sources:
            if not os.path.isfile(src):
                print(f"File not found: {src}", file=sys.stderr)
                continue
            p = Path(src)
            name_without_ext = p.stem
            ext = p.suffix.lstrip('.') or 'txt'
            dirpath = Path(tmpdir) / name_without_ext
            dirpath.mkdir(parents=True, exist_ok=True)

            # Read in binary to preserve exact bytes and line endings
            with open(src, 'rb') as f:
                content = f.read()
            # splitlines(keepends=True) preserves newline bytes; handles last line without newline
            lines = content.splitlines(keepends=True)
            # If file is empty, ensure we create zero or one line file? We'll create 0 files in that case.
            if not lines and len(content) == 0:
                # create a single empty line file to represent the empty file
                line_filename = dirpath / f"line_{1:04d}.{ext}"
                line_filename.write_bytes(b'')
            else:
                for i, line_bytes in enumerate(lines, start=1):
                    line_filename = dirpath / f"line_{i:04d}.{ext}"
                    line_filename.write_bytes(line_bytes)

        # Create zip
        with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, tmpdir)
                    zf.write(abs_path, rel_path)
        print(f"Archive created: {output_zip}")
    finally:
        # cleanup
        import shutil
        shutil.rmtree(tmpdir)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 create_lines_zip.py output.zip file1 [file2 ...]")
        sys.exit(1)
    output_zip = sys.argv[1]
    sources = sys.argv[2:]
    create_lines_zip(output_zip, sources)

if __name__ == "__main__":
    main()