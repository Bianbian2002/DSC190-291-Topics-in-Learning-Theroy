#!/usr/bin/env bash
# Pandoc + XeLaTeX: theory, AI report, and one combined PDF for Gradescope.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

PDF_ENGINE="${PDF_ENGINE:-pdflatex}"
COMMON=(
  --pdf-engine="$PDF_ENGINE"
  -V documentclass=article
  -V geometry:margin=1in
  -V fontsize=11pt
  --resource-path=.
)

pandoc theory.md -o theory.pdf "${COMMON[@]}"
pandoc ai_report.md -o ai_report.pdf "${COMMON[@]}"
pandoc theory.md ai_report.md -o hw3_writeup.pdf "${COMMON[@]}"
echo "Wrote theory.pdf ai_report.pdf hw3_writeup.pdf"
