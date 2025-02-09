import arff
import numpy as np
import json
from sklearn.model_selection import train_test_split, KFold

dataset = arff.load(open('dataset.arff', 'r'))#r is for read 
data = np.array(dataset['data'])

# Selected only the relevant features we needed for classification
data = data[:, [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 22, 30]]

# Split data into features X and labels y The last column contains our target labels (phishing=1, legitimate=0)
X, y = data[:, :-1], data[:, -1]
y.reshape(y.shape[0])

# Split into training (70%) and testing (30%) sets using random_state=0 for reproducible results
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Save the numpy arr for later to use in train
np.save('X_train.npy', X_train)
np.save('X_test.npy', X_test)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)

test_data = dict()
test_data['X_test'] = X_test.tolist() # This allows the frontend to use the same test data for predictions
test_data['y_test'] = y_test.tolist()
with open('../../static/testdata.json', 'w') as tdfile:
    json.dump(test_data, tdfile)# Export test data as JSON for web interface
    

