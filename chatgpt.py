import os
import openai
import tiktoken
from IPython.display import Markdown, display
from forex_python.converter import CurrencyRates

#DEFAULT_MODEL = 'gpt-3.5-turbo'
DEFAULT_MODEL = 'gpt-4'
VALID_MODELS = ['gpt-4','gpt-3.5-turbo']

class ChatGPT(object):
    def __init__(self, model=DEFAULT_MODEL):
        assert(self.isValidModel(model))
        self._model = model
        self._encoding = tiktoken.encoding_for_model(self.model).name
        try:
            self._rate = CurrencyRates().get_rate('USD', 'GBP')
        except Exception as e:
            print(f'Exception on currency rate: {e}')
            print(f'Using rate of 0.82')
            self._rate = 0.82
        os.environ['OPENAI_API_KEY'] = self.readFromFile('.openAIKey')
        os.environ['OPENAI_ORG_ID'] = self.readFromFile('.openAIOrg')
        openai.organization = os.getenv("OPENAI_ORG_ID")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def readFromFile(self, file):
        with open(file) as f:
            key = f.read()
        return key

    @property
    def model(self):
        return self._model
    
    @property
    def encoding(self):
        return self._encoding
    
    def renderCompletion(self, text):
        return display(Markdown(text))

    def isValidModel(self, model):
        if model in VALID_MODELS:
            return True
        return False

    def getCompletion(self, text, getTokens=False):
        tokens = cost = 0
        try:
            completion = openai.ChatCompletion.create(
              model = self.model,
              messages = [{'role': 'user', 'content': text}]
            )
            content = completion.get('choices')[0].get('message').get('content').strip()
            tokens = completion.get('usage').get('prompt_tokens')
            cost = self.getCompletionCost(tokens, self.model)
        except Exception as e:
            content = f'ERROR: {e}'
        if getTokens:
            return content, tokens, cost
        return content

    def getCompletionCost(self, tokens, model):
        cost = 0
        if model == 'gpt-4':
            cost = (tokens/1024) * 0.06 * self._rate
        elif model == 'gpt-3.5-turbo':
            cost = (tokens/1024) * 0.002 * self._rate
        return round(cost, 6)

if __name__ == '__main__':
    for i,(model, encoding) in enumerate([('gpt-4','cl100k_base'),('gpt-3.5-turbo','cl100k_base')]):
        print(f'---- {i+1} Testing model={model}, encoding={encoding} ----')
        cgpt = ChatGPT(model)
        assert(cgpt.model == model)
        assert(cgpt.encoding == encoding)
        prompt = 'Can you explain to me why the sky is blue?'
        completion, tokens, cost = cgpt.getCompletion(prompt, getTokens=True)
        print(f'Using model="{cgpt.model}" with encoding="{cgpt.encoding}".\nPrompt={prompt}\nCompletion (token count={tokens}, cost=£{cost})=\n{completion}')
        cgpt.renderCompletion(completion)
