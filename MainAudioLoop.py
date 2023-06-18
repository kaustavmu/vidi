import sys
from daqhats import hat_list, HatIDs, mcc118
import wave
import struct
import gpiozero as g
import subprocess
import cv2

CH = 7

board_list = hat_list(filter_by_id = HatIDs.ANY)
entry = board_list[0]
add = entry.address
board = mcc118(entry.address)
if not board_list:
    print("No boards found")
    sys.exit()

button = g.Button(23)

while True:
    while not button.is_pressed:
        continue
    #cv2.waitKey(0)
    frames = []
    #i = 0
    while button.is_pressed:
        #while i < 20000:
        frames.append(board.a_in_read(CH))
        #i += 1
        
    w = wave.open('test1.wav', 'wb')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(8000)
    allframes = [int(i*10000) for i in frames]
    data = struct.pack('h' * len(allframes), *allframes)
    w.writeframes(data)
    w.close()
    
    p = subprocess.Popen(["./vidivenv/bin/python3", "CurrentProcess.py"])
