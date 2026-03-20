#!/bin/bash
# Global Cursor beforeShellExecution hook: block git commit and git push only.

input=$(cat)
command=$(echo "$input" | jq -r '.command // empty')

if echo "$command" | grep -qE '(^|[;&|]+\s*)git\s+(.*\s+)?(commit|push)(\s|$)'; then
  cat <<EOF
{
  "continue": true,
  "permission": "deny",
  "user_message": "git commit and git push are blocked in the agent shell. Please run them in your own terminal.",
  "agent_message": "git commit / git push has been blocked by a hook. Do not run these commands in the agent shell. Ask the user to run them in their local terminal instead."
}
EOF
else
  echo '{"continue":true,"permission":"allow"}'
fi
