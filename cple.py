from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection import cross_val_score
from scipy.optimize import fmin_bfgs

X_a, Y_a = load_digits(return_X_y=True)

X = np.vstack((X_a[Y_a == 0], X_a[Y_a == 1]))
Y = np.vstack(
    (np.expand_dims(Y_a, axis=1)[Y_a == 0], np.expand_dims(Y_a, axis=1)[Y_a == 1])
)

nb_samples = X.shape[0]
nb_dimensions = X.shape[1]

nb_unlabeled = 150

Y_true = np.zeros((nb_unlabeled,))

unlabled_idx = np.random.choice(np.arange(0, nb_samples, 1), replace=False, size=nb_unlabeled)
Y_true = Y[unlabled_idx].copy()
Y[unlabled_idx] = -1

lr_test = LogisticRegression(solver='lbfgs', max_iter=10000, n_jobs=-1, random_state=1000)
lr_test.fit(X[Y.squeeze() != -1], Y[Y.squeeze()!= -1].squeeze())
unlabled_score = lr_test.score(X[Y.squeeze() == -1], Y_true)

# print(unlabled_score)

total_cv_scores = cross_val_score(LogisticRegression(solver='lbfgs', max_iter=10000, random_state=1000), X, Y.squeeze(), cv=10, n_jobs=-1)
# print(total_cv_scores)

lr = LogisticRegression(solver='lbfgs', max_iter=10000, random_state=1000)

q0 = np.random.uniform(0, 1, size=nb_unlabeled)

trh = np.vectorize(lambda x: 0.0 if x < 0.5 else 1.0)

def weighted_log_loss(yt, p, w=None, eps=1e-15):
    if w is None:
        w_t = np.ones((yt.shape[0], 2))
    else:
        w_t = np.vstack((w, 1.0 - w)).T

    Y_t = np.vstack((1.0 - yt.squeeze(), yt.squeeze())).T
    L_t = np.sum(w_t * Y_t * np.log(np.clip(p, eps, 1.0 - eps)), axis=1)

    return np.mean(L_t)

def build_dataset(q):
    Y_unlabled = trh(q)

    X_n = np.zeros((nb_samples, nb_dimensions))
    X_n[0:nb_samples - nb_unlabeled] = X[Y.squeeze() != -1]
    X_n[nb_samples - nb_unlabeled:] = X[Y.squeeze() == -1]

    Y_n = np.zeros((nb_samples, 1))
    Y_n[0:nb_samples - nb_unlabeled] = Y[Y.squeeze() != -1]
    Y_n[nb_samples - nb_unlabeled:] = np.expand_dims(Y_unlabled, axis=1)

    return X_n, Y_n

def log_likelihood(q):
    X_n, Y_n = build_dataset(q)
    Y_soft = trh(q)

    lr.fit(X_n, Y_n.squeeze())

    p_sup = lr.predict_proba(X[Y.squeeze() != -1])
    p_semi = lr.predict_proba(X[Y.squeeze() == -1])

    l_sup = weighted_log_loss(Y[Y.squeeze() != -1], p_sup)
    l_semi = weighted_log_loss(Y_soft, p_semi, q)

    return l_semi - l_sup

q_end = fmin_bfgs(f=log_likelihood, x0=q0, maxiter=1000, disp=False)

X_n, Y_n = build_dataset(q_end)

final_semi_cv_scores = cross_val_score(
    LogisticRegression(solver='lbfgs', max_iter=10000, random_state=1000), X_n, Y_n.squeeze(), cv=10, n_jobs=1
)

print(final_semi_cv_scores)