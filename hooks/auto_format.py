#!/usr/bin/env python3
"""
PostToolUse Hook: 自動用 ruff 格式化 Python 檔案
"""
import json
import subprocess
import sys
import os

event = json.load(sys.stdin)
file_path = event.get("tool_input", {}).get("file_path", "")

if not file_path or not file_path.endswith(".py") or not os.path.isfile(file_path):
    sys.exit(0)

try:
    subprocess.run(["ruff", "format", "--quiet", file_path], capture_output=True, timeout=10)
    subprocess.run(["ruff", "check", "--fix", "--quiet", file_path], capture_output=True, timeout=10)
except (FileNotFoundError, subprocess.TimeoutExpired):
    pass

sys.exit(0)
