# JARVIS

# TODO
# - trivia questions

# HOW TO APP
# pip3 install -U py2app
# py2applet --make-setup MyApplication.py
# python3 setup.py py2app -A

# imports
import requests # web scraping
from bs4 import BeautifulSoup # web scraping
import speech_recognition as sr # speech to text
from googletrans import Translator, constants # translating
from pprint import pprint
import ctypes
import pyttsx3 # text to speech
from random import random # random
from PyDictionary import PyDictionary # definition
import os # opening apps
import smtplib # email
import wikipedia # wikipedia
from tkinter import * # GUI
import threading # threading
from geopy.geocoders import Nominatim # lat and long for weather
from dadjokes import Dadjoke # dad jokes
import opentdbpy # trivia
import webbrowser # opeing url


r = sr.Recognizer() # instance of Recognizer class
engine = pyttsx3.init() # text to speech engine
translator = Translator() # Google API traslator
dictionary = PyDictionary() # definitions
gmail_user = 'jarvis2020r@gmail.com' # gmail user
sent_from = gmail_user # gmail
geolocator = Nominatim(user_agent="JARVIS") # lat and long
trivia = opentdbpy.Client() # trivia
d = '/Applications' # applications
apps = list(map(lambda x: x.split('.app')[0], os.listdir(d))) # apps list


# engine properties
engine.setProperty('rate', 170)

# voices
voices = engine.getProperty('voices')
jarvisIndex = 7 # voice index for jarvis
engine.setProperty('voice', voices[jarvisIndex].id)
frenchIndex = 3
spanishIndex = 14
hebrewIndex = 5
russianIndex = 27
italianIndex = 2
lang = ""

# message array of all inputs and outputs
# message = []

def formatEmail(name, text):
    return "Dear " + name  + ",\n\n\t" + text + ".\n\n From, Jarvis"

def sendEmail(recipient_email, subject, body, name):
    gmail_password = 'GOOGLEryanlevy123' # gmail password
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(recipient_email), subject, formatEmail(name, body))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, recipient_email, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

def getLatAndLong(location):
    latitude = str(round((geolocator.geocode(location).latitude), 4))
    longitude = str(round((geolocator.geocode(location).longitude), 4))
    return [latitude, longitude]

def getCurrentWeather(input):
    location = "Woodbury"
    latitude = str(round((geolocator.geocode(location).latitude), 4))
    longitude = str(round((geolocator.geocode(location).longitude), 4))
    if input.find("in") > -1:
        location = input[input.find("in") + 2:].strip()
        latitude = str(round((geolocator.geocode(location).latitude), 4))
        longitude = str(round((geolocator.geocode(location).longitude), 4))

    page = requests.get(str("https://forecast.weather.gov/MapClick.php?lat=" + latitude + "&lon=" + longitude + "#.X2-wGZNKiEs"))
    soup = BeautifulSoup(page.content, 'html.parser')
    seven_day = soup.find(id="seven-day-forecast")
    forecast_items = seven_day.find_all(class_="tombstone-container")
    tonight = forecast_items[0]

    period = tonight.find(class_="period-name").get_text()
    short_desc = tonight.find(class_="short-desc").get_text()
    temp = tonight.find(class_="temp").get_text()
    print(period)
    print(short_desc)
    print(temp)

    img = tonight.find("img")
    desc = img['title']
    return "The weather in " + location + " is. " + desc

def randresponse():
    r = random() * 3
    list = ["That's nice to hear sir", "Interesting, tell me more", "you don't say", "What do you think about that"]
    return list[r]

def triviaQuestion(categoryIndex):
    questionArr = trivia.get_questions(category=categoryIndex)
    r = int(random() * len(questionArr))
    question = questionArr[r]
    answer = question.correct_answer
    print(question)
    print(answer)
    engine.say(str(question))
    engine.runAndWait()
    userAnswer = recordAudio()
    if str(userAnswer.lower()) == str(answer.lower()):
        return "That's Correct"
    else:
        return "That's Incorrect. The correct answer is...  " + str(answer)

def cleanConvo(message):
    for i in range(len(message)):
        if i % 2 == 0:
            message[i] = "JARVIS: " + message[i] + "\n"
        else:
            message[i] = "You: " + message[i] + "\n"

    cleanedConvo = ""

    for m in message:
        cleanedConvo += m + "\n"


