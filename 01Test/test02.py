import queue
import threading

def my_function(argument, result_queue):
    # Your function code here
    result = argument + 1
    result_queue.put(result)

# Create a queue to store the results
result_queue = queue.Queue()

# Create threads and pass the queue as an argument
thread1 = threading.Thread(target=my_function, args=(1, result_queue))
thread2 = threading.Thread(target=my_function, args=(2, result_queue))

# Start threads
thread1.start()
thread2.start()

# Get thread return values from the queue
thread1_result = result_queue.get()
thread2_result = result_queue.get()

# Print thread return values
print("thread1_result:", thread1_result)
print("thread2_result:", thread2_result)