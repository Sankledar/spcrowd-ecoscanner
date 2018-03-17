import api_client.auth as auth
import os
import io
import json
import math
# Imports the Google Cloud client library
#from google.cloud import vision
#from google.cloud.vision import types

from google.cloud import vision_v1p1beta1 as vision
from google.cloud.vision_v1p1beta1 import types

from google.protobuf.json_format import MessageToJson

def annotate_image(imagePath):
    apiClient = auth.get_Api_client()

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=apiClient._credentials)

    # The name of the image file to annotate
    # file_name = os.path.join(os.path.dirname(__file__), imagePath)
    file_name = imagePath

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    features = [
        types.Feature(type=types.Feature.LABEL_DETECTION, max_results=8),
        types.Feature(type=types.Feature.LOGO_DETECTION, max_results=8),
        types.Feature(type=types.Feature.TEXT_DETECTION, max_results=8),
        types.Feature(type=types.Feature.WEB_DETECTION, max_results=15),
        # types.Feature(type=types.Feature., max_results=8),
    ]
    request = {
        'image': image,
        'features': features,
    }
    resp = client.annotate_image(request)
    # labels = resp.label_annotations
    return resp

def annotate_image_batch(imagePathes):
    apiClient = auth.get_Api_client()

    # Instantiates a client
    client = vision.ImageAnnotatorClient(credentials=apiClient._credentials)

    features = [
        types.Feature(type=types.Feature.LABEL_DETECTION),
        types.Feature(type=types.Feature.LOGO_DETECTION),
        types.Feature(type=types.Feature.TEXT_DETECTION),
        types.Feature(type=types.Feature.WEB_DETECTION),
        # types.Feature(type=types.Feature., max_results=8),
    ]
    requests = []

    for imagePath in imagePathes:
        pass
        # The name of the image file to annotate
        file_name = imagePath

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)
    
        request = {
            'image': image,
            'features': features,
        }
        requests.append(request)
    responses = []
    i = 0
    batch = 10
    while i < len(requests):
        to = min(i+batch, len(requests))
        resp = client.batch_annotate_images(requests[i:to])
        i = i+batch
        for response in resp.responses:
            respStr = MessageToJson(response)
            tt = json.loads(respStr)
            responses.append(tt)
    return responses

def annotate_image_json(imagePath):
    return MessageToJson(annotate_image(imagePath))

def annotate_image_batch_json(imagePathes):
    batchResult = annotate_image_batch(imagePathes)
    return json.dumps({'data':batchResult}, indent=3)