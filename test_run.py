import os
import cv2
import threading
import time

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import msgpack

from sklearn.metrics import accuracy_score

dir = "D:\cam_1"
topic_in = "face-recognized-test"
topic_out = "face-detected-test"
BROKER_URI = '10.10.3.159:9092'

def main():
    entries = os.listdir(dir)
    y_true = []
    y_predicted = []

    threading.Thread(target=send_batch_images(entries, y_true)).start()

    consumer = KafkaConsumer(
        topic_in,
        value_deserializer=lambda m: msgpack.unpackb(m, raw=False),
        bootstrap_servers=[BROKER_URI],
        auto_offset_reset='latest',
        enable_auto_commit=True)

    for msg in consumer:

        data = msg.value
        user_id = data['face_index']
        y_predicted.append(int(user_id))
        print("Message Received: %d." % user_id)


    if len(y_true) == len(y_predicted):
        print('Calculando as métricas...')
        print_metrics(y_true, y_predicted)
    else:
        print("Erro. y_true=%d e y_predicted=%" % (len(y_true), len(y_predicted)))


def print_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred) * 100
    print("Total de imagens: {0}.".format(len(y_true)))
    print("Acurácia: %.3f" % acc)
    #print("{}. {} appears {} times.".format(i, key, wordBank[key]))


def send_batch_images(entries, y_true):

    #time.sleep(10)
    producer = KafkaProducer(
        bootstrap_servers=BROKER_URI,
        value_serializer=lambda m: msgpack.packb(m, use_bin_type=True))

    face_index = 1
    faces_total = len(entries)
    for file_name in entries:
        path_filename = dir + '\\' + file_name

        img = cv2.imread(path_filename)
        ret, img_encoded = cv2.imencode('*.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

        msg_object = dict()
        msg_object['face_detected'] = img_encoded.tobytes()
        msg_object['face_index'] = face_index

        y_true.append(int(file_name[0:3]))

        producer.send(topic_out, msg_object).add_errback(on_send_error)
        #print("Enviado: ", face_index)  # For debug
        face_index += 1

    producer.flush()
    producer.close()


def on_send_error(excp):
    print(excp)


if __name__ == "__main__":
    main()
