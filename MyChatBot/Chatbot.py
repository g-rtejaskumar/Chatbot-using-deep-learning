import os
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow.compat.v1 as tensorflow
tensorflow.disable_v2_behavior()
import random
import json
import pickle

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use absolute paths
json_path = os.path.join(script_dir, "dataset", "question.json")
pickle_path = os.path.join(script_dir, "data.pickle")
model_path = os.path.join(script_dir, "model", "model.tflearn")

# Make sure the model directory exists
os.makedirs(os.path.join(script_dir, "model"), exist_ok=True)

with open(json_path) as file:
    data = json.load(file)

try:
    with open(pickle_path, "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open(pickle_path, "wb") as f:
        pickle.dump((words, labels, training, output), f)

# Improve model architecture
tensorflow.reset_default_graph()

# Get the input size dynamically
input_size = len(training[0])
output_size = len(output[0])

print(f"Input size: {input_size}, Output size: {output_size}")

# Create a simpler, more stable model
net = tflearn.input_data(shape=[None, input_size])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, output_size, activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# Define bag_of_words function before using it
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

# Test the model on some examples
def test_model():
    print("\nTesting model with some examples:")
    test_cases = [
        "hi there",
        "how are you doing",
        "what is the meaning of life",
        "why are we here",
        "can you translate",
        "what languages do you speak",
        "you're stupid"
    ]
    
    for test in test_cases:
        results = model.predict([bag_of_words(test, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        confidence = results[0][results_index]
        print(f"Input: '{test}', Predicted: '{tag}', Confidence: {confidence:.4f}")

# Train with reasonable epochs
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save(model_path)

test_model()

print("Start talking with the bot (type quit to stop)!")
while True:
    inp = input("You: ")
    if inp.lower() == "quit":
        break
    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
    print(random.choice(responses)) 
