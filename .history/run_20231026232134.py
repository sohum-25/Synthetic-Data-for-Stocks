import random
import math

def generate_tick_by_tick_data(symbol, S0):
    def calculate_ltp():
        r = 0.05  # Interest rate
        sigma = 0.2  # Volatility
        T = 1.0  # Time

        z = random.gauss(0, 1)  # Random normal variable

        ltp = S0 * math.exp((r - 0.5 * sigma**2) * T + sigma * math.sqrt(T) * z)

        return round(ltp, 2)

    while True:
        ltp = calculate_ltp()

        tick_data = {
            "ltp": ltp,
            "symbol": symbol
        }

        yield tick_data

# Example usage:
symbol = "XYZ"
initial_price = 100.00
ticker = generate_tick_by_tick_data(symbol, initial_price)

# Simulate tick-by-tick data stream
for _ in range(10):  # Simulate 10 ticks
    tick = next(ticker)
    print(f"Tick Data: {tick}")
