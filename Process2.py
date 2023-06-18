import os
import time
import cv2
import numpy as np
import sys

#print("subprocess 2")

camquery = open("camquery/placeholder.txt", "w")
camquery.write("ocr")
camquery.close()

while not os.path.isfile("/home/kaustav/vidi/camresults/placeholder.txt"):
    continue
os.remove("/home/kaustav/vidi/camresults/placeholder.txt")
#print("camera done")

text = []

if os.path.isfile("/home/kaustav/vidi/camresults/text.npy"):
    text = np.load("/home/kaustav/vidi/camresults/text.npy")
    os.remove("/home/kaustav/vidi/camresults/text.npy")

#print("checked")

if text == []:
    speech = "No text was legible. You can try getting closer to the object or hold it at a different angle."
else:
    speech = ", ".join([i[2] for i in text])

#print(speech)

timestr = time.strftime("%Y%m%d-%H%M%S")
f = open("/home/kaustav/vidi/speakerqueue/" + timestr + ".txt", "w")
f.write(speech)
f.close()

pid = os.getpid()
#print(pid)
os.remove("PIDs/" + str(pid) + ".pid")

#print("finishedprocess")
