import urllib
from urllib.request import urlopen
import cv2
import cvlib as cv
import numpy as np


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def imageRecog(url):
    if url.startswith('https'):
        image = url_to_image(url)
    else:
        image = cv2.imread(url)
        image = cv2.cvtColor(image, cv2.IMREAD_COLOR)
    bbox, label, conf = cv.detect_common_objects(image)
    list_of_things = []
    list_of_genders = []
    list_of_gender_conf = []
    personInfo = []
    for i in range(len(label)):
        # object = object.lstrip("['")
        # object = object.rstrip("']")
        # confidence = confidence.lstrip("['")
        # confidence = confidence.rstrip("']")
        if label[i] not in list_of_things:
            list_of_things.append(label[i])

        if label[i] == 'person':
            label2, confidence = cv.detect_gender(image, False)

            if confidence[0] > confidence[1]: #Male
                confidence[0] = int(confidence[0] *100)
                list_of_genders.append(confidence[0])
                list_of_gender_conf.append(label2[0])
                personInfo = [list_of_genders, list_of_gender_conf]
            else:
                confidence[1] = int(confidence[1] *100)
                list_of_genders.append(confidence[1])
                list_of_gender_conf.append(label2[1])
                personInfo = [list_of_genders, list_of_gender_conf]
            faces, confidences = cv.detect_face(image)
    confidence = 0
    for i in range(len(conf)):
        confidence = confidence + conf[i]

    avgConf = confidence/len(conf)
    return list_of_things, avgConf, personInfo
