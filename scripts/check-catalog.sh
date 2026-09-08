#!/usr/bin/env bash
# Compare skills/ directories to README, AGENTS clusters, and evals.
set -euo pipefail

ROOT="${CHECK_CATALOG_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

section() {
  local file="$1" heading="$2"
  awk -v h="$heading" '
    $0 == h {p=1; next}
    p && /^## / {exit}
    p {print}
  ' "$file"
}

fs_skills() {
  local d name
  for d in "$ROOT/skills"/*/SKILL.md; do
    [ -f "$d" ] || continue
    name="$(basename "$(dirname "$d")")"
    [ "$name" = "_shared" ] && continue
    printf '%s\n' "$name"
  done | sort -u
}

readme_install() {
  section "$ROOT/README.md" "## Quick Install" \
    | { grep -E 'npx skills add' || true; } \
    | { grep -oE -- '--skill[[:space:]]+[a-z0-9-]+' || true; } \
    | awk '{print $2}' \
    | sort -u
}

readme_table() {
  section "$ROOT/README.md" "## Skills" \
    | { grep -oE '\[`[a-z0-9-]+`\]\(skills/[a-z0-9-]+/SKILL\.md\)' || true; } \
    | sed -E 's/\[`([a-z0-9-]+)`\]\(skills\/[a-z0-9-]+\/SKILL\.md\)/\1/' \
    | sort -u
}

agents_clusters() {
  section "$ROOT/AGENTS.md" "## Reference — skill clusters" \
    | awk -F'|' '
      NR<=2 {next}
      NF<3 {next}
      {
        col=$3
        if (match(col, /`[a-z0-9-]+`/)) {
          s=substr(col, RSTART+1, RLENGTH-2)
          print s
        }
      }
    ' | sort -u
}

evals_expected() {
  awk -F'|' '
    /^\|/ && $2 !~ /^[[:space:]]*#/ && $2 !~ /---/ && NF>=4 {
      col=$4
      while (match(col, /`[a-z0-9-]+`/)) {
        s=substr(col, RSTART+1, RLENGTH-2)
        if (s != "none") print s
        col=substr(col, RSTART+RLENGTH)
      }
    }
  ' "$ROOT/evals/trigger-cases.md" | sort -u
}

diff_set() {
  local label="$1" got="$2" want="$3"
  local missing extra
  missing="$(comm -23 "$want" "$got" | tr '\n' ' ' | sed 's/[[:space:]]*$//')"
  extra="$(comm -13 "$want" "$got" | tr '\n' ' ' | sed 's/[[:space:]]*$//')"
  if [ -n "$missing" ]; then
    echo "MISSING $label: $missing"
    RC=1
  fi
  if [ -n "$extra" ]; then
    echo "EXTRA $label: $extra"
    RC=1
  fi
}

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

fs_skills > "$TMP/fs"
readme_install > "$TMP/readme-install"
readme_table > "$TMP/readme-table"
agents_clusters > "$TMP/agents-clusters"
evals_expected > "$TMP/evals"

RC=0
diff_set "readme-install" "$TMP/readme-install" "$TMP/fs"
diff_set "readme-table" "$TMP/readme-table" "$TMP/fs"
diff_set "agents-clusters" "$TMP/agents-clusters" "$TMP/fs"
diff_set "evals" "$TMP/evals" "$TMP/fs"

if [ "$RC" -ne 0 ]; then
  exit 1
fi
echo "All catalog sources match skills/."
