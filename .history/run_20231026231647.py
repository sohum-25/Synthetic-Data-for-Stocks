import time

def sample_function(id):
    print(f"Function {id} started")
    time.sleep(2)  # Simulate some work (e.g., 2 seconds)
    print(f"Function {id} completed")

if __name__ == '__main__':
    for i in range(1, 11):
        sample_function(i)
