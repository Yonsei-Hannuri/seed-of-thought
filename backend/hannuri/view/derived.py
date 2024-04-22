from hannuri.models import *
from django.http import HttpResponse
import json
from hannuri.component import detgoriSentenceApi

def SentenceSearch(request):
    if not request.user:
        return HttpResponse('Unauthorized', status=401)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    tokens = body['tokens']
    page = body['page']
    
    res = detgoriSentenceApi.search_detgori_sentences(' '.join(tokens), page, page_size=5)
    total_count = res['total_count']
    sources = res['result']
    sentences = []
    for source in sources:
        detgori = Detgori.objects.get(pk=source['detgoriId'])
        sentences.append(
            {
                'content': source['sentence'], 
                'semester': f'{detgori.parentSession.season.year}-{detgori.parentSession.season.semester}', 
                'title': detgori.title, 
                'author': detgori.author.name,
                'link': detgori.googleId
            }
        )

    return HttpResponse(json.dumps({
        'sentences': sentences,
        'totalCount': total_count
    }), status=200)  


