
# coding: utf-8

# In[9]:


from sklearn.tree import _tree  # Import the private _tree module from scikit-learn

# This function converts data to JSON FORMAT
def tree_to_json(tree):
    tree_ = tree.tree_  
    # Lets say we have 30 dates
    feature_names = range(30)
    
    # Map feature indices to feature names, handle undefined features
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    # Helper function to recursively build the JSON structure
    def recurse(node):
        tree_json = dict()
        
        # If this node splits on a feature (not a leaf)
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            tree_json['type'] = 'split'
            threshold = tree_.threshold[node]
            # Create a human-readable split condition
            tree_json['threshold'] = "{} <= {}".format(feature_name[node], threshold)
            # Recursively process left and right children
            tree_json['left'] = recurse(tree_.children_left[node])
            tree_json['right'] = recurse(tree_.children_right[node])
        else:
            # Leaf node - contains the prediction values
            tree_json['type'] = 'leaf'
            tree_json['value'] = tree_.value[node].tolist()
        return tree_json

    # Start the recursion from the root node (0)
    return recurse(0)


# In[11]:


def forest_to_json(forest):
    # Initialize a dictionary to store the random forest's properties
    forest_json = dict()
    
    # Store basic characteristics of the forest
    forest_json['n_features'] = forest.n_features_  # Number of features used for prediction
    forest_json['n_classes'] = forest.n_classes_    # Number of target classes
    forest_json['classes'] = forest.classes_.tolist()  # List of possible class labels
    forest_json['n_outputs'] = forest.n_outputs_    # Number of outputs in prediction
    forest_json['n_estimators'] = forest.n_estimators  # Number of trees in the forest
    
    # Convert each decision tree in the forest to JSON format
    # Uses the tree_to_json function defined earlier
    forest_json['estimators'] = [tree_to_json(estimator) for estimator in forest.estimators_]
    
    return forest_json

