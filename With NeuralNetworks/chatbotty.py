import nltk
import pickle
import json
import random
import numpy as np
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
#nltk.download('punkt')
#nltk.download('wordnet')
import speech_recognition as sr
import pyttsx3
import datetime




model = load_model('chatbot_model.chat')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

WordNetLemmatizer = WordNetLemmatizer()

def Cleanup(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [WordNetLemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def WordsBag(sentence, words, show_details=True):
    sentence_words = Cleanup(sentence)
    words_bag = [0]*len(words)
    for sentence in sentence_words:
        for i, word in enumerate(words):
            if word == sentence:
                words_bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(words_bag))

def PredictClass(sentence, model):
    words_bag = WordsBag(sentence, words, show_details=False)
    model_result = model.predict(np.array([words_bag]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, result] for i, result in enumerate(model_result) if result > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(intents, intents_json):
    tag = intents[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def GetChatbotResponse(text):
    intent = PredictClass(text, model)
    results = getResponse(intent, intents)
    speak(results)


print('Caricando il tuo assistente personale - Elsa')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("rate", 190)
engine.setProperty("voice", voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Ciao buongiorno Giorgia")
        print("Ciao Buongiorno Giorgia")
    elif hour>=12 and hour<18:
        speak("Buon pomeriggio Giorgia")
        print("Buon pomeriggio Giorgia")
    else:
        speak("Buonasera Giorgia")
        print("Buonasera Giorgia")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ascoltando...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio , language='it-IT')
            print(f"l'utente ha detto:{statement}\n")

        except Exception as e:
            speak("Scusami non ho capito, puoi ripetere")
            return "None"
        return statement

speak("Caricando il tuo assistente personale ")
wishMe()


if __name__=='__main__':


    while True:
        speak("Cosa posso fare per lei?")
        statement = takeCommand().lower()
        if statement==0:
            continue
        GetChatbotResponse(statement)



