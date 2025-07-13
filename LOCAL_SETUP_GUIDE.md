# 🚀 Local Hyperfrequent Arbitrage Setup Guide

This guide shows you how to set up hyperfrequent arbitrage monitoring on your local machine for maximum responsiveness and control.

## 🎯 Why Local Execution?

- **⚡ No delays**: Instant execution without GitHub Actions queue times
- **🔄 Hyperfrequent**: Check every few seconds (vs 10+ minutes on GitHub)
- **📊 Full control**: Customize intervals, logging, and behavior
- **💾 Local storage**: Direct access to opportunity data
- **🛡️ Reliability**: No dependency on external services

## 🖥️ Setup Instructions by OS

### 🪟 Windows Setup

#### Option 1: Quick Manual Start
```batch
# Double-click to run
start_arbitrage.bat
```

#### Option 2: Automated Task Scheduler (Recommended)
```powershell
# Run as Administrator for best results
.\setup_windows_task.ps1

# Custom interval (e.g., every 5 seconds)
.\setup_windows_task.ps1 -IntervalSeconds 5

# Remove the task
.\setup_windows_task.ps1 -Remove
```

#### Option 3: Direct Python Command
```powershell
# Run every 10 seconds (default)
python3 scripts\hyperfrequent_arbitrage.py

# Run every 5 seconds
python3 scripts\hyperfrequent_arbitrage.py 5

# Run every 30 seconds
python3 scripts\hyperfrequent_arbitrage.py 30
```

### 🐧 Linux/Mac Setup

#### Option 1: Direct Python Command
```bash
# Run every 10 seconds (default)
python3 scripts/hyperfrequent_arbitrage.py

# Run every 5 seconds
python3 scripts/hyperfrequent_arbitrage.py 5

# Run in background
nohup python3 scripts/hyperfrequent_arbitrage.py 10 &
```

#### Option 2: Systemd Service (Linux)
```bash
# Create service file
sudo nano /etc/systemd/system/crypred-arbitrage.service
```

Add this content:
```ini
[Unit]
Description=CRYPRED Hyperfrequent Arbitrage Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/CRYPRED
ExecStart=/usr/bin/python3 scripts/hyperfrequent_arbitrage.py 10
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable crypred-arbitrage
sudo systemctl start crypred-arbitrage

# Check status
sudo systemctl status crypred-arbitrage

# View logs
sudo journalctl -u crypred-arbitrage -f
```

#### Option 3: Screen Session (Linux/Mac)
```bash
# Start in detached screen session
screen -dmS arbitrage python3 scripts/hyperfrequent_arbitrage.py 10

# Attach to view
screen -r arbitrage

# Detach: Ctrl+A, then D
```

## ⚙️ Configuration Options

### Interval Settings
```bash
# Ultra-fast (every 5 seconds) - for high-frequency trading
python3 scripts/hyperfrequent_arbitrage.py 5

# Fast (every 10 seconds) - default, good balance
python3 scripts/hyperfrequent_arbitrage.py 10

# Moderate (every 30 seconds) - less resource intensive
python3 scripts/hyperfrequent_arbitrage.py 30

# Conservative (every 60 seconds) - minimal impact
python3 scripts/hyperfrequent_arbitrage.py 60
```

### Advanced Configuration
Edit `arbitrage_config.json`:
```json
{
  "arbitrage_settings": {
    "min_spread_percent": 0.3,    // Lower threshold for more opportunities
    "max_spread_percent": 15.0,   // Higher threshold for volatile markets
    "check_interval_seconds": 10   // Default interval
  }
}
```

## 📊 Monitoring and Logs

### Log Files
- **`arbitrage_runner.log`**: Detailed execution logs
- **`data/arbitrage/`**: Saved arbitrage opportunities
- **Console output**: Real-time opportunity alerts

### View Logs
```bash
# Windows
Get-Content arbitrage_runner.log -Tail 20 -Wait

# Linux/Mac  
tail -f arbitrage_runner.log
```

### Monitor Data
```bash
# Check saved opportunities
ls data/arbitrage/

# View latest opportunity
cat data/arbitrage/arbitrage_opportunities_*.json | tail -1
```

## 🔧 Management Commands

### Windows Task Scheduler
```powershell
# Start the task
Start-ScheduledTask -TaskName "CrypredArbitrage"

# Stop the task
Stop-ScheduledTask -TaskName "CrypredArbitrage"

# Check task status
Get-ScheduledTask -TaskName "CrypredArbitrage"

# Remove the task
.\setup_windows_task.ps1 -Remove
```

