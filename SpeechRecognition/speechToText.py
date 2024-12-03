# import library
import speech_recognition as sr
from googletrans import Translator, constants
from pprint import pprint
import pyttsx3

# init the Google API translator
translator = Translator()
# text to speach
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.5)

def engToFrench(text):
    traslation = translator.translate(text, dest="fr")
    return traslation.text

# voices
voices = engine.getProperty('voices')
fr_voice = engine.setProperty('voice', voices[7].id)
en_voice = engine.setProperty('voice', voices[0].id)

# for i in range(35):
#     engine.setProperty('voice', voices[i].id) #changing index changes voices but ony 0 and 1 are working here
#     engine.say('Bounjour tout le monde. Comment ça va')
#     engine.runAndWait()

# instance of Recognizer class
r = sr.Recognizer()


def listning():
    # set source to microphone input
    with sr.Microphone() as source:
        print("Say Something: ")
        # listen to the source
        audio = r.listen(source)

    try:
        # convert audio to text
        text = r.recognize_google(audio)
        engine.setProperty('voice', voices[0].id)
        print("You said: " + text)
        engine.say(text)
        print(engToFrench(text))
        engine.setProperty('voice', voices[3].id)
        engine.say(engToFrench(text))
        engine.runAndWait()
    except:
        # if audio isn't recognized
        print("Could not recognize your voice")

    while text != "stop":
        # set source to microphone input
        with sr.Microphone() as source:
            print("Say Something: ")
            # listen to the source
            audio = r.listen(source)

        try:
            # convert audio to text
            text = r.recognize_google(audio)
            engine.setProperty('voice', voices[0].id)
            print("You said: " + text)
            engine.say(text)
            print(engToFrench(text))
            engine.setProperty('voice', voices[3].id)
            engine.say(engToFrench(text))
            engine.runAndWait()
        except:
            # if audio isn't recognized
            print("Could not recognize your voice")

listning()
