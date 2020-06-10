from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

import numpy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from keras.utils import plot_model

seed = 9
numpy.random.seed(seed)

# load datasets
#csv files were filtered based on the data.
input_file = "filtereddata.csv"
test_file = "filtereddata.csv"

dataset = pd.read_csv(input_file).values

# read training data
datasetTest = pd.read_csv(test_file).values

# split into input (X) and output (Y) variables
X = dataset[:,0:8].astype("int32")
Y = dataset[:,8]
XT = datasetTest[:,0:8].astype("int32")

encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)

# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

(X_train, X_test, Y_train, Y_test) = train_test_split(X, dummy_y, test_size=0.001, random_state=seed)
# create model
model = Sequential()
model.add(Dense(8, input_dim=8, init='normal', activation='relu'))
model.add(Dense(4, init='normal', activation='relu'))
model.add(Dense(3, init='normal', activation='tanh'))
model.add(Dense(3, init='normal', activation='softmax'))
print(model.summary())
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model

print(X_train.shape)
print(Y_train.shape)
print("Before calling the fit() method on model ...")
history = model.fit(X_train, Y_train, validation_split=0.3, epochs=16, batch_size=128)

# evaluate the model
scores = model.evaluate(X_test, Y_test)

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

print(type(history))
plot_model(model, to_file='model.png')

plt.figure(1)
# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.figure(2)
# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show()

#from sklearn.metrics import confusion_matrix
#y_pred_keras = model.predict_classes(XT)

#csv = open("C:\\DeepSlice\\5G\\output.csv", "w")
#"w" indicates that you're writing strings to the file

#pd.DataFrame(y_pred_keras).to_csv("C:\\DeepSlice\\5G\\output.csv")
#cm = confusion_matrix(Y_test, y_pred_keras, labels=[0, 1, 2])

#csv = open("C:\\DeepSlice\\5G\\input.csv", "w")
#"w" indicates that you're writing strings to the file

#pd.DataFrame(XT).to_csv("C:\\DeepSlice\\5G\\input.csv")
