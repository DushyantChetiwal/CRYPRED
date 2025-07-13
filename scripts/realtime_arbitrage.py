#!/usr/bin/env python3
"""
Real-time Crypto Arbitrage System
Monitors price differences between INR and USD markets for arbitrage opportunities
"""

import requests
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
import concurrent.futures
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Price:
    """Price data structure"""
    symbol: str
    price: float
    exchange: str
    currency: str
    timestamp: datetime
    volume_24h: float = 0.0

@dataclass
class ArbitrageOpportunity:
    """Arbitrage opportunity data structure"""
    symbol: str
    inr_price: float
    usd_price: float
    inr_price_normalized: float  # INR price converted to USD
    spread_percent: float
    signal: str  # 'BUY' or 'SELL'
    timestamp: datetime
    confidence: float = 0.0

class RealTimeArbitrage:
    """Real-time arbitrage detection system"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ArbitrageBot/1.0',
            'Accept': 'application/json'
        })
        
        # Exchange URLs
        self.coindcx_url = "https://api.coindcx.com/exchange/ticker"
        self.binance_url = "https://api.binance.com/api/v3/ticker/24hr"
        self.usd_inr_url = "https://api.exchangerate-api.com/v4/latest/USD"
        
        # Target trading pairs
        self.target_pairs = {
            'BTC': {'coindcx': 'BTCINR', 'binance': 'BTCUSDT'},
            'ETH': {'coindcx': 'ETHINR', 'binance': 'ETHUSDT'},
            'XRP': {'coindcx': 'XRPINR', 'binance': 'XRPUSDT'},
            'SOL': {'coindcx': 'SOLINR', 'binance': 'SOLUSDT'},
            'ADA': {'coindcx': 'ADAINR', 'binance': 'ADAUSDT'},
            'DOGE': {'coindcx': 'DOGEINR', 'binance': 'DOGEUSDT'},
        }
        
        # Current prices and exchange rate
        self.current_prices = {}
        self.usd_inr_rate = 83.0  # Default fallback
        self.last_rate_update = None
        
        # Arbitrage settings
        self.min_spread_percent = 0.5  # Minimum 0.5% spread to consider
        self.max_spread_percent = 10.0  # Maximum 10% spread (likely data error)
        
        # Rate limiting
        self.last_coindcx_call = 0
        self.last_binance_call = 0
        self.call_interval = 1.0  # 1 second between calls
        
    def fetch_with_retry(self, url: str, params: Optional[Dict] = None, max_retries: int = 3) -> Optional[Dict]:
        """Fetch data with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5 ** attempt)
                else:
                    logger.error(f"Failed to fetch from {url} after {max_retries} attempts")
                    return None
    
    def get_usd_inr_rate(self) -> bool:
        """Fetch current USD/INR exchange rate"""
        try:
            # Update rate only if it's been more than 5 minutes
            if (self.last_rate_update is None or 
                (datetime.now() - self.last_rate_update).seconds > 300):
                
                data = self.fetch_with_retry(self.usd_inr_url)
                if data and 'rates' in data and 'INR' in data['rates']:
                    self.usd_inr_rate = float(data['rates']['INR'])
                    self.last_rate_update = datetime.now()
                    logger.info(f"Updated USD/INR rate: {self.usd_inr_rate:.2f}")
                    return True
            return True
        except Exception as e:
            logger.error(f"Error fetching USD/INR rate: {e}")
            return False
    
    def get_coindcx_prices(self) -> Dict[str, Price]:
        """Fetch current prices from CoinDCX"""
        now = time.time()
        if now - self.last_coindcx_call < self.call_interval:
            time.sleep(self.call_interval - (now - self.last_coindcx_call))
        
        try:
            data = self.fetch_with_retry(self.coindcx_url)
            if not data:
                return {}
            
            prices = {}
            timestamp = datetime.now(timezone.utc)
            
            for ticker in data:
                market = ticker.get('market', '')
                for symbol, pair_info in self.target_pairs.items():
                    if market == pair_info['coindcx']:
                        price = Price(
                            symbol=symbol,
                            price=float(ticker.get('last_price', 0)),
                            exchange='CoinDCX',
                            currency='INR',
                            timestamp=timestamp,
                            volume_24h=float(ticker.get('volume', 0))
                        )
                        prices[symbol] = price
                        break
            
            self.last_coindcx_call = time.time()
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching CoinDCX prices: {e}")
            return {}
    
    def get_binance_prices(self) -> Dict[str, Price]:
        """Fetch current prices from Binance"""
        now = time.time()
        if now - self.last_binance_call < self.call_interval:
            time.sleep(self.call_interval - (now - self.last_binance_call))
        
        try:
            data = self.fetch_with_retry(self.binance_url)
            if not data:
                return {}
            
            prices = {}
            timestamp = datetime.now(timezone.utc)
            
            for ticker in data:
                symbol_name = ticker.get('symbol', '')
                for symbol, pair_info in self.target_pairs.items():
                    if symbol_name == pair_info['binance']:
                        price = Price(
                            symbol=symbol,
                            price=float(ticker.get('lastPrice', 0)),
                            exchange='Binance',
                            currency='USDT',
                            timestamp=timestamp,
                            volume_24h=float(ticker.get('volume', 0))
                        )
                        prices[symbol] = price
                        break
            
            self.last_binance_call = time.time()
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching Binance prices: {e}")
            return {}
    
    def fetch_all_prices(self) -> Tuple[Dict[str, Price], Dict[str, Price]]:
        """Fetch prices from both exchanges concurrently"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_coindcx = executor.submit(self.get_coindcx_prices)
            future_binance = executor.submit(self.get_binance_prices)
            
            coindcx_prices = future_coindcx.result()
            binance_prices = future_binance.result()
            
            return coindcx_prices, binance_prices
    
    def calculate_arbitrage_opportunities(self, inr_prices: Dict[str, Price], 
                                        usd_prices: Dict[str, Price]) -> List[ArbitrageOpportunity]:
        """Calculate arbitrage opportunities between INR and USD prices"""
        opportunities = []
        
        for symbol in self.target_pairs.keys():
            if symbol not in inr_prices or symbol not in usd_prices:
                continue
                
            inr_price = inr_prices[symbol]
            usd_price = usd_prices[symbol]
            
            # Convert INR price to USD
            inr_price_usd = inr_price.price / self.usd_inr_rate
            
            # Calculate spread
            spread = (inr_price_usd - usd_price.price) / usd_price.price * 100
            
            # Skip if spread is too small or too large (likely error)
            if abs(spread) < self.min_spread_percent or abs(spread) > self.max_spread_percent:
                continue
            
            # Determine signal
            if spread > self.min_spread_percent:
                signal = 'SELL'  # INR price is higher, sell in INR market
            elif spread < -self.min_spread_percent:
                signal = 'BUY'   # INR price is lower, buy in INR market
            else:
                continue
            
            # Calculate confidence based on volume and spread size
            volume_factor = min(inr_price.volume_24h / 1000000, 1.0)  # Normalize volume
            spread_factor = min(abs(spread) / 5.0, 1.0)  # Normalize spread
            confidence = (volume_factor + spread_factor) / 2.0
            
            opportunity = ArbitrageOpportunity(
                symbol=symbol,
                inr_price=inr_price.price,
                usd_price=usd_price.price,
                inr_price_normalized=inr_price_usd,
                spread_percent=spread,
                signal=signal,
                timestamp=datetime.now(timezone.utc),
                confidence=confidence
            )
            
            opportunities.append(opportunity)
        
        return opportunities
    
    def print_opportunities(self, opportunities: List[ArbitrageOpportunity]):
        """Print arbitrage opportunities in a formatted way"""
        if not opportunities:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No arbitrage opportunities found")
            return
        
        print(f"\n🚀 [{datetime.now().strftime('%H:%M:%S')}] ARBITRAGE OPPORTUNITIES")
        print("=" * 80)
        
        for opp in sorted(opportunities, key=lambda x: abs(x.spread_percent), reverse=True):
            signal_emoji = "🟢 BUY" if opp.signal == 'BUY' else "🔴 SELL"
            confidence_stars = "⭐" * int(opp.confidence * 5)
            
            print(f"{signal_emoji} {opp.symbol}")
            print(f"  INR Price: ₹{opp.inr_price:,.2f} (~${opp.inr_price_normalized:.2f})")
            print(f"  USD Price: ${opp.usd_price:.2f}")
            print(f"  Spread: {opp.spread_percent:+.2f}% {confidence_stars}")
            print(f"  Strategy: {opp.signal} in INR market")
            print()
    
    def run_continuous_monitoring(self):
        """Run continuous arbitrage monitoring"""
        logger.info("🚀 Starting real-time arbitrage monitoring...")
        logger.info(f"Monitoring {len(self.target_pairs)} pairs for arbitrage opportunities")
        logger.info(f"Minimum spread: {self.min_spread_percent}%")
        
        while True:
            try:
                # Update USD/INR rate
                self.get_usd_inr_rate()
                
                # Fetch prices from both exchanges
                inr_prices, usd_prices = self.fetch_all_prices()
                
                # Calculate arbitrage opportunities
                opportunities = self.calculate_arbitrage_opportunities(inr_prices, usd_prices)
                
                # Display opportunities
                self.print_opportunities(opportunities)
                
                # Wait before next check
                time.sleep(30)  # Check every 30 seconds
                
            except KeyboardInterrupt:
                logger.info("Stopping arbitrage monitoring...")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Wait 5 seconds before retrying

def main():
    """Main function"""
    arbitrage = RealTimeArbitrage()
    arbitrage.run_continuous_monitoring()

if __name__ == "__main__":
    main() 