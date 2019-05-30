import os
import cv2
import msgpack
from kafka import KafkaProducer

dir = "D:\cam_1"
topic = "face-detected-test"
BROKER_URI = '10.10.3.159:9092'

def main():
    entries = os.listdir(dir)
    producer = KafkaProducer(
        bootstrap_servers=BROKER_URI,
        value_serializer=lambda m: msgpack.packb(m, use_bin_type=True))

    cv2.imshow("PRODUCER", cv2.imread("database/click.png"))
    cv2.waitKey(0)
    for file_name in entries:
        path_filename = dir + '\\' + file_name
        
        img = cv2.imread(path_filename)
        ret, img_encoded = cv2.imencode('*.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

        cv2.imshow("PRODUCER", img)
        
        msg_object = dict()
        msg_object['faceDetected'] = img_encoded.tobytes()
        msg_object['face_index'] = file_name[0:3]

        producer.send(topic, msg_object).add_errback(on_send_error)
        print(path_filename)

def on_send_error(excp):
    print(excp)

if __name__ == "__main__":
    main()