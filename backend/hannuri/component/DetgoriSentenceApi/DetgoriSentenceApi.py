import requests
import time
import datetime
import json
import os
from pathlib import Path

class DetgoriSentenceApi:
    
    def __init__(self):
        configs_file_path = os.path.join(Path(__file__).parent.absolute(), 'secret', 'configs.json')
        with open(configs_file_path) as f:
            configs = json.load(f)
        self.es_url = configs['esUrl']
        self.detgori_index_name = configs['detgoriIndexName']

    def save_detgori_sentences(self, sentences, detgori_id):
        if len(sentences) == 0:
            return
        payload = []
        for i in range(len(sentences)):
            payload.append('{"index": { }}')
            payload.append(json.dumps({
                'detgoriId': detgori_id,
                'sentence': sentences[i],
                'sentenceIndex': i+1
            }))
        payload.append('\n')
        MAX_RETRY_COUNT = 3
        t = 0
        res = None
        while t < MAX_RETRY_COUNT:
            t += 1
            try:
                res = requests.post(f'{self.es_url}/{self.detgori_index_name}/_bulk', headers={"Content-Type" : "application/json"}, data='\n'.join(payload))  
                break
            except:
                time.sleep(5)

        if res is None or res.json()["errors"] :
            error_message = json.dumps(
                    {
                        "description": "댓거리 문장 저장 중 오류 발생", 
                        "detgoriId": detgori_id, 
                        "dbError": res.json()
                    }
                )
            raise DetgoriSentenceApi.ApiException(error_message)
        
    def search_detgori_sentences_among_detgoris(self, token, detgori_ids=None, page = 0, page_size=5):
        page = page
        week_num = datetime.datetime.now().isocalendar()[1]
        must_conditions = [{"match": {"sentence": {"query": token, "operator": "and"}}}]
        if isinstance(detgori_ids, list):
            must_conditions.append({ "terms" : { "detgoriId" : detgori_ids }})
        query = {
            "from": page_size * page,
            "size": page_size,
            "query": {
                "function_score": {
                    "query": { 
                        "bool": { 
                                "must": must_conditions
                            }
                        },
                    "random_score": {"seed": week_num, "field": "_seq_no"}, 
                    "boost": 1, # random score를 얼마나 스코어에 반영할지
                    "boost_mode": "multiply"
                }
            }
        }
        res = requests.get(f'{self.es_url}/{self.detgori_index_name}/_search', headers={"Content-Type" : "application/json"}, data=json.dumps(query))
        body = res.json()
        sources = [hit['_source'] for hit in body['hits']['hits']]
        total_count = body['hits']['total']['value']
        return {'result' : sources, 'total_count': total_count}
    
    def search_detgori_sentences(self, token, page, page_size=5):
        return self.search_detgori_sentences_among_detgoris(token, page=page, page_size=page_size)
    
    def delete_sentences_of_detgori(self, detgori_id):
        query = {
            "query": {
                "term": {
                    "detgoriId": detgori_id
                }
            }
        }

        MAX_RETRY_COUNT = 3
        t = 0
        res = None
        while t < MAX_RETRY_COUNT:
            t += 1
            try:
                res = requests.post(f'{self.es_url}/{self.detgori_index_name}/_delete_by_query', headers={"Content-Type" : "application/json"}, data=json.dumps(query))
                break
            except:
                time.sleep(0.5)

        if res is None or len(res.json()["failures"]) != 0:
            error_message = json.dumps(
                    {
                        "description": "댓거리 문장 삭제 중 오류 발생", 
                        "detgoriId": detgori_id, 
                        "dbError": res.json()
                    }
                )
            raise DetgoriSentenceApi.ApiException(error_message)

    
    class ApiException(Exception):
        pass
        

