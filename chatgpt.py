import os
import openai
import tiktoken
from IPython.display import Markdown, display
from forex_python.converter import CurrencyRates

DEFAULT_MODEL = 'gpt-4'
VALID_MODELS = ['gpt-4','gpt-3.5-turbo']

class ChatGPT(object):
    def __init__(self, model=DEFAULT_MODEL):
        isValidModel = lambda model: model in VALID_MODELS
        assert(isValidModel(model))
        self._model = model
        self._encoding = tiktoken.encoding_for_model(self.model).name
        try:
            self._rate = CurrencyRates().get_rate('USD', 'GBP')
        except Exception as e:
            print(f'Exception on currency rate: {e}')
            print(f'Using rate of 0.82')
            self._rate = 0.82
        readFromFile = lambda file: open(file).read()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            os.environ['OPENAI_API_KEY'] = readFromFile('.openAIKey')
            os.environ['OPENAI_ORG_ID'] = readFromFile('.openAIOrg')
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.org_id = os.getenv('OPENAI_ORG_ID')
        self.client = openai.OpenAI(api_key=self.api_key)
        self.models = self.client.models.list()

    @property
    def model(self):
        return self._model
    
    @property
    def encoding(self):
        return self._encoding
    
    def renderCompletion(self, text):
        return display(Markdown(text))

    def getCompletion(self, text, getTokens=False):
        tokens = cost = 0
        try:
            completion = self.client.chat.completions.create(model = self.model, messages = [{'role': 'user', 'content': text}])
            content = completion.choices[0].message.content.strip()
            tokens = completion.usage.prompt_tokens
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
        print(f'---- {i+1}. Testing model={model}, encoding={encoding} ----')
        cgpt = ChatGPT(model)
        assert(cgpt.model == model)
        assert(cgpt.encoding == encoding)
        prompt = 'Can you explain to me why the sky is blue?'
        completion, tokens, cost = cgpt.getCompletion(prompt, getTokens=True)
        print(f'Using model="{cgpt.model}" with encoding="{cgpt.encoding}".\nPrompt={prompt}\nCompletion (token count={tokens}, cost=£{cost})=\n{completion}')
        cgpt.renderCompletion(completion)
