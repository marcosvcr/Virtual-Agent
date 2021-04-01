from __future__ import print_function
import requests
import json
from flask import jsonify
import cv2
import io
import zlib
import numpy as np
from utils import Compression
from utils import VoiceRecognition
import ast

#search = DataSearch.DataSearch()
recognition = VoiceRecognition.VoiceRecognition()


class Client:

    height = None
    width = None

    def __init__(self, _addr):

        self.addr = _addr
        
        self.search_url = self.addr + '/api/search'

        self.motion_url = self.addr + '/api/motion'
        self.detection_url = self.addr + '/api/detection'
        self.mask_url = self.addr + '/api/detectionMask'
        self.save_url = self.addr + '/api/saveImage'
        self.identify_person = self.addr + '/api/recognition'
        self.content_type = 'image/jpeg'
        self.set_name = self.addr + '/api/setName'
        self.headers = {'content-type': self.content_type}       




    def setDimension(self, _h, _w):
        height = _h
        width = _w


    def setName(self, name):
        print(name)
        r = requests.post(self.set_name, json={"name": name})
        return r.status_code

    def recognition(self):
        
        speech = recognition.listen()       
        
        phrase = {"phrase": speech }

        if (type(phrase["phrase"])== str):
            print("-> {}".format(speech))   
            response = self.get_search(phrase)
        else:
            response=None
        #response = self.get_search("ramal Guilherme Nunes")

        return response
    

    def get_search(self,phrase): #GUILHERME
                       
        response = requests.post(self.search_url, json=phrase)
        #print("TAGS: {}".format(tags))
        #print("DATAS: {}".format(response.text))

        response = ast.literal_eval(response.text) #dict

        return response

    def get_identification(self,img):
        _, img_encoded = cv2.imencode('.jpg', img)
        response = requests.post(self.identify_person, data=img_encoded.tostring(), headers = self.headers)
        data = Compression.Compression.uncompress_nparr(response.content)
        return data


    def post_image(self,img):
        _, img_encoded = cv2.imencode('.jpg', img)
        response = requests.post(self.motion_url, data=img_encoded.tostring(), headers = self.headers)

        data = Compression.Compression.uncompress_nparr(response.content)
        return data



    def detect_face(self, img):

        _, img_encoded = cv2.imencode('.jpg', img)
        response = requests.post(self.detection_url, data=img_encoded.tostring(), headers = self.headers)

        data = Compression.Compression.uncompress_nparr(response.content)
        return data

    def detect_mask(self, img):

        _, img_encoded = cv2.imencode('.jpg', img)
        response = requests.post(self.mask_url, data=img_encoded.tostring(), headers = self.headers)

        data = Compression.Compression.uncompress_nparr(response.content)
        return data

    def save_image(self, img):
        _,img_encoded = cv2.imencode('.jpg', img)
        response =requests.post(self.save_url, data = img_encoded.tostring(), headers = self.headers)

        data = Compression.Compression.uncompress_nparr(response.content)
        return data







