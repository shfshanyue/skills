#!/usr/bin/env bash
# Fixture tests for check-catalog.sh. Not run by CI.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHECKER="$ROOT/scripts/check-catalog.sh"
FAIL=0

assert_exit() {
  local want="$1" label="$2"
  shift 2
  local rc=0
  "$@" > /tmp/check-catalog-out.txt 2>&1 || rc=$?
  if [ "$rc" -ne "$want" ]; then
    echo "FAIL $label: exit $rc want $want"
    cat /tmp/check-catalog-out.txt
    FAIL=1
  else
    echo "PASS $label (exit $want)"
  fi
}

assert_grep() {
  local pattern="$1" label="$2"
  if grep -E "$pattern" /tmp/check-catalog-out.txt >/dev/null; then
    echo "PASS $label"
  else
    echo "FAIL $label: no match /$pattern/"
    cat /tmp/check-catalog-out.txt
    FAIL=1
  fi
}

make_fixture() {
  local dir="$1"
  rm -rf "$dir"
  mkdir -p "$dir/skills/alpha" "$dir/skills/beta" "$dir/evals"
  printf '%s\n' '---' 'name: alpha' '---' '# A' > "$dir/skills/alpha/SKILL.md"
  printf '%s\n' '---' 'name: beta' '---' '# B' > "$dir/skills/beta/SKILL.md"
  cat > "$dir/README.md" <<'EOF'
# fixture

## Quick Install

```bash
npx skills add org/skills --skill alpha
npx skills add org/skills --skill beta
npx skills add org/skills
```

## Skills

| Skill | One-line |
|-------|----------|
| [`alpha`](skills/alpha/SKILL.md) | A |
| [`beta`](skills/beta/SKILL.md) | B |

## Hooks
EOF
  cat > "$dir/AGENTS.md" <<'EOF'
# AGENTS

## Reference — skill clusters

| User intent | Skill |
|-------------|-------|
| Alpha work | `alpha` |
| Beta work | `beta` (helper) |

## Reference — hooks
EOF
  cat > "$dir/evals/trigger-cases.md" <<'EOF'
# Trigger eval cases

| # | Prompt | Expected skill | Pass criterion |
|---|--------|----------------|----------------|
| 1 | do alpha | `alpha` | loads |
| 2 | do both | `alpha` → `beta` | hand-off |
| 3 | unrelated | none | no load |
EOF
}

FIX=$(mktemp -d)
trap 'rm -rf "$FIX"' EXIT
make_fixture "$FIX"

export CHECK_CATALOG_ROOT="$FIX"
assert_exit 0 "complete fixture" bash "$CHECKER"

# Missing from README table
sed -i.bak '/skills\/beta\/SKILL.md/d' "$FIX/README.md"
assert_exit 1 "missing readme-table" bash "$CHECKER"
assert_grep 'MISSING readme-table:.*beta' "reports missing beta table"
make_fixture "$FIX"

# Extra in evals
printf '%s\n' '| 4 | ghost | `ghost` | no |' >> "$FIX/evals/trigger-cases.md"
assert_exit 1 "extra evals" bash "$CHECKER"
assert_grep 'EXTRA evals:.*ghost' "reports extra ghost"
make_fixture "$FIX"

# none is not a skill
# (already in fixture; complete fixture must still pass — covered above)

if [ "$FAIL" -ne 0 ]; then
  echo "test-check-catalog: FAILED"
  exit 1
fi
echo "test-check-catalog: all passed"
