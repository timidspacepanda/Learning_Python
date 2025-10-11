from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt

iris = load_iris()
X = iris.data
y = iris.target

# Train on 2 feaures for easier visulaization
X2 = X[:, :2]
logit_model = LogisticRegression().fit(X2, y)
lda_model = LinearDiscriminantAnalysis().fit(X2, y)

# Meshgrid for descion boundary
x_min, x_max = X2[:, 0].min() - 0.5, X2[:, 0].max() + 0.5
y_min, y_max = X2[:, 1].min() - 0.5, X2[:, 1].max() + 0.5

xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), 
                     np.arange(y_min, y_max, 0.02))

Z = logit_model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.3)
plt.scatter(X2[:,0], X2[:, 1], c=y, edgecolors='k')
plt.xlabel(iris.feature_names[0])
plt.xlabel(iris.feature_names[1])
plt.show()


