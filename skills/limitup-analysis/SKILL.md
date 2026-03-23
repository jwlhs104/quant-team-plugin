---
name: limitup-analysis
description: 每日漲停股篩選與漲停黑K預測分析。當使用者需要查詢今日漲停股、分析漲停後走勢、或進行漲停黑K策略分析時使用。
---

# 漲停分析與黑K預測 (Limit-Up Analysis & Black Candle Prediction)

## 分析流程

### Step 1: 搜尋今日漲停股

使用 WebSearch 搜尋當日漲停資訊：

```
搜尋關鍵字：
- "今日漲停股 TWSE"
- "台股漲停 {YYYYMMDD}"
- "漲停板 site:goodinfo.tw"
- "漲停家數 site:cmoney.tw"
```

記錄以下資訊：
- 股票代碼與名稱
- 漲停價格
- 漲停時間（是否早盤即鎖漲停）
- 成交量

### Step 2: 取得 OHLCV 資料

對每檔漲停股，使用 yfinance 取得價格資料：

```python
import yfinance as yf
import pandas as pd

ticker = "XXXX.TW"
df = yf.download(ticker, period="3mo")

# 取得最新一筆資料
latest = df.iloc[-1]
print(f"Open:   {latest['Open']:.2f}")
print(f"High:   {latest['High']:.2f}")
print(f"Low:    {latest['Low']:.2f}")
print(f"Close:  {latest['Close']:.2f}")
print(f"Volume: {latest['Volume']:.0f}")
```

### Step 3: 判斷是否形成漲停黑K

**漲停黑K 定義**: 當日觸及漲停價但收盤低於開盤（收黑K）

```python
# 漲停黑K判斷邏輯
limit_up_price = round(prev_close * 1.10, 2)  # 台股漲停幅度 10%

conditions = {
    "觸及漲停": latest['High'] >= limit_up_price,
    "收黑K": latest['Close'] < latest['Open'],
    "上影線長": (latest['High'] - latest['Close']) > (latest['Close'] - latest['Low']),
    "成交量放大": latest['Volume'] > df['Volume'].rolling(5).mean().iloc[-2] * 1.5,
}

is_black_candle = conditions["觸及漲停"] and conditions["收黑K"]
```

**嚴重程度分級**：

| 等級 | 條件 | 意義 |
|------|------|------|
| 強烈空方 | 收盤跌破開盤 > 3% | 主力大量出貨 |
| 中度空方 | 收盤跌破開盤 1-3% | 追價力道不足 |
| 輕度空方 | 收盤略低於開盤 < 1% | 觀望訊號 |

### Step 4: 歷史型態交叉比對

使用回測腳本驗證歷史勝率：

```bash
python scripts/backtest_black_candle.py --ticker XXXX.TW --start 2024-01-01 --end 2026-03-01
```

比對項目：
- 該股過去出現漲停黑K後的平均跌幅
- 隔日開低比例
- 5日內最大跌幅
- 反彈機率與時間

### Step 5: 產生分析報告

**報告儲存路徑**: `docs/outputs/漲停分析_{YYYYMMDD}.md`

**參考既有報告**:
- `docs/outputs/漲停黑K分析_20260318.md`
- `docs/outputs/漲停黑K分析_20260319.md`

---

## 報告格式

### 漲停分析日報 — {YYYY}/{MM}/{DD}

**大盤概況**: 加權指數 {index_close}，漲停家數 {count}

#### 漲停黑K 警示清單

| 代碼 | 名稱 | 漲停價 | 收盤價 | 黑K幅度 | 成交量倍數 | 風險等級 |
|------|------|--------|--------|---------|-----------|---------|
| XXXX | OOO | xxx.x | xxx.x | -x.x% | x.xX | 高/中/低 |

#### 個股詳細分析

**{stock_name} ({ticker})**
- K線型態: 漲停黑K，上影線 {shadow}%
- 成交量: {volume} 張 ({vol_ratio}X 五日均量)
- 歷史勝率: 漲停黑K後5日下跌機率 {win_rate}%
- 平均跌幅: {avg_drop}%

---

## 風險評估與部位建議

### 部位規模建議

| 風險等級 | 建議部位 | 停損設定 |
|---------|---------|---------|
| 高確信 | 總資金 5% | 漲停價上方 1% |
| 中確信 | 總資金 3% | 漲停價上方 2% |
| 低確信 | 總資金 1% 或觀望 | 漲停價上方 3% |

### 注意事項

- 漲停黑K 為「短線」訊號，持有期間建議 1-5 個交易日
- 需搭配大盤趨勢判斷（空頭市場勝率較高）
- 避開業績利多股（法說會、財報超預期）
- 處置股與注意股需額外留意流動性風險

---

## Telegram 推送格式

報告需同時準備 Telegram 精簡版：

```
📊 漲停黑K日報 {MM/DD}

🔴 高風險警示：
• {ticker} {name} 收{close}（黑K {drop}%）
  量能{vol_ratio}X｜歷史勝率{win_rate}%

🟡 觀察名單：
• {ticker} {name} 收{close}（黑K {drop}%）

⚠️ 以上為技術面分析，非投資建議
```
