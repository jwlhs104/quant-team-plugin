---
name: stock-analysis
description: 台股四大面向分析法。當使用者需要分析個股、評估投資標的、查詢技術指標或基本面資料時使用。
---

# 台股四大面向分析法 (Stock Analysis Framework)

## 分析架構

針對台股標的進行「技術面、基本面、籌碼面、消息面」四大面向綜合分析。

## 資料來源

| 資料類型 | 來源 | 用法 |
|---------|------|------|
| 股價 OHLCV | yfinance | `yf.download("2330.TW", period="6mo")` |
| 新聞 / 基本面 | WebSearch | 搜尋即時新聞與財報資訊 |
| 券商報告 | mcp__broker-reports | 取得券商研究報告 |

---

## 一、技術面分析 (Technical Analysis)

### K線型態辨識
- **紅K / 黑K**: 判斷多空方向
- **十字線**: 轉折訊號
- **長上影線 / 長下影線**: 壓力與支撐
- **吞噬型態**: 反轉訊號
- **漲停黑K**: 短線反轉（參見 limitup-analysis skill）

### 技術指標計算

```python
import yfinance as yf
import pandas as pd

ticker = "2330.TW"
df = yf.download(ticker, period="6mo")

# 均線 (Moving Averages)
df['MA5'] = df['Close'].rolling(5).mean()
df['MA10'] = df['Close'].rolling(10).mean()
df['MA20'] = df['Close'].rolling(20).mean()
df['MA60'] = df['Close'].rolling(60).mean()

# RSI (Relative Strength Index)
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
df['RSI'] = 100 - (100 / (1 + gain / loss))

# MACD
ema12 = df['Close'].ewm(span=12).mean()
ema26 = df['Close'].ewm(span=26).mean()
df['MACD'] = ema12 - ema26
df['Signal'] = df['MACD'].ewm(span=9).mean()
df['Histogram'] = df['MACD'] - df['Signal']

# KD 隨機指標 (Stochastic Oscillator)
low_min = df['Low'].rolling(9).min()
high_max = df['High'].rolling(9).max()
df['RSV'] = (df['Close'] - low_min) / (high_max - low_min) * 100
df['K'] = df['RSV'].ewm(com=2).mean()
df['D'] = df['K'].ewm(com=2).mean()

# 成交量分析
df['Vol_MA5'] = df['Volume'].rolling(5).mean()
df['Vol_Ratio'] = df['Volume'] / df['Vol_MA5']
```

### 技術面判讀規則

| 指標 | 多方訊號 | 空方訊號 |
|------|---------|---------|
| 均線 | MA5 > MA20 > MA60 多頭排列 | MA5 < MA20 < MA60 空頭排列 |
| RSI | RSI < 30 超賣反彈 | RSI > 70 超買修正 |
| MACD | MACD 金叉（上穿 Signal） | MACD 死叉（下穿 Signal） |
| KD | K 值 < 20 超賣區 | K 值 > 80 超買區 |
| 成交量 | 價漲量增，突破有效 | 價漲量縮，假突破 |

---

## 二、基本面分析 (Fundamental Analysis)

### 關鍵指標

| 指標 | 說明 | 評估標準 |
|------|------|---------|
| EPS | 每股盈餘 | 逐季成長為佳 |
| PE Ratio | 本益比 | 低於產業平均為便宜 |
| 營收成長率 | 月營收年增率 | > 10% 為成長股 |
| 毛利率 | Gross Margin | 穩定或上升為佳 |
| 股利殖利率 | Dividend Yield | > 4% 為高殖利率 |
| ROE | 股東權益報酬率 | > 15% 為優質 |

### 資料取得方式

```python
# 使用 yfinance 取得基本面資訊
import yfinance as yf
stock = yf.Ticker("2330.TW")
info = stock.info
print(f"PE Ratio: {info.get('trailingPE')}")
print(f"Dividend Yield: {info.get('dividendYield')}")
print(f"Market Cap: {info.get('marketCap')}")
```

使用 WebSearch 搜尋補充資料：
- 搜尋 `"{ticker} 月營收"` 取得最新營收
- 搜尋 `"{ticker} EPS 季報"` 取得獲利資訊

---

## 三、籌碼面分析 (Institutional Flow Analysis)

### 關注指標

| 指標 | 來源 | 意義 |
|------|------|------|
| 三大法人買賣超 | WebSearch TWSE | 外資/投信/自營商動向 |
| 融資融券 | WebSearch | 散戶槓桿方向 |
| 大戶持股比例 | WebSearch | 籌碼集中度 |
| 董監持股異動 | WebSearch | 內部人動態 |

### 搜尋指令範例

- `"{stock_name} 三大法人買賣超"` — 法人進出
- `"{stock_name} 融資融券餘額"` — 散戶槓桿
- `"{stock_name} 持股分級"` — 大戶集中度
- `"TWSE 三大法人買賣超排行"` — 全市場法人動向

---

## 四、消息面分析 (News & Sentiment Analysis)

### 資訊來源

1. **即時新聞**: WebSearch `"{stock_name} 最新消息"`
2. **法說會**: WebSearch `"{stock_name} 法說會"`
3. **券商報告**: 使用 `mcp__broker-reports` MCP 工具取得
4. **產業趨勢**: WebSearch `"{industry} 產業趨勢 2026"`

### 消息面評估要點

- 是否有重大利多/利空事件
- 產業上下游供需變化
- 政策法規影響
- 國際市場連動性

---

## 輸出報告模板

### {stock_name} ({ticker}) 綜合分析報告

**分析日期**: {date}
**收盤價**: {close_price}

| 面向 | 評分 | 重點發現 |
|------|------|---------|
| 技術面 | ★★★★☆ | {technical_summary} |
| 基本面 | ★★★☆☆ | {fundamental_summary} |
| 籌碼面 | ★★★★☆ | {institutional_summary} |
| 消息面 | ★★★☆☆ | {news_summary} |

**綜合評分**: ★★★★☆ (X / 5)

**風險等級**: 低 / 中 / 高

**目標價**: {target_price}（依據: {rationale}）

**關鍵發現**:
1. {finding_1}
2. {finding_2}
3. {finding_3}

**操作建議**: {recommendation}

---

## 報告儲存

檔案路徑：`docs/outputs/analysis_{ticker}_{YYYYMMDD}.md`

以 markdown 格式儲存完整分析報告，方便後續追蹤與比對。
