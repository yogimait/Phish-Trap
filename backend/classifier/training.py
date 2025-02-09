
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import numpy as np
import json
import dump

#  (legitimate vs phishing)
X_train = np.load('../dataset/X_train.npy')
y_train = np.load('../dataset/y_train.npy')

# Create and evaluate a Random Forest Classifier 
clf = RandomForestClassifier()
print('Cross Validation Score: {0}'.format(np.mean(cross_val_score(clf, X_train, y_train, cv=10))))

# Train the Random Forest model on the entire training dataset
clf.fit(X_train, y_train)

# Load the test data for final evaluation
X_test = np.load('../dataset/X_test.npy')
y_test = np.load('../dataset/y_test.npy')

pred = clf.predict(X_test)

# Save the trained model as a JSON file
json.dump(dump.forest_to_json(clf), open('../../static/classifier.json', 'w'))
