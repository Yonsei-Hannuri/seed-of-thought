import requests
import time
import datetime
import json
import os
from pathlib import Path

class ElasticSearchClient:
    
    def __init__(self):
        configs_file_path = os.path.join(Path(__file__).parent.absolute(), 'secret', 'configs.json')
        with open(configs_file_path) as f:
            configs = json.load(f)
        self.es_url = configs['esUrl']

    def save_detgori_sentences(self, sentences, detgori_id):
        MAX_RETRY_COUNT = 3
        for i in range(len(sentences)):
            d = {
                'detgoriId': detgori_id,
                'sentence': sentences[i],
                'sentenceIndex': i+1
            }
            t = 0
            while t < MAX_RETRY_COUNT:
                t += 1
                try:
                    res = requests.post(f'{self.es_url}/detgori/_doc', headers={"Content-Type" : "application/json"}, data=json.dumps(d))
                    if res.status_code != 201 :
                        raise IOError(f'**Error** status code is {res.status_code}: {res.json()}')
                    break
                except:
                    time.sleep(5)
        
    def search_detgori_sentences(self, token, page):
        page_size = 5
        page = page
        week_num = datetime.datetime.now().isocalendar()[1]
        query = {
            "from": page_size * page,
            "size": page_size,
            "query": {
                "function_score": {
                    "query": { 
                        "bool": { 
                                "must": [
                                    {"match": {"sentence": {"query": token, "operator": "and"}}}
                                ]
                            }
                        },
                    "random_score": {"seed": week_num, "field": "_seq_no"}, 
                    "boost": 1, # random score를 얼마나 스코어에 반영할지
                    "boost_mode": "multiply"
                }
            }
        }
        res = requests.get(f'{self.es_url}/detgori/_search', headers={"Content-Type" : "application/json"}, data=json.dumps(query))
        return res.json()