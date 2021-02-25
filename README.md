# Sistem de numarare al persoanelor folosind computer vision
Sistemul de numarare a persoanelor este o aplicatie care are ca scop recunoasterea si urmarirea sensului de deplasare a persoanelor, aceasta indicand atat numarul de persoane ce se afla intr-un stream video cat si sensul de deplasare al acestora.

# Requirements

Pentru a utiliza aceasta aplicatie avem nevoie de urmatoarele librarii python:



-NumPy : "https://numpy.org/" version 1.19.4

-OpenCV : "https://pypi.org/project/opencv-python/" version 4.5.1

-dlib : "http://dlib.net/" version  19.21.1

-imutils : "https://github.com/jrosebr1/imutils" version 0.5.3

Si de modelul de detector:

-MobileNetSSD: "https://github.com/chuanqi305/MobileNet-SSD" 





## Project structure & Usage

├── classe

---  ├── centroidtracker.py

--- └── trackableobject.py

├── mobilenet_ssd

---  ├── MobileNetSSD_deploy.caffemodel

---  └── MobileNetSSD_deploy.prototxt

├── videos

--- ├── example_01.mp4

....

├── output(optional)

--- ├── output_01.avi

....

└── Sistem_de_numarare.py



## Functionalities



Momentan proiectul este functional si stabil! 

- Implementat obiectele de tip trackableobject si centroidtracker

- Implementat argument parser

- Implementat functionalitate de baza si recunoastere persoane

- Implementat counter si display frame

- Implementat consola(ghid)

- Implementat skip frames




## Limitari&Bugs


- In functie de argumentul de confidenta dat exista cateva probleme de recunoastere pe diferite exemple video(spre exemplu o persoana este recunoscuta prea tarziu si astfel sensul de deplasare poate fi eronat ).

- De optimizat momentele de skipframes(momentele din stream peste care sar cand detectorul nu se afla in stare de detectie sau tracking)



## FuturePlans



- Fix skipframes.
- Move to RaspberryPi





