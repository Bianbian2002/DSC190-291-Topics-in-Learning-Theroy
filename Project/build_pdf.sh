#!/usr/bin/env bash
# Build REPORT.md -> REPORT.pdf with pandoc + LuaLaTeX.
# LuaLaTeX is used (not xelatex) so the Menlo+STIX font fallback in header.tex works,
# letting the Lean unicode (𝒜, ℕ, ∀, ⊆, ∈, ∩, …) render in code blocks.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

pandoc REPORT.md -o REPORT.pdf \
  --pdf-engine=lualatex \
  -H header.tex \
  -V documentclass=article \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V colorlinks=true \
  --syntax-highlighting=tango \
  --resource-path=.

echo "Wrote REPORT.pdf"
