import pyttsx3
import os
import time

engine = pyttsx3.init();
engine.setProperty('voice', 'english_rp+f3')

while True:
    files = sorted([i for i in os.listdir("speakerqueue")])
    #print(files)
    for file in files:
        #print("speakerfile", file)
        time.sleep(0.2)
        f = open("/home/kaustav/vidi/speakerqueue/" + file)
        speech = f.read()
        print(speech)
        engine.say(speech)
        engine.runAndWait()
        os.remove("/home/kaustav/vidi/speakerqueue/" + file)
        
