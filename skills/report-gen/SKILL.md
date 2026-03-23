---
name: report-gen
description: 產生投資綜合報告。當使用者需要週報、策略比較報告、持倉檢視報告、或任何投資績效彙整時使用。
---

# 投資報告產生器 (Investment Report Generator)

## 報告類型

| 類型 | 說明 | 頻率 |
|------|------|------|
| 週報 | 本週交易摘要與市場回顧 | 每週五 |
| 策略比較 | 各策略績效橫向比較 | 依需求 |
| 持倉檢視 | 目前持倉損益與風險評估 | 依需求 |

---

## 資料來源

### 回測績效資料
- **回測報告目錄**: `docs/outputs/backtest*/final_report.md`
- **策略文件**: `docs/collaboration/*.md`

掃描所有 `final_report.md` 取得各策略關鍵績效指標。

### 策略績效排名（基準參考）

| 排名 | 策略 | Sharpe Ratio | 備註 |
|------|------|-------------|------|
| 1 | CB Bond Floor（可轉債債底） | 3.11 | 最穩健，低波動 |
| 2 | Day-Trade ORB_15（當沖） | 1.86 | 高頻交易，需盯盤 |
| 3 | Warrant IVD（權證隱波折價） | 0.99 | 中等風險報酬 |
| 4 | Swing Breakout（波段突破） | 0.79 | 波動較大 |

---

## 一、週報 (Weekly Summary)

### 產生步驟

1. 掃描本週 `docs/outputs/` 中所有新產生的報告
2. 彙整本週交易紀錄與損益
3. 回顧大盤走勢（使用 WebSearch 搜尋 "台股週報 {date}"）
4. 各策略本週表現摘要
5. 下週展望與注意事項

### 週報模板

```markdown
# 投資週報 — {YYYY}W{WW}（{MM/DD} ~ {MM/DD}）

## 本週大盤概況
- 加權指數: {close}（週漲跌 {change}%）
- 成交量: 日均 {avg_vol} 億
- 類股輪動: {sector_rotation}

## 策略績效摘要

| 策略 | 本週報酬 | 累計報酬 | 交易次數 | 勝率 |
|------|---------|---------|---------|------|
| ORB_15 當沖 | +x.x% | +xx.x% | x | xx% |
| 波段突破 | +x.x% | +xx.x% | x | xx% |
| 可轉債 | +x.x% | +xx.x% | x | xx% |
| 權證 IVD | +x.x% | +xx.x% | x | xx% |

## 重點交易回顧
1. {trade_1_summary}
2. {trade_2_summary}

## 下週展望
- {outlook_1}
- {outlook_2}

## 風險提醒
- {risk_1}
- {risk_2}
```

---

## 二、策略比較報告 (Strategy Comparison)

### 產生步驟

1. 讀取各策略 `final_report.md` 中的績效指標
2. 統一比較期間（取交集日期範圍）
3. 計算風險調整後報酬
4. 產生比較表格與排名

### 比較維度

| 指標 | 說明 | 權重 |
|------|------|------|
| Sharpe Ratio | 風險調整後報酬 | 30% |
| Max Drawdown | 最大回撤 | 25% |
| Win Rate | 勝率 | 15% |
| Profit Factor | 獲利因子 | 15% |
| 交易頻率 | 月均交易次數 | 10% |
| 執行難度 | 是否需要即時盯盤 | 5% |

### 比較報告模板

```markdown
# 策略績效比較報告 — {date}

## 綜合績效比較

| 指標 | CB Bond Floor | ORB_15 | Warrant IVD | Swing Breakout |
|------|-------------|--------|-------------|----------------|
| 年化報酬 | xx% | xx% | xx% | xx% |
| Sharpe Ratio | 3.11 | 1.86 | 0.99 | 0.79 |
| Max Drawdown | -x% | -x% | -x% | -x% |
| 勝率 | xx% | xx% | xx% | xx% |
| Profit Factor | x.xx | x.xx | x.xx | x.xx |
| 月均交易次數 | x | x | x | x |

## 策略適用建議
- **保守型投資人**: CB Bond Floor 為首選（Sharpe 3.11）
- **積極型投資人**: ORB_15 當沖（需有盯盤能力）
- **均衡配置**: CB 50% + ORB_15 30% + Warrant 20%

## 相關性分析
各策略報酬相關性矩陣，低相關性有助分散風險。
```

---

## 三、持倉檢視報告 (Portfolio Review)

### 產生步驟

1. 取得目前持倉清單（由使用者提供或從紀錄讀取）
2. 使用 yfinance 取得最新價格
3. 計算未實現損益
4. 評估各持股風險水位
5. 產生調整建議

### 持倉報告模板

```markdown
# 持倉檢視報告 — {date}

## 持倉總覽

| 標的 | 成本價 | 現價 | 持股 | 損益 | 報酬率 | 部位比重 |
|------|--------|------|------|------|--------|---------|
| {ticker} | xxx | xxx | xxx張 | +xxx | +x.x% | xx% |

**總市值**: ${total_value}
**未實現損益**: ${unrealized_pnl}（{pnl_pct}%）

## 風險評估
- 集中度風險: 最大持股佔比 {max_weight}%
- 產業分散度: {sector_count} 個產業
- Beta 曝險: 組合 Beta {portfolio_beta}

## 調整建議
1. {suggestion_1}
2. {suggestion_2}
```

---

## Telegram 推送格式最佳化

報告需優化為 Telegram 閱讀格式：

- 使用 **粗體** 標示重點數據
- 使用表格呈現比較數據
- 趨勢指標：📈 上漲 / 📉 下跌 / ➡️ 持平
- 風險等級：🔴 高風險 / 🟡 中風險 / 🟢 低風險
- 段落精簡，每段不超過 3-4 行
- 重要數字使用 `code` 格式標示

---

## 報告儲存

- **儲存目錄**: `docs/outputs/reports/`
- **週報命名**: `weekly_{YYYY}W{WW}.md`
- **策略比較**: `strategy_comparison_{YYYYMMDD}.md`
- **持倉檢視**: `portfolio_review_{YYYYMMDD}.md`

---

## 免責聲明

每份報告底部必須附上以下免責聲明：

```
---
⚠️ 免責聲明：本報告由 AI 自動產生，僅供參考，不構成任何投資建議。
投資有風險，過去績效不代表未來表現。請依個人風險承受度審慎評估，
投資決策應自行負責。
```
