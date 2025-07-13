#!/usr/bin/env python3
"""
Real-time Arbitrage GUI with Interactive Charts
Displays live arbitrage data with navigable line graphs
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
import time
import queue
import json
import os
from collections import defaultdict, deque
from realtime_arbitrage import RealTimeArbitrage

class ArbitrageGUI:
    """Real-time arbitrage monitoring GUI with interactive charts"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CRYPRED - Real-Time INR/USDT Arbitrage Monitor")
        self.root.geometry("1400x900")
        
        # Data storage
        self.data_history = defaultdict(lambda: {
            'timestamps': deque(maxlen=1000),
            'inr_prices': deque(maxlen=1000),
            'usdt_prices': deque(maxlen=1000),
            'spreads': deque(maxlen=1000),
            'signals': deque(maxlen=1000)
        })
        
        # GUI state
        self.is_running = False
        self.current_pair = 'BTC'
        self.view_start_idx = 0
        self.view_window_size = 100
        self.data_queue = queue.Queue()
        
        # Arbitrage system
        self.arbitrage = RealTimeArbitrage()
        
        # Create GUI elements
        self.setup_gui()
        
        # Start data collection thread
        self.data_thread = None
        
        # Animation for real-time updates
        self.animation = None
        
    def setup_gui(self):
        """Setup the GUI layout and widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start/Stop buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.LEFT)
        
        self.start_btn = ttk.Button(button_frame, text="Start Monitoring", 
                                   command=self.start_monitoring, style="Success.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Monitoring", 
                                  command=self.stop_monitoring, state=tk.DISABLED, 
                                  style="Danger.TButton")
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Pair selection
        pair_frame = ttk.Frame(control_frame)
        pair_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Label(pair_frame, text="Select Pair:").pack(side=tk.LEFT)
        
        self.pair_var = tk.StringVar(value=self.current_pair)
        pair_combo = ttk.Combobox(pair_frame, textvariable=self.pair_var, 
                                 values=['BTC', 'ETH', 'XRP', 'SOL', 'ADA', 'DOGE'],
                                 state="readonly", width=8)
        pair_combo.pack(side=tk.LEFT, padx=(5, 0))
        pair_combo.bind('<<ComboboxSelected>>', self.on_pair_changed)
        
        # Status display
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(side=tk.RIGHT)
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped", foreground="red")
        self.status_label.pack(side=tk.RIGHT)
        
        # Chart container
        chart_container = ttk.Frame(main_frame)
        chart_container.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(14, 8), dpi=100)
        self.figure.patch.set_facecolor('white')
        
        # Create subplots
        self.price_ax = self.figure.add_subplot(2, 1, 1)
        self.spread_ax = self.figure.add_subplot(2, 1, 2)
        
        # Canvas for matplotlib
        self.canvas = FigureCanvasTkAgg(self.figure, chart_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Navigation toolbar
        toolbar_frame = ttk.Frame(chart_container)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Custom navigation controls
        nav_frame = ttk.Frame(toolbar_frame)
        nav_frame.pack(side=tk.LEFT)
        
        ttk.Button(nav_frame, text="◄◄", command=self.scroll_to_start, width=4).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="◄", command=self.scroll_left, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="►", command=self.scroll_right, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="►►", command=self.scroll_to_end, width=4).pack(side=tk.LEFT, padx=2)
        
        # Window size control
        window_frame = ttk.Frame(toolbar_frame)
        window_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Label(window_frame, text="View Window:").pack(side=tk.LEFT)
        self.window_var = tk.StringVar(value="100")
        window_spinbox = ttk.Spinbox(window_frame, from_=50, to=500, increment=50, 
                                   textvariable=self.window_var, width=8,
                                   command=self.on_window_size_changed)
        window_spinbox.pack(side=tk.LEFT, padx=(5, 0))
        
        # Info panel
        info_frame = ttk.LabelFrame(main_frame, text="Current Arbitrage Info", padding=10)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create info grid
        info_grid = ttk.Frame(info_frame)
        info_grid.pack(fill=tk.X)
        
        # Current prices
        price_frame = ttk.Frame(info_grid)
        price_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.inr_price_label = ttk.Label(price_frame, text="INR Price: --", font=("Arial", 12, "bold"))
        self.inr_price_label.pack(anchor=tk.W)
        
        self.usd_price_label = ttk.Label(price_frame, text="USDT Price: --", font=("Arial", 12, "bold"))
        self.usd_price_label.pack(anchor=tk.W)
        
        # Spread info
        spread_frame = ttk.Frame(info_grid)
        spread_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.spread_label = ttk.Label(spread_frame, text="Spread: --", font=("Arial", 12, "bold"))
        self.spread_label.pack(anchor=tk.W)
        
        self.signal_label = ttk.Label(spread_frame, text="Signal: --", font=("Arial", 12, "bold"))
        self.signal_label.pack(anchor=tk.W)
        
        # Statistics
        stats_frame = ttk.Frame(info_grid)
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.opportunities_label = ttk.Label(stats_frame, text="Opportunities: 0", font=("Arial", 10))
        self.opportunities_label.pack(anchor=tk.E)
        
        self.uptime_label = ttk.Label(stats_frame, text="Uptime: 0:00:00", font=("Arial", 10))
        self.uptime_label.pack(anchor=tk.E)
        
        # Setup initial chart
        self.setup_charts()
        
    def setup_charts(self):
        """Setup initial chart configuration"""
        
        # Price chart
        self.price_ax.clear()
        self.price_ax.set_title(f"{self.current_pair} Price Comparison", fontsize=14, fontweight='bold')
        self.price_ax.set_ylabel("Price (USDT)", fontsize=12)
        self.price_ax.grid(True, alpha=0.3)
        self.price_ax.legend(['INR (Normalized)', 'USDT'], loc='upper left')
        
        # Spread chart
        self.spread_ax.clear()
        self.spread_ax.set_title(f"{self.current_pair} Spread Analysis", fontsize=14, fontweight='bold')
        self.spread_ax.set_ylabel("Spread (%)", fontsize=12)
        self.spread_ax.set_xlabel("Time", fontsize=12)
        self.spread_ax.grid(True, alpha=0.3)
        self.spread_ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # Color zones
        self.spread_ax.axhspan(-10, -0.5, alpha=0.1, color='green', label='BUY Zone')
        self.spread_ax.axhspan(0.5, 10, alpha=0.1, color='red', label='SELL Zone')
        self.spread_ax.legend(loc='upper left')
        
        self.canvas.draw()
        
    def start_monitoring(self):
        """Start the arbitrage monitoring"""
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.now()
            
            # Update GUI state
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Running", foreground="green")
            
            # Start data collection thread
            self.data_thread = threading.Thread(target=self.data_collection_loop, daemon=True)
            self.data_thread.start()
            
            # Start animation for real-time updates
            self.animation = FuncAnimation(self.figure, self.update_charts, 
                                         interval=1000, blit=False, cache_frame_data=False)
            
            # Start GUI update loop
            self.update_gui_info()
            
    def stop_monitoring(self):
        """Stop the arbitrage monitoring"""
        if self.is_running:
            self.is_running = False
            
            # Update GUI state
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Stopped", foreground="red")
            
            # Stop animation
            if self.animation:
                self.animation.event_source.stop()
                self.animation = None
                
    def data_collection_loop(self):
        """Background thread for collecting arbitrage data"""
        while self.is_running:
            try:
                # Update USDT/INR rate
                self.arbitrage.get_usdt_inr_rate()
                
                # Fetch prices from both exchanges
                inr_prices, usdt_prices = self.arbitrage.fetch_all_prices()
                
                # Calculate arbitrage opportunities
                opportunities = self.arbitrage.calculate_arbitrage_opportunities(inr_prices, usdt_prices)
                
                # Store data for each pair
                current_time = datetime.now()
                
                for symbol in self.arbitrage.target_pairs.keys():
                    if symbol in inr_prices and symbol in usdt_prices:
                        inr_price = inr_prices[symbol]
                        usdt_price = usdt_prices[symbol]
                        inr_normalized = inr_price.price / self.arbitrage.usdt_inr_rate
                        
                        # Calculate spread
                        spread = (inr_normalized - usdt_price.price) / usdt_price.price * 100
                        
                        # Determine signal
                        signal = "SELL" if spread > 0.5 else ("BUY" if spread < -0.5 else "HOLD")
                        
                        # Store in history
                        self.data_history[symbol]['timestamps'].append(current_time)
                        self.data_history[symbol]['inr_prices'].append(inr_normalized)
                        self.data_history[symbol]['usdt_prices'].append(usdt_price.price)
                        self.data_history[symbol]['spreads'].append(spread)
                        self.data_history[symbol]['signals'].append(signal)
                
                # Put opportunities in queue for GUI updates
                self.data_queue.put(('opportunities', opportunities))
                
                # Wait before next collection
                time.sleep(10)  # 10 second intervals
                
            except Exception as e:
                print(f"Error in data collection: {e}")
                time.sleep(5)
                
    def update_charts(self, frame):
        """Update charts with new data (called by FuncAnimation)"""
        if not self.is_running or self.current_pair not in self.data_history:
            return
            
        data = self.data_history[self.current_pair]
        
        if len(data['timestamps']) == 0:
            return
            
        # Get data for current view window
        total_points = len(data['timestamps'])
        
        # Auto-scroll to end if we're at the end
        if self.view_start_idx >= total_points - self.view_window_size:
            self.view_start_idx = max(0, total_points - self.view_window_size)
            
        end_idx = min(self.view_start_idx + self.view_window_size, total_points)
        start_idx = max(0, end_idx - self.view_window_size)
        
        if start_idx >= end_idx:
            return
            
        # Extract data for view window
        timestamps = list(data['timestamps'])[start_idx:end_idx]
        inr_prices = list(data['inr_prices'])[start_idx:end_idx]
        usdt_prices = list(data['usdt_prices'])[start_idx:end_idx]
        spreads = list(data['spreads'])[start_idx:end_idx]
        signals = list(data['signals'])[start_idx:end_idx]
        
        if len(timestamps) == 0:
            return
            
        # Update price chart
        self.price_ax.clear()
        self.price_ax.set_title(f"{self.current_pair} Price Comparison", fontsize=14, fontweight='bold')
        self.price_ax.set_ylabel("Price (USDT)", fontsize=12)
        
        # Plot price lines
        self.price_ax.plot(timestamps, inr_prices, 'b-', linewidth=2, label='INR (Normalized)', alpha=0.8)
        self.price_ax.plot(timestamps, usdt_prices, 'r-', linewidth=2, label='USDT (Binance)', alpha=0.8)
        
        self.price_ax.grid(True, alpha=0.3)
        self.price_ax.legend(loc='upper left')
        
        # Update spread chart
        self.spread_ax.clear()
        self.spread_ax.set_title(f"{self.current_pair} Spread Analysis", fontsize=14, fontweight='bold')
        self.spread_ax.set_ylabel("Spread (%)", fontsize=12)
        self.spread_ax.set_xlabel("Time", fontsize=12)
        
        # Plot spread line
        spread_colors = ['green' if s < -0.5 else 'red' if s > 0.5 else 'gray' for s in spreads]
        self.spread_ax.plot(timestamps, spreads, 'k-', linewidth=2, alpha=0.8)
        
        # Scatter points for signals
        for i, (ts, spread, signal) in enumerate(zip(timestamps, spreads, signals)):
            color = 'green' if signal == 'BUY' else 'red' if signal == 'SELL' else 'gray'
            self.spread_ax.scatter(ts, spread, c=color, s=50, alpha=0.7)
            
        # Reference lines
        self.spread_ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        self.spread_ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
        self.spread_ax.axhline(y=-0.5, color='green', linestyle='--', alpha=0.5)
        
        # Color zones
        self.spread_ax.axhspan(-10, -0.5, alpha=0.1, color='green')
        self.spread_ax.axhspan(0.5, 10, alpha=0.1, color='red')
        
        self.spread_ax.grid(True, alpha=0.3)
        
        # Format x-axis
        self.figure.autofmt_xdate()
        
        # Tight layout
        self.figure.tight_layout()
        
    def update_gui_info(self):
        """Update GUI info panel"""
        if not self.is_running:
            return
            
        try:
            # Process any queued data
            while not self.data_queue.empty():
                data_type, data = self.data_queue.get_nowait()
                if data_type == 'opportunities':
                    self.process_opportunities(data)
                    
            # Update uptime
            if hasattr(self, 'start_time'):
                uptime = datetime.now() - self.start_time
                hours, remainder = divmod(uptime.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                self.uptime_label.config(text=f"Uptime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
                
            # Update current pair info
            self.update_current_pair_info()
            
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Error updating GUI info: {e}")
            
        # Schedule next update
        if self.is_running:
            self.root.after(1000, self.update_gui_info)
            
    def process_opportunities(self, opportunities):
        """Process new arbitrage opportunities"""
        opportunity_count = len(opportunities)
        self.opportunities_label.config(text=f"Opportunities: {opportunity_count}")
        
    def update_current_pair_info(self):
        """Update current pair information in info panel"""
        if self.current_pair in self.data_history:
            data = self.data_history[self.current_pair]
            
            if len(data['timestamps']) > 0:
                # Get latest data
                latest_inr = data['inr_prices'][-1]
                latest_usdt = data['usdt_prices'][-1]
                latest_spread = data['spreads'][-1]
                latest_signal = data['signals'][-1]
                
                # Update labels
                self.inr_price_label.config(text=f"INR Price: {latest_inr:,.2f} USDT")
                self.usd_price_label.config(text=f"USDT Price: {latest_usdt:,.2f} USDT")
                
                spread_color = "green" if latest_spread < -0.5 else "red" if latest_spread > 0.5 else "black"
                self.spread_label.config(text=f"Spread: {latest_spread:+.2f}%", foreground=spread_color)
                
                signal_color = "green" if latest_signal == "BUY" else "red" if latest_signal == "SELL" else "black"
                self.signal_label.config(text=f"Signal: {latest_signal}", foreground=signal_color)
                
    def on_pair_changed(self, event):
        """Handle pair selection change"""
        self.current_pair = self.pair_var.get()
        self.setup_charts()
        self.view_start_idx = 0  # Reset view to start
        
    def on_window_size_changed(self):
        """Handle view window size change"""
        try:
            self.view_window_size = int(self.window_var.get())
        except ValueError:
            self.view_window_size = 100
            
    def scroll_left(self):
        """Scroll view left"""
        self.view_start_idx = max(0, self.view_start_idx - 10)
        
    def scroll_right(self):
        """Scroll view right"""
        if self.current_pair in self.data_history:
            max_start = max(0, len(self.data_history[self.current_pair]['timestamps']) - self.view_window_size)
            self.view_start_idx = min(max_start, self.view_start_idx + 10)
            
    def scroll_to_start(self):
        """Scroll to beginning"""
        self.view_start_idx = 0
        
    def scroll_to_end(self):
        """Scroll to end"""
        if self.current_pair in self.data_history:
            self.view_start_idx = max(0, len(self.data_history[self.current_pair]['timestamps']) - self.view_window_size)
            
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            self.stop_monitoring()
        self.root.destroy()

def main():
    """Main function to run the GUI"""
    try:
        # Check dependencies
        import matplotlib
        matplotlib.use('TkAgg')
        
        # Create and run GUI
        root = tk.Tk()
        
        # Configure styles
        style = ttk.Style()
        style.configure("Success.TButton", background="green")
        style.configure("Danger.TButton", background="red")
        
        app = ArbitrageGUI(root)
        
        # Handle window close
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        print("🖥️  Starting CRYPRED Arbitrage GUI...")
        print("📊 Real-time charts with navigable historical data")
        print("🎯 Select cryptocurrency pairs to monitor")
        print("⚡ Click 'Start Monitoring' to begin live data collection")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please install required packages:")
        print("   pip install matplotlib pandas")
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")

if __name__ == "__main__":
    main() 