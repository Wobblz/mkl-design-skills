#!/usr/bin/env bash
# Greps a project for the typography traps in SKILL.md. Each hit is a lead,
# not a verdict: read the line before changing it.
#   bash type-lint.sh [project-dir]
set -u
dir="${1:-.}"
src=(--include=*.css --include=*.scss --include=*.ts --include=*.tsx --include=*.js --include=*.jsx --include=*.html --include=*.mdx)
skip=(--exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build --exclude-dir=.git)
hits=0

check() { # message, grep -E pattern
  local out
  out=$(grep -rnE "${src[@]}" "${skip[@]}" -- "$2" "$dir" 2>/dev/null | head -20)
  if [ -n "$out" ]; then
    hits=$((hits + 1))
    printf '\n• %s\n%s\n' "$1" "$out"
  fi
}

google=$(grep -rlE "${src[@]}" "${skip[@]}" -- "next/font/google|fonts\.googleapis|@fontsource/" "$dir" 2>/dev/null | head -1)
if [ -n "$google" ]; then
  check "Feature the Google/Fontsource file doesn't ship (check with font-check.py, or self-host the full font)" \
    "\\b(oldstyle-nums|small-caps|all-small-caps|slashed-zero|font-variant-alternates)\\b|font-feature-settings[^;]*\"(ss[0-9]{2}|cv[0-9]{2}|case|smcp|c2sc|onum|dlig|zero)\""
fi

check "Weight through font-variation-settings: breaks <strong> and weight utilities" \
  "font-variation-settings:[^;]*\"wght\""
check "Root font size in px: ignores the reader's browser setting" \
  "html[^{]*\{[^}]*font-size:[[:space:]]*[0-9.]+px"
check "font-feature-settings on html/body: any component that sets its own wipes it" \
  "(html|body)[^{]*\{[^}]*font-feature-settings"
check "vw-only fluid size (no rem term): fails 200% zoom" \
  "clamp\([^,]*,[[:space:]]*-?[0-9.]+vw[[:space:]]*,"
check "tabular-nums alone on a serif with old-style default figures: drops lining-nums (pair them)" \
  "font-serif[^\"]*tabular-nums|font-serif[^\"]*\btabular\b"
check "U+2007 / U+2009 / U+202F padding: Geist and many UI fonts lack these, so they fall back" \
  "\\\\u2007|\\\\u2009|\\\\u202f|\\\\u202F|&#8199;|&#8201;|&#8239;|\\\\2007|\\\\202F"
check "Bold weight added in dark mode: light on dark already reads heavier, step it down instead" \
  "dark[^{]*\{[^}]*font-weight:[[:space:]]*(6|7|8|9)00"
check "Hyphenation without a language-aware reason (headings, UI): keep it to prose" \
  "(h[1-6]|button|label|th)[^{]*\{[^}]*hyphens:[[:space:]]*auto"

html_lang=$(grep -rlE "${src[@]}" "${skip[@]}" -- "<html[^>]*lang=" "$dir" 2>/dev/null | head -1)
html_tag=$(grep -rlE "${src[@]}" "${skip[@]}" -- "<html" "$dir" 2>/dev/null | head -1)
if [ -n "$html_tag" ] && [ -z "$html_lang" ]; then
  hits=$((hits + 1))
  printf '\n• <html> without lang: no Bulgarian forms, no hyphenation, wrong quotes\n%s\n' "$html_tag"
fi

[ "$hits" -eq 0 ] && echo "No typography traps found." || printf '\n%d kinds of lead found.\n' "$hits"
