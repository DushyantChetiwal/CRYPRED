# 🚀 Crypto Arbitrage System

A real-time cryptocurrency arbitrage detection system that monitors price differences between Indian Rupee (INR) and US Dollar (USDT) markets to identify profitable trading opportunities.

## 🎯 How It Works

### The Strategy
1. **Monitor Two Markets**: CoinDCX (INR) and Binance (USDT)
2. **Normalize Prices**: Convert INR prices to USD using real-time exchange rates
3. **Find Spreads**: Calculate price differences between normalized INR and USDT prices
4. **Generate Signals**: 
   - **BUY Signal**: When INR price is lower than USDT price (buy in INR market)
   - **SELL Signal**: When INR price is higher than USDT price (sell in INR market)

### Example
```
BTC Price on CoinDCX: ₹10,300,000
BTC Price on Binance: $123,500 USDT
USD/INR Rate: 83.50

Normalized INR Price: ₹10,300,000 ÷ 83.50 = $123,353
Spread: ($123,353 - $123,500) / $123,500 = -0.12%

Signal: BUY (INR is cheaper, buy on CoinDCX)
```

## 📊 Features

- **Real-time monitoring** of 6 major cryptocurrencies
- **Concurrent API calls** for faster data fetching
- **Configurable spread thresholds** (default: 0.5% minimum)
- **Confidence scoring** based on volume and spread size
- **Rate limiting** to respect API limits
- **Error handling** with retry logic
- **Data persistence** for analysis

## 🔧 Setup

### Prerequisites
```bash
pip install requests python-dateutil
```

### Configuration
Edit `arbitrage_config.json` to customize:
- Minimum spread percentage
- Check intervals
- Trading pairs
- API endpoints

### Usage

#### Test the System
```bash
python3 scripts/test_arbitrage.py
```

#### Run Continuous Monitoring
```bash
python3 scripts/realtime_arbitrage.py
```

## 📈 Monitored Pairs

| Symbol | CoinDCX (INR) | Binance (USDT) |
|--------|---------------|----------------|
| BTC    | BTCINR        | BTCUSDT        |
| ETH    | ETHINR        | ETHUSDT        |
| XRP    | XRPINR        | XRPUSDT        |
| SOL    | SOLINR        | SOLUSDT        |
| ADA    | ADAINR        | ADAUSDT        |
| DOGE   | DOGEINR       | DOGEUSDT       |

## 🎯 Signal Types

### 🟢 BUY Signal
- **Condition**: INR price < USDT price (normalized)
- **Action**: Buy on CoinDCX (INR market)
- **Reason**: INR market is undervalued, will likely catch up

### 🔴 SELL Signal
- **Condition**: INR price > USDT price (normalized)
- **Action**: Sell on CoinDCX (INR market)
- **Reason**: INR market is overvalued, will likely correct down

## 📊 Output Format

```
🚀 [14:30:45] ARBITRAGE OPPORTUNITIES
================================================================================
🟢 BUY BTC
  INR Price: ₹10,300,000 (~$123,353)
  USD Price: $123,500
  Spread: -0.12% ⭐⭐⭐
  Strategy: BUY in INR market

🔴 SELL ETH
  INR Price: ₹255,000 (~$3,054)
  USD Price: $3,045
  Spread: +0.30% ⭐⭐
  Strategy: SELL in INR market
```

## ⚙️ Configuration Options

### Arbitrage Settings
- `min_spread_percent`: Minimum spread to consider (default: 0.5%)
- `max_spread_percent`: Maximum spread to avoid errors (default: 10.0%)
- `check_interval_seconds`: How often to check prices (default: 30s)

### Risk Management
- **Spread Validation**: Ignores spreads that are too large (likely data errors)
- **Volume Filtering**: Considers trading volume for confidence scoring
- **Rate Limiting**: Respects API limits to avoid blocks

## 📁 Data Storage

The system saves arbitrage opportunities to:
```
data/arbitrage/
├── arbitrage_opportunities_20250713_143045.json
├── arbitrage_opportunities_20250713_143115.json
└── ...
```

## 🔍 Analysis Tips

1. **Volume Matters**: Higher volume = more reliable opportunities
2. **Spread Persistence**: Look for spreads that persist across multiple checks
3. **Market Hours**: INR markets may have different activity patterns
4. **Fees**: Consider transaction fees when calculating profitability

## ⚠️ Important Notes

### Market Dynamics
- **INR follows USDT**: Indian markets generally follow global price trends
- **Lower volume**: INR markets have ~1800x less volume than USDT
- **Arbitrage window**: Price differences usually close within minutes

### Risks
- **Execution delays**: Time between signal and execution
- **Fee impact**: Trading fees can eat into small spreads
- **Market volatility**: Rapid price changes can invalidate signals
- **Regulatory**: Comply with local trading regulations

## 🚀 Getting Started

1. **Test first**: Run `test_arbitrage.py` to verify setup
2. **Check spreads**: Look for patterns in your market
3. **Paper trade**: Practice without real money
4. **Start small**: Begin with small position sizes
5. **Monitor closely**: Watch for execution timing

## 🔧 Customization

You can easily modify the system to:
- Add more trading pairs
- Use different exchanges
- Adjust spread thresholds
- Add email/SMS notifications
- Integrate with trading APIs

## 📞 Support

For questions or issues:
1. Check the logs in `data/logs/`
2. Review saved opportunities in `data/arbitrage/`
3. Test individual components with `test_arbitrage.py` 