from flask import Flask, Response
from kafka import KafkaConsumer
import face_recognition  
import PIL.Image
import argparse
import msgpack
import pickle
import cv2
import io

print("[INFO] loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

topic = "face-detected-test"

consumer = KafkaConsumer(
    topic,
    value_deserializer=lambda m: msgpack.unpackb(m, raw=False),
    bootstrap_servers=['10.10.3.159:9092'])
 
# Set the consumer in a Flask App
app = Flask(__name__)

@app.route('/video', methods=['GET'])
def video():
    return Response(
        get_video_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream():
    for msg in consumer:
        data = msg.value        
        label = str(data['true_label'])        
        img = data['face_detected']        
        i = PIL.Image.open(io.BytesIO(img)).convert("RGB")
        path = "database/"+label+".png"
        i.save(path)
        
        picture = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(picture)[0]
        print(encoding)
        data = pickle.loads(open("encodings.pickle", "rb").read())
        
        matches = face_recognition.compare_faces(data["encodings"], encoding)
 
        if matches[0] == True:
            print(label)
        else:
            print("Not found")
        
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + img + b'\r\n\r\n')

if __name__ == "__main__":
    app.run(host='localhost', debug=True)