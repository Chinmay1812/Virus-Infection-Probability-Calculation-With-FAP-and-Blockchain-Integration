from random import randint
import time

arr = [randint(0, 10000) for i in range(50000000)]

#1

start = time.time()

d = {}

minn = min(arr)
maxx = max(arr)

for i in range(minn, maxx+1):
    d[i] = 0
    
for i in arr:
    d[i] += 1

sorted_arr = []

for i in range(minn, maxx+1):
    for k in range(d[i]):
        sorted_arr.append(i)

end = time.time()

print(end-start)

#2

start = time.time()

arr.sort()
            
end = time.time()

print(end-start)