def recordAudio():
    e = sr.Recognizer()
    with sr.Microphone() as source:
        # wait for audio
        audio = e.listen(source)
    try:
        # convert audio to text
        text = e.recognize_google(audio)
        body = text
        print("You said: " + text)
        return text
    except:
        print("no audio")
        
        

        engine.say("You are sending an email to " + name + " saying " + text + ". Is this ok. Respond yes or no")
        engine.runAndWait()

def startJarvis():
    # greeting = "Hello. I am Jarvis. My program is still in the testing phase. Please wait 5 full seconds after I speak, for you to speak, for the sake of the program. Thank you"
    greeting = "Hello sir"

    # add to array
    # message.append(greeting)

    # set voice to british
    engine.setProperty('voice', voices[jarvisIndex].id)
    # say greeting
    engine.say(greeting)
    # run audio
    engine.runAndWait()
    print("Say Something: ")
    with sr.Microphone() as source:
        # wait for audio
        audio = r.listen(source)
    try:
        # convert audio to text
        text = r.recognize_google(audio)
        print("You said: " + text)
        # message.append(text)
        # put audio throught response function
        response = getresponse(text)
        # message.append(response)
        print("response: " + response)
        engine.say(response)
        engine.runAndWait()
        engine.setProperty('voice', voices[jarvisIndex].id)
    except:
        print("no audio")

    while True:
        with sr.Microphone() as source:
            # wait for audio
            audio = r.listen(source)
        try:
            # convert audio to text
            text = r.recognize_google(audio)
            print("You said: " + text)
            # message.append(text)
            # put audio throught response function
            response = getresponse(text)
            print("response: " + response)
            # message.append(response)
            engine.say(response)
            engine.runAndWait()
            engine.setProperty('voice', voices[jarvisIndex].id)
        except:
            print("no audio")
    
