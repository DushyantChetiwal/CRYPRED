# 🖥️ CRYPRED Arbitrage GUI Guide

A comprehensive real-time graphical interface for monitoring cryptocurrency arbitrage opportunities with interactive charts and historical data navigation.

## 🎯 What is the Arbitrage GUI?

The CRYPRED Arbitrage GUI is a powerful desktop application that provides:
- **Real-time price charts** showing INR vs USD rates for cryptocurrencies
- **Interactive navigation** to scroll through historical data from session start
- **Live arbitrage detection** with visual indicators for buy/sell opportunities
- **Multi-cryptocurrency monitoring** with easy pair switching
- **Professional charts** with color-coded zones and signals

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install matplotlib pandas
```

### 2. Launch the GUI

#### 🪟 Windows (Easy)
```batch
# Double-click to run
start_gui.bat
```

#### 🐧 Linux/Mac/Windows (Direct)
```bash
python3 scripts/arbitrage_gui.py
```

## 📊 GUI Overview

### Main Interface Components

```
┌─────────────────────────────────────────────────────────────────┐
│                CRYPRED - Real-Time Arbitrage Monitor             │
├─────────────────────────────────────────────────────────────────┤
│ Controls: [Start] [Stop] | Select Pair: [BTC ▼] | Status: Ready │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📈 BTC Price Comparison Chart                                  │
│     ● Blue Line: INR Price (normalized to USD)                  │
│     ● Red Line: USD Price (Binance)                             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 BTC Spread Analysis Chart                                   │
│     ● Green Zone: BUY opportunities (INR < USD)                 │
│     ● Red Zone: SELL opportunities (INR > USD)                  │
│     ● Colored dots: Signal indicators                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Navigation: [◄◄] [◄] [►] [►►] | View Window: [100]             │
├─────────────────────────────────────────────────────────────────┤
│ Current Info: INR: $123,456 | USD: $123,500 | Spread: -0.04%   │
│              Signal: BUY     | Opportunities: 3 | Uptime: 5:23  │
└─────────────────────────────────────────────────────────────────┘
```

## 🎛️ Control Panel Features

### Start/Stop Monitoring
- **Start Monitoring**: Begin real-time data collection and chart updates
- **Stop Monitoring**: Pause data collection (historical data remains viewable)
- **Status Indicator**: Shows current monitoring state (Running/Stopped)

### Cryptocurrency Pair Selection
- **Dropdown menu** with 6 supported pairs:
  - BTC (Bitcoin)
  - ETH (Ethereum)
  - XRP (Ripple)
  - SOL (Solana)
  - ADA (Cardano)
  - DOGE (Dogecoin)
- **Instant switching** between pairs without losing data
- **Independent history** for each cryptocurrency pair

## 📈 Chart Features

### Price Comparison Chart (Top)
- **Blue Line**: INR price (normalized to USD using live exchange rates)
- **Red Line**: USD price from Binance
- **Real-time updates**: New data points every 10 seconds
- **Auto-scaling**: Y-axis adjusts to price ranges automatically
- **Grid lines**: Easy to read price levels

### Spread Analysis Chart (Bottom)
- **Black Line**: Percentage spread between INR and USD prices
- **Color-coded zones**:
  - 🟢 **Green Zone** (below -0.5%): BUY opportunities
  - 🔴 **Red Zone** (above +0.5%): SELL opportunities
  - ⚪ **Neutral Zone** (-0.5% to +0.5%): No clear signal
- **Signal dots**: Colored points showing buy/sell/hold signals
- **Reference lines**: 0%, +0.5%, -0.5% thresholds

## 🧭 Navigation Controls

### Scroll Controls
| Button | Function | Description |
|--------|----------|-------------|
| **◄◄** | Jump to Start | Go to beginning of recorded data |
| **◄** | Scroll Left | Move back 10 data points |
| **►** | Scroll Right | Move forward 10 data points |
| **►►** | Jump to End | Go to latest data (auto-follow mode) |

### View Window Settings
- **View Window**: Controls how many data points to show (50-500)
- **Default**: 100 data points (~17 minutes at 10-second intervals)
- **Adjustable**: Use spinbox to change window size
- **Auto-scroll**: When at the end, automatically follows new data

## 📊 Information Panel

### Current Price Display
- **INR Price**: Latest normalized INR price in USD
- **USD Price**: Latest Binance price in USD
- **Live updates**: Refreshes every 10 seconds

### Arbitrage Analysis
- **Spread**: Current percentage difference between markets
- **Signal**: Current trading recommendation (BUY/SELL/HOLD)
- **Color coding**: Green for BUY, Red for SELL, Black for HOLD

### Session Statistics
- **Opportunities**: Number of arbitrage opportunities found in current session
- **Uptime**: How long the monitoring session has been running
- **Running totals**: Accumulates throughout the session

## 🎨 Visual Indicators

### Chart Color System
| Color | Meaning | Usage |
|-------|---------|-------|
| 🔵 **Blue** | INR prices | Price comparison chart line |
| 🔴 **Red** | USD prices | Price comparison chart line |
| 🟢 **Green** | BUY signals | Spread chart zones and dots |
| 🔴 **Red** | SELL signals | Spread chart zones and dots |
| ⚫ **Black** | Spread line | Main spread trend line |
| ⚪ **Gray** | HOLD signals | Neutral signal indicators |

### Status Indicators
- **🟢 Green Status**: System running, collecting data
- **🔴 Red Status**: System stopped, viewing mode only
- **Signal Colors**: Match chart color scheme for consistency

## ⚙️ Advanced Features

### Data Storage
- **In-memory history**: Stores up to 1000 data points per cryptocurrency
- **Session persistence**: Data remains available until application restart
- **Multi-pair tracking**: Independent history for each cryptocurrency
- **Real-time updates**: Continuously updates while monitoring

### Performance Optimization
- **Efficient rendering**: Only redraws visible data points
- **Smooth animations**: 1-second update intervals for responsiveness
- **Memory management**: Automatic cleanup of old data points
- **Thread safety**: Background data collection doesn't block GUI

### Customization Options
- **Window sizing**: Adjust view window size (50-500 points)
- **Pair switching**: Instant switching between cryptocurrencies
- **Navigation freedom**: Jump anywhere in the recorded timeline
- **Auto-follow mode**: Automatically track latest data

## 📖 How to Use

### Basic Workflow
1. **Launch the GUI** using `start_gui.bat` or direct Python command
2. **Select cryptocurrency pair** from dropdown menu
3. **Click "Start Monitoring"** to begin data collection
4. **Watch real-time charts** update every 10 seconds
5. **Navigate history** using scroll controls when needed
6. **Switch pairs** to monitor different cryptocurrencies
7. **Stop monitoring** when finished or for review mode

### Reading the Charts

#### Identifying Arbitrage Opportunities
1. **Check spread chart**: Look for points in green or red zones
2. **Confirm with price chart**: Verify price difference visually
3. **Check signal dots**: Green = BUY, Red = SELL opportunities
4. **Monitor trend**: Watch for persistent spreads vs momentary spikes

#### Understanding Price Movements
1. **Price convergence**: When blue and red lines are close together
2. **Price divergence**: When lines separate, creating arbitrage opportunities
3. **Trend analysis**: Use navigation to see longer-term patterns
4. **Market timing**: Observe how quickly spreads typically close

### Best Practices

#### For Active Trading
- **Monitor multiple pairs**: Switch between different cryptocurrencies
- **Watch for persistence**: Look for spreads that last multiple data points
- **Use navigation**: Check recent history for pattern recognition
- **Real-time focus**: Keep view at latest data (►►) for immediate opportunities

#### For Analysis
- **Historical review**: Use navigation to study past opportunities
- **Pattern recognition**: Look for recurring arbitrage patterns
- **Window adjustment**: Increase view window for longer-term trends
- **Multi-session**: Run monitoring sessions to build historical data

## 🔧 Troubleshooting

### Common Issues

#### GUI Won't Start
```bash
# Check dependencies
python3 -c "import matplotlib, pandas"

