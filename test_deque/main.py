import time
from collections import deque

# implementazione di una coda con lista e con deque

# coda = [X1, X2, X3, X4, X5, X6] <-- X7 (FIFO)

# implementazione con lista:

lista = []

tic = time.time()
for i in range(10000):
    lista.append(i)
toc = time.time()

print(f"Tempo per aggiungere valori alla lista: {toc - tic}s")

tic = time.time()
for i in range(10000):
    lista.pop(0)
toc = time.time()

print(f"Tempo per togliere valori dalla lista: {toc - tic}s")

# implementazione con deque:

d = deque()

tic = time.time()
for i in range(10000):
    d.append(i)
toc = time.time()

print(f"Tempo per aggiungere valori al deque: {toc - tic}s")

tic = time.time()
for i in range(10000):
    d.popleft()
toc = time.time()

print(f"Tempo per togliere valori dal deque: {toc - tic}s")