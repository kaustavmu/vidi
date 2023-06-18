# Vidi
Say hi to Vidi, an all-new personal assistant that can help individuals with visual impairment to gain a better understanding of the world around them. By implementing a camera, speaker, and microphone in a sleeker package, individuals with visual impairment can query the system and have it help them with a multitude of routines.
## Inspiration
A few years ago, one of us worked on a project to help individuals with visual impairment read restaurant menus. In reflecting on that pursuit, we realised that recent developments in LLM technology can act as an improved interface between these individuals and the world around them. 
## What it Does
A key issue with individuals who have visual impairment is difficulty in being independent. With over 200 million individuals with visual impairment and 40 million blind individuals all around the world, it's important that we try to leverage new technologies to benefit these people as well.

Vidi is a pair of glasses with a built in AI chatbot that can act as an AI chatbot, but also activate routines that will help the user with certain tasks. As of right now, we have two routines built into the system:
### 1. Finding an Object
When I lose or misplace something, I can just look for it. If I was unable to do that, how much harder would that be? Our first routine uses the inbuilt camera and YoloV8 to find objects that the user is looking for and tell them where they are.
### 2. Reading Text
It's challening for an individual with visual impairment to read text on anything physical in front or around them. Our second routine uses EasyOCR to try and detect text in the world around them.
## How We Built It
The system is built on a Raspberry Pi, equipped with a microphone, speaker, GPS, compass, and camera, along with a button for input. This package is located separate to the glasses, allowing our users to retain their dignity, while the glasses contain only the speaker and camera.

The software is as lightweight as possible, running on Python 3.9.
## Challenges We Ran Into
Trying to run computationally expensive AI models that are designed to optimize GPUs are a large challenge on the Raspberry Pi. We've tried to speed things up as much as possbile, but there's definitely more that we have in mind to improve on the product.
## Accomplishments That We're Proud Of
We're proud to have been able to design the glasses to be as sleek as it is, and fit all of the electronics in the box. The design is bulky, but for a prototype, we're quite proud of it. Additionally, we were able to optimize the software to run as fast as possible, with the exception of the AI inference, and we're happy to have been able to do that.
## What We Learned
As a project that sits on the edge between hardware and software, it was a great learning experience from all sides of the field.  
## What's Next for Vidi
Vidi is still in its infancy. Iterative improvements in the mechanical and hardware design will allow it to be more compact, while multiple more software features are planned for implementation, allowing individuals with visual impairment to activate even more routines and ease their daily lives.
