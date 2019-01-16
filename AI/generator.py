import random

import hypothesis
import hypothesis.strategies


rand = random.Random()


def genint(size=100, min=0, max=10000):
    data = []
    for i in range(size):
        data.append(rand.randint(min, max))
    return data


def get_generator(type):
    if type == int:
        return hypothesis.strategies.integers


def sortlist(data):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] > data[j]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
    return data
