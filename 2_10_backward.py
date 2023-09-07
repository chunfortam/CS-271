import math
import numpy as np
from sklearn.preprocessing import normalize
##init

# N = 2 #number of state
# M = 27
##create obv
obv = []
with open("/Users/chun/IdeaProjects/CS-271/output.txt", 'r') as file:
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
# a = np.random.uniform(1/N - 1/(10*N),1/N + 1/(10*N),(N,N))
# a = normalize(a, axis=1, norm='l1')
# b = np.random.uniform(1/M - 1/(10*M),1/M + 1/(10*M),(N,M))
# b = normalize(b, axis=1, norm='l1')
# pi = np.random.uniform(1/N - 1/(10*N),1/N + 1/(10*N),(1,N))
# pi = normalize(pi , axis=1, norm='l1')[0]

a = np.matrix([[.7,.3],[.4,.6]])
b = np.matrix([[.1,.4,.5], [.7,.2,.1]])
pi = [.6,.4]
obv = [0,1,0,2]
T = len(obv)
M = 3
N = 2
maxlters = 100
# a = np.zeros((N,N))
# b = np.zeros((N,M))
iters = 0
oldLogProb = -math.inf

##Caculating alpha_0:
alpha = np.zeros((T,N))
c = np.zeros(T)
## i is which state, so needs to go in front
## 0 is the number of obversation
for i in range(0, N):
    tmp = pi[i] * b[i,obv[0]]
    alpha[0,i] = tmp
    c[0] += alpha[0][i]
c[0] = 1/c[0]
for i in range(0,N):
    alpha[0,i] *= c[0]
print(alpha)

def alpha_t():
    print("alpha_t")
    ##Compute alpha_t(i)
    ##t from 1 to 2 to go over the last 2 obv
    for t in range(1, T):
        c[t] = 0
        for i in range(0, N):
            alpha[t,i] = 0
            ## i is state and t is obv, j is previous state
            for j in range(0,N):
                alpha[t,i] += alpha[t-1,j]*a[j,i]
            alpha[t,i] *= b[i,obv[t]]
            c[t] += alpha [t,i]
        c[t] = 1/ c[t]
        for i in range(0,N):
            alpha[t,i] *= c[t]
alpha_t()

##backward init
beta = np.zeros((T,N))
for row in beta:
    row[-1] = 1
for i in range(0, N):
    beta[T-1,i] = c[T-1]
beta

##beta-pass
def backward():
    print("backward")
    for t in range(T-2,-1,-1):
        for i in range(0, N):
            beta[t,i] = 0
            for j in range(0, N):
                beta[t,i] += a[i,j] * b[j,obv[t+1]] * beta[t+1,j]
            beta[t,i] *= c[t]
backward()
print(beta)

##Gammas init
gammas = np.zeros((T,N))
de_gammas = np.zeros((T,N,N))

##Gammas

def cal_gammas():
    print("cal_gammas")
    for t in range(0, T-1):
        denom = 0
        for i in range(0, N):
            for j in range(0, N):
                denom += alpha[t,i] * a[i,j] * b[j,obv[t+1]] * beta[t+1,j]
        for i in range(0, N):
            gammas[t,i] = 0
            for j in range(0, N):
                de_gammas[t,i,j] = alpha[t,i] * a[i,j] * b[j,obv[t+1]]*beta[t+1,j] / denom
                gammas[t,i] += de_gammas[t,i,j]
    denom = 0
    for i in range(0, N):
        denom += alpha[T-1,i]
    for i in range(0, N):
        gammas[T-1,i] = alpha[T-1,i]/denom
cal_gammas()
print(gammas)
# de_gammas
# gammas

## re-estimate
def reestimate():
    print("reestimate")
    ##for pi
    for i in range(0, N):
        pi[i] = gammas[0,i]
    ##for A
    for i in range(0, N):
        for j in range(0,N):
            numer = 0
            denom = 0
            for t in range(0, T-1):
                numer += de_gammas[t,i,j]
                denom += gammas[t,i]
            a[i,j] = numer/denom
    ##for B
    for i in range(0,N):
        for j in range(0, M):
            numer = 0
            denom = 0
            for t in range(0, T-1):
                if obv[t] == j:
                    numer += gammas[t,i]
                denom += gammas[t,i]
            print(i,j,t)
            b[i,j] = numer/denom
reestimate()

# ##stopping Criteria
# iters = 0
# maxIters = 100
# oldLogProb = -math.inf
# def stopping():
#     logProb = 0
#     for i in range(0, T):
#         logProb += math.log(c[i])
#     logProb = -logProb
#     iters += 1
#     if iters < maxIters and logProb > oldLogProb:
#         oldLogProb = logProb
#         alpha_t()
#         backward()
#         cal_gammas()
#         reestimate()
#         stopping()
#     else:
#         print(pi)
#         print(a)
#         print(b)
# stopping()

##stopping Criteria
# iters = 0
# maxIters = 100
# oldLogProb = -math.inf
# def stopping(iters,maxIters,oldLogProb,a,b,c,alpha,pi,beta,obv,gammas,de_gammas,T,M,N):
#     print(iters,maxIters,oldLogProb,a,b,c,alpha,pi,beta,obv,gammas,de_gammas,T,M,N)
#     logProb = 0
#     for i in range(0, T):
#         logProb += math.log(c[i])
#     logProb = -logProb

#     iters += 1
#     if iters < maxIters and logProb > oldLogProb:
#         oldLogProb = logProb
#         alpha_t()
#         backward()
#         cal_gammas()
#         reestimate()
#         stopping()
#     else:
#         print("asdf")
# #         print(pi)
# #         print(a)
# #         print(b)
# stopping(iters=iters,maxIters=maxIters,oldLogProb=oldLogProb,a=a,b=b,c=c,alpha=alpha,pi=pi,beta=beta,obv=obv,
#         gammas=gammas,de_gammas=de_gammas,T=T,M=M,N=N)

