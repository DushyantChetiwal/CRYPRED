#!/usr/bin/env python3
"""
CoinDCX Data Analysis Script
Analyzes collected crypto data and provides trading insights
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import glob
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class CryptoDataAnalyzer:
    """Analyzes crypto trading data for insights and signals"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.trades_dir = os.path.join(data_dir, "trades")
        self.tickers_dir = os.path.join(data_dir, "tickers")
        
    def load_latest_ticker_data(self) -> Optional[pd.DataFrame]:
        """Load the most recent ticker data"""
        try:
            ticker_files = glob.glob(os.path.join(self.tickers_dir, "ticker_*.json"))
            if not ticker_files:
                print("No ticker data files found")
                return None
            
            latest_file = max(ticker_files, key=os.path.getctime)
            print(f"Loading latest ticker data from: {latest_file}")
            
            with open(latest_file, 'r') as f:
                data = json.load(f)
            
            df = pd.DataFrame(data['data'])
            
            # Convert numeric columns
            numeric_cols = ['volume', 'last_price', 'high', 'low', 'bid', 'ask', 'change_24_hour']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
            
        except Exception as e:
            print(f"Error loading ticker data: {e}")
            return None
    
    def load_trade_history(self, pair: str, limit: int = 10) -> Optional[pd.DataFrame]:
        """Load trade history for a specific pair"""
        try:
            safe_pair = pair.replace('/', '_').replace('-', '_')
            pattern = os.path.join(self.trades_dir, f"trades_{safe_pair}_*.json")
            trade_files = glob.glob(pattern)
            
            if not trade_files:
                print(f"No trade files found for {pair}")
                return None
            
            # Get the most recent files
            recent_files = sorted(trade_files, key=os.path.getctime, reverse=True)[:limit]
            
            all_trades = []
            for file in recent_files:
                with open(file, 'r') as f:
                    data = json.load(f)
                    if 'trades' in data:
                        all_trades.extend(data['trades'])
            
            if not all_trades:
                return None
            
            df = pd.DataFrame(all_trades)
            df['timestamp'] = pd.to_datetime(df['T'], unit='ms')
            df['price'] = pd.to_numeric(df['p'], errors='coerce')
            df['quantity'] = pd.to_numeric(df['q'], errors='coerce')
            df['value'] = df['price'] * df['quantity']
            
            return df.sort_values('timestamp')
            
        except Exception as e:
            print(f"Error loading trade history for {pair}: {e}")
            return None
    
    def analyze_market_overview(self, df: pd.DataFrame) -> Dict:
        """Analyze overall market conditions"""
        if df is None or df.empty:
            return {}
        
        # Remove any rows with NaN values in key columns
        df_clean = df.dropna(subset=['volume', 'change_24_hour', 'last_price'])
        
        total_markets = len(df_clean)
        positive_change = (df_clean['change_24_hour'] > 0).sum()
        negative_change = (df_clean['change_24_hour'] < 0).sum()
        
        top_gainers = df_clean.nlargest(5, 'change_24_hour')[['market', 'change_24_hour', 'volume']]
        top_losers = df_clean.nsmallest(5, 'change_24_hour')[['market', 'change_24_hour', 'volume']]
        highest_volume = df_clean.nlargest(5, 'volume')[['market', 'volume', 'change_24_hour']]
        
        return {
            'total_markets': total_markets,
            'positive_markets': positive_change,
            'negative_markets': negative_change,
            'market_sentiment': 'Bullish' if positive_change > negative_change else 'Bearish',
            'top_gainers': top_gainers.to_dict('records'),
            'top_losers': top_losers.to_dict('records'),
            'highest_volume': highest_volume.to_dict('records'),
            'avg_change': df_clean['change_24_hour'].mean(),
            'total_volume': df_clean['volume'].sum()
        }
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for trade data"""
        if df is None or df.empty:
            return df
        
        # Sort by timestamp
        df = df.sort_values('timestamp').copy()
        
        # Calculate moving averages
        df['ma_5'] = df['price'].rolling(window=5).mean()
        df['ma_10'] = df['price'].rolling(window=10).mean()
        df['ma_20'] = df['price'].rolling(window=20).mean()
        
        # Calculate RSI
        df['rsi'] = self.calculate_rsi(df['price'])
        
        # Calculate VWAP
        df['vwap'] = (df['value'].cumsum() / df['quantity'].cumsum())
        
        # Volume-based indicators
        df['volume_ma'] = df['quantity'].rolling(window=10).mean()
        df['volume_ratio'] = df['quantity'] / df['volume_ma']
        
        return df
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI (Relative Strength Index)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def find_trading_opportunities(self, ticker_df: pd.DataFrame) -> List[Dict]:
        """Identify potential trading opportunities"""
        if ticker_df is None or ticker_df.empty:
            return []
        
        opportunities = []
        
        # Clean the data
        df_clean = ticker_df.dropna(subset=['volume', 'change_24_hour', 'last_price'])
        
        # High volume with positive momentum
        high_volume_threshold = df_clean['volume'].quantile(0.8)
        momentum_coins = df_clean[
            (df_clean['volume'] > high_volume_threshold) & 
            (df_clean['change_24_hour'] > 2)
        ]
        
        for _, coin in momentum_coins.iterrows():
            opportunities.append({
                'type': 'MOMENTUM',
                'pair': coin['market'],
                'reason': f'High volume ({coin["volume"]:.2f}) with positive momentum ({coin["change_24_hour"]:.2f}%)',
                'volume': coin['volume'],
                'change_24h': coin['change_24_hour'],
                'price': coin['last_price']
            })
        
        # Oversold conditions (potential bounce)
        oversold_coins = df_clean[df_clean['change_24_hour'] < -5]
        high_volume_oversold = oversold_coins[
            oversold_coins['volume'] > oversold_coins['volume'].median()
        ]
        
        for _, coin in high_volume_oversold.iterrows():
            opportunities.append({
                'type': 'OVERSOLD',
                'pair': coin['market'],
                'reason': f'Oversold condition ({coin["change_24_hour"]:.2f}%) with decent volume',
                'volume': coin['volume'],
                'change_24h': coin['change_24_hour'],
                'price': coin['last_price']
            })
        
        # Volume spikes
        volume_threshold = df_clean['volume'].quantile(0.95)
        volume_spikes = df_clean[df_clean['volume'] > volume_threshold]
        
        for _, coin in volume_spikes.iterrows():
            opportunities.append({
                'type': 'VOLUME_SPIKE',
                'pair': coin['market'],
                'reason': f'Unusual volume spike ({coin["volume"]:.2f})',
                'volume': coin['volume'],
                'change_24h': coin['change_24_hour'],
                'price': coin['last_price']
            })
        
        return opportunities
    
    def generate_report(self) -> str:
        """Generate a comprehensive analysis report"""
        report = []
        report.append("=" * 60)
        report.append("CRYPTO TRADING DATA ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Load and analyze ticker data
        ticker_df = self.load_latest_ticker_data()
        if ticker_df is not None:
            market_analysis = self.analyze_market_overview(ticker_df)
            
            report.append("📊 MARKET OVERVIEW")
            report.append("-" * 30)
            report.append(f"Total Markets: {market_analysis.get('total_markets', 0)}")
            report.append(f"Positive Markets: {market_analysis.get('positive_markets', 0)}")
            report.append(f"Negative Markets: {market_analysis.get('negative_markets', 0)}")
            report.append(f"Market Sentiment: {market_analysis.get('market_sentiment', 'Unknown')}")
            report.append(f"Average 24h Change: {market_analysis.get('avg_change', 0):.2f}%")
            report.append("")
            
            # Top gainers
            report.append("🚀 TOP GAINERS")
            report.append("-" * 30)
            for gainer in market_analysis.get('top_gainers', []):
                report.append(f"{gainer['market']}: +{gainer['change_24_hour']:.2f}% (Vol: {gainer['volume']:.2f})")
            report.append("")
            
            # Top losers
            report.append("📉 TOP LOSERS")
            report.append("-" * 30)
            for loser in market_analysis.get('top_losers', []):
                report.append(f"{loser['market']}: {loser['change_24_hour']:.2f}% (Vol: {loser['volume']:.2f})")
            report.append("")
            
            # Highest volume
            report.append("💹 HIGHEST VOLUME")
            report.append("-" * 30)
            for vol_coin in market_analysis.get('highest_volume', []):
                report.append(f"{vol_coin['market']}: {vol_coin['volume']:.2f} ({vol_coin['change_24_hour']:.2f}%)")
            report.append("")
            
            # Trading opportunities
            opportunities = self.find_trading_opportunities(ticker_df)
            if opportunities:
                report.append("🎯 TRADING OPPORTUNITIES")
                report.append("-" * 30)
                for opp in opportunities[:10]:  # Show top 10
                    report.append(f"{opp['type']}: {opp['pair']}")
                    report.append(f"  Reason: {opp['reason']}")
                    report.append(f"  Price: ${opp['price']}")
                    report.append("")
        
        return "\n".join(report)
    
    def analyze_specific_pair(self, pair: str) -> str:
        """Analyze a specific trading pair"""
        report = []
        report.append(f"DETAILED ANALYSIS FOR {pair}")
        report.append("=" * 50)
        
        # Load trade data
        trade_df = self.load_trade_history(pair, limit=20)
        if trade_df is not None and not trade_df.empty:
            # Calculate technical indicators
            trade_df = self.calculate_technical_indicators(trade_df)
            
            latest_price = trade_df['price'].iloc[-1]
            price_change = ((latest_price - trade_df['price'].iloc[0]) / trade_df['price'].iloc[0]) * 100
            
            report.append(f"Latest Price: ${latest_price:.6f}")
            report.append(f"Price Change: {price_change:.2f}%")
            report.append(f"Total Trades: {len(trade_df)}")
            report.append(f"Average Trade Size: {trade_df['quantity'].mean():.6f}")
            report.append(f"Total Volume: {trade_df['quantity'].sum():.6f}")
            
            if 'vwap' in trade_df.columns:
                latest_vwap = trade_df['vwap'].iloc[-1]
                report.append(f"VWAP: ${latest_vwap:.6f}")
                report.append(f"Price vs VWAP: {((latest_price - latest_vwap) / latest_vwap * 100):.2f}%")
            
            if 'rsi' in trade_df.columns and not trade_df['rsi'].isna().all():
                latest_rsi = trade_df['rsi'].iloc[-1]
                if not pd.isna(latest_rsi):
                    report.append(f"RSI: {latest_rsi:.2f}")
                    if latest_rsi > 70:
                        report.append("  Signal: OVERBOUGHT")
                    elif latest_rsi < 30:
                        report.append("  Signal: OVERSOLD")
                    else:
                        report.append("  Signal: NEUTRAL")
        else:
            report.append("No trade data available for this pair")
        
        return "\n".join(report)

def main():
    """Main function"""
    analyzer = CryptoDataAnalyzer()
    
    # Generate main report
    print("Generating crypto trading analysis report...")
    report = analyzer.generate_report()
    print(report)
    
    # Save report to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f"analysis_report_{timestamp}.txt"
    with open(report_filename, 'w') as f:
        f.write(report)
    print(f"\nReport saved to: {report_filename}")
    
    # Analyze specific pairs if available
    print("\nAnalyzing specific pairs...")
    popular_pairs = ['B-BTC_USDT', 'B-ETH_USDT', 'B-BNB_USDT']
    
    for pair in popular_pairs:
        pair_analysis = analyzer.analyze_specific_pair(pair)
        print(f"\n{pair_analysis}")

if __name__ == "__main__":
    main() 