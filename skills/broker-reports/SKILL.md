---
name: broker-reports
description: 深度搜尋券商報告，用多組關鍵字交叉搜尋，並補充網路分析師觀點。Use when the user wants to search broker reports, find analyst opinions, or look up research reports for a stock or industry.
allowed-tools: mcp__broker-reports__search_broker_reports, mcp__broker-reports__get_report_detail, WebSearch
---

# broker-reports

## Usage
/broker-reports <關鍵字>
例如：/broker-reports AES-KY 或 /broker-reports 電力設備

## Instructions

當使用者觸發此 skill 時，請依序執行以下步驟：

### Step 1：多組關鍵字交叉搜尋券商報告
使用券商報告工具 (mcp__broker-reports__search_broker_reports)，針對輸入的關鍵字展開多角度搜尋：

如果是**個股**：
- 股票代號（如 6781）
- 公司英文名稱（如 AES-KY）
- 公司中文名稱（如 先進能源）
- 所屬產業關鍵字（如 鋰電池、電池模組）
- 主要產品/應用（如 電動堆高機、AGV）

如果是**產業/主題**：
- 直接搜尋該關鍵字
- 搜尋相關同義詞或上下游關鍵字
- 搜尋英文關鍵字

每次搜尋 limit 設為 10，盡量撈到最多結果。

### Step 2：去重與整理
- 將所有搜尋結果去重（依 ID）
- 按日期排序（最新在前）

### Step 3：補充網路分析師觀點
- 如果券商報告少於 3 篇，使用 WebSearch 搜尋：
  - "<公司名稱> 分析師 目標價"
  - "<公司名稱> 研究報告"
- 補充找到的分析師觀點

### Step 4：輸出格式

```
## 券商報告搜尋結果：<關鍵字>

### 券商報告（共 N 篇）
| # | 日期 | 券商 | 標題 | 評等 | 目標價 |
|---|---|---|---|---|---|
| 1 | | | | | |

### 涵蓋率分析
- 共 N 家券商出具報告
- 最新報告日期：YYYY/MM/DD
- 評等分佈：買進 N / 中立 N / 賣出 N

### 網路補充觀點
（若有從網路找到的額外分析師意見）

> 報告搜尋結果取決於資料庫收錄範圍，可能不完整。
```
