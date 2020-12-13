import os, io
from google.cloud import vision_v1 as vision
from google.cloud.vision_v1 import types
import pandas as pd
import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

client = vision.ImageAnnotatorClient()

def detectText(img):
    with io.open(img, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    df = pd.DataFrame(columns=['description'])
    for text in texts:
        print('\n"{}"'.format(text.description))

        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])
        #
        # print('bounds: {}'.format(','.join(vertices)))

        df = df.append(
            dict(
                description=text.description,
                x0=text.bounding_poly.vertices[0].x,
                y0=text.bounding_poly.vertices[0].y,
                x1=text.bounding_poly.vertices[1].x,
                y1=text.bounding_poly.vertices[1].y,
                x2=text.bounding_poly.vertices[2].x,
                y2=text.bounding_poly.vertices[2].y,
                x3=text.bounding_poly.vertices[3].x,
                y3=text.bounding_poly.vertices[3].y,
            ),
            ignore_index=True
        )
    return df

FILE_NAME = sys.argv[1]
FOLDER_PATH = r'C:\PythonProjects\ReceiptOCR_Project\VisionAPI\image_receipts'
img = os.path.join(FOLDER_PATH, FILE_NAME)
df1 = detectText(img)
df1.to_csv('temp.csv', index=False)
