"""
Core component for the Random forest
"""

from __future__ import division, print_function
import numpy as np


def calculate_proportions(label_array):
    """Calculate the class proportions for a given array

    Args:
        label_array - 1d numpy array of labels
    """
    assert len(label_array.shape) == 1, "Input array not 1 dimensional"
    unique_labels = np.unique(label_array)
    num_items = label_array.shape[0]
    proportions = {}
    for label in unique_labels:
        label_prop = (label_array==label).sum()
        proportions[label] = label_prop / num_items
    return proportions


def gini_index(class_proportions):
    """
    Calculate and return the Gini index

    Args:
        class_proportions - dict of {class label: proportion}
    Returns:
        gini - value of gini index
    """
    gini = 0
    for label, proportion in class_proportions.items():
        gini += proportion * (1 - proportion)
    return gini


def _calc_split_impurities(label_array_subset, impurity_func):
    subset_proportions = calculate_proportions(label_array_subset)
    return impurity_func(subset_proportions)


def get_all_splits(feature_array, label_array, impurity_func=gini_index):
    """
    Get feature split values for a single feature for a set of observations

    Generator that scans over feature values for a set of observations and
    yields each feature split value with their weighted, summed impurity

    Args:
        feature_array - Array containing values for a single feature for a set
                        of observations
        label_array   - Array containing class labels for a set of observations
                        in the region
        impurity_func - function which takes a class proportions dict
                        and returns an impurity value
    Returns:
        tuple         - (feature split value, impurity measure)
    """
    sorted_index = np.argsort(feature_array)  # The index of the sorted array
    last_feature_val = feature_array[sorted_index[0]]
    num_examples = len(sorted_index)

    for ix in xrange(1, num_examples):
        feature_val = feature_array[sorted_index[ix]]
        if feature_val == last_feature_val:
            # Continue through the sorted feature values until
            # a new value appears
            continue
        # Impurity in sub-region 1
        split1_impurity = _calc_split_impurities(
            label_array.take(sorted_index[:ix]), impurity_func)
        # Impurity in sub-region 2
        split2_impurity = _calc_split_impurities(
            label_array.take(sorted_index[ix:]), impurity_func)
        # Split val is imputed (half way) between the feature values
        split_val = (feature_val + last_feature_val) / 2

        # Number of observations in each sub-region
        n_split1 = ix
        n_split2 = num_examples - ix

        yield (split_val,
               n_split1 * split1_impurity + n_split2 * split2_impurity)

        last_feature_val = feature_val


def recursively_split(node, X, y, n_features, n_examples, log=False):
    """Recursively split a region until node purity

    Args:
        node       - Node object representing region being split
        X          - Feature ndarray of shape (n_obs, n_feats)
        y          - Observation labels array
        n_features - Number of features (n_feats)
        n_examples - Number of observations in region (n_obs)
        log        - Flag to enable logging
    Returns:
        list       - list of Node object

    TODO: Calculating the impurity twice is inefficient
    """

    node.class_proportions = calculate_proportions(y)
    node.impurity = node.impurity_func(node.class_proportions)

    # Check if the node is pure
    unique_vals = np.unique(y)
    if len(unique_vals) == 1:
        node.is_leaf = True
        node.label = unique_vals[0]
        log and print("Purity reached. Level: {}".format(node.depth))
        return [node]

    best_split = (None,  # Column index
                  None,  # Feature value
                  1e10)  # Split impurity measure

    # Iterate over features
    for col_ix in xrange(n_features):
        feature_vals = X[:, col_ix]
        # Iterate over feature values
        for split_val, impurity in get_all_splits(feature_vals, y,
                                                  node.impurity_func):
            if impurity < best_split[2]:
                best_split = (col_ix, split_val, impurity)

    node.split_column = best_split[0]
    node.split_val = best_split[1]

    best_split_mask = X[:, node.split_column] < node.split_val
    split1_n_examples = best_split_mask.sum()

    node1 = Node(node.depth+1, node.impurity_func)
    node2 = Node(node.depth+1, node.impurity_func)
    node.children = (node1, node2)

    # Recursively split region represented by node1
    node1_nodes = recursively_split(node1,
                      X[best_split_mask],
                      y[best_split_mask],
                      n_features,
                      split1_n_examples,
                      log)
    # Recursively split region represented by node2
    node2_nodes = recursively_split(node2,
                      X[~best_split_mask],
                      y[~best_split_mask],
                      n_features,
                      n_examples - split1_n_examples,
                      log)

    log and print("Done! Level: {}".format(node.depth))

    # Return a list of Node objects
    return [node] + node1_nodes + node2_nodes


class Node(object):
    """
    Class representing a Tree node
    """
    def __init__(self, depth, impurity_func=gini_index):

        self.depth = depth
        self.impurity_func = impurity_func

        self.split_column = None  # Column index used to split node
        self.class_proportions = None
        self.impurity = None
        self.is_leaf = False
        self.children = (None, None)
        self.split_val = None
        self.label = None


class ClassificationTree(object):
    """
    Class to build a CART tree
    """
    def __init__(self, verbose=False, impurity_func=gini_index):
        self.root = Node(0, impurity_func)
        self.nodes = []
        self.verbose = verbose
        self.trained = False
        self.impurity_func = gini_index

    def train(self, X, y):
        """
        Train ClassificationTree on data X, y

        :param X: Feature ndarray of shape (n_obs, n_feats)
        :param y: Class labels array
        :return: Classification tree object
        """
        if self.trained:
            raise AttributeError("Can't retrain a trained ClassificationTree")

        self.n_features = X.shape[1]
        self.nodes = recursively_split(self.root, X, y,
                                       self.n_features,
                                       X.shape[0],
                                       self.verbose)
        return self

    def predict(self, X_i):
        """Predict label for 1D array of features

        Args:
            X_i - Feature values for an observation shape (n_feats,)
        Returns:
            label - Predicted label
        """
        assert X_i.shape[0] == self.n_features

        node = self.root
        while not node.is_leaf:
            split_ix = node.split_column
            feat_val = X_i[split_ix]
            if feat_val <= node.split_val:
                node = node.children[0]
            else:
                node = node.children[1]
        return node.label