from sklearn.datasets import make_blobs
from scipy.stats import multivariate_normal as mvn
import numpy as np

nb_samples = 250 #unlabeled
nb_unlabeled = 200 #labeled

X, Y = make_blobs(n_samples=nb_samples, n_features=2, centers=2, cluster_std=1.25, random_state=42)

unlabeled_idx = np.random.choice(np.arange(0,nb_samples, 1), replace=False, size=nb_unlabeled)
Y[unlabeled_idx] = -1

# two gaussian distributions with mean, covariance and weight
m1 = np.random.uniform(-7.5, 10.0, size=2)
c1 = np.random.uniform(5.0, 15.0, size=(2, 2))
c1 = np.dot(c1, c1.T)
q1 = 0.5

m2 = np.random.uniform(-7.5, 10.0, size=2)
c2 = np.random.uniform(5.0, 15.0, size=(2, 2))
c2 = np.dot(c2, c2.T)
q2 = 0.5

#orientation angle of the the major axis v1
w1, v1 = np.linalg.eigh(c1)
w2, v2 = np.linalg.eigh(c2)

nv1 = v1 / np.linalg.norm(v1)
nv2 = v2 / np.linalg.norm(v2)

a1 = np.arccos(np.dot(nv1[:, 1], [1.0, 0.0]) / np.linalg.norm(nv1[:,1])) * 180.0 / np.pi
a2 = np.arccos(np.dot(nv2[:1], [1.0, 0.0]) / np.linalg.norm(nv2[:, 1])) * 180.0 / np.pi

#training
#define temporary placeholders for the parameters computed at the previous iteration
#a function to compute the sum of the norms of all differences between current and previous values

threshold = 1e-4

def total_norm():
    global m1, m1_old, m2, m2_old, c1, c1_old, c2, c2_old, q1, q1_old, q2, q2_old

    return (
            np.linalg.norm(m1 - m1_old) +
            np.linalg.norm(m2 - m2_old) +
            np.linalg.norm(c1 - c1_old) +
            np.linalg.norm(c2 - c2_old) +
            np.linalg.norm(q1 - q1_old) +
            np.linalg.norm(q2 - q2_old)
            )

# Iterate until the parameters become stable (sum of the norms become less than the threshold)
m1_old = np.zeros((2,))
c1_old = np.zeros((2, 2))
q1_old = 0

m2_old = np.zeros((2,))
c2_old = np.zeros((2, 2))
q2_old = 0

while total_norm() > threshold:
    m1_old = m1.copy()
    c1_old = c1.copy()
    q1_old = q1

    m2_old = m2.copy()
    c2_old = c2.copy()
    q2_old = q2

    pij = np.zeros((nb_samples, 2))

    #E step
    for i in range(nb_samples):
        if Y[i] == -1:
            #Gaussian probability
            p1 = mvn.pdf(X[i], m1, c1, allow_singular=True) * q1
            p2 = mvn.pdf(X[i], m2, c2, allow_singular=True) * q2

            pij[i] = [p1, p2] / (p1 + p2)
        else:
            pij[i, :] = [1.0, 0.0] if Y[i] == 0 else [0.0, 1.0]

    #M step
    n = np.sum(pij, axis=0)
    m = np.sum(np.dot(pij.T, X), axis=0)

    m1 = np.dot(pij[:, 0], X) / n[0]
    m2 = np.dot(pij[:, 1], X) / n[1]

    q1 = n[0] / float(nb_samples)
    q2 = n[1] / float(nb_samples)

    c1 = np.zeros((2, 2))
    c2 = np.zeros((2, 2))

    for t in range(nb_samples):
        c1 += pij[t, 0] * np.outer(X[t] - m1, X[t] - m1)
        c2 += pij[t, 1] * np.outer(X[t] - m2, X[t] - m2)

    c1 /= n[0]
    c2 /= n[1]

print(np.round(X[Y==-1][0:5], 3))
print(np.round(pij[Y==-1][0:10], 3))
