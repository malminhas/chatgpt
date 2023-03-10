import os
import openai
from IPython.display import Markdown, display

def initChatGpt():
    configureEnvVars(getAPIKey('.openAIKey'),getOrganisationId('.openAIOrg'))
    openai.organization = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
def configureEnvVars(key, org_id):
    # NB: host url is not prepended with \"https\" nor does it have a trailing slash.
    os.environ['OPENAI_API_KEY'] = key
    os.environ['OPENAI_ORG_ID'] = org_id

def getOrganisationId(file):
    with open(file) as f:
        key = f.read()
    return key
    
def getAPIKey(file):
    with open(file) as f:
        key = f.read()
    return key

def getResponse(text):
    completion = openai.ChatCompletion.create(
      model = 'gpt-3.5-turbo', 
      messages = [{'role': 'user', 'content': text}]
    )
    return completion.get('choices')[0].get('message').get('content')

def renderResponse(text):
    return display(Markdown(getResponse(text)))

if __name__ == '__main__':
    initChatGpt()
    question = 'Can you explain to me why the sky is blue?'
    print(f'Question:\n{question}')
    text = completeMe(f'{question}').strip()
    print(f'Completion:\n{text}')
    renderMe(text)