### Linux Systemd
```bash
# Start service
sudo systemctl start crypred-arbitrage

# Stop service
sudo systemctl stop crypred-arbitrage

# Restart service
sudo systemctl restart crypred-arbitrage

# Check status
sudo systemctl status crypred-arbitrage
```

### Manual Process Management
```bash
# Find running process
ps aux | grep hyperfrequent_arbitrage

# Kill by process ID
kill <PID>

# Kill by name (Linux/Mac)
pkill -f hyperfrequent_arbitrage
```

## 📈 Performance Tuning

### Recommended Intervals by Use Case

| Use Case | Interval | Pros | Cons |
|----------|----------|------|------|
| **High-Frequency Trading** | 5s | Maximum responsiveness | High CPU/network usage |
| **Active Monitoring** | 10s | Good balance | Moderate resource usage |
| **Passive Monitoring** | 30s | Low resource usage | May miss short opportunities |
| **Background Checking** | 60s | Minimal impact | Lowest opportunity capture |

### Resource Usage
- **5-second intervals**: ~720 API calls/hour
- **10-second intervals**: ~360 API calls/hour  
- **30-second intervals**: ~120 API calls/hour

### API Rate Limits
- **CoinDCX**: No explicit limit mentioned
- **Binance**: 1200 requests/minute
- **Exchange Rate API**: 1500 requests/month (free tier)

## 🚨 Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Windows: Install Python 3.x from python.org
# Add to PATH during installation

# Linux: Install Python 3
sudo apt update && sudo apt install python3 python3-pip

# Mac: Install via Homebrew
brew install python3
```

#### Dependencies Missing
```bash
pip install -r requirements.txt

# Or manually
pip install requests python-dateutil
```

#### Permission Errors (Windows)
```powershell
# Run PowerShell as Administrator
# Or modify execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Network Connectivity
```bash
# Test API connectivity
curl https://api.coindcx.com/exchange/ticker
curl https://api.binance.com/api/v3/ticker/24hr

# Check DNS resolution
nslookup api.coindcx.com
```

#### High CPU Usage
- Increase check interval (e.g., 30 seconds instead of 5)
- Reduce log verbosity in code
- Monitor system resources

### Performance Monitoring
```bash
# Check system resources
# Windows: Task Manager or Resource Monitor
# Linux: htop, top, or systemctl status
# Mac: Activity Monitor or top

# Monitor network usage
# Windows: Resource Monitor -> Network tab
# Linux: iftop, nethogs
# Mac: Activity Monitor -> Network tab
```

## 🔒 Security Considerations

### Best Practices
- **No API keys required**: Uses only public endpoints
- **Local execution**: No data leaves your machine
- **Rate limiting**: Built-in delays to respect API limits
- **Error handling**: Graceful degradation on failures

### Network Security
- Consider running behind VPN for additional privacy
- Monitor API usage to avoid rate limiting
- Use firewall to restrict unnecessary connections

## 🚀 Advanced Usage

### Multiple Intervals
```bash
# Run different instances for different strategies
python3 scripts/hyperfrequent_arbitrage.py 5 &   # Fast opportunities
python3 scripts/hyperfrequent_arbitrage.py 60 &  # Background monitoring
```

### Custom Notification
Add to your cron job or task:
```bash
# Email notifications on opportunities (Linux)
python3 scripts/hyperfrequent_arbitrage.py 10 | mail -s "Arbitrage Alert" your@email.com
```

### Data Analysis
```python
# Analyze collected opportunities
import json
import glob

files = glob.glob('data/arbitrage/*.json')
opportunities = []
for file in files:
    with open(file) as f:
        data = json.load(f)
        opportunities.extend(data['opportunities'])

# Find best opportunities
best = sorted(opportunities, key=lambda x: abs(x['spread_percent']), reverse=True)[:10]
```

## 📞 Support

### Getting Help
1. **Check logs**: `arbitrage_runner.log`
2. **Test connectivity**: `python3 scripts/test_arbitrage.py`
3. **Verify setup**: Run manual command first
4. **Resource monitoring**: Check CPU/memory usage

### Optimization Tips
1. **Start conservative**: Begin with 30-second intervals
2. **Monitor resources**: Watch CPU and network usage
3. **Adjust gradually**: Decrease interval as system allows
4. **Use logging**: Keep logs for pattern analysis
5. **Regular maintenance**: Clean old opportunity files

---

🎯 **Ready to start?** Run `start_arbitrage.bat` (Windows) or `python3 scripts/hyperfrequent_arbitrage.py` (all platforms) to begin hyperfrequent arbitrage monitoring! 