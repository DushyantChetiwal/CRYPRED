#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify the CoinDCX data fetcher setup
"""

import sys
import os
import requests
import json
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import pandas as pd
        import numpy as np
        import requests
        from datetime import datetime
        print("[SUCCESS] All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def test_api_connectivity():
    """Test connectivity to CoinDCX API"""
    try:
        # Test ticker endpoint
        response = requests.get("https://api.coindcx.com/exchange/ticker", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] API connectivity test passed ({len(data)} markets available)")
            return True
        else:
            print(f"[ERROR] API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] API connectivity test failed: {e}")
        return False

def test_data_fetcher():
    """Test the data fetcher functionality"""
    try:
        # Import the fetcher
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from fetch_coindcx_data import CoinDCXDataFetcher
        
        # Initialize fetcher
        fetcher = CoinDCXDataFetcher()
        
        # Test basic functionality
        ticker_data = fetcher.get_ticker_data()
        if ticker_data and len(ticker_data) > 0:
            print(f"[SUCCESS] Data fetcher test passed ({len(ticker_data)} tickers fetched)")
            
            # Test target pairs functionality
            target_pairs = fetcher.get_target_pairs()
            target_coins = fetcher.get_pair_ticker_data(ticker_data, target_pairs)
            if target_pairs and len(target_pairs) > 0:
                print(f"[SUCCESS] Target pairs test passed ({len(target_pairs)} pairs configured)")
                print(f"   Found data for {len(target_coins)} pairs")
                if target_pairs:
                    print(f"   First target pair: {target_pairs[0]}")
                return True
            else:
                print("[ERROR] Target pairs test failed")
                return False
        else:
            print("[ERROR] Data fetcher test failed - no data received")
            return False
    except Exception as e:
        print(f"[ERROR] Data fetcher test failed: {e}")
        return False

def test_directory_structure():
    """Test if data directories can be created"""
    try:
        directories = ['data', 'data/trades', 'data/tickers', 'data/logs']
        for dir_path in directories:
            os.makedirs(dir_path, exist_ok=True)
        print("[SUCCESS] Directory structure test passed")
        return True
    except Exception as e:
        print(f"[ERROR] Directory structure test failed: {e}")
        return False

def test_data_analysis():
    """Test data analysis functionality"""
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from analyze_data import CryptoDataAnalyzer
        
        analyzer = CryptoDataAnalyzer()
        print("[SUCCESS] Data analysis module imported successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Data analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("CoinDCX Data Fetcher Setup Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("API Connectivity", test_api_connectivity),
        ("Directory Structure", test_directory_structure),
        ("Data Fetcher", test_data_fetcher),
        ("Data Analysis", test_data_analysis)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"See README.md for setup instructions")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll tests passed! Your setup is ready.")
        print("You can now run the data fetcher with:")
        print("   python scripts/fetch_coindcx_data.py")
        print("\nTo analyze data:")
        print("   python scripts/analyze_data.py")
        print("\nTo enable automation, push this to GitHub and enable Actions.")
    else:
        print(f"\n{total - passed} test(s) failed. Please fix the issues above.")
        print("Check the README.md for detailed setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 