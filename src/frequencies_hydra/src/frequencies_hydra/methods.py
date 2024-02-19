import numpy as np
from collections import Counter, defaultdict

def if_contains_else(biglist: list) -> None:
    # using if-else is as the 'slowest' method
    frequencies = dict()
    for i in biglist:
        if i in frequencies:
            frequencies[i] += 1
        else:
            frequencies[i] = 1

def for_counter(biglist: list) -> None:
    # this can be the least efficient method because of the for loop
    frequencies = Counter()
    for i in biglist:
        frequencies[i] += 1

def counter(biglist: list) -> None:
    # using the Counter class directly is the fastest method
    frequencies = Counter(biglist)

def get_or_default(biglist: list) -> None:
    frequencies = dict()
    for i in biglist:
        frequencies[i] = frequencies.get(i, 0) + 1

def default_dict(biglist: list):
    # more elegant than get_or_default
    frequencies = defaultdict(int)
    for i in biglist:
        frequencies[i] += 1

def numpy_freq(biglist: list) -> None:
    # numpy array creation overhead make this slow
    np.unique(biglist, return_counts=True)

# def numpy_freq_precreated(biglist):
#     # without overhead, still slower than Counter for this size
#     unique, counts = np.unique(arr_biglist, return_counts=True)

def try_except(biglist: list) -> None:
    # using a try clause is surprisingly good
    frequencies = dict()
    for i in biglist:
        try:
            frequencies[i] += 1
        except Exception:
            frequencies[i] = 1
