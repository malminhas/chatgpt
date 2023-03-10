import io
import os
import boto3
from PIL import Image, ImageDraw, ImageFont

def getLabels(im_file, n = 10):
    response = None
    rek_client = boto3.client('rekognition')
    with open(im_file, "rb") as image:
        f = image.read()
        im_bytes = bytearray(f)
        max_labels = n
        response = rek_client.detect_labels(Image={'Bytes': im_bytes}, MaxLabels=max_labels)
    return response

def formatLabels(im_file, n = 10):
    response = getLabels(im_file, n)
    labels = [(item.get('Name'),item.get('Confidence'),item.get('Categories'),item.get('Instances')) for item in response.get('Labels')]
    for label in labels:
        print(label)
    return response

def drawBoundingBox(im_file, response):
    '''  import Image, ImageDraw, ImageFont ''' 
    modified_im_file = f'modified_{im_file}'
    with open(im_file, "rb") as image:
        f = image.read()
        im_bytes = bytearray(f)
        image = Image.open(io.BytesIO(im_bytes))
        font = ImageFont.truetype('arial.ttf', size=40)
        draw = ImageDraw.Draw(image)
        # Get all labels
        w, h = image.size
        for i, label in enumerate(response['Labels']):
            name = label['Name']
            # Draw all instancex box, if any
            for instance in label['Instances']:
                print(f'Found bounding box for "{name}"')
                bbox = instance['BoundingBox']
                x0 = int(bbox['Left'] * w) 
                y0 = int(bbox['Top'] * h)
                x1 = x0 + int(bbox['Width'] * w)
                y1 = y0 + int(bbox['Height'] * h)
                draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=10)
                draw.text((x0, y1), name, font=font, fill=(255, 0, 0))
                draw.text((x0, y1), name, fill=(255, 0, 0))
        image.save(modified_im_file)
    return modified_im_file

if __name__ == '__main__':
    im_file = 'generated_image.png'
    response = formatLabels(im_file)
    modified_file = drawBoundingBox(im_file,response)
    print(f'Generated modified file in {modified_file}')