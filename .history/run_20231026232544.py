import random
import math
import time
import multiprocessing

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
    {"symbol": "ABC", "initial_price": 150.00},
    {"symbol": "DEF", "initial_price": 200.00},
    {"symbol": "GHI", "initial_price": 250.00},
    {"symbol": "JKL", "initial_price": 300.00},
    {"symbol": "MNO", "initial_price": 350.00},
    {"symbol": "PQR", "initial_price": 400.00},
    {"symbol": "STU", "initial_price": 450.00},
    {"symbol": "VWX", "initial_price": 500.00},
    {"symbol": "YZA", "initial_price": 550.00},
    {"symbol": "BCD", "initial_price": 600.00},
]

def run_tick_generator(config):
    symbol = config["symbol"]
    initial_price = config["initial_price"]
    ticker = generate_tick_by_tick_data(symbol, initial_price)
    
    for _ in range(20):  # Simulate 20 ticks for each instance
        tick = next(ticker)
        print(f"Tick Data for {symbol}: {tick}")

if __name__ == '__main__':
    processes = []

    # Create and run 10 instances of the tick generator, each in its own process
    for config in configs:
        process = multiprocessing.Process(target=run_tick_generator, args=(config,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()
