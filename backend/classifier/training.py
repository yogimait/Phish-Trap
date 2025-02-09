# coding: utf-8

# Import necessary machine learning and utility libraries
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import numpy as np
import json
import dump

# Load the training data from numpy files
# X_train contains the feature vectors
# y_train contains the corresponding labels (legitimate vs phishing)
X_train = np.load('../dataset/X_train.npy')
y_train = np.load('../dataset/y_train.npy')

# Create and evaluate a Random Forest Classifier using 10-fold cross validation
# This helps us understand how well our model generalizes to unseen data
clf = RandomForestClassifier()
print('Cross Validation Score: {0}'.format(np.mean(cross_val_score(clf, X_train, y_train, cv=10))))

# Train the Random Forest model on the entire training dataset
clf.fit(X_train, y_train)

# Load the test data for final evaluation
# X_test contains feature vectors for testing
# y_test contains the true labels for testing
X_test = np.load('../dataset/X_test.npy')
y_test = np.load('../dataset/y_test.npy')

# Make predictions on the test data
pred = clf.predict(X_test)

# Save the trained model as a JSON file
# This allows the model to be used in web applications
json.dump(dump.forest_to_json(clf), open('../../static/classifier.json', 'w'))
