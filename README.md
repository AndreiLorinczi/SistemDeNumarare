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

.

├── classe

---  ├── __init__.py

---  ├── centroidtracker.py

--- └── trackableobject.py

├── mobilenet_ssd

---  ├── MobileNetSSD_deploy.caffemodel

---  └── MobileNetSSD_deploy.prototxt

├── videos

--- ├── example_01.mp4

--- ├──  example_02.mp4

--- ├──  example_03.mp4

--- ├──  example_06.mp4

--- ├──  example_07.mp4

├── output(optional)

│   ├── output_01.avi

│   └── output_02.avi
.
.
.
.

└── people_counter.py




Clasa CentroidTracker preia bounding box-ul obiectelor detectate si apoi foloseste un algoritm care asuma faptul ca perechile de centroizi(baricentre) cu distanta Euclidiana minima intre ele sunt acelasi obiect. 

Clasa TrackableObject e o simpla clasa de stocare care stocheaza diferite informatii despre obiectul curent.

Pentru detectie folosim un model de la Google, un single shot detector MobileNetSSD.


Faza 1 — Detectia: In cursul fazei de detectie mai costisitoare folosim un object tracker pentru a detecta daca obiecte noi au intrat in vedere si vedem daca putem gasi obiecte care sunt declarate disparute in timpul detectiei. Pentru fiecare obiect detectat folosim sau updatam object tracker cu coordonate noi. Deoarece acest process este destul de costisitor folosim acest proces odata la N frame-uri. 


Faza 2 — Tracking: In momentul in care nu detectam intram in faza de tracking. Pentru fiecare obiect detectat, creeam un obiect tracker pentru a face tracking obiectului care se misca in frame. Object tracker-ul este rapid si eficient decat detectorul. Folosim acest object tracker pana cand ajungem la N frame si apoi reaplicam detectorul. Acest proces se repeta de mai multe ori.



## Functionalities



Momentan proiectul este functional si stabil! 

- Implementat obiectele de tip trackableobject si centroidtracker

- Implementat argument parser

- Implementat functionalitate de baza si recunoastere persoane

- Implementat counter si display frame

- Implementat consola(ghid)

- Implementat skip frames




## Limitari&Bugs


- In functie de argumentul de confidenta dat exista cateva probleme de recunoastere pe diferite exemple video(spre exemplu o persoana este recunoscuta prea tarziu si orientatia sus/jos poate fi eronata ).

- De optimizat momentele de skipframes(momentele din stream peste care sar cand detectorul nu se afla in stare de detectie sau tracking)



## FuturePlans



- Fix skipframes.
- Move to RaspberryPi


## Bibliografie



- PyImageSearch 

https://www.pyimagesearch.com/ - site/forum specializat in domeniul Computer Vision.

-Despre SSD: 

https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/ 

https://arxiv.org/abs/1704.04861

- Object tracking: 

https://www.pyimagesearch.com/category/object-tracking/

https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
