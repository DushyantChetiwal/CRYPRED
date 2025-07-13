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
- **Hyperfrequent checking**: Every 5-60 seconds (configurable)
- Concurrent API calls for faster data fetching
- Automatic USD/INR rate conversion

### 📊 **Smart Signal Generation**
- **🟢 BUY Signal**: When INR price < USD price (undervalued)
- **🔴 SELL Signal**: When INR price > USD price (overvalued)
- Configurable spread thresholds (default: 0.5% minimum)
- Confidence scoring based on volume and spread size

### 🖥️ **Professional GUI Interface**
- **Real-time interactive charts** with navigable price graphs
- **Visual arbitrage detection** with color-coded buy/sell zones
- **Historical data navigation** from session start with scroll controls
- **Multi-cryptocurrency monitoring** with instant pair switching
- **Professional visualization** with matplotlib-powered charts

### 🛡️ **Local Execution Benefits**
- **⚡ No delays**: Instant execution without cloud queue times
- **🔄 Hyperfrequent**: Check every few seconds for maximum responsiveness
- **📊 Full control**: Customize intervals, logging, and behavior
- **💾 Local storage**: Direct access to opportunity data

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

### 2. Choose Your Interface

#### 🖥️ **GUI Mode (Recommended for Visualization)**
```batch
# Windows - Double-click to run
start_gui.bat

# Or direct command (all platforms)
python3 scripts/arbitrage_gui.py
```

#### ⚡ **Command Line Mode (For Background Monitoring)**
```bash
# Quick test
python3 scripts/test_arbitrage.py

# Hyperfrequent monitoring
python3 scripts/hyperfrequent_arbitrage.py
```

### 3. Start Monitoring

#### 🪟 Windows Automation
```batch
# Set up automatic Windows Task
.\setup_windows_task.ps1

# Manual start with prompts
start_arbitrage.bat
```

#### 🐧 Linux/Mac/Windows (Direct)
```bash
# Default: every 10 seconds
python3 scripts/hyperfrequent_arbitrage.py

# High-frequency: every 5 seconds
python3 scripts/hyperfrequent_arbitrage.py 5

# Background mode (Linux/Mac)
nohup python3 scripts/hyperfrequent_arbitrage.py 10 &
```

## 📊 GUI Interface Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                CRYPRED - Real-Time Arbitrage Monitor             │
├─────────────────────────────────────────────────────────────────┤
│ Controls: [Start] [Stop] | Select Pair: [BTC ▼] | Status: Ready │
├─────────────────────────────────────────────────────────────────┤
│  📈 Price Comparison Chart (INR vs USD)                         │
│     ● Blue Line: INR Price (normalized to USD)                  │
│     ● Red Line: USD Price (Binance)                             │
├─────────────────────────────────────────────────────────────────┤
│  📊 Spread Analysis Chart                                       │
│     🟢 Green Zone: BUY opportunities | 🔴 Red Zone: SELL        │
├─────────────────────────────────────────────────────────────────┤
│ Navigation: [◄◄] [◄] [►] [►►] | Current: Spread +2.3% SELL    │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Example Output

### Command Line Mode
```
🚀 [14:30:45] ARBITRAGE OPPORTUNITIES
================================================================================
🔴 SELL XRP
  INR Price: ₹242.02 (~$2.82)
  USD Price: $2.74
  Spread: +3.04% ⭐⭐⭐⭐
  Strategy: SELL in INR market

📊 ARBITRAGE RUNNER STATS
⏱️  Uptime: 0:05:23
🔄 Total Checks: 32
🎯 Opportunities Found: 18
📈 Success Rate: 56.3%
```

### GUI Mode
- **Interactive real-time charts** showing price movements
- **Visual indicators** for buy/sell opportunities
- **Historical navigation** to review past arbitrage opportunities
- **Color-coded zones** for immediate opportunity identification

## ⚙️ Configuration

