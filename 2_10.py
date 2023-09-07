import math
import numpy as np
from sklearn.preprocessing import normalize

N = 2 #number of state
M = 27
##create obv
obv = []
with open("output.txt", 'r') as file:
    for line in file:
        for char in line:
            if char == " ":
                obv.append(26)
            else:
                obv.append(ord(char.lower()) - ord('a'))
for i in obv:
    if i >= 27 or i < 0:
        print(i)

##initlizing a,b,pi
T = len(obv)
print(T)
a = np.random.uniform(1/N - 1/(10*N),1/N + 1/(10*N),(N,N))
a = normalize(a, axis=1, norm='l1')
b = np.random.uniform(1/M - 1/(10*M),1/M + 1/(10*M),(N,M))
b = normalize(b, axis=1, norm='l1')
pi = np.random.uniform(1/N - 1/(10*N),1/N + 1/(10*N),(1,N))
pi = normalize(pi , axis=1, norm='l1')[0]
maxlters = 100
iters = 0
oldLogProb = -math.inf

##Caculating forward:
alpha = np.zeros((N, T))
c = np.zeros(T)
## i is which state, so needs to go in front
## 0 is the number of obversation
for i in range(0, N):
    tmp = pi[i] * b[i][obv[0]]
    alpha[i][0] = tmp
    c[0] += alpha[i][0]
c[0] = 1/c[0]
for i in range(0,N):
    alpha[i][0] *= c[0]


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

# print(alpha)
##backward
beta = np.zeros((N,T))
gammas = np.zeros((N,T))
de_gammas = np.zeros((N,N,T))

##setting last one to 1
for row in beta:
    row[-1] = 1
for i in range(0, N):
    beta[i][T-1] = c[T-1]
# print(beta)

##beta-pass
for t in range(T-2,-1,-1):
    for i in range(0, N):
        beta[i][t] = 0
        for j in range(0, N):
            beta[i][t] += a[i][j] * b[i][obv[t+1]] * beta[j][t+1]
        beta[i][t] *= c[t]
print(beta)


for t in range(0, T-1):
    denom = 0
    for i in range(0, N):
        for j in range(0, N):
            denom += alpha[i][t] * a[i][j] * b[j][t+1] * beta[j][t+1]
    for i in range(0, N):
        gammas[i][t] = 0
        for j in range(0, N):
            de_gammas[i][j][t] = alpha[i][t] * a[i][j] * b[j][obv[t+1]]*beta[j][t+1] / denom
            gammas[i][t] += de_gammas[i][j][t]

denom = 0
for i in range(0, N):
    denom += alpha[i][T-1]
for i in range(0,N):
    gammas[i][T-1] = alpha[i][T-1]/denom


##Re-estimation pi
for i in range(0, N):
    pi[i] = gammas[i][0]

##Re-estimate A
for i in range(0, N):
    for j in range(0,N):
        numer = 0
        denom = 0
        for t in range(0, T-1):
            numer += gammas[i][j][t]
            denom += gammas[i][t]
        a[i][j] = numer/denom

##Re-esetimate B
for i in range(0, N):
    for j in range(0, M):
        numer = 0
        denom = 0
        for t in range(0, T-1):
            if obv[t] == j:
                numer += gammas[i][t]
            denom += gammas[i][t]
        b[j][i] = numer/denom




























# # Specify the input file path
# input_file = 'output.txt'
#
# # Initialize a variable to store the character count
# char_count = 0
#
# # Open the input file
# with open(input_file, 'r') as file:
#     # Read lines from the file
#     for line in file:
#         # Count characters in each line
#         char_count += len(line)
#
# print(f"Total number of characters in '{input_file}': {char_count}")