# what jarvis can do
# - translate english to [french, spanish, hebrew, russian, italian]
# - get's information on any topic
# - give the definition of a word
# - spell a word
# - email someone
# - tell you the weather in NY
# - open safari
# - search
# - pick a card
# - flip a coin
# - roll 1 or 2 dice
def getresponse(input):
    response = ""

    # formats input
    input = input.strip() # removes leading and trailing whitespaces
    input = input.lower() # makes text all lowercase
    
    

    if input.find("how do you say") > -1:

        language = ""
        lang = ""
        voiceIndex = 0
        restOfText = ""
        startPhrase = "how do you say"
        endPhrase = "in"

        startOfText = input.find(startPhrase) + 14 # gets the index at the start of the text
        oppEndPhrase = endPhrase[::-1] # flips the end phrase
        indexOfIn = input[::-1].find(oppEndPhrase) # gets the first (last bc it's flipped) of end phrase
        language = input[len(input) - indexOfIn : len(input)].strip() # getting language
        restOfText = input[startOfText : len(input) - indexOfIn - len(endPhrase)].strip() # getting rest of phrase

        if language.lower() == "french":
            lang = "fr"
            engine.setProperty('voice', voices[frenchIndex].id)
        elif language.lower() == "spanish":
            lang = "es"
            engine.setProperty('voice', voices[spanishIndex].id)
        elif language.lower() == "hebrew":
            lang = 'iw'
            engine.setProperty('voice', voices[hebrewIndex].id)
        elif language.lower() == 'russian':
            lang = 'ru'
            engine.setProperty('voice', voices[russianIndex].id)
        elif language.lower() == 'italian':
            lang = 'it'
            engine.setProperty('voice', voices[italianIndex].id)

        traslation = translator.translate(restOfText, dest=lang)

        response = traslation.text

    elif input.find("definition") > -1 or input.find("meaning") > -1:
        restOfText = ""

        startIndex = input.find("of") + 2
        restOfText = input[startIndex:]
        meaning = dictionary.meaning(restOfText)
        response = "The meaning of " + restOfText + " is. " + meaning.get(list(meaning)[0])[0]

    elif input.find("email") > -1: # send an email to ____
        if input.find("to") == -1:
            engine.say("Who would you like to send an email to")
            # message.append("Who would you like to send an email to")
            engine.runAndWait()
            name = recordAudio()
            # message.append(name)
        else:
            name = input[(input.find("to") + 2):].strip()
            # message.append(name)

        engine.say("What is " + name + "'s email")
        # message.append("What is " + name + "'s email")
        engine.runAndWait()

        text = recordAudio()
    
        # extracting email
        startEmail = (text[:text.find("at")].strip())
        endEmail = (text[text.find("at") + 2:].strip())
        to_email = str(startEmail + "@" + endEmail)
        to_email = to_email.replace(" ", "")
        print("Email: " + to_email)
        # message.append(to_email)

        engine.say("What would you like to say to " + name)
        # message.append("What would you like to say to " + name)
        engine.runAndWait()

            
        body = recordAudio()
        print("You said: " + body)
        # message.append(body)

        engine.say("You are sending an email to " + name + " saying " + body + ". Is this ok. Respond yes or no")
        # message.append("You are sending an email to " + name + " saying " + body + ". Is this ok. Respond yes or no")
        engine.runAndWait()

        text2 = recordAudio()
        # message.append(text2)

        if text2 == "yes":
            sendEmail(to_email.lower(), "", body, name)
            response = "Email sent"
        else:
            response = "Email disgarded"

    elif input.find("info") > -1: # give me info on ___
        search = input[input.find("on") + 2:].strip()

        try:
            results = wikipedia.summary(search, sentences=2)
            response = results
        except:
            response = "I cannot find information on " + search + ". Please make your request more specific"


    elif input.find("search") > -1: # search ____ or search for ___
        query = ""
        query = input[input.find("search") + 6:]
        if input.find("search for") > -1:
            query = input[input.find("search for") + 10:]
        webbrowser.open('https://www.google.com/search?q=' + query + '&oq=dog&aqs=chrome..69i57j69i59j69i60l4.545j0j15&sourceid=chrome&ie=UTF-8&safe=active&ssui=on')


    elif input.find("trivia") > -1:
        response = triviaQuestion(0)

    elif input.find("trivia game") > -1:
        triviaGame(1) # general knoledge

    elif input.find("joke") > -1:
        dadjoke = Dadjoke()
        joke = dadjoke.joke
        joke = joke.replace("?", ".... ")
        response = joke

    elif input.find("weather") > -1:
        response = getCurrentWeather(input)

    elif input.find("open") > -1:
        app = input[(input.find("open") + 4):].strip()
        app = app.capitalize()
        response = "Opening " + app
        os.system('open ' +d+'/%s.app' %app.replace(' ','\ '))
        
    elif input.find("card") > -1:
        card = ''
        suit = ''

        cardRand = int(random() * 14)
        suitRand = int(random() * 5)
        colorRand = int(random() * 3)

        cardList = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
        suitList = ['diamonds', 'hearts', 'spades', 'clubs']
        colorList = ['red', 'black']

        card = cardList[cardRand]
        suit = suitList[suitRand]

        response = "Your card is the " + card + " of " + suit
        print("card")

    elif input.find("hi") == 0 or input.find("hello") == 0 or input.find("hey") == 0:
        response = "How are you doing today"

    elif input.find("fine") > -1 or input.find("good") > -1 or input.find("ok") > -1 or input.find("well") > -1:
        response = "That's nice to hear"
    
    elif input.find("thank") > -1:
        response = "My Pleasure Sir"

    elif input.find("bad") > -1 or input.find("not good") > -1 or input.find("awful") > -1:
        response = "I'm sorry to hear that sir"

    elif input.find("spell") > -1:
        word = (input[input.find("spell") + 5:].strip())
        spelledWord = ""
        for w in list(word):
            spelledWord += w + ", "
        response = word + " is spelled, " + spelledWord

    elif input.find("flip a coin") > -1:
        r = int(random() * 2)
        results = ["heads", "tails"]
        response = "I flipped " + results[r]

    elif input.find("roll a di") > -1:
        r = int(random() * 7)
        response = str(r)
    
    elif input.find("roll two di") > -1:
        r = int(random() * 7)
        ra = int(random() * 7)
        response = str(r) + " and. " + str(ra)

    elif input.find("go to sleep") > -1 or input.find("stop") > -1:
        engine.say("Goodbye Sir")
        # message.append("Goodbye Sir")
        engine.runAndWait()
        # print(message)
        os._exit(0)

    else:
        response = "Sorry. I don't know that"

        

    return response


startJarvis()

# "https://www.google.com/maps/place/21+Pond+Path,+Woodbury,+NY+11797/@40.8119165,-73.4788062,15z/data=!3m1!4b1!4m5!3m4!1s0x89c28209271a4d8f:0xded52ac730fa79fe!8m2!3d40.8119006!4d-73.4700729"
