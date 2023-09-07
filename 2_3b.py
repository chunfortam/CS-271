import numpy as np
from itertools import product
a = np.array([[0.7,0.3],[0.4,0.6]])
b = np.array([[0.1,0.4,0.5],[0.7,0.2,0.1]])
pi = [0.6,0.4]
state = ["H", "C"]
N = len(state) ## 2
T = 4

observations = [0, 1, 2]
combinations = list(product(observations, repeat=4))
sum_comb = 0
# combinations = [[0,1,0,2]]
##compute a_0(i)

for obv in combinations:
    alpha = np.zeros((N, T))
    c = np.zeros(T)
    ## i is which state, so needs to go in front
    ## 0 is the number of obversation
    for i in range(0, N):
        tmp = pi[i] * b[i][obv[0]]
        alpha[i][0] = tmp
        c[0] += alpha[i][0]
#scaling
    c[0] = 1/ c[0]
    for i in range(0,N):
        alpha[i][0] *= c[0]
    print(alpha)

    ##Compute alpha_t(i)
    ##t from 1 to 2 to go over the last 2 obv
    for t in range(1, T):
        c[t] = 0
        for i in range(0, N):
        ## i is state and t is obv, j is previous state
            for j in range(0,N):
                alpha[i][t] += alpha[j][t-1]*a[j][i]
            alpha[i][t] *= b[i][obv[t]]
            c[t] += alpha[i][t]

        c[t] = 1/ c[t]
        for i in range(0,N):
            alpha[i][t] *= c[t]
    # obv_prob = alpha[0][-1] + alpha[1][-1]
    sum_comb += 1/np.product(c)
    # # print("{} : {}".format(obv,obv_prob))
print(sum_comb)


