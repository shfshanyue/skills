#!/usr/bin/env bash
# Verify canonical _shared/ files match their sync copies.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

diff "$ROOT/skills/_shared/drill-loop.md" "$ROOT/skills/english-collocations/drill-loop-core.md"
diff "$ROOT/skills/_shared/drill-loop.md" "$ROOT/skills/minimal-pairs/drill-loop-core.md"
diff "$ROOT/skills/_shared/plain-text-line.md" "$ROOT/skills/idiom-chain/plain-text-line.md"
diff "$ROOT/skills/_shared/plain-text-line.md" "$ROOT/skills/poetry-quiz/plain-text-line.md"

echo "All shared file copies are in sync."
