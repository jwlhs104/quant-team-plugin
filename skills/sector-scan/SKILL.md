---
name: sector-scan
description: 產業鏈掃描，搜尋特定產業的所有券商報告，列出相關個股與產業趨勢。Use when the user wants to scan an industry sector, find related stocks, or understand supply chain dynamics.
allowed-tools: mcp__broker-reports__search_broker_reports, mcp__broker-reports__get_report_detail, WebSearch
---

# sector-scan

## Usage
/sector-scan <產業名稱>
例如：/sector-scan 電力設備 或 /sector-scan AI伺服器

## Instructions

當使用者觸發此 skill 時，請依序執行以下步驟：

### Step 1：廣泛搜尋產業相關券商報告
使用券商報告工具 (mcp__broker-reports__search_broker_reports)，用多組關鍵字搜尋：

- 產業名稱本身（如「電力設備」）
- 相關同義詞（如「電力」「配電」「輸電」）
- 英文關鍵字（如「power equipment」）
- 上游關鍵字（如「變壓器」「開關設備」）
- 下游/應用端關鍵字（如「資料中心」「AI用電」）
- 相關概念（如「綠能」「儲能」）

每次搜尋 limit 設為 15，盡量撈到最多結果。

### Step 2：彙整個股清單
- 從所有報告中提取被提及的個股
- 去重並整理成清單

### Step 3：網路補充產業趨勢
使用 WebSearch 搜尋：
- "<產業名稱> 產業趨勢 2025 2026"
- "<產業名稱> 台股 概念股"
- 取得最新的產業動態

### Step 4：輸出格式

```
## 產業掃描：<產業名稱>

### 產業趨勢摘要
（3-5 點近期產業重要趨勢）

### 券商報告總覽（共 N 篇）
| # | 日期 | 券商 | 標題 | 相關個股 | 評等 |
|---|---|---|---|---|---|
| 1 | | | | | |

### 相關個股清單
| 股票代號 | 公司名稱 | 券商評等 | 在產業鏈中的角色 |
|---|---|---|---|
| | | | |

### 產業鏈圖譜
（用文字描述上中下游關係）
- 上游：...
- 中游：...
- 下游/應用端：...

> 以上資訊僅供研究參考，不構成投資建議。
```
