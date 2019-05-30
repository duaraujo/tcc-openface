import sys
import time
import cv2
from kafka import KafkaProducer

topic = "face-detected-test"

def publish_video(video_file):

    producer = KafkaProducer(bootstrap_servers='10.10.3.159:9092')

    video = cv2.VideoCapture(video_file)
    
    print('publishing video...')

    while(video.isOpened()):
        success, frame = video.read()

        if not success:
            print("bad read!")
            break
        
        ret, buffer = cv2.imencode('.jpg', frame)

        producer.send(topic, buffer.tobytes())

        time.sleep(0.2)
    video.release()
    print('publish complete')

def publish_camera():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')    
    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(topic, buffer.tobytes())            
            time.sleep(0.2)
    except:
        print("\nExiting.")
        sys.exit(1)

    
    camera.release()

if __name__ == '__main__':
    
    #if(len(sys.argv) > 1):
    #    video_path = sys.argv[1]
    publish_video("database/videos/output.mp4")
    #else:
    #    print("publishing feed!")
    #    publish_camera()