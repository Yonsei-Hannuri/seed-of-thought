from django.core.files.storage import FileSystemStorage

from hannuri.component import detgoriSentenceApi, detgoriPdfTextExtracter, textAnalyzer
from hannuri.models import Detgori, DetgoriOnProcessingDerived
from django.core.exceptions import ObjectDoesNotExist

import logging
import time
import json
from multiprocessing import Process

logger = logging.getLogger('common')

class DetgoriDerivedDataAgent:
    
    def create_derived(self, pdf_bytes, detgori_id):
        detgori_on_processing = DetgoriOnProcessingDerived(detgori_id=detgori_id)
        detgori_on_processing.save()
        t = Process(target=DetgoriDerivedDataAgent._create_derived, args=(pdf_bytes, detgori_id))
        t.start()

    def _create_derived(pdf_bytes, detgori_id):
        try:
            FileSystemStorage(location="/tmp").save(f'{detgori_id}', pdf_bytes)
            text = detgoriPdfTextExtracter.extract_text(f'/tmp/{detgori_id}')
        except Exception as e:
            logger.error(f'{detgori_id}번 댓거리의 PDF에서 텍스트를 추출하는데 실패했습니다. {e}')
            return
        
        DetgoriDerivedDataAgent._generate_wordcount(text, detgori_id)
        DetgoriDerivedDataAgent._generate_sentences(text, detgori_id)

        detgori_on_proceesing = DetgoriOnProcessingDerived.objects.get(detgori_id=detgori_id)
        detgori_on_proceesing.delete()



    def _generate_wordcount(text, detgori_id):
        # count word and save
        try:
            word_count = textAnalyzer.count_words(text)
            detgori = Detgori.objects.get(pk=detgori_id)
            detgori.words = json.dumps(word_count)
            detgori.pureText = text
            detgori.save(update_fields=['words', 'pureText'])
        except ObjectDoesNotExist as e:
            # 댓거리가 파생데이터 생성 전 이미 삭제된 케이스
            pass
        except Exception as e:
            logger.error(f'{detgori_id} 댓거리의 텍스트에서 단어개수 데이터 생성 작업을 실패했습니다. {e}')

    def _generate_sentences(text, detgori_id):
        # parse to sentences and save to elastic search
        sentences = textAnalyzer.split_into_sentences(text)
        try:
            detgoriSentenceApi.save_detgori_sentences(sentences, detgori_id)
        except Exception as e:
            logger.error(f'{detgori_id} 댓거리의 텍스트에서 문장을 데이터를 생성하는 작업에 실패했습니다. {e}')
    
    def remove_derived(self, detgori_id):
        t = Process(target=DetgoriDerivedDataAgent._remove_derived, args=(detgori_id,))
        t.start()

    def _remove_derived(detgori_id):
        max_try = 10
        sleep_time = 10
        for _ in range(max_try):
            is_detgori_on_process = False if DetgoriOnProcessingDerived.objects.filter(detgori_id=detgori_id).count() == 0 else True
            if is_detgori_on_process:
                time.sleep(sleep_time)
                continue
            try:
                detgoriSentenceApi.delete_sentences_of_detgori(detgori_id)
            except Exception as e:
                logger.error(f'{detgori_id} 댓거리의 문장 파생데이터를 삭제하는 실패했습니다. {e}')
            finally:
                return
            
        logger.error(f'{detgori_id} 댓거리의 문장 파생데이터를 삭제하는 실패했습니다. 댓거리 프로세싱 관련 테이블 데이터에 문제가 있는 것 같습니다.')