import time
import multiprocessing

def sample_function(id):
    print(f"Function {id} started")
    time.sleep(0.56)  # Simulate some work (e.g., 2 seconds)
    print(f"Function {id} completed")

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