#!/usr/bin/env python3
"""
Test script for the arbitrage system
Performs a single check instead of continuous monitoring
"""

import json
import os
from datetime import datetime
from realtime_arbitrage import RealTimeArbitrage

def test_arbitrage():
    """Test the arbitrage system with a single check"""
    print("🔍 Testing Arbitrage System")
    print("=" * 50)
    
    # Create arbitrage instance
    arbitrage = RealTimeArbitrage()
    
    # Update USD/INR rate
    print("📊 Fetching USD/INR exchange rate...")
    success = arbitrage.get_usd_inr_rate()
    if success:
        print(f"✅ USD/INR Rate: {arbitrage.usd_inr_rate:.2f}")
    else:
        print("❌ Failed to fetch USD/INR rate, using default")
    
    # Fetch prices from both exchanges
    print("\n💰 Fetching prices from exchanges...")
    inr_prices, usd_prices = arbitrage.fetch_all_prices()
    
    print(f"✅ CoinDCX (INR): {len(inr_prices)} prices fetched")
    print(f"✅ Binance (USDT): {len(usd_prices)} prices fetched")
    
    # Show current prices
    print("\n📋 Current Prices:")
    for symbol in arbitrage.target_pairs.keys():
        inr_price = inr_prices.get(symbol)
        usd_price = usd_prices.get(symbol)
        
        if inr_price and usd_price:
            inr_usd = inr_price.price / arbitrage.usd_inr_rate
            print(f"{symbol}: INR ₹{inr_price.price:,.2f} (~${inr_usd:.2f}) | USD ${usd_price.price:.2f}")
        else:
            print(f"{symbol}: ❌ Price data missing")
    
    # Calculate arbitrage opportunities
    print("\n🎯 Calculating arbitrage opportunities...")
    opportunities = arbitrage.calculate_arbitrage_opportunities(inr_prices, usd_prices)
    
    # Display opportunities
    arbitrage.print_opportunities(opportunities)
    
    # Save opportunities to file
    if opportunities:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"arbitrage_opportunities_{timestamp}.json"
        
        # Convert to serializable format
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
        
        # Save to file
        os.makedirs('data/arbitrage', exist_ok=True)
        filepath = os.path.join('data/arbitrage', filename)
        with open(filepath, 'w') as f:
            json.dump({
                'usd_inr_rate': arbitrage.usd_inr_rate,
                'opportunities': opportunities_data
            }, f, indent=2)
        
        print(f"💾 Opportunities saved to: {filepath}")
    
    print("\n✅ Arbitrage test completed!")

if __name__ == "__main__":
    test_arbitrage() 