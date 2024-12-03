import speech_recognition as sr
print(sr.__version__)

# creates intstance of Regognizer class
r = sr.Recognizer()

# creates audio file
harvard = sr.AudioFile('harvard.wav')
with harvard as source:
    audio = r.record(source)

print(type(audio))

# prints the text from wav file
print(r.recognize_google(audio))

