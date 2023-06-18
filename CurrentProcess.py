import subprocess
import os
import psutil
import time

import openai
openai.organization = "org-a1F5yEuczwOyZWJtZC22o4AM"
openai.api_key = "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"

from Speech2Text import speechtotext

def speak(text):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    f = open("/home/kaustav/vidi/speakerqueue/" + timestr + ".txt", "w")
    f.write(text)
    f.close()

def startProcess(args):
    process = subprocess.Popen(args)

    pid = process.pid
    #print(pid)
    pidfilename = "PIDs/" + str(pid) + ".pid"
    pidfile = open(pidfilename, 'w')
    pidfile.write(str(pid))
    pidfile.close()

#print("1")
userinput = "".join(speechtotext())
print("Your input: " + userinput)
#userinput = "Find me a rubik's cube."

#Step 1: Use GPT to Parse

with open("context.txt", "r") as f:
    context = f.read()

systemmsg = {"role": "system", "content": context}
usermsg = {"role": "user", "content": userinput}

MODEL_NAME = "gpt-4"

response = openai.ChatCompletion.create(model = MODEL_NAME, messages = [systemmsg, usermsg])["choices"][0]["message"]["content"]

try:
    response = eval(response)
except:
    speak("Sorry, I can't find that object.")
    exit()

#print(response)

#Step 2: Based on response, execute processes.

if response[0] == 0 or response[0] == 2:
    PIDs = [i[:-4] for i in os.listdir("PIDs")]
    for pid in PIDs:
        p = psutil.Process(int(pid))
        p.terminate()
        os.remove("PIDs/" + pid + ".pid")

if response[0] == 1 or response[0] == 2:
    speak("Sure, give me let me take a look.")
    startProcess(["./vidivenv/bin/python3", "Process1.py", response[1]])
elif response[0] == 3:
    speak("Sorry, I can't find that object.")
elif response[0] == 4:
    systemmsg = {"role": "system", "content": "You are Vidi, an AI chatbot. Answer the user's questions but keep the responses short and sweet." }
    usermsg = {"role": "user", "content": userinput}

    MODEL_NAME = "gpt-4"

    response2 = openai.ChatCompletion.create(model = MODEL_NAME, messages = [systemmsg, usermsg])["choices"][0]["message"]["content"]
    speak(response2)
elif response[0] == 5:
    speak("Give me a moment, it takes me a little bit of time to read.")
    startProcess(["./vidivenv/bin/python3", "Process2.py"])
