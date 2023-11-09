import random
import math
import time

def generate_tick_by_tick_data(symbol, S0):
    def calculate_ltp():
        r = 0.05  # Interest rate
        sigma = 0.2  # Volatility
        T = 1.0  # Time

        z = random.gauss(0, 1)  # Random normal variable

        ltp = S0 * math.exp((r - 0.5 * sigma**2) * T + sigma * math.sqrt(T) * z)

        return round(ltp, 2)

    while True:
        ticks_per_second = random.randint(1, 5)
        time_interval = 1 / ticks_per_second

        ltp = calculate_ltp()

        tick_data = {
            "ltp": ltp,
            "symbol": symbol
        }

        yield tick_data
        time.sleep(time_interval)

# Create a list of configurations for 10 instances
configs = [
    {"symbol": "RELIANCE", "initial_price": 2500.00},
    {"symbol": "TATASTEEL", "initial_price": 1400.00},
    {"symbol": "HDFCBANK", "initial_price": 1500.00},
    {"symbol": "INFY", "initial_price": 1800.00},
    {"symbol": "ITC", "initial_price": 250.00},
    {"symbol": "TCS", "initial_price": 3200.00},
    {"symbol": "HDFC", "initial_price": 2300.00},
    {"symbol": "ICICIBANK", "initial_price": 650.00},
    {"symbol": "KOTAKBANK", "initial_price": 1800.00},
    {"symbol": "LT", "initial_price": 1600.00},
    {"symbol": "M&M", "initial_price": 850.00},
    {"symbol": "MARUTI", "initial_price": 9000.00},
    {"symbol": "ONGC", "initial_price": 150.00},
    {"symbol": "POWERGRID", "initial_price": 175.00},
    {"symbol": "SBIN", "initial_price": 450.00},
    {"symbol": "SUNPHARMA", "initial_price": 700.00},
    {"symbol": "TITAN", "initial_price": 1800.00},
    {"symbol": "UPL", "initial_price": 900.00},
    {"symbol": "ULTRACEMCO", "initial_price": 4500.00},
    {"symbol": "WIPRO", "initial_price": 600.00},
]

def run_tick_generators(configs):
    for config in configs:
        symbol = config["symbol"]
        initial_price = config["initial_price"]
        ticker = generate_tick_by_tick_data(symbol, initial_price)

        for _ in range(20):  # Simulate 20 ticks for each instance
            tick = next(ticker)
            print(f"Tick Data for {symbol}: {tick}")

# Run tick generators sequentially
run_tick_generators(configs)
