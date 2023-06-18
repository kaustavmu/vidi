import subprocess
import time
import os

folders = ["PIDs", "speakerqueue", "camquery", "camresults"]

for folder in folders:
    for i in os.listdir(folder):
        os.remove(folder + "/" + i)

processes = ["CameraLoop.py", "SpeakerPlayer.py", "MainAudioLoop.py"]

for process in processes:
    subprocess.Popen(["./vidivenv/bin/python3", process])

time.sleep(3)

timestr = time.strftime("%Y%m%d-%H%M%S")
f = open("/home/kaustav/vidi/speakerqueue/" + timestr + ".txt", "w")
f.write("Welcome to Vidi.")
f.close()