# Install if missing
pip install matplotlib pandas

# Try direct launch
python3 scripts/arbitrage_gui.py
```

#### No Data Appearing
1. **Check internet connection**: API calls need network access
2. **Verify monitoring status**: Ensure "Start Monitoring" was clicked
3. **Wait for first update**: Initial data appears after ~10 seconds
4. **Check console**: Look for error messages in terminal

#### Charts Not Updating
1. **Confirm monitoring is running**: Green status indicator
2. **Check if paused**: Stop and restart monitoring
3. **Verify API access**: Test basic arbitrage script first
4. **Restart application**: Close and reopen GUI

#### Navigation Issues
1. **No data to navigate**: Start monitoring first to collect data
2. **Stuck at one view**: Use ►► to return to latest data
3. **Window too small**: Increase view window size
4. **Missing history**: Data is only stored during current session

### Performance Tips

#### For Smooth Operation
- **Close other applications**: Free up system resources
- **Use default window size**: 100 points is optimal for most systems
- **Avoid rapid pair switching**: Allow charts to stabilize
- **Monitor system resources**: Watch CPU and memory usage

#### For Better Visualization
- **Maximize window**: Use full screen for better chart readability
- **Adjust view window**: Find optimal balance for your analysis needs
- **Use navigation wisely**: Don't over-scroll during active monitoring
- **Keep sessions reasonable**: Restart for very long monitoring sessions

## 📊 Understanding the Data

### Data Collection
- **Frequency**: Every 10 seconds during monitoring
- **Sources**: CoinDCX (INR prices) and Binance (USD prices)
- **Normalization**: INR prices converted to USD using live exchange rates
- **Storage**: In-memory for current session only

### Chart Interpretation
- **Price movements**: Reflect real market changes
- **Spread calculations**: (INR_normalized - USD_price) / USD_price × 100
- **Signal generation**: Based on configurable thresholds (±0.5%)
- **Historical context**: Shows progression of opportunities over time

### Arbitrage Logic
- **BUY Signal**: INR price < USD price (buy cheap in INR market)
- **SELL Signal**: INR price > USD price (sell high in INR market)
- **HOLD Signal**: Prices too close for profitable arbitrage
- **Threshold**: 0.5% minimum spread to account for fees

## 💡 Pro Tips

### Effective Monitoring
1. **Start with BTC**: Usually has the most stable data
2. **Check multiple pairs**: Different cryptocurrencies show different patterns
3. **Use view window effectively**: 100 points ≈ 17 minutes of history
4. **Watch for trends**: Persistent spreads are more reliable than spikes

### Pattern Recognition
1. **Time-based patterns**: Some arbitrage opportunities occur at specific times
2. **Volatility correlation**: High market volatility often creates more opportunities
3. **Spread persistence**: Look for opportunities that last multiple data points
4. **Cross-pair analysis**: Switch between pairs to find the best opportunities

### Technical Analysis
1. **Support/resistance**: Use navigation to identify key price levels
2. **Trend analysis**: Longer view windows help identify market trends
3. **Volatility assessment**: Frequent spread changes indicate high volatility
4. **Timing entries**: Use real-time view for optimal entry/exit timing

---

🎯 **Ready to start?** Launch the GUI with `start_gui.bat` and begin monitoring real-time arbitrage opportunities with professional-grade charts and analysis tools! 