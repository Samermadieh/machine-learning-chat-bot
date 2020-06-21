#Import Libraries
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#Importing Article
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus = article.text

#Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text) # A list of sentences

#Greeting Reply
def greeting_response(text):
    text = text.lower()
    botGreetings = ['hello','hey','hi','howdy','hola']
    userGreetings = ['hi','hey','hello','hola','greetings','wassup']

    for word in text.split():
        if word in userGreetings:
            return random.choice(botGreetings)

#How Are You Reply
def howAreYou_response(text):
    text = text.lower()
    botHRU = ["I'm great! How can I help you?","Good thanks! How may I help you?"]
    userHRU = ['how','are', 'you', 'you?', 'r', 'u', 'u?', 'doing']

    numWords = len(text.split())
    numSimilarWords = 0;
    for word in text.split():
        if word in userHRU:
            numSimilarWords += 1

    if numWords < 5:
        if numSimilarWords > 1:
            return random.choice(botHRU)



def index_sort(listVar):
    length = len(listVar)
    listIndex = list(range(0, length))
    x = listVar

    for i in range(length):
        for j in range(length):
            if x[listIndex[i]] > x[listIndex[j]]:
                temp = listIndex[i]
                listIndex[i] = listIndex[j]
                listIndex[j] = temp
    return listIndex

#Bot Reply
def bot_response(userInput):
    userInput = userInput.lower()
    sentence_list.append(userInput)
    botResponse = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarityScores = cosine_similarity(cm[-1], cm)
    similarityScoresList = similarityScores.flatten()
    index = index_sort(similarityScoresList)
    index = index[1:]
    responseFlag = 0

    j = 0
    for i in range(len(index)):
        if similarityScoresList[index[i]] > 0.0:
            botResponse = botResponse + ' ' + sentence_list[index[i]]
            responseFlag = 1
            j += 1
        if j > 2:
            break

    if responseFlag == 0:
        botResponse = botResponse + ' ' + "I apologize, I do not understand."

    sentence_list.remove(userInput)

    return botResponse

print("Dr Bot: I am Dr Bot. I will answer your questions about chronic kidney disease. If you want to exit type bye.")

exitList = ['exit','see you later','bye','quit','break']

while(True):
    userInput = input("Me: ")
    if userInput.lower() in exitList:
        print("Dr Bot: Chat with you later!")
        break
    else:
        if greeting_response(userInput) != None:
            print("Dr Bot: " + greeting_response(userInput))
        elif howAreYou_response(userInput) != None:
            print("Dr Bot: " + howAreYou_response(userInput))
        else:
            print("Dr Bot: " + bot_response(userInput))






