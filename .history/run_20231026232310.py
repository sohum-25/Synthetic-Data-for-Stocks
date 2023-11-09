import random
import math
import time

def generate_tick_by_tick_data(symbol, S0):
    def calculate_ltp():
        r = 0.05  # Interest rate
        sigma = 0.02  # Volatility
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

# Example usage:
symbol = "XYZ"
initial_price = 100.00
ticker = generate_tick_by_tick_data(symbol, initial_price)

# Simulate tick-by-tick data stream
for _ in range(20):  # Simulate 20 ticks
    tick = next(ticker)
    print(f"Tick Data: {tick}")
