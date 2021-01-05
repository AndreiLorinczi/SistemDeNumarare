
# cu input file
# python3 people_counter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --input videos/example_01.mp4 --output output/output_01.avi
#
# de la camera web
# python3 people_counter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --output output/webcam_output.avi

# import the necessary packages
from classe.centroidtracker import CentroidTracker
from classe.trackableobject import TrackableObject
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

# parsam argumentele
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-i", "--input", type=str,
	help="path to optional input video file")
ap.add_argument("-o", "--output", type=str,
	help="path to optional output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
	help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip-frames", type=int, default=30,
	help="# of skip frames between detections")
args = vars(ap.parse_args())

# clasele SSD-ului de la mobilenet, practic putem recunoaste orice clasa
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# load model
print("[INFO-CONSOLA] Se incarca modelul...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# Daca o cale video nu a fost data, start webcam.
if not args.get("input", False):
	print("[INFO-CONSOLA] Se porneste web...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# Altfel luam video de la input
else:
	print("[INFO-CONSOLA] Se deschide fisierul video...")
	vs = cv2.VideoCapture(args["input"])

writer = None
W = None
H = None

#instantiem centeroid si countere
ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
trackers = []
trackableObjects = {}
totalFrames = 0
totalDown = 0
totalUp = 0

#fps counter
fps = FPS().start()

# bucla la frame-uri
while True:
	frame = vs.read()
	frame = frame[1] if args.get("input", False) else frame
	if args["input"] is not None and frame is None:
		break

	#facem resize la 500 px pentru a procesa mai repede video, de asemenea transformam de la bgr la rgb.
	frame = imutils.resize(frame, width=500)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# scriem pe disc
	if args["output"] is not None and writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(W, H), True)

	status = "In curs de asteptare"
	rects = []

    # pentru procesare mai puternica .

	if totalFrames % args["skip_frames"] == 0:
		
		status = "In curs de detectare"
		trackers = []


        # convertim frameul intr-un blob si il pasam mai departe la modelul de detectie
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
		net.setInput(blob)
		detections = net.forward()

		# bucla in detectii
		for i in np.arange(0, detections.shape[2]):
			# daca s-a precizat in parser o anumita confidenta se ia in calcul.
			confidence = detections[0, 0, i, 2]

			# filtram detectiile in functie de o confidenta anume altfel default
			if confidence > args["confidence"]:
                # extragem index
				idx = int(detections[0, 0, i, 1])

				# daca clasa de index actual nu e un obiect de tip persoana atunci continuam.
				if CLASSES[idx] != "person":
					continue

				# calculam (x,y) pentru obiectul gasit si construim box-ul
				box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
				(startX, startY, endX, endY) = box.astype("int")
                
                
                #construim un dreptunghi folosind dlib pornind de la box si apoi pornim trackerul
				tracker = dlib.correlation_tracker()
				rect = dlib.rectangle(startX, startY, endX, endY)
				tracker.start_track(rgb, rect)

				# adaug tracker actual in lista pentru a-l folosi la skipframe.
				trackers.append(tracker)
    # altfel, standard tracker pentru o rata de procesare mai buna
	else:
		# bucla peste trackere
		for tracker in trackers:
			# schimb status
			status = "In curs de urmarire"

			# update tracker
			tracker.update(rgb)
			pos = tracker.get_position()

			# salvam pozitia
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())

			# cream dreptunghiul
			rects.append((startX, startY, endX, endY))
    
    # desenam linia de mijloc pentru a determina daca persoanele urca sau coboara in video 
	cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)

	objects = ct.update(rects)

	# bucla peste obiectele trackuite
	for (objectID, centroid) in objects.items():
		to = trackableObjects.get(objectID, None)
		if to is None:
			to = TrackableObject(objectID, centroid)
		else:
            # diferenta dintre coordonatele de pe y ne va spune daca obiectul se deplaseaza in jos sau in sus 
            # negativ pentru sus si pozitiv pt jos
			y = [c[1] for c in to.centroids]
			direction = centroid[1] - np.mean(y)
			to.centroids.append(centroid)

			# verific daca obiectul a fost deja numarat
			if not to.counted:
				# daca directia e negativa numar.
				if direction < 0 and centroid[1] < H // 2:
					totalUp += 1
					to.counted = True

				# altfel daca e pozitiva numar jos..
				elif direction > 0 and centroid[1] > H // 2:
					totalDown += 1
					to.counted = True

		# salvam obiectele in dictionar
		trackableObjects[objectID] = to

		# desenam atat id-ul obiectului cat si centeroid-ul acestuia.
		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

	# info pt frame , countere
	info = [
		("Sus", totalUp),
		("Jos", totalDown),
		("Status", status),
	]

	for (i, (k, v)) in enumerate(info):
		text = "{}: {}".format(k, v)
		cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	# verificam sa vedem daca trebuie sa scriem pe disc
	if writer is not None:
		writer.write(frame)

	# afisam output pe frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# daca se apasa q se iese din bucla
	if key == ord("q"):
		break

	# update la frame.
	totalFrames += 1
	fps.update()

# oprim timer la fps si facem display la rezultate
fps.stop()
print("[INFO-OUTPUT] Durata: {:.2f}".format(fps.elapsed()))
print("[INFO-OUTPUT] Medie FPS: {:.2f}".format(fps.fps()))
print("[INFO-OUTPUT] Numar de persoane totale:",totalUp+totalDown)
print("[INFO-OUTPUT] Numar de persoane sus:",totalUp)
print("[INFO-OUTPUT] Numar de persoane jos:",totalDown)

if writer is not None:
	writer.release()

# stop camera stream
if not args.get("input", False):
	vs.stop()

else:
	vs.release()

cv2.destroyAllWindows()
