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
net = tflearn.input_data(shape=[None, 46])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 6, activation="softmax")
net = tflearn.regression(net)

words = []
data = []
with open("D:\\College\\5 chatbot application\\Chatbot\\MyChatBot\\data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

with open("D:\\College\\5 chatbot application\\Chatbot\\MyChatBot\\dataset\\question.json") as file:
    data = json.load(file)

model = tflearn.DNN(net)

model.load("D:\\College\\5 chatbot application\\Chatbot\\MyChatBot\\model\\model.tflearn")
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

def UserScreen(request):
    if request.method == 'GET':
        return render(request, 'UserScreen.html', {})

def ChatData(request):
    if request.method == 'GET':
        question = request.GET.get('mytext', False)
        results = model.predict([bag_of_words(question, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        str = "no result found"
        for tg in data["intents"]:
           if tg['tag'] == tag:
              responses = tg['responses']
              str = random.choice(responses) 
        
        print(question+" "+str)
        return HttpResponse(str, content_type="text/plain")
