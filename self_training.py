from sklearn.datasets import load_iris
from sklearn.utils import shuffle
from sklearn.naive_bayes import  GaussianNB
from sklearn.metrics import classification_report
import numpy as np

iris = load_iris()
# shuffle to meet the unlabeled samples at random
X, Y = shuffle(iris["data"], iris["target"], random_state=42)

# split the X, and Y arrays
# get 20 labeled samples
nb_samples = X.shape[0]
nb_labeled = 20
nb_unlabeled = nb_samples - nb_labeled
nb_unlabeled_samples = 2

X_train = X[:nb_labeled]
Y_train = Y[:nb_labeled]

X_unlabeled = X[nb_labeled:]

# train the Gaussian Naive Bayes classifier using the default parameters
nb0 = GaussianNB()
nb0.fit(X, Y)

# print(classification_report(Y, nb0.predict(X), target_names=iris['target_names']))

# training a semi-supervised model based on self training

while X_train.shape[0] <= nb_samples:
    nb = GaussianNB()
    nb.fit(X_train, Y_train)

    if X_train.shape[0] == nb_samples:
        break

    probs = nb.predict_proba(X_unlabeled)
    top_conf_idxs = np.argsort(np.max(probs, axis=1)).astype(np.int64)[::-1]

    selected_idxs = top_conf_idxs[0:nb_unlabeled_samples]

    X_new_train = X_unlabeled[selected_idxs]
    Y_new_train = nb.predict(X_new_train)

    X_train = np.concatenate((X_train, X_new_train), axis=0)
    Y_train = np.concatenate((Y_train, Y_new_train), axis=0)

    X_unlabeled = np.delete(X_unlabeled, selected_idxs, axis=0)

# new classifier with the original dataset
print(classification_report(Y, nb.predict(X), target_names=iris['target_names']))