from inspect import getframeinfo
import json
import cv2
from collections import deque
import numpy as np
IMAGE_HEIGHT , IMAGE_WIDTH = 128, 128
SEQUENCE_LENGTH = 25
CLASSES_LIST = ["stand", "jump"]
from tensorflow import keras
model = keras.models.load_model('./model.h5')

PREDICTED_CLASS_NAME=''
HEART_RATE=0
def predict_on_video(output_file_path, SEQUENCE_LENGTH):
   
    vid = cv2.VideoCapture("D:/Summer/exergame/jump/54.mp4")
    original_video_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(original_video_width,original_video_height)
    
    frames_queue = deque(maxlen = SEQUENCE_LENGTH)

    predicted_class_name = ''

    while True:

            ok, frame = vid.read() 
             
            # cv2.imshow('frame', frame)
            if not ok:
                break

            resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
            
            normalized_frame = resized_frame / 255

            frames_queue.append(normalized_frame)

            if len(frames_queue) == SEQUENCE_LENGTH:

                predicted_labels_probabilities = model.predict(np.expand_dims(frames_queue, axis = 0))[0]
                predicted_label = np.argmax(predicted_labels_probabilities)

                predicted_class_name = CLASSES_LIST[predicted_label]
                PREDICTED_CLASS_NAME=predicted_class_name
            print(predicted_class_name)
            f=cv2.resize(frame, (400, 540))
            cv2.imshow('frame', f)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    vid.release()
    
predict_on_video("D:/Summer/exergame/outputvideos/a.mp4",SEQUENCE_LENGTH)
# from flask import Flask,request,jsonify

# app = Flask(__name__)
   
  
# @app.route("/")
# def home():
#     print("ok")
#     return "boh!"
# @app.route("/sensor/")
# def sensor():
#     return "ok"
# @app.route("/getactionpulse/")
# def getactionpulse():
#     # print(request.args.get.sensor)
#     print("hello")
#     jsonresponse={"action":PREDICTED_CLASS_NAME,"bpm":0}
#     return jsonify(jsonresponse) 
    
# if __name__=="__main__":
#     app.run(host="localhost",port=3000)
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
class handler(BaseHTTPRequestHandler):

    def do_getfromunity(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'action': PREDICTED_CLASS_NAME, 'bpm': HEART_RATE}).encode())

    def do_gettingsensorreadings(self):
        message="hello"
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        message = query_components["sensor"]
        HEART_RATE=(float)(query_components["sensor"])
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        if self.path=='/getfromunity':
            self.do_getfromunity()
        else:
            self.do_gettingsensorreadings()

with HTTPServer(('', 3000), handler) as server:
    server.serve_forever()

