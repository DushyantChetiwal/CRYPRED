#!/usr/bin/env python3
"""
Hyperfrequent Local Arbitrage Runner
Runs arbitrage detection every few seconds locally for maximum responsiveness
"""

import time
import sys
import os
import signal
import threading
from datetime import datetime, timezone
import logging
from realtime_arbitrage import RealTimeArbitrage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arbitrage_runner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HyperfrequentArbitrage:
    """Hyperfrequent arbitrage runner for local execution"""
    
    def __init__(self, check_interval=10):
        """
        Initialize hyperfrequent arbitrage runner
        
        Args:
            check_interval (int): Seconds between checks (default: 10)
        """
        self.check_interval = check_interval
        self.arbitrage = RealTimeArbitrage()
        self.running = True
        self.stats = {
            'total_checks': 0,
            'opportunities_found': 0,
            'last_opportunity': None,
            'start_time': datetime.now()
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def print_stats(self):
        """Print current statistics"""
        uptime = datetime.now() - self.stats['start_time']
        avg_interval = uptime.total_seconds() / max(self.stats['total_checks'], 1)
        
        print(f"\n📊 ARBITRAGE RUNNER STATS")
        print(f"⏱️  Uptime: {uptime}")
        print(f"🔄 Total Checks: {self.stats['total_checks']}")
        print(f"🎯 Opportunities Found: {self.stats['opportunities_found']}")
        print(f"📈 Success Rate: {(self.stats['opportunities_found']/max(self.stats['total_checks'],1)*100):.1f}%")
        print(f"⚡ Avg Check Interval: {avg_interval:.1f}s")
        if self.stats['last_opportunity']:
            print(f"🕐 Last Opportunity: {self.stats['last_opportunity']}")
        print("=" * 50)
    
    def run_single_check(self):
        """Run a single arbitrage check"""
        try:
            start_time = time.time()
            
            # Update USD/INR rate (every 5 minutes)
            self.arbitrage.get_usd_inr_rate()
            
            # Fetch prices from both exchanges
            inr_prices, usd_prices = self.arbitrage.fetch_all_prices()
            
            # Calculate arbitrage opportunities
            opportunities = self.arbitrage.calculate_arbitrage_opportunities(inr_prices, usd_prices)
            
            # Update stats
            self.stats['total_checks'] += 1
            if opportunities:
                self.stats['opportunities_found'] += 1
                self.stats['last_opportunity'] = datetime.now().strftime('%H:%M:%S')
            
            # Display opportunities
            if opportunities:
                self.arbitrage.print_opportunities(opportunities)
                
                # Save to file
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                import json
                os.makedirs('data/arbitrage', exist_ok=True)
                
                opportunities_data = []
                for opp in opportunities:
                    opportunities_data.append({
                        'symbol': opp.symbol,
                        'inr_price': opp.inr_price,
                        'usd_price': opp.usd_price,
                        'inr_price_normalized': opp.inr_price_normalized,
                        'spread_percent': opp.spread_percent,
                        'signal': opp.signal,
                        'timestamp': opp.timestamp.isoformat(),
                        'confidence': opp.confidence
                    })
                
                filepath = f"data/arbitrage/arbitrage_opportunities_{timestamp}.json"
                with open(filepath, 'w') as f:
                    json.dump({
                        'usd_inr_rate': self.arbitrage.usd_inr_rate,
                        'opportunities': opportunities_data
                    }, f, indent=2)
                
                logger.info(f"💾 Saved {len(opportunities)} opportunities to {filepath}")
            else:
                # Just log no opportunities found
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"[{current_time}] No arbitrage opportunities found (check #{self.stats['total_checks']})")
            
            execution_time = time.time() - start_time
            logger.debug(f"Check completed in {execution_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error in arbitrage check: {e}")
    
    def run_continuous(self):
        """Run continuous arbitrage monitoring"""
        logger.info(f"🚀 Starting hyperfrequent arbitrage runner...")
        logger.info(f"⏰ Check interval: {self.check_interval} seconds")
        logger.info(f"🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            while self.running:
                self.run_single_check()
                
                # Print stats every 20 checks
                if self.stats['total_checks'] % 20 == 0:
                    self.print_stats()
                
                # Wait for next check
                if self.running:  # Check again in case we got a signal
                    time.sleep(self.check_interval)
                    
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Cleanup and shutdown"""
        self.running = False
        self.print_stats()
        
        logger.info("📊 Final Summary:")
        logger.info(f"Total runtime: {datetime.now() - self.stats['start_time']}")
        logger.info(f"Total opportunities found: {self.stats['opportunities_found']}")
        logger.info("🛑 Arbitrage runner stopped")

def main():
    """Main function"""
    # Default to 10 seconds, but allow command line override
    interval = 10
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
            if interval < 1:
                print("⚠️  Interval must be at least 1 second")
                sys.exit(1)
        except ValueError:
            print("⚠️  Invalid interval specified")
            sys.exit(1)
    
    print(f"🚀 Starting hyperfrequent arbitrage with {interval}s intervals")
    print("💡 Usage: python hyperfrequent_arbitrage.py [interval_seconds]")
    print("🛑 Press Ctrl+C to stop gracefully")
    
    runner = HyperfrequentArbitrage(check_interval=interval)
    runner.run_continuous()

if __name__ == "__main__":
    main() 