import numpy as np
from itertools import product
a = np.array([[0.7,0.3],[0.4,0.6]])
b = np.array([[0.1,0.4,0.5],[0.7,0.2,0.1]])
pi = [0.6,0.4]
state = [0,1]
N = len(state) ## 2
T = 4

observations = [0, 1, 2]
obv_comb = list(product(observations, repeat=4))
# obv_comb = [[0,1,0,2]]
state_comb = list(product(state, repeat=4))
# state_comb = [[0,0,1,1]]


all_prob = 0

for obv in obv_comb:
    obv_prob = 0
    obv_digit= [int(char) for char in obv]
    for st in state_comb:
        st_digit = [int(char) for char in st]
        prob = pi[st_digit[0]] * b[st[0]][obv_digit[0]] ## pi * b
        # print(st,prob)
        for i in range(0,3):
            a_xi =  a[st[i]][st[i+1]]
            b_xi = b[st[i+1]][obv_digit[i+1]]
            prob *= a_xi * b_xi
            # print(i,st,prob)

        obv_prob += prob
    all_prob += obv_prob
    print("{} : {}".format(obv,obv_prob))
print(all_prob)



