#!/usr/bin/env bash
# Verify canonical _shared/ files match their sync copies.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

diff "$ROOT/skills/_shared/drill-loop.md" "$ROOT/skills/language/english-collocations/drill-loop-core.md"
diff "$ROOT/skills/_shared/drill-loop.md" "$ROOT/skills/language/minimal-pairs/drill-loop-core.md"
diff "$ROOT/skills/_shared/plain-text-line.md" "$ROOT/skills/language/idiom-chain/plain-text-line.md"
diff "$ROOT/skills/_shared/plain-text-line.md" "$ROOT/skills/language/poetry-quiz/plain-text-line.md"

echo "All shared file copies are in sync."
