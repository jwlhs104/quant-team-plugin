# quant-team-plugin

量化研究團隊共享 Claude Code Plugin — 台股分析、券商報告、回測、產業掃描、安全護欄。

> 本 plugin 整合了原 [claude-plugin-taiwan-stocks](https://github.com/jwlhs104/claude-plugin-taiwan-stocks) 的所有功能，並新增 hooks 與更多 skills。

## 使用方式

```bash
claude --plugin-dir /path/to/quant-team-plugin
```

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

| Server | 說明 |
|---|---|
| `broker-reports` | 券商報告搜尋引擎（需設定 `BROKER_REPORTS_PATH` 環境變數） |

## 環境變數

| 變數 | 說明 |
|---|---|
| `BROKER_REPORTS_PATH` | broker-reports MCP server 的路徑 |

## 安裝到團隊專案

```bash
# 方法 1：--plugin-dir（開發/測試）
claude --plugin-dir ./quant-team-plugin

# 方法 2：marketplace 安裝（正式使用）
claude plugin install quant-team
```

## 從 taiwan-stocks 遷移

本 plugin 完全取代 `claude-plugin-taiwan-stocks`，包含其所有 skills + 額外的回測、報告、漲停分析 skills 與安全 hooks。
