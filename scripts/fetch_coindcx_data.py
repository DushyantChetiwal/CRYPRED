#!/usr/bin/env python3
"""
CoinDCX Data Fetcher for Crypto Trading Bot
Fetches trade data from CoinDCX API for most traded coins
"""

import requests
import json
import pandas as pd
from datetime import datetime, timezone
import os
import logging
import time
from typing import Dict, List, Optional, Tuple
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CoinDCXDataFetcher:
    """Fetches and processes crypto trading data from CoinDCX API"""
    
    def __init__(self):
        self.base_url = "https://api.coindcx.com"
        self.public_url = "https://public.coindcx.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoBot/1.0',
            'Accept': 'application/json'
        })
        
        # Create data directories
        self.data_dir = "data"
        self.trades_dir = os.path.join(self.data_dir, "trades")
        self.tickers_dir = os.path.join(self.data_dir, "tickers")
        self.logs_dir = os.path.join(self.data_dir, "logs")
        
        for dir_path in [self.trades_dir, self.tickers_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def make_request(self, url: str, params: Optional[Dict] = None, max_retries: int = 3) -> Optional[Dict]:
        """Make HTTP request with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch data from {url} after {max_retries} attempts")
                    return None
    
    def get_ticker_data(self) -> Optional[List[Dict]]:
        """Fetch ticker data for all markets"""
        url = f"{self.base_url}/exchange/ticker"
        logger.info("Fetching ticker data...")
        return self.make_request(url)
    
    def get_market_details(self) -> Optional[List[Dict]]:
        """Fetch detailed market information"""
        url = f"{self.base_url}/exchange/v1/markets_details"
        logger.info("Fetching market details...")
        return self.make_request(url)
    
    def get_trade_history(self, pair: str, limit: int = 100) -> Optional[List[Dict]]:
        """Fetch trade history for a specific pair"""
        url = f"{self.public_url}/market_data/trade_history"
        params = {'pair': pair, 'limit': limit}
        logger.info(f"Fetching trade history for {pair}...")
        return self.make_request(url, params)
    
    def identify_top_coins(self, ticker_data: List[Dict], top_n: int = 20) -> List[Dict]:
        """Identify top N most traded coins by volume"""
        try:
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(ticker_data)
            
            # Convert volume to numeric and sort
            df['volume_numeric'] = pd.to_numeric(df['volume'], errors='coerce')
            df = df.dropna(subset=['volume_numeric'])
            
            # Sort by volume in descending order
            top_coins = df.nlargest(top_n, 'volume_numeric')
            
            logger.info(f"Identified top {len(top_coins)} coins by volume")
            return top_coins.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error identifying top coins: {e}")
            return []
    
    def get_market_pair_mapping(self, market_details: List[Dict]) -> Dict[str, str]:
        """Create mapping from market symbol to pair format"""
        mapping = {}
        for market in market_details:
            if 'symbol' in market and 'pair' in market:
                mapping[market['symbol']] = market['pair']
        return mapping
    
    def save_ticker_data(self, ticker_data: List[Dict], timestamp: str) -> None:
        """Save ticker data to JSON file"""
        filename = f"ticker_{timestamp}.json"
        filepath = os.path.join(self.tickers_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump({
                    'timestamp': timestamp,
                    'data': ticker_data
                }, f, indent=2)
            logger.info(f"Saved ticker data to {filepath}")
        except Exception as e:
            logger.error(f"Error saving ticker data: {e}")
    
    def save_trade_data(self, pair: str, trade_data: List[Dict], timestamp: str) -> None:
        """Save trade data for a specific pair"""
        safe_pair = pair.replace('/', '_').replace('-', '_')
        filename = f"trades_{safe_pair}_{timestamp}.json"
        filepath = os.path.join(self.trades_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump({
                    'pair': pair,
                    'timestamp': timestamp,
                    'trades': trade_data
                }, f, indent=2)
            logger.info(f"Saved trade data for {pair} to {filepath}")
        except Exception as e:
            logger.error(f"Error saving trade data for {pair}: {e}")
    
    def save_summary_data(self, summary: Dict, timestamp: str) -> None:
        """Save summary data with current snapshot"""
        filename = f"summary_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(summary, f, indent=2)
            logger.info(f"Saved summary data to {filepath}")
        except Exception as e:
            logger.error(f"Error saving summary data: {e}")
    
    def save_logs(self, timestamp: str) -> None:
        """Save logs to file"""
        log_filename = f"fetch_log_{timestamp}.txt"
        log_filepath = os.path.join(self.logs_dir, log_filename)
        
        # This is a placeholder for log saving - in production you'd capture actual logs
        with open(log_filepath, 'w') as f:
            f.write(f"Data fetch completed at {timestamp}\n")
    
    def run(self) -> None:
        """Main execution function"""
        start_time = time.time()
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        
        logger.info(f"Starting data fetch at {timestamp}")
        
        try:
            # Fetch ticker data
            ticker_data = self.get_ticker_data()
            if not ticker_data:
                logger.error("Failed to fetch ticker data")
                return
            
            # Fetch market details
            market_details = self.get_market_details()
            if not market_details:
                logger.error("Failed to fetch market details")
                return
            
            # Create pair mapping
            pair_mapping = self.get_market_pair_mapping(market_details)
            
            # Identify top coins
            top_coins = self.identify_top_coins(ticker_data, top_n=15)
            
            # Save ticker data
            self.save_ticker_data(ticker_data, timestamp)
            
            # Fetch trade data for top coins
            trade_data_summary = {}
            successful_fetches = 0
            
            for coin in top_coins:
                market_symbol = coin.get('market', '')
                pair = pair_mapping.get(market_symbol, market_symbol)
                
                if pair:
                    trade_data = self.get_trade_history(pair, limit=50)
                    if trade_data:
                        self.save_trade_data(pair, trade_data, timestamp)
                        trade_data_summary[pair] = {
                            'trades_count': len(trade_data),
                            'volume_24h': coin.get('volume', 0),
                            'last_price': coin.get('last_price', 0),
                            'change_24h': coin.get('change_24_hour', 0)
                        }
                        successful_fetches += 1
                    else:
                        logger.warning(f"No trade data available for {pair}")
                    
                    # Rate limiting - small delay between requests
                    time.sleep(0.1)
            
            # Create summary
            summary = {
                'timestamp': timestamp,
                'execution_time_seconds': round(time.time() - start_time, 2),
                'total_markets': len(ticker_data),
                'top_coins_analyzed': len(top_coins),
                'successful_fetches': successful_fetches,
                'trade_data': trade_data_summary
            }
            
            self.save_summary_data(summary, timestamp)
            self.save_logs(timestamp)
            
            logger.info(f"Data fetch completed successfully in {summary['execution_time_seconds']} seconds")
            logger.info(f"Processed {successful_fetches} pairs out of {len(top_coins)} top coins")
            
        except Exception as e:
            logger.error(f"Error in main execution: {e}")
            logger.error(traceback.format_exc())
            
            # Save error log
            error_log = {
                'timestamp': timestamp,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            error_filepath = os.path.join(self.logs_dir, f"error_{timestamp}.json")
            with open(error_filepath, 'w') as f:
                json.dump(error_log, f, indent=2)

def main():
    """Main function"""
    fetcher = CoinDCXDataFetcher()
    fetcher.run()

if __name__ == "__main__":
    main() 