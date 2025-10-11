from sklearn.datasets import load_iris
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Lodad dataset
iris = load_iris()

# Features and labels
X = iris.data
y = iris.target

# Convert to pandas DataFrame
df = pd.DataFrame(X, columns=iris.feature_names)
df['species'] = pd.Categorical.from_codes(y, iris.target_names)

print(df.head())

sns.pairplot(df, hue="species")
plt.show()