# quant-team-plugin

量化研究團隊共享 Claude Code Plugin — 台股分析、券商報告、回測、產業掃描、安全護欄。

> 本 plugin 整合了原 [claude-plugin-taiwan-stocks](https://github.com/jwlhs104/claude-plugin-taiwan-stocks) 的所有功能，並新增 subagents、hooks 與更多 skills。

## 使用方式

```bash
# 1. Clone
git clone https://github.com/jwlhs104/quant-team-plugin.git

# 2. 設定 MCP Server URL（指向團隊部署的券商報告 MCP server）
export BROKER_REPORTS_URL=http://192.168.1.100:8100/mcp

# 3. 啟動
claude --plugin-dir /path/to/quant-team-plugin
```

## Server 端部署

本 plugin 的 MCP server 已改為遠端架構（Streamable HTTP），不再隨 plugin 一起打包。
團隊需自行部署 MCP server，plugin 端只需設定 `BROKER_REPORTS_URL` 環境變數指向該 server。

**部署步驟：**

1. 在 server 機器上部署 `broker-reports` MCP server（獨立 repo 或 Docker image）
2. 確保 server 監聽在團隊可存取的位址，例如 `http://192.168.1.100:8100/mcp`
3. 每位團隊成員設定環境變數：
   ```bash
   export BROKER_REPORTS_URL=http://<server-ip>:8100/mcp
   ```
4. 啟動 Claude Code 即可自動連線

> 如果是本機開發測試，可以把 server 跑在 localhost：`export BROKER_REPORTS_URL=http://localhost:8100/mcp`

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

| Server | 說明 | 連線方式 |
|---|---|---|
| `broker-reports` | 券商報告搜尋引擎（8000+ 份報告） | 遠端 Streamable HTTP（需設定 `BROKER_REPORTS_URL`） |

## 環境變數

| 變數 | 說明 |
|---|---|
| `BROKER_REPORTS_URL` | 券商報告 MCP server 的 URL（例如 `http://192.168.1.100:8100/mcp`） |

## 專案結構

```
quant-team-plugin/
├── .claude-plugin/plugin.json     <- Plugin 描述
├── .mcp.json                      <- MCP server 連線設定（遠端）
├── agents/                        <- 3 個 subagents
├── hooks/                         <- 2 個 hooks + 腳本
└── skills/                        <- 8 個 skills
```
