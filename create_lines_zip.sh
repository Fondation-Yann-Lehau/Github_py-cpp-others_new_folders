#!/usr/bin/env bash
# create_lines_zip.sh
# Usage: ./create_lines_zip.sh output.zip file1 [file2 ...]
# Example: ./create_lines_zip.sh lines_archive.zip unified_robot_system.cpp unified_hybrid_system.py
#
# Comportement :
# - Crée un répertoire par fichier source (nom = nom_sans_extension).
# - Chaque ligne (y compris vides) devient un fichier line_0001.<ext>, line_0002.<ext>, ...
# - L'extension conservée est la même que le fichier source.
# - Archive ZIP finale contenant tous les répertoires.
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 output.zip file1 [file2 ...]"
  exit 1
fi

OUT_ZIP="$1"
shift

TMPDIR="$(mktemp -d)"
echo "Working directory: $TMPDIR"

for SRC in "$@"; do
  if [ ! -f "$SRC" ]; then
    echo "File not found: $SRC" >&2
    continue
  fi

  BASENAME="$(basename "$SRC")"
  NAME_WITHOUT_EXT="${BASENAME%.*}"
  EXT="${BASENAME##*.}"
  # sanitize directory name loosely
  DIR="$TMPDIR/$NAME_WITHOUT_EXT"
  mkdir -p "$DIR"

  LINE_NO=0
  # Read file preserving empty lines; note: read strips newline, we add it back.
  while IFS='' read -r LINE || [ -n "$LINE" ]; do
    LINE_NO=$((LINE_NO + 1))
    FILENAME=$(printf "line_%04d.%s" "$LINE_NO" "$EXT")
    # Write the line (may be empty). This will normalize line endings to LF and ensure a trailing newline.
    printf "%s\n" "$LINE" > "$DIR/$FILENAME"
  done < "$SRC"
done

# Create the ZIP archive
( cd "$TMPDIR" && zip -r -q "$OLDPWD/$OUT_ZIP" . )

echo "Archive created: $OUT_ZIP"
# Cleanup
rm -rf "$TMPDIR"