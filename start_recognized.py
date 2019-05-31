from kafka import KafkaConsumer
from kafka import KafkaProducer
import face_recognition  
import PIL.Image
import argparse
from time import sleep
import numpy as np
import msgpack
import pickle
import cv2
import io

# python start_recognized.py  --encodings encodings.pickle --topic1 face-detected-test --topic2 face-recognized-test
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--broker", type=str, required=False, default="10.10.3.159:9092", help="informe o broker")
ap.add_argument("-e", "--encodings", required=True, help="caminho para os encodings das faces")
ap.add_argument("-t1", "--topic1", type=str, required=True, help="topic face-detected-test")
ap.add_argument("-t2", "--topic2", type=str, required=True, help="topic face-recognized-test")
args = vars(ap.parse_args())

rede = pickle.loads(open(args["encodings"], "rb").read())

topic = args["topic1"]
topic2 = args["topic2"]
BROKER_URI = args["broker"]

consumer = KafkaConsumer(
    topic,
    value_deserializer=lambda m: msgpack.unpackb(m, raw=False),
    bootstrap_servers=BROKER_URI)

producer = KafkaProducer(
        bootstrap_servers=BROKER_URI,
        value_serializer=lambda m: msgpack.packb(m, use_bin_type=True)) 

for msg in consumer:    
    data = msg.value    
    img = data['face_detected']  
    data['id_user'] = '0'   
    
    i = PIL.Image.open(io.BytesIO(img)).convert("RGB")    
    unknown_face_encodings = face_recognition.face_encodings(np.array(i))       
    if len(unknown_face_encodings) > 0:
        unknown_face_encoding = unknown_face_encodings[0]               
    
    matches = face_recognition.compare_faces(rede["encodings"], unknown_face_encoding)    
    
    if True in matches:  
        first_match_index = matches.index(True)      
        data['id_user'] = rede["names"][first_match_index] 
        print("Deu matche do ["+data['id_user'] +"] com o ["+ data['face_index']+"]")               
    

    producer.send(topic2, data)
    #sleep(15)