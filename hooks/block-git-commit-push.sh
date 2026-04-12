#!/bin/bash
# Cursor beforeShellExecution hook: prompt before git commit / git push in the agent shell.

input=$(cat)
command=$(echo "$input" | jq -r '.command // empty')

if echo "$command" | grep -qE '(^|[;&|]+\s*)git\s+(.*\s+)?(commit|push)(\s|$)'; then
  cat <<EOF
{
  "permission": "ask",
  "user_message": "This shell command runs git commit or git push. Approve only if you intend to let the agent perform this; otherwise cancel and run it in your own terminal.",
  "agent_message": "A hook is asking the user to approve git commit or git push in the agent shell. Wait for their decision; if they decline, suggest running the command locally."
}
EOF
else
  echo '{"permission":"allow"}'
fi
