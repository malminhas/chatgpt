import os
import openai
import requests
import getpass, os
from IPython.display import Image as ImageDisplay, Markdown, display

class Dalle(object):
    def __init__(self):
        ''' Initialise Dalle instance.  If env variables are not set up look in .openAIKey and .openAIOrg files '''
        readFromFile = lambda file: open(file).read()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            os.environ['OPENAI_API_KEY'] = readFromFile('.openAIKey')
            os.environ['OPENAI_ORG_ID'] = readFromFile('.openAIOrg')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.org_id = os.getenv('OPENAI_ORG_ID')
        self.client = openai.OpenAI(api_key=self.api_key)
        self.models = self.client.models.list()

    def getModels(self):
        for model in self.models:
            print(f'model "{model.id}" owned by {model.owned_by}')
            
    def textToImage(self, prompt_text: str, target: str, engine: str='dalle', show: bool=False) -> str:
        response = self.client.images.generate(prompt=prompt_text, n=1, size="1024x1024")
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        with open(target, 'wb') as handler:
            handler.write(img_data)
        return image_url

    def displayImage(self, im_file: str, width: int=600):
        display(ImageDisplay(im_file, width=width))

if __name__ == '__main__':
    print(f'1. Create Dalle object')
    dH = Dalle()
    print(f'2. Get models')
    dH.getModels()
    prompt_text = 'an image showing a happy female Technical Program Manager'
    image_file = 'test_dalle.png'
    print(f'3. Generate image with prompt: "{prompt_text}"')
    image_url = dH.textToImage(prompt_text, image_file)
    print(f'generated image in local file: {image_file} of size {os.path.getsize(image_file)}')
    _ = dH.displayImage(image_file)
