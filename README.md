# quant-team-plugin

量化研究團隊共享 Claude Code Plugin — 台股分析、券商報告、回測、產業掃描、安全護欄。

> 本 plugin 整合了原 [claude-plugin-taiwan-stocks](https://github.com/jwlhs104/claude-plugin-taiwan-stocks) 的所有功能，並新增 subagents、hooks 與更多 skills。

## 使用方式

```bash
# 1. Clone
git clone https://github.com/jwlhs104/quant-team-plugin.git

# 2. 設定券商報告資料路徑（放你的 reports/ 和 reports.db 的目錄）
export BROKER_DATA_PATH=/path/to/your/broker-data

# 3. 啟動
claude --plugin-dir /path/to/quant-team-plugin
```

## Subagents（3 個）

| Agent | 說明 | 工具限制 | 記憶 |
|---|---|---|---|
| `quant-team:stock-researcher` | 唯讀研究員 — 搜券商報告、新聞、基本面 | 只能讀取和搜尋 | user（跨專案） |
| `quant-team:backtest-runner` | 回測執行員 — 跑腳本、讀結果 | 不能寫入檔案 | 無 |
| `quant-team:report-writer` | 報告撰寫員 — 產生結構化投資報告 | 可寫入 docs/ | project（記住團隊慣例） |

## Skills（8 個）

| Skill | 說明 |
|---|---|
| `/quant-team:stock-analysis` | 個股四維度分析（技術面、基本面、籌碼面、消息面） |
| `/quant-team:backtest-workflow` | 台股策略回測工作流程 |
| `/quant-team:report-gen` | 投資報告生成（週報、策略比較、持倉檢視） |
| `/quant-team:limitup-analysis` | 漲停板分析與黑K偵測 |
| `/quant-team:broker-reports` | 券商報告多關鍵字交叉搜尋 |
| `/quant-team:stock-overview` | 個股基本面總覽 |
| `/quant-team:compare` | 同業個股比較 |
| `/quant-team:sector-scan` | 產業鏈掃描 |

## Hooks（2 個）

| Hook | 類型 | 說明 |
|---|---|---|
| `safety_check.py` | PreToolUse | 阻止危險 shell 命令（rm -rf、force push 等） |
| `auto_format.py` | PostToolUse | 自動用 ruff 格式化 Python 檔案 |

## MCP Servers

| Server | 說明 | 程式碼位置 |
|---|---|---|
| `broker-reports` | 券商報告搜尋引擎（8000+ 份報告） | `servers/broker-reports/` |

## 環境變數

| 變數 | 說明 |
|---|---|
| `BROKER_DATA_PATH` | 券商報告資料目錄（放 `reports/` 和 `reports.db` 的位置） |

## 新增 MCP Server

將新的 server 程式碼放在 `servers/<name>/`，然後在 `.mcp.json` 加一筆：

```json
{
  "new-server": {
    "command": "python",
    "args": ["-m", "src.server"],
    "cwd": "${CLAUDE_PLUGIN_ROOT}/servers/new-server"
  }
}
```

## 專案結構

```
quant-team-plugin/
├── .claude-plugin/plugin.json     ← Plugin 描述
├── .mcp.json                      ← MCP server 串接設定
├── agents/                        ← 3 個 subagents
├── hooks/                         ← 2 個 hooks + 腳本
├── skills/                        ← 8 個 skills
└── servers/                       ← MCP server 程式碼（mono repo）
    └── broker-reports/
        ├── src/                   ← server 程式碼
        └── config.yaml            ← server 設定
```
