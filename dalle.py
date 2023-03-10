import os
import openai
import requests
import getpass, os
from IPython.display import Image as ImageDisplay, Markdown, display

def initDalle():
    configureEnvVars(getAPIKey('.openAIKey'),getOrganisationId('.openAIOrg'))
    openai.organization = os.getenv('OPENAI_ORG_ID')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    models = openai.Model.list()

def configureEnvVars(key, org_id):
    # NB: host url is not prepended with \"https\" nor does it have a trailing slash.
    os.environ['OPENAI_API_KEY'] = key
    os.environ['OPENAI_ORG_ID'] = org_id

def getAPIKey(file):
    with open(file) as f:
        key = f.read()
    return key

def getOrganisationId(file):
    with open(file) as f:
        key = f.read()
    return key

def textToImage(prompt_text, target, engine='dalle', show=False):
    response = openai.Image.create(prompt=prompt_text, n=1, size="1024x1024")
    image_url = response['data'][0]['url']
    img_data = requests.get(image_url).content
    with open(target, 'wb') as handler:
        handler.write(img_data)
    return image_url

def displayImage(im_file, width=600):
    display(ImageDisplay(im_file, width=width))
    
if __name__ == '__main__':
    initDalle()
    prompt_text = 'an image showing a happy female Technical Program Manager'
    image_file = 'test_dalle.png'
    image_url = textToImage(prompt_text, image_file)
    print(f'generated image {image_url} of size {os.path.getsize(image_file)}')
    displayImage(image_file)