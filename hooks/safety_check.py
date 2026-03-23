#!/usr/bin/env python3
"""
PreToolUse Hook: Bash 命令安全檢查
阻止危險命令，保護專案安全。
"""
import json
import re
import sys

event = json.load(sys.stdin)
command = event.get("tool_input", {}).get("command", "")
if not command:
    sys.exit(0)

DANGEROUS_PATTERNS = [
    (r"rm\s+-[rf]*\s+(/|~/|\.\./)", "禁止刪除根目錄或上層目錄"),
    (r"rm\s+-rf\s+\.", "禁止 rm -rf 當前目錄"),
    (r"git\s+push\s+.*--force\s+.*main", "禁止 force push 到 main"),
    (r"git\s+push\s+.*--force\s+.*master", "禁止 force push 到 master"),
    (r"git\s+reset\s+--hard\s+origin", "禁止 git reset --hard origin"),
    (r"cat\s+\.env\b", "禁止直接 cat .env"),
    (r"chmod\s+-R\s+777", "禁止 chmod -R 777"),
    (r"curl\s+.*\|\s*(bash|sh)", "禁止 curl | bash"),
]

for pattern, reason in DANGEROUS_PATTERNS:
    if re.search(pattern, command, re.IGNORECASE):
        print(f"⛔ {reason}\n   命令: {command}", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
