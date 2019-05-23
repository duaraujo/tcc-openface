# USAGE
# python reconhecimento_facial.py --encodings encodings.pickle

import face_recognition
import imutils
import argparse
import pickle
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

#video_capture = cv2.VideoCapture('rtsp://server:qawsed@cameras.institutoitn.com.br:554/cam/realmonitor?channel=6&subtype=0')
video_capture = cv2.VideoCapture('rtsp://itn:1q2w3e4r@10.10.3.161:554/cam/realmonitor?channel=1&subtype=0')
#video_capture = cv2.VideoCapture(0)

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
                ret, frame = video_capture.read()
	
                #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                small_frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    
                rgb_small_frame = small_frame[:, :, ::-1]

                if process_this_frame:

                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                        face_names = []

                        for encoding in face_encodings:
		
                                matches = face_recognition.compare_faces(data["encodings"],
                                encoding)
                                name = "Desconhecido"
		
                                if True in matches:
                                        first_match_index = matches.index(True)
                                        name = data["names"][first_match_index]

                                face_names.append(name)

                process_this_frame = not process_this_frame	

                for (top, right, bottom, left), name in zip(face_locations, face_names):

                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4
        
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

video_capture.release()
cv2.destroyAllWindows()
