---
name: backtest-workflow
description: 台股回測工作流程。當使用者需要執行策略回測、測試交易策略、比較策略績效、或產生回測報告時使用。
---

# 台股回測工作流程 (Backtest Workflow)

## 可用策略一覽

| 策略名稱 | 代號 | 說明 | 適用情境 |
|---------|------|------|---------|
| 當沖策略 | ORB_15 | Opening Range Breakout 15分鐘 | 高波動個股當沖 |
| 波段策略 | Swing | Momentum Breakout 動能突破 | 中期波段操作 |
| 可轉債策略 | CB Bond Floor | Bond Floor Hunter 債底獵手 | 低風險套利 |
| 權證策略 | Warrant IVD | IV Discount 隱波折價 | 權證套利 |
| 處置效果策略 | Disposition | Disposition Effect 處置效應 | 事件驅動 |
| 漲停黑K策略 | Black Candle | 漲停後黑K反轉 | 短線反轉訊號 |

## 執行步驟

### Step 1: 確認策略與參數

向使用者確認以下資訊：

- **策略類型**: 上述六種之一
- **標的代碼**: 使用 `.TW` 後綴（例如 `2330.TW`）
- **回測期間**: 起始日期與結束日期（格式 `YYYY-MM-DD`）
- **持有天數**: 預設依策略不同（當沖=1天, 波段=5-20天）

### Step 2: 設定台股預設參數

```python
# 台股交易成本預設值
COMMISSION_RATE = 0.001425   # 手續費 0.1425%
TAX_RATE = 0.003             # 證交稅 0.3% (當沖減半 0.15%)
TIMEZONE = "Asia/Taipei"
TRADING_HOURS = "09:00-13:30"
```

### 常用標的代碼

| 代碼 | 名稱 | 類型 |
|------|------|------|
| 2330.TW | 台積電 | 半導體龍頭 |
| 2317.TW | 鴻海 | 電子代工 |
| 0050.TW | 元大台灣50 | ETF |
| 2454.TW | 聯發科 | IC設計 |
| 2881.TW | 富邦金 | 金融股 |
| 2303.TW | 聯電 | 半導體 |

### Step 3: 執行回測腳本

```bash
# 漲停黑K回測
python scripts/backtest_black_candle.py --ticker 2330.TW --start 2025-01-01 --end 2026-01-01

# 其他策略依對應腳本執行
```

**參考腳本路徑**: `scripts/backtest_black_candle.py`

### Step 4: 讀取與分析結果

回測完成後，讀取產生的報告：

- **回測結果目錄**: `docs/outputs/backtest*/`
- **最終報告**: `docs/outputs/backtest*/final_report.md`
- **策略文件參考**: `docs/collaboration/*.md`

### Step 5: 產生績效摘要

向使用者報告以下關鍵指標：

- **總報酬率** (Total Return %)
- **年化報酬率** (Annualized Return %)
- **夏普比率** (Sharpe Ratio)
- **最大回撤** (Max Drawdown %)
- **勝率** (Win Rate %)
- **獲利因子** (Profit Factor)
- **總交易次數** (Total Trades)

### Step 6: 產生權益曲線圖表

使用 matplotlib 產生視覺化圖表：

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

# 上圖：權益曲線 (Equity Curve)
axes[0].plot(dates, equity, label='策略淨值')
axes[0].set_title(f'{ticker} 回測權益曲線')
axes[0].set_ylabel('淨值')
axes[0].legend()

# 下圖：回撤 (Drawdown)
axes[1].fill_between(dates, drawdown, 0, alpha=0.3, color='red')
axes[1].set_ylabel('回撤 (%)')

plt.tight_layout()
plt.savefig(f'docs/outputs/backtest_{ticker}_{date}.png', dpi=150)
```

## 輸出格式

檔案命名規則：`docs/outputs/backtest_{策略}_{標的}_{YYYYMMDD}.md`

報告內容應包含：
1. 策略說明與參數設定
2. 關鍵績效指標表格
3. 權益曲線圖表（PNG）
4. 交易明細（前10筆）
5. 風險評估與建議
