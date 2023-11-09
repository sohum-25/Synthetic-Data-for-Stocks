import time
import multiprocessing
import math
import random
def sample_function(id):
    print(f"Function {id} started")

    ltp = calculate_ltp()
    symbol = f"SYMBOL-{id}"

    data = {
        "ltp": ltp,
        "symbol": symbol
    }

    time.sleep(1 / random.randint(1, 4))  # Simulate 1-4 dicts per second

    print(f"Function {id} completed")
    
    return data

def calculate_ltp():
    S0 = random.uniform(100, 10000)  # Random initial price between 100 and 10,000
    r = 0.05  # Interest rate
    sigma = 0.2  # Volatility
    T = 1.0  # Time

    z = random.gauss(0, 1)  # Random normal variable

    ltp = S0 * math.exp((r - 0.5 * sigma**2) * T + sigma * math.sqrt(T) * z)
    
    return round(ltp, 2)

if __name__ == '__main__':
    data_list = []

    for i in range(10):
        data = sample_function(i)
        data_list.append(data)

    for data in data_list:
        print(f"Received data: {data}")

if __name__ == '__main__':
    processes = []

    # Create 10 processes, each running the sample_function with a unique ID
    for i in range(1, 11):
        process = multiprocessing.Process(target=sample_function, args=(i,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()