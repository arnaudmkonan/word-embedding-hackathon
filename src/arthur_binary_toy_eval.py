#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 16:51:01 2018

@author: johnstevenson

Borrowed heavily from Keras tutorial docs
"""

import os
import sys
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from sklearn.preprocessing import LabelEncoder

import pandas as pd
import datetime, time
import pickle

TRAINING_DATA_PATH = './data_construction.pickle'

EMBEDDING_DIR = os.path.join('../..', 'glove.6B')
EMBEDDING_FILE_NAME = 'glove.6B.100d.txt'
EMBEDDING_DIM = 100

MAX_SEQUENCE_LENGTH = 250
MAX_NUM_WORDS = 20000
VALIDATION_SPLIT = 0.2


def word_embed_index_create(glove_dir, glove_file):
    print('Indexing word vectors.')  
    embeddings_index = {}
    f = open(os.path.join(glove_dir, glove_file))
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    
    print('Found %s word vectors.' % len(embeddings_index))
    return embeddings_index

def tokenize_texts(texts, max_num_words, max_sequence_length):   
    print('Found %s texts.' % len(texts))
    
    # finally, vectorize the text samples into a 2D integer tensor
    tokenizer = Tokenizer(num_words=max_num_words)
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    
    data = pad_sequences(sequences, maxlen=max_sequence_length)
    print('Shape of data tensor:', data.shape)
    return word_index, data

# Load training data from pickle file
training_df = pickle.load( open(TRAINING_DATA_PATH, "rb" ) )

embeddings_index = word_embed_index_create(EMBEDDING_DIR, EMBEDDING_FILE_NAME)

word_index, data = tokenize_texts(list(training_df['desc_of_operations']), MAX_NUM_WORDS, MAX_SEQUENCE_LENGTH)

labels = to_categorical(np.asarray(list(training_df['target'])))

# encode class values as integers (for sigmoid output)
encoder = LabelEncoder()
encoder.fit(list(training_df['target']))
encoded_labels = encoder.transform(list(training_df['target']))

# Split into training/test sets
print('Shape of label tensor:', labels.shape)
num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])
x_train = data[:-num_validation_samples]
y_train = labels[:-num_validation_samples]
x_val = data[-num_validation_samples:]
y_val = labels[-num_validation_samples:]

# for sigmoid need labels encoded
y_train_enc = encoded_labels[:-num_validation_samples]
y_val_enc = encoded_labels[-num_validation_samples:]

num_words = min(MAX_NUM_WORDS, len(word_index))
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

# load pre-trained word embeddings into an Embedding layer
# note that we set trainable = False so as to keep the embeddings fixed
embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

print('Training model.')

# train a 1D convnet with global maxpooling

sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
x = Conv1D(128, 5, activation='relu')(embedded_sequences)
x = MaxPooling1D(5)(x)
x = Conv1D(128, 5, activation='relu')(x)
x = MaxPooling1D(5)(x)
x = Conv1D(128, 5, activation='relu')(x)
x = GlobalMaxPooling1D()(x)
x = Dense(128, activation='relu')(x)
preds_sig = Dense(1, activation='sigmoid')(x)

model_sig = Model(sequence_input, preds_sig)
model_sig.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])

model_sig.fit(x_train, y_train_enc,
          batch_size=128,
          epochs=3,
          validation_data=(x_val, y_val_enc))




## If additional classes are needed as output:
# preds = Dense(len(labels[0]), activation='softmax')(x)

# model = Model(sequence_input, preds)
# model.compile(loss='categorical_crossentropy',
#               optimizer='rmsprop',
#               metrics=['acc'])

# model.fit(x_train, y_train,
#           batch_size=128,
#           epochs=3,
#           validation_data=(x_val, y_val))




## For saving model
# model.save_weights('arthur_binary.h5')

# # saving
# with open('tokenizer.pickle', 'wb') as handle:
#     pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    
# # loading
# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle) 
    
    
#  # serialize model to JSON
# model_json = model.to_json()
# with open("model.json", "w") as json_file:
#     json_file.write(model_json)   
    
    
        