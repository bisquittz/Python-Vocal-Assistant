import nltk
import pickle
import random
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

words = []
classes = []
documents = []
training = []
ignore_words = ['?', '!']
intents = pd.read_json('intents.json')
WordNetLemmatizer = WordNetLemmatizer()

for intent in intents['intents']:
    for pattern in intent['patterns']:
        tokenize_word = nltk.word_tokenize(pattern)
        words.extend(tokenize_word)
        documents.append((tokenize_word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [WordNetLemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


empty_output = [0] * len(classes)
for document in documents:
    word_bag = []
    pattern_words = document[0]
    pattern_words = [WordNetLemmatizer.lemmatize(word.lower()) for word in pattern_words]

    for word in words:
        word_bag.append(1) if word in pattern_words else word_bag.append(0)
        output_row = list(empty_output)
    output_row[classes.index(document[1])] = 1
    training.append([word_bag, output_row])

random.shuffle(training)
training = np.array(training)
x_train = list(training[:,0])
y_train = list(training[:,1])

sequential_model = Sequential()
sequential_model.add(Dense(128, input_shape=(len(x_train[0]),), activation='relu'))
sequential_model.add(Dropout(0.5))
sequential_model.add(Dense(64, activation='relu'))
sequential_model.add(Dropout(0.5))
sequential_model.add(Dense(len(y_train[0]), activation='softmax'))


sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
sequential_model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#fitting and saving the model
model = sequential_model.fit(np.array(x_train), np.array(y_train), epochs=200, batch_size=5, verbose=1)
sequential_model.save('chatbot_model.chat', model)
print('il modello ?? creato!')