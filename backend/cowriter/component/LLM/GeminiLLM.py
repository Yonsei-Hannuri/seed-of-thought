import os
from pathlib import Path
import json
import requests

class GeminiLLM:
    def __init__(self):
        secret_path = os.path.join(Path(__file__).parent.absolute(), 'secret', 'secret.json')
        with open(secret_path) as f:
            configs = json.load(f)
            self.url = configs['url']

        self.headers = {"Content-Type": "application/json"}

    def input(self, input_text):
        llm_input = {
            "contents": [
                {
                    "parts":[
                        {
                            "text":input_text
                        }
                    ]
                }
            ]
        }
        response = requests.post(
            self.url, 
            headers=self.headers, 
            json=llm_input
        )
        llm_ouput = response.json()['candidates'][0]
        finish_reason = llm_ouput['finishReason']
        if finish_reason == 'STOP':
            return llm_ouput['content']['parts'][0]['text'].replace("*", "")
        elif finish_reason == 'SAFETY':
            safeties = llm_ouput['safetyRatings']
            for safety in safeties:
                if safety['probability'] != 'NEGLIGIBLE':
                    category = safety['category']
                    if category == 'HARM_CATEGORY_SEXUALLY_EXPLICIT':
                        raise Exception('성적표현이 포함되어있는 것 같습니다.')
                    if category == 'HARM_CATEGORY_HATE_SPEECH':
                        raise Exception('혐오표현이 포함되어있는 것 같습니다.')
                    if category == 'HARM_CATEGORY_HARASSMENT':
                        raise Exception('혐오표현이 포함되어있는 것 같습니다.')
                    if category == 'HARM_CATEGORY_DANGEROUS_CONTENT':
                        raise Exception('위험한 내용이 포함되어있는 것 같습니다.')


