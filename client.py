import hashlib
import os
import threading

def get_cores():
    #a function that returns the number of cores
    return os.cpu_count()

def create_threads(start, end, target, results):
    #a function that creates multiple threads that each one of them checks if the hashed number is in its given range
    num_of_cores = get_cores()
    #calculating how many numbers each core should check
    numbers_for_core = (end - start) // num_of_cores
    #creating a list that contains lists of ranges for each thread
    ranges_for_cores = [[start + core * numbers_for_core, start + (core + 1) * numbers_for_core] for core in range(num_of_cores)]
    threads = []

    for core in range(num_of_cores):
        #a for loop that threads that will run the crack number function
        t = threading.Thread(target=crack_number, args=(ranges_for_cores[core], target, results))
        t.start()
        threads.append(t)
    print(threads)
    
    for t in threads:
        t.join()


def crack_number(range_list, target, results):
    #a function that searches for a hashed number in a specific number range to find the number
    start, end = range_list
    while start <= end:
        #changing the number to a specific format
        string_number = f"{start:010d}"
        
        #hashing the number and checking if the number is the hashed target
        hashed_number = hashlib.md5(string_number.encode())
        if hashed_number.hexdigest() == target.hexdigest():
            results.append(f"The number is: {start}")
            return
        start += 1
    
    #in case that the number is not in the range
    results.append("The number is not in the range")
    return

start = 0
end = 10000000
target = 513242300
#a list that contains the result of each thread
results = []
target = hashlib.md5((f"{target:010d}").encode())
print(target.hexdigest())

create_threads(start, end, target, results)
for result in results:
    print(result)