---
name: stock-overview
description: 一鍵查詢台股個股基本面總覽，自動彙整公司資訊。Use when the user wants to look up a stock, get company overview, or check fundamentals of a Taiwan stock.
allowed-tools: mcp__broker-reports__search_broker_reports, mcp__broker-reports__get_report_detail, WebSearch
---

# stock-overview

## Usage
/stock-overview <股票代號或名稱>
例如：/stock-overview 6781 或 /stock-overview AES-KY

## Instructions

當使用者觸發此 skill 時，請依序執行以下步驟：

### Step 1：券商報告搜尋
- 使用券商報告工具 (mcp__broker-reports__search_broker_reports)，用以下多組關鍵字分別搜尋：
  - 股票代號（如 6781）
  - 公司名稱（如 AES-KY）
  - 公司中文名稱（如果知道的話）
- 彙整所有找到的報告

### Step 2：網路搜尋補充
- 使用 WebSearch 搜尋以下資訊：
  - 公司基本介紹、核心業務、主要產品
  - 近期營收、EPS、財務數據
  - 近期產業動態與新聞
- 搜尋時加上當前年份以取得最新資訊

### Step 3：輸出固定格式摘要

請用以下格式輸出：

```
## <公司名稱>（<股票代號>）總覽

### 公司簡介
- 產業分類：
- 主要業務：
- 主要產品/服務：
- 主要客戶/應用場景：

### 近期財務數據
| 項目 | 數值 |
|---|---|
| 近期月營收 | |
| 營收年增率 | |
| 近期 EPS | |
| 近四季 EPS 合計 | |

### 券商觀點
（列出找到的券商報告摘要，若無則註明「目前無券商報告覆蓋」）

### 近期動態
（近期重要新聞或產業趨勢摘要，2-3 點）

> 以上資訊僅供參考，不構成投資建議。
```
