#!/usr/bin/env bash
# Usage: ./create_lines_zip.sh output.zip file1 file2 ...
# Exemple: ./create_lines_zip.sh lines_archive.zip unified_robot_system.cpp unified_hybrid_system.py

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 output.zip file1 [file2 ...]"
  exit 1
fi

OUT_ZIP="$1"
shift

TMPDIR="$(mktemp -d)"
echo "Working in: $TMPDIR"

for SRC in "$@"; do
  if [ ! -f "$SRC" ]; then
    echo "File not found: $SRC"
    continue
  fi

  BASENAME="$(basename "$SRC")"
  NAME_WITHOUT_EXT="${BASENAME%.*}"
  EXT="${BASENAME##*.}"
  DIR="$TMPDIR/$NAME_WITHOUT_EXT"
  mkdir -p "$DIR"

  LINE_NO=0
  # Read file preserving empty lines
  while IFS='' read -r LINE || [ -n "$LINE" ]; do
    LINE_NO=$((LINE_NO + 1))
    FILENAME=$(printf "line_%04d.%s" "$LINE_NO" "$EXT")
    # Write the line exactly as is (may be empty)
    printf "%s\n" "$LINE" > "$DIR/$FILENAME"
  done < "$SRC"
done

# Create the ZIP archive
( cd "$TMPDIR" && zip -r -q "$OLDPWD/$OUT_ZIP" . )

echo "Archive created: $OUT_ZIP"
# Cleanup
rm -rf "$TMPDIR"