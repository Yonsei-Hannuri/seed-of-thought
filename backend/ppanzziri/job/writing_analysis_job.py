import logging
import threading

from django.db import close_old_connections
from django.utils import timezone

from ppanzziri.component import llm_client
from ppanzziri.models import WritingRecord


logger = logging.getLogger(__name__)


class WritingAnalysisJob:
    """글 제출 후 비동기로 Claude API 분석을 수행한다.

    시작/종료 상태는 WritingRecord.analysis_status 플래그로 관리한다.
    - 'pending': 분석 대기
    - 'done': 분석 완료
    """

    @staticmethod
    def spawn(record_id):
        """백그라운드 스레드로 분석 작업을 시작한다."""
        thread = threading.Thread(
            target=WritingAnalysisJob._run,
            args=(record_id,),
            daemon=True,
        )
        thread.start()

    @staticmethod
    def _run(record_id):
        try:
            WritingAnalysisJob._analyze(record_id)
        except RuntimeError as exc:
            logger.error('WritingAnalysisJob config error for record %s: %s', record_id, exc)
        except _anthropic_exceptions() as exc:
            logger.error('WritingAnalysisJob API error for record %s: %s', record_id, exc)
        finally:
            close_old_connections()

    @staticmethod
    def _analyze(record_id):
        try:
            record = WritingRecord.objects.get(
                pk=record_id,
                analysis_status=WritingRecord.STATUS_PENDING,
            )
        except WritingRecord.DoesNotExist:
            return

        result = llm_client.analyze(record.content)

        record.summary = result.get('summary', '')
        record.keywords = result.get('keywords', [])
        record.analyzed_at = timezone.now()
        record.analysis_status = WritingRecord.STATUS_DONE
        record.save(update_fields=['summary', 'keywords', 'analyzed_at', 'analysis_status'])


def _anthropic_exceptions():
    """anthropic 예외 튜플을 지연 로딩 — 런타임에만 참조."""
    import anthropic
    return (anthropic.APIError, anthropic.APIConnectionError)
