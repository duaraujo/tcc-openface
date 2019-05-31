from flask import Flask, Response, render_template
from kafka import KafkaConsumer
import face_recognition  
import PIL.Image
import msgpack
import pickle
import cv2
import io

print("Carregar rede...")
rede = pickle.loads(open("encodings.pickle", "rb").read())
topic = "face-detected-test"

consumer = KafkaConsumer(
    topic,
    value_deserializer=lambda m: msgpack.unpackb(m, raw=False),
    bootstrap_servers=['10.10.3.159:9092'])
 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video', methods=['GET'])
def video():
    return Response(
        get_video_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame')


def get_video_stream():
    count = 1
    for msg in consumer:
        data = msg.value        
        #id = str(data['id'])        
        img = data['faceDetected']        
        i = PIL.Image.open(io.BytesIO(img)).convert("RGB")
        path = "database/"+str(count)+".png"
        i.save(path)
        count +=1

        unknow_picture = face_recognition.load_image_file(path)
        unknow_face_encodings = face_recognition.face_encodings(unknow_picture)
        
        if(len(unknow_face_encodings) > 0):
            unknow_face_encodings = unknow_face_encodings[0]
            matches = face_recognition.compare_faces(rede["encodings"], unknow_face_encodings)
            if True in matches:
                first_match_index = matches.index(True)
                rotulo = rede["names"][first_match_index]
            print (rotulo)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + img + b'\r\n\r\n')

if __name__ == "__main__":
    app.run(host='localhost', debug=True)