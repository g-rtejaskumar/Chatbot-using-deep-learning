from django.shortcuts import render
from django.http import HttpResponse
import numpy
import tflearn
import tensorflow.compat.v1 as tensorflow
tensorflow.disable_v2_behavior()
import random
import json
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Use path joining for better compatibility
pickle_path = os.path.join(current_dir, "data.pickle")
json_path = os.path.join(current_dir, "dataset", "question.json")
model_path = os.path.join(current_dir, "model", "model.tflearn")

words = []
data = []
with open(pickle_path, "rb") as f:
    words, labels, training, output = pickle.load(f)

with open(json_path) as file:
    data = json.load(file)

# Create model with matching dimensions
input_size = len(words)
output_size = len(labels)

# Use the exact same architecture as in Chatbot.py
tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, input_size])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, output_size, activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.load(model_path)

# Improved bag_of_words function
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def landing(request):
    return render(request, "index.html")  

def UserScreen(request):
    if request.method == 'GET':
        return render(request, 'UserScreen.html', {})

def ChatData(request):
    if request.method == 'GET':
        question = request.GET.get('mytext', False)
        
        # Handle empty input
        if not question or question.strip() == "":
            return HttpResponse("I didn't catch that. Could you please say something?", content_type="text/plain")
            
        results = model.predict([bag_of_words(question, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        
        response = "I'm not sure I understand. Could you rephrase that?"
        for tg in data["intents"]:
           if tg['tag'] == tag:
              responses = tg['responses']
              response = random.choice(responses) 
        
        print(f"Question: {question}, Intent: {tag}, Response: {response}")
        return HttpResponse(response, content_type="text/plain")
