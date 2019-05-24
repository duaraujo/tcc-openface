from kafka import KafkaConsumer
import face_recognition  
import PIL.Image
import msgpack
import pickle
import cv2
import io

rede = pickle.loads(open("encodings.pickle", "rb").read())
topic = "face-detected-test"
BROKER_URI = '10.10.3.159:9092'
count = 0

consumer = KafkaConsumer(
    topic,
    value_deserializer=lambda m: msgpack.unpackb(m, raw=False),
    bootstrap_servers=BROKER_URI)

for msg in consumer:
    data = msg.value        
    label = str(data['true_label'])        
    img = data['face_detected']        
    i = PIL.Image.open(io.BytesIO(img)).convert("RGB")
    path = "database/"+label+".png"
    i.save(path)
    
    picture = face_recognition.load_image_file(path)
    #list index out of range = dlib nao conseguiu encontrar um rosto na imagem
    #necessario normalizar antes de encodar
    unknown_face_encodings = face_recognition.face_encodings(picture)
    if len(unknown_face_encodings) > 0:
        encodings = face_recognition.face_encodings(picture)[0]           
    matches = face_recognition.compare_faces(rede["encodings"], encodings)
    rotulo = label + " - Desconhecido"
    if True in matches:
        count=count+1
        first_match_index = matches.index(True)
        rotulo = rede["names"][first_match_index]
    print (rotulo)
print ("Número de acertos: "+count)    