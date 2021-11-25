import csv
import cv2
import boto3
from gtts import gTTS
from playsound import playsound

def mainFUN():
    def imagerecon(name):
        l = []
        photo = name
        with open('credentials.csv', 'r') as input:
            next(input)
            reader = csv.reader(input)
            for line in reader:
                access_key_id = line[2]
                secret_access_key = line[3]

        client = boto3.client('rekognition', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key,
                              region_name='us-west-2')

        with open(photo, 'rb') as source_image:
            source_bytes = source_image.read()

        response = client.detect_labels(Image={'Bytes': source_bytes}, MaxLabels=5, MinConfidence=80)
        for label in response['Labels']:
            l.append(label['Name'])
        try:
            obj = l[0]
            obj2 = l[1]
            out="The Scanned Object is" + obj + "and/or" + obj2
        except:
            obj = l[0]
            out = "The Scanned Object is" + obj

        mytext = out
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("object.mp3")
        playsound('/Users/keval/PycharmProjects/pythonProject/object.mp3')

    def photocapture():
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("Scan")

        img_counter = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = "{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
                return img_name

        cam.release()

        cv2.destroyAllWindows()
    name = photocapture()
    imagerecon(name)

mainFUN()