### Interval Settings
| Interval | Use Case | API Calls/Hour | Resource Usage |
|----------|----------|----------------|----------------|
| **5s** | High-frequency trading | ~720 | High |
| **10s** | Active monitoring | ~360 | Moderate |
| **30s** | Passive monitoring | ~120 | Low |
| **60s** | Background checking | ~60 | Minimal |

### Advanced Settings (`arbitrage_config.json`)
```json
{
  "arbitrage_settings": {
    "min_spread_percent": 0.5,
    "max_spread_percent": 10.0,
    "check_interval_seconds": 10
  }
}
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
│   ├── realtime_arbitrage.py       # Core arbitrage detection system
│   ├── hyperfrequent_arbitrage.py  # Local hyperfrequent runner
│   ├── arbitrage_gui.py            # Professional GUI interface
│   └── test_arbitrage.py           # Test script for quick checks
├── data/
│   └── arbitrage/                 # Saved arbitrage opportunities
├── archive/                       # Archived old files
├── start_arbitrage.bat           # Windows quick start (command line)
├── start_gui.bat                 # Windows GUI launcher
├── setup_windows_task.ps1        # Windows Task Scheduler setup
├── LOCAL_SETUP_GUIDE.md          # Detailed setup instructions
├── GUI_GUIDE.md                  # Comprehensive GUI guide
├── arbitrage_config.json         # Configuration settings
└── requirements.txt              # Python dependencies
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

### Multiple Monitoring
```bash
# Run different instances for different strategies
python3 scripts/hyperfrequent_arbitrage.py 5 &   # Fast opportunities
python3 scripts/hyperfrequent_arbitrage.py 60 &  # Background monitoring

# GUI + Command line combination
python3 scripts/arbitrage_gui.py &               # Visual monitoring
python3 scripts/hyperfrequent_arbitrage.py 30 &  # Background logging
```

### Data Analysis
```python
import json
import glob

# Load and analyze saved opportunities
files = glob.glob('data/arbitrage/*.json')
opportunities = []
for file in files:
    with open(file) as f:
        data = json.load(f)
        opportunities.extend(data['opportunities'])

# Find best opportunities
best = sorted(opportunities, key=lambda x: abs(x['spread_percent']), reverse=True)[:10]
```

## 📈 Performance Tracking

The system automatically tracks:
- **Opportunity Frequency**: How often arbitrage opportunities occur
- **Spread Distribution**: Common spread ranges
- **Confidence Levels**: Quality of opportunities
- **Success Rates**: Percentage of checks finding opportunities

## 🔗 API Documentation

### CoinDCX API
- **Endpoint**: `https://api.coindcx.com/exchange/ticker`
- **Rate Limit**: No explicit limit mentioned
- **Documentation**: [CoinDCX API Docs](https://docs.coindcx.com/)

### Binance API
- **Endpoint**: `https://api.binance.com/api/v3/ticker/24hr`
- **Rate Limit**: 1200 requests/minute
- **Documentation**: [Binance API Docs](https://binance-docs.github.io/apidocs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For questions or issues:
- **Quick Setup**: See `LOCAL_SETUP_GUIDE.md` for detailed instructions
- **GUI Usage**: See `GUI_GUIDE.md` for comprehensive GUI documentation
- **Test System**: Run `python3 scripts/test_arbitrage.py`
- **Check Logs**: Review `arbitrage_runner.log`
- **Monitor Data**: Check files in `data/arbitrage/`
- **GitHub Issues**: Report bugs or request features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CoinDCX**: For providing robust Indian crypto market data
- **Binance**: For reliable global cryptocurrency pricing
- **Exchange Rate API**: For real-time USD/INR conversion rates

---

**⚡ Ready to start hyperfrequent arbitrage?** 

🖥️ **For Visual Monitoring**: Run `start_gui.bat` to launch the professional GUI interface  
⚡ **For Background Monitoring**: Run `start_arbitrage.bat` or `python3 scripts/hyperfrequent_arbitrage.py`

Start monitoring real-time crypto arbitrage opportunities with your preferred interface! 