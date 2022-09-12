import random

random.seed(42)

print(random.sample(range(20),k=10))

st = random.getstate()  # remeber this state 

print(random.sample(range(20),k=20)) # print 20

random.setstate(st)     # restore state

print(random.sample(range(20),k=10)) #print same first 10
