from ultralytics import YOLO
import cv2
from ultralytics.yolo.utils.plotting import Annotator
from picamera2 import Picamera2, Preview
import torch
import numpy as np
import os
import easyocr
import time

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1440)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)

model = YOLO('yolov8n.pt')
names = model.names
#names = {names[key]: key for key in names}

picam2.start()

reader = easyocr.Reader(['en'])

while True:
    while os.listdir("camquery/") == []:
        continue
    time.sleep(0.2)
    with open("camquery/placeholder.txt", "r") as f:
        which = f.read()
    os.remove("camquery/placeholder.txt")
    frame = picam2.capture_array()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite("pleasework.jpg", img)
    #print(which)
    if which == "yolo":
        results = model.predict(img)
        for result in results:
            #masks = result.masks
            boxes = result.boxes
            if boxes:
                returnarray = []
                for box in boxes:
                    xyxy = box.xyxy[0]
                    x = (xyxy[0] + xyxy[2]) * 0.5
                    y = (xyxy[1] + xyxy[3]) * 0.5
                    clss = names[box.cls[0].item()]
                    returnarray.append([x.item(), y.item(), clss])
                #print(returnarray)
                np.save("camresults/boxes.npy", np.array(returnarray))
            #if masks:
            #    msk = np.array(masks.data)
            #    cv2.imwrite("camresults/masks.jpg", np.uint8(msk*255)[0])
    if which == "ocr":
        textresults = reader.readtext(img)
        #print(textresults)
        textreturn = []
        for text in textresults:
            #print(text)
            if text[2] > 0.1:
                cords = text[0]
                x = 0.25 * (cords[0][0] + cords[1][0] + cords[2][0] + cords[3][0])
                y = 0.25 * (cords[0][1] + cords[1][1] + cords[2][1] + cords[3][1])
                textreturn.append([x, y, text[1]])
                #print(textreturn)
        if textreturn != []:
            np.save("camresults/text.npy", np.array(textreturn))
    camresults = open("camresults/placeholder.txt", "w")
    camresults.close()

