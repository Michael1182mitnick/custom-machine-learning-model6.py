# Custom_machine_learning_model_from_scratch
# Implement a simple neural network or decision tree from scratch using only NumPy, without relying on machine learning libraries like TensorFlow or PyTorch.
# implementing a decision tree classifier

import numpy as np


class DecisionTreeNode:
    def __init__(self, gini, num_samples, num_samples_per_class, predicted_class):
        self.gini = gini
        self.num_samples = num_samples
        self.num_samples_per_class = num_samples_per_class
        self.predicted_class = predicted_class
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None


def gini_index(y):
    """Calculate Gini Impurity for a node."""
    m = len(y)
    if m == 0:
        return 0
    return 1.0 - sum((np.sum(y == c) / m) ** 2 for c in np.unique(y))


class DecisionTreeClassifier:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def _best_split(self, X, y):
        """Find the best split for a node."""
        m, n = X.shape
        if m <= 1:
            return None, None

        # Count of each class in the current node
        num_parent = [np.sum(y == c) for c in np.unique(y)]

        # Gini of the current node
        best_gini = 1.0 - sum((num / m) ** 2 for num in num_parent)
        best_idx, best_thr = None, None

        # Loop through all features
        for idx in range(n):
            # Sort data along selected feature
            sorted_indices = np.argsort(X[:, idx])
            X_sorted, y_sorted = X[sorted_indices], y[sorted_indices]

            # Iterate through the dataset and find the best split
            num_left = [0] * len(np.unique(y))
            num_right = num_parent.copy()
            for i in range(1, m):
                c = y_sorted[i - 1]
                num_left[c] += 1
                num_right[c] -= 1
                gini_left = 1.0 - \
                    sum((num_left[x] / i) **
                        2 for x in range(len(np.unique(y))))
                gini_right = 1.0 - \
                    sum((num_right[x] / (m - i)) **
                        2 for x in range(len(np.unique(y))))
                gini = (i * gini_left + (m - i) * gini_right) / m

                # Update best split if needed
                if X_sorted[i, idx] == X_sorted[i - 1, idx]:
                    continue
                if gini < best_gini:
                    best_gini = gini
                    best_idx = idx
                    best_thr = (X_sorted[i, idx] + X_sorted[i - 1, idx]) / 2
        return best_idx, best_thr

    def _grow_tree(self, X, y, depth=0):
        """Recursively build the tree."""
        num_samples_per_class = [np.sum(y == i) for i in np.unique(y)]
        predicted_class = np.argmax(num_samples_per_class)
        node = DecisionTreeNode(
            gini=gini_index(y),
            num_samples=len(y),
            num_samples_per_class=num_samples_per_class,
            predicted_class=predicted_class,
        )

        # Stopping criteria
        if depth < self.max_depth:
            idx, thr = self._best_split(X, y)
            if idx is not None:
                indices_left = X[:, idx] < thr
                X_left, y_left = X[indices_left], y[indices_left]
                X_right, y_right = X[~indices_left], y[~indices_left]
                node.feature_index = idx
                node.threshold = thr
                node.left = self._grow_tree(X_left, y_left, depth + 1)
                node.right = self._grow_tree(X_right, y_right, depth + 1)
        return node

    def fit(self, X, y):
        """Build decision tree classifier."""
        self.tree_ = self._grow_tree(X, y)

    def _predict(self, inputs):
        """Predict class for a single sample."""
        node = self.tree_
        while node.left:
            if inputs[node.feature_index] < node.threshold:
                node = node.left
            else:
                node = node.right
        return node.predicted_class

    def predict(self, X):
        """Predict classes for all samples."""
        return [self._predict(inputs) for inputs in X]


# Example usage
if __name__ == "__main__":
    # XOR problem (example dataset)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 1, 1, 0])

    # Create decision tree classifier instance
    tree = DecisionTreeClassifier(max_depth=3)
    tree.fit(X, y)

    # Predict on the training set
    predictions = tree.predict(X)
    print("Predictions:", predictions)
