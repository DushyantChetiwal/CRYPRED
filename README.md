# 🚀 CRYPRED - Real-Time Crypto Arbitrage System

A sophisticated real-time cryptocurrency arbitrage detection system that monitors price differences between Indian Rupee (INR) and US Dollar (USDT) markets to identify profitable trading opportunities.

## 🎯 What is CRYPRED?

CRYPRED is a real-time arbitrage detection system that:
- **Monitors multiple exchanges simultaneously** (CoinDCX INR vs Binance USDT)
- **Detects price discrepancies** between INR and USD markets
- **Generates actionable buy/sell signals** based on normalized price differences
- **Provides real-time alerts** for arbitrage opportunities
- **Tracks confidence levels** based on volume and spread persistence

## 🔥 Key Features

### 🎯 **Real-Time Arbitrage Detection**
- Monitors 6 major cryptocurrencies (BTC, ETH, XRP, SOL, ADA, DOGE)
- Checks prices every 30 seconds (configurable)
- Concurrent API calls for faster data fetching
- Automatic USD/INR rate conversion

### 📊 **Smart Signal Generation**
- **🟢 BUY Signal**: When INR price < USD price (undervalued)
- **🔴 SELL Signal**: When INR price > USD price (overvalued)
- Configurable spread thresholds (default: 0.5% minimum)
- Confidence scoring based on volume and spread size

### 🛡️ **Risk Management**
- Spread validation (ignores unrealistic spreads)
- Rate limiting to respect API limits
- Error handling with retry logic
- Volume-based confidence scoring

### 📈 **Data Persistence**
- Saves all arbitrage opportunities to JSON files
- Historical tracking for pattern analysis
- Real-time USD/INR rate updates
- Comprehensive logging

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/DushyantChetiwal/CRYPRED.git
cd CRYPRED
pip install -r requirements.txt
```

### 2. Test the System
```bash
python3 scripts/test_arbitrage.py
```

### 3. Run Continuous Monitoring
```bash
python3 scripts/realtime_arbitrage.py
```

## 📊 Example Output

```
🚀 [14:30:45] ARBITRAGE OPPORTUNITIES
================================================================================
🔴 SELL XRP
  INR Price: ₹242.02 (~$2.82)
  USD Price: $2.74
  Spread: +3.04% ⭐⭐⭐⭐
  Strategy: SELL in INR market

🟢 BUY BTC
  INR Price: ₹10,200,000 (~$122,500)
  USD Price: $123,500
  Spread: -0.81% ⭐⭐⭐
  Strategy: BUY in INR market
```

## 🔧 Configuration

### Basic Settings (`arbitrage_config.json`)
```json
{
  "arbitrage_settings": {
    "min_spread_percent": 0.5,
    "max_spread_percent": 10.0,
    "check_interval_seconds": 30
  }
}
```

### Monitored Trading Pairs
| Symbol | CoinDCX (INR) | Binance (USDT) |
|--------|---------------|----------------|
| BTC    | BTCINR        | BTCUSDT        |
| ETH    | ETHINR        | ETHUSDT        |
| XRP    | XRPINR        | XRPUSDT        |
| SOL    | SOLINR        | SOLUSDT        |
| ADA    | ADAINR        | ADAUSDT        |
| DOGE   | DOGEINR       | DOGEUSDT       |

## 🎯 How Arbitrage Works

### The Strategy
1. **Fetch Real-Time Prices**: Get current prices from CoinDCX (INR) and Binance (USDT)
2. **Normalize Currencies**: Convert INR prices to USD using live exchange rates
3. **Calculate Spreads**: Find percentage differences between normalized prices
4. **Generate Signals**: Identify buy/sell opportunities based on price discrepancies
5. **Execute Trades**: Act on signals within the arbitrage window

### Example Calculation
```
BTC Price on CoinDCX: ₹10,300,000
BTC Price on Binance: $123,500 USDT
USD/INR Rate: 83.50

Normalized INR Price: ₹10,300,000 ÷ 83.50 = $123,353
Spread: ($123,353 - $123,500) / $123,500 = -0.12%

Signal: 🟢 BUY (INR is cheaper, buy on CoinDCX)
```

## 📁 Project Structure

```
CRYPRED/
├── scripts/
│   ├── realtime_arbitrage.py    # Main arbitrage detection system
│   └── test_arbitrage.py        # Test script for quick checks
├── data/
│   └── arbitrage/              # Saved arbitrage opportunities
├── arbitrage_config.json       # Configuration settings
├── ARBITRAGE_README.md         # Detailed documentation
└── requirements.txt            # Python dependencies
```

## 🔍 Market Insights

### Why This Works
- **Market Inefficiency**: INR and USDT markets don't always sync perfectly
- **Volume Differences**: INR markets have ~1800x less volume than USDT
- **Arbitrage Windows**: Price differences usually close within minutes
- **Predictable Patterns**: INR markets generally follow global price trends

### Current Market Status
Based on live data analysis:
- INR markets often trade at 1-3% premium to global prices
- XRP typically shows the largest spreads
- Best opportunities occur during high volatility periods
- Average arbitrage window: 2-5 minutes

## ⚠️ Important Disclaimers

### Risks
- **Execution Speed**: Arbitrage opportunities close quickly
- **Trading Fees**: Transaction costs can eat into profits
- **Market Volatility**: Rapid price changes can invalidate signals
- **Regulatory Compliance**: Ensure compliance with local trading laws

### Best Practices
1. **Start Small**: Begin with small position sizes
2. **Monitor Closely**: Watch execution timing carefully
3. **Factor in Fees**: Include trading fees in profit calculations
4. **Stay Informed**: Keep up with market regulations
5. **Paper Trade First**: Practice without real money

## 🛠️ Advanced Usage

### Custom Monitoring
```python
from scripts.realtime_arbitrage import RealTimeArbitrage

# Create custom arbitrage instance
arbitrage = RealTimeArbitrage()
arbitrage.min_spread_percent = 1.0  # Higher threshold
arbitrage.run_continuous_monitoring()
```

### Data Analysis
```python
import json

# Load saved opportunities
with open('data/arbitrage/arbitrage_opportunities_20250713_143045.json') as f:
    data = json.load(f)
    
# Analyze patterns
opportunities = data['opportunities']
avg_spread = sum(abs(opp['spread_percent']) for opp in opportunities) / len(opportunities)
```

## 📈 Performance Tracking

The system automatically tracks:
- **Opportunity Frequency**: How often arbitrage opportunities occur
- **Spread Distribution**: Common spread ranges
- **Confidence Levels**: Quality of opportunities
- **Market Timing**: Best times for arbitrage

## 🔗 API Documentation

### CoinDCX API
- **Endpoint**: `https://api.coindcx.com/exchange/ticker`
- **Rate Limit**: 1 request per second
- **Documentation**: [CoinDCX API Docs](https://docs.coindcx.com/)

### Binance API
- **Endpoint**: `https://api.binance.com/api/v3/ticker/24hr`
- **Rate Limit**: 1 request per second
- **Documentation**: [Binance API Docs](https://binance-docs.github.io/apidocs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For questions or issues:
- **Documentation**: See `ARBITRAGE_README.md` for detailed usage
- **Test System**: Run `python3 scripts/test_arbitrage.py`
- **Check Logs**: Review files in `data/arbitrage/`
- **GitHub Issues**: Report bugs or request features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CoinDCX**: For providing robust Indian crypto market data
- **Binance**: For reliable global cryptocurrency pricing
- **Exchange Rate API**: For real-time USD/INR conversion rates

---

**⚡ Ready to start arbitrage trading? Run `python3 scripts/test_arbitrage.py` to see live opportunities!** 