
from sklearn.linear_model import LinearRegression as SklearnLinearRegression
import numpy as np

class LinearRegression:
    def __init__(self):
        self.model = SklearnLinearRegression()
        self.weights = None

    def fit(self, X: list[list[float]], y: list[float]) -> None:
        """
        Fit the linear regression model.
        :param X: A 2D list or array of shape (n_samples, n_features)
        :param y: A list or array of shape (n_samples,)
        """
        X_np = np.array(X)
        y_np = np.array(y)
        self.model.fit(X_np, y_np)
        self.weights = np.concatenate(([self.model.intercept_], self.model.coef_))

    def getWeights(self) -> list[float]:
        """
        Get the regression weights. The first value is the intercept.
        :return: A list of weights [intercept, coef1, coef2, ...]
        """
        if self.weights is None:
            raise ValueError("Model is not fitted yet.")
        return self.weights.tolist()