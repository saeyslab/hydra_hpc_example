import numpy as np
import random

# create datasets, note that this does not take different frequency patters into account
def smalllist(n: int = 100, k: int = 1_000):
    return random.choices(range(n), k=k)

def biglist(n: int = 10_000, k: int = 1_000_000):
    return random.choices(range(n), k=k)

def arr_smalllist(n: int = 100, k: int = 1_000):
    return np.array(smalllist(n, k))

def arr_biglist(n: int = 10_000, k: int = 1_000_000):
    return np.array(biglist(n, k))