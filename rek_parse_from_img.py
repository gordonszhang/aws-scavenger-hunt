import io
import boto3
import re
import json
import urllib


def lambda_haldler(event, context):
    rekognition = boto3.client('rekognition', 'us-west-2')
    is_correct = "is not correct"
    targets = ["Clemson", "is", "cool"]

    fileName = 'input.jpg'
    # bucket = 'rekognition-examples-bucket'

    # assuming this is an http post method
    if event['httpMethod'] == 'POST':
        image = event['image']
        response = rekognition.detect_text(Image={'Bytes': image})

    # response = rekognition.detect_text(
    #    Image={'S3Object': {'Bucket': bucket, 'Name': fileName}})

    # Labels = TextDetections
    # Name = DetectedText

    found = []
    # pull score form db
    score = 3

    print('Detected labels for ' + fileName)
    for label in response['TextDetections']:
        # print (label['DetectedText'] + ' : ' + str(label['Confidence']))
        if label['DetectedText'] in targets:  # && not already found
            # flag as found in the db
            # add to found list
            found.append(label['DetectedText'])
    t = ""
    if is_correct == "is not correct":
        t += "image submission {} no valid records were found for your image".format(
            is_correct)
        t += "either you have already found this word, this word was not recognized, or"
        t += " this image does not contain a target word."
    else:
        # the found list contains all things the user found in this image
        t += "image submission {}".format(is_correct) + " you found _____"
        t += " you need to find ___."
    t += "Your score is {}".format(score)
    # Slack expects the body to be returned in this format
    body = {  # should also print score
        "text": t
    }
