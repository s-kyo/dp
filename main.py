######################################################
#
# This program is an implemention for basic RAPPOR
#
######################################################


import scipy
import numpy as np
import matplotlib.pyplot as plt
import random
import math

def freq_mining(data, freq_data):
    for x in data:
        freq_data[x] += 1

def freq_mining_with_vec(data, d, freq_data):
    n = data
    for i in range(d):
        if (n&1) == 1:
            freq_data[i] += 1
        n = n>>1

def int2binvec(i):
    return 1<<i

def int2binstr(n):
    return bin(n).replace('0b','')


def flip_with(n, d, p, q):
    _n = n
    __n = 0
    ___n = 0
    for i in range(d):
        __n = _n & 1
        if __n == 1:
            coin = random.uniform(0, 1)
            if coin > p:
                __n = 0
        else:
            coin = random.uniform(0, 1)
            if coin <= q:
                __n = 1
        ___n = ___n + (__n << i)
        _n = _n >> 1
    return ___n

def support(data, i, j, d):
    # 1.......0000000  = data[i]
    # ^       ^
    # |       |
    # d-th  (j+1)-th
    return ((data[i] & (1 << j)) >> j)

if __name__ == "__main__":
    n = 100
    d = 20
    p = 0.5
    q = 1/(1+math.exp(1))
    # generate n data into d items
    # [0, 0, 0, 0, 1, 1, 2, 3]
    raw_data = [int(-math.log(1-float(i)/n, 2)) for i in range(n)]
    # print "raw_data:", raw_data
    # =========================ENCODE=========================
    # we encode data like this:
    # 0 -> (1)_2
    # 1 -> (10)_2
    # ..
    # j -> (10..0)_2
    #       ^
    #       |
    #       j+1 th
    encode_data = [int2binvec(i) for i in raw_data]
    #print encode_data
    # ========================PERTURB========================
    perturbed_data = [flip_with(i, d, p, q) for i in encode_data]
    #for i in perturbed_data:
    #    print bin(i),",",
    # =======================AGGERGATE=======================
    # estimate
    est_data_freq = [0 for j in range(d)]
    for item in range(d):
        for user in range(n):
            est_data_freq[item] += support(perturbed_data, user, item, d)
        est_data_freq[item] = int((est_data_freq[item]-n*q)/(p-q))
    print "estimated freq:\t", est_data_freq

    # true frequency 
    data_freq = [0 for j in range(d)]
    freq_mining(raw_data, data_freq)
    print "real freq:\t", data_freq