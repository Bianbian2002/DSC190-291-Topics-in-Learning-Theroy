#!/usr/bin/env bash
# Build PDFs from Markdown with Pandoc + XeLaTeX (math + Unicode).
# Run from anywhere; outputs land next to the .md files in this directory.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

PDF_ENGINE="${PDF_ENGINE:-xelatex}"
COMMON=(
  --pdf-engine="$PDF_ENGINE"
  -V documentclass=article
  -V geometry:margin=1in
  -V fontsize=11pt
  --resource-path=.
)

for name in repo theory discussion ai_report; do
  echo "Building ${name}.pdf ..."
  pandoc "${name}.md" -o "${name}.pdf" "${COMMON[@]}"
done

echo "Building hw1_writeup.pdf (repo + theory + discussion + ai_report) ..."
pandoc repo.md theory.md discussion.md ai_report.md -o hw1_writeup.pdf "${COMMON[@]}"

echo "Done: repo.pdf theory.pdf discussion.pdf ai_report.pdf hw1_writeup.pdf"
