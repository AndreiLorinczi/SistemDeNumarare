# People Counter

# Requirements



-NumPy : "https://numpy.org/" version 1.19.4

-OpenCV : "https://pypi.org/project/opencv-python/" version 4.5.1

-dlib : "http://dlib.net/" version  19.21.1

-imutils : "https://github.com/jrosebr1/imutils" version 0.5.3

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





## FuturePlans



- Fix skipframes.
- Move to RaspberryPi





