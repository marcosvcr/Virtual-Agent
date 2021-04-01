from flask import Flask, request, Response, make_response, jsonify
import jsonpickle
import numpy as np
import cv2
import json
from processing import Motion
from processing import Detection
from utils import Compression, DataManager
from processing import Mask
from processing import Recognition

from ontology import DataSearch
from ontology import Extraction
from ontology import Morphology


# Initialize the Flask application
app = Flask(__name__)
motion = Motion.Motion()
detection = Detection.Detection()
maskDetection = Mask.Mask()
dataManager = DataManager.DataManager()
recognition = Recognition.Recognition()

morphology = Morphology.Morphology()
extraction = Extraction.Extraction()
search = DataSearch.DataSearch()

class Server:

    motion = None


    def __init__(self):
        print("Starting Server")
        super(Server, self)
        recognition.train()
        
        morphology.tagger()


    @app.route('/api/search', methods=['POST', 'GET'])
    def search():
        global search, extraction, morphology

        r = request.json

        morphology.tokenize(r["phrase"])
        morfology_phrase = morphology.getToken()
        
        extraction.namesHotkeys(morfology_phrase)
        toSearch = extraction.getSearch()
        
        if (toSearch['names']!= ''):
            search.search(toSearch)
            data = search.getdata()
        else:
            data=toSearch
            #data['names']=None
            data = [{'D': toSearch['D'], 'R': toSearch['R'], 'E': toSearch['E']}]
            #print("SEM NOMES")

        #print("Retorno: {}".format(data))
        
        return str(data)
        

    # route http posts to this method
    @app.route('/api/motion', methods=['POST'])
    def motion():
        global motion
        
        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        target = motion.detect(img)


        resp, _, _ = Compression.Compression.compress_nparr(target)
        return Response(response=resp, status=200,
                        mimetype="application/octet_stream")
        
        

    @app.route('/api/detection', methods=['POST'])
    def detection():
        global detection
        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        target =detection.detect(img)


        resp, _, _ = Compression.Compression.compress_nparr(target)
        return Response(response=resp, status=200,
                        mimetype="application/octet_stream")




    @app.route('/api/saveImage', methods = ['POST'])
    def saveImage():
        global dataManager
        r = request
        nparr = np.fromstring(r.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        target = dataManager.saveImage(img)
        if target == 1:
            print("Image stored successfully")
        elif target == 0:
            print("There was an error. Please try again")

        resp,_,_ = Compression.Compression.compress_nparr(target)
        return Response(response=resp, status=200,
                        mimetype="application/octet_stream")


    @app.route('/api/recognition', methods = ['GET', 'POST'])
    def recognition():
        global recognition
        r = request
        nparr = np.fromstring(r.data, np.uint8)
        img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        #rgb = img[:, :, ::-1]
        target = recognition.predict(img)
        resp,_,_ = Compression.Compression.compress_nparr(target)
        return Response(response=resp, status=200,
                        mimetype="application/octet_stream")




    @app.route('/api/setName', methods = ['POST', 'GET'])
    def setName():
        global dataManager
        r = request.json
        name = r["name"]
        dataManager.setTarget(name)
        return jsonify({"code":True})
        



    @app.route('/api/detectionMask', methods=['POST'])
    def detectionMask():
        global detection
        global maskDetection
        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        predictions =detection.detect(img)
        target = maskDetection.predict(img,predictions)
        print(target)

        resp, _, _ = Compression.Compression.compress_nparr(target)
        return Response(response=resp, status=200,
                        mimetype="application/octet_stream")


    def start_server(self):
        global app
        app.run(host = "0.0.0.0", port = 5000)
