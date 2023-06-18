import os
import time
import cv2
import numpy as np
import sys

objecttofind = sys.argv[1]

#print("subprocess")

camquery = open("camquery/placeholder.txt", "w")
camquery.write("yolo")
camquery.close()

while not os.path.isfile("/home/kaustav/vidi/camresults/placeholder.txt"):
    continue
os.remove("/home/kaustav/vidi/camresults/placeholder.txt")
#print("camera done")

boxcheck = False
maskcheck = False
#textcheck = False

if os.path.isfile("/home/kaustav/vidi/camresults/boxes.npy"):
    boxes = np.load("/home/kaustav/vidi/camresults/boxes.npy") 
    boxcheck = True
    #print(boxes)
    os.remove("/home/kaustav/vidi/camresults/boxes.npy")

if os.path.isfile("/home/kaustav/vidi/camresults/masks.jpg"):
    masks = cv2.imread("/home/kaustav/vidi/camresults/masks.jpg")
    maskcheck = True
    #print(masks.shape)
    os.remove("/home/kaustav/vidi/camresults/masks.jpg")
'''
if os.path.isfile("/home/kaustav/vidi/camresults/text.npy"):
    text = cv2.imread("/home/kaustav/vidi/camresults/text.npy")
    textcheck = True
    #print(masks.shape)
    os.remove("/home/kaustav/vidi/camresults/text.npy")
'''
#print("checked")

directions = []

if boxcheck:
    directions = [("right" if float(x[0]) < 320 else "left") for x in boxes if x[2] == objecttofind]
#if text == None:
#    a = 0
#elif textcheck:
#    directions2 = [("right" if float(x[0]) > 320 else "left") for x in text if x[2].lower() == objecttofind.lower()]

#directions = directions1 + directions2
i = len(directions)
rights = directions.count("right")
lefts = directions.count("left")
if i == 0:
    speech = "No " + objecttofind + "s were found."
else:
    if i == 1:
        speech = "A total of " + str(i) + " " + objecttofind + " was found."
    else:
        speech = "A total of " + str(i) + " " + objecttofind + "s were found."
    speech = speech + " " + str(rights) + " on your right and " + str(lefts) + " on your left."
'''
i = len(directions)

if len(boxes) != 0:
    print(boxes
    i = len([1 for j in boxes if j[2] == objecttofind])
    directions = [("right" if float(x[0]) > 320 else "left") for x in boxes if x[2] == objecttofind]
    rights = directions.count("right")
    lefts = directions.count("left")
    if i == 1:
        speech = "A total of " + str(i) + " " + objecttofind + " was found."
    else:
        speech = "A total of " + str(i) + " " + objecttofind + "s were found."
    speech.append(" " + str(rights) + " are on your right and " + str(lefts) + " are on your left." )
else:
    speech = "A total of 0 items were found."
'''

#print(speech)

timestr = time.strftime("%Y%m%d-%H%M%S")
f = open("/home/kaustav/vidi/speakerqueue/" + timestr + ".txt", "w")
f.write(speech)
f.close()

pid = os.getpid()
#print(pid)
os.remove("PIDs/" + str(pid) + ".pid")

#print("finishedprocess")
