import numpy as np

import helpers as h

from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator

# Тело программы поиска ответов
class NeighborSampler(BaseEstimator):

    # тело программы k=5, temperature=10.0 можно подбирать
    def __init__(self, k=2, temperature=10.0):
        self.k=k
        self.temperature = temperature

    def fit(self, X, y):
        self.tree_ = BallTree(X)
        self.y_ = np.array(y)

    def predict(self, X, random_state=None):
        distances, indices = self.tree_.query(X, return_distance=True, k=self.k)
        result = []

        for distance, index in zip(distances, indices):
            result.append(np.random.choice(index, p = h.softmax(distance * self.temperature)))

        return self.y_[result]