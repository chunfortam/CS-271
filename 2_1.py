##2.1
import numpy as np

state = ["H", "C"]
a = np.array([[0.7,0.3],[0.4,0.6]])
b = np.array([[0.1,0.4,0.5],[0.7,0.2,0.1]])
pi = np.array([0,1])
obv = [1,0,2]
N = len(state) ## 2
T = len(obv) ## 3

##compute a_0(i)
alpha = np.zeros((N, T))
c_0 = 0
## i is which state, so needs to go in front
## 0 is the number of obversation
for i in range(0, N):
    tmp = pi[i] * b[i][obv[0]]
    alpha[i][0] = tmp

print(alpha)

##scaling

##Compute alpha_t(i)
##t from 1 to 2 to go over the last 2 obv
for t in range(1, T):
    c_t = 0
    for i in range(0, N):
        ## i is state and t is obv, j is previous state
        for j in range(0,N):
            alpha[i][t] += alpha[j][t-1]*a[j][i]
        alpha[i][t] *= b[i][obv[t]]
        c_t += alpha[i][t]
    ##scaling

    print(alpha)

