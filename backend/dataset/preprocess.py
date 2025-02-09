
# coding: utf-8

# In[16]:


import arff
import numpy as np
import json
from sklearn.model_selection import train_test_split, KFold


# In[17]:


# Load the ARFF dataset file containing phishing website features
dataset = arff.load(open('dataset.arff', 'r'))
data = np.array(dataset['data'])

# Select only the relevant features we need for classification
# Removed some features that weren't good predictors based on analysis
data = data[:, [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 22, 30]]

# Split data into features (X) and labels (y)
# The last column contains our target labels (phishing=1, legitimate=0)
X, y = data[:, :-1], data[:, -1]
y.reshape(y.shape[0])

# Split into training (70%) and testing (30%) sets
# Using random_state=0 for reproducible results
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Save the numpy arrays to disk for later use in training
np.save('X_train.npy', X_train)
np.save('X_test.npy', X_test)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)

# Export test data as JSON for web interface
# This allows the frontend to use the same test data for predictions
test_data = dict()
test_data['X_test'] = X_test.tolist()
test_data['y_test'] = y_test.tolist()
with open('../../static/testdata.json', 'w') as tdfile:
    json.dump(test_data, tdfile)
    

