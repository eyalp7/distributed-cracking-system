import hashlib

def crack_number(start, end, target):
    #a function that searches for a hashed number in a specific number range to find the number

    while start <= end:
        #changing the number to a specific format
        string_number = f"{start:010d}"
        print(string_number)
        
        #hashing the number and checking if the number is the hashed target
        hashed_number = hashlib.md5(string_number.encode())
        if hashed_number.hexdigest() == target.hexdigest():
            return (f"The number is: {start}")
        start += 1
    
    #in case that the number is not in the range
    return ("The number is not in the range")

start = 100
end = 10000
target = 4953
target = hashlib.md5((f"{target:010d}").encode())
print(target.hexdigest())

print(crack_number(start, end, target))