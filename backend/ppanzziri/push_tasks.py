import json
import logging
import os
import random
from datetime import date, datetime, time

from django.db.models import Sum
from pywebpush import WebPushException, webpush

from ppanzziri.models import PushSubscription, WritingGoal, WritingRecord


logger = logging.getLogger('common')

MORNING_MESSAGES = [
    '오늘도 한 줄부터 시작해볼까요?',
    '아침의 첫 글이 하루를 결정합니다.',
    '머릿속의 생각을 글로 남겨주세요.',
    '글쓰기로 돈 버는 하루, 시작합시다.',
]


def _vapid_claims():
    email = os.environ.get('VAPID_CLAIMS_EMAIL', '')
    return {'sub': f'mailto:{email}'} if email else {}


def _vapid_private_key():
    return os.environ.get('VAPID_PRIVATE_KEY', '')


def _send_push(subscription, title, body):
    payload = json.dumps({'title': title, 'body': body})
    try:
        webpush(
            subscription_info={
                'endpoint': subscription.endpoint,
                'keys': {
                    'p256dh': subscription.p256dh,
                    'auth': subscription.auth,
                },
            },
            data=payload,
            vapid_private_key=_vapid_private_key(),
            vapid_claims=_vapid_claims(),
        )
        return True
    except WebPushException as exc:
        # 410 Gone: subscription expired - remove from DB
        if exc.response is not None and exc.response.status_code in (404, 410):
            subscription.delete()
            logger.warning('Push subscription expired and removed: id=%s', subscription.id)
            return False
        logger.warning('Push send failed: id=%s status=%s', subscription.id, exc)
        return False


def _broadcast(title, body):
    sent = 0
    for subscription in PushSubscription.objects.all():
        if _send_push(subscription, title, body):
            sent += 1
    return sent


def _today_char_count():
    today = date.today()
    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)
    aggregate = WritingRecord.objects.filter(
        submitted_at__range=(start, end)
    ).aggregate(total=Sum('char_count'))
    return aggregate.get('total') or 0


def _current_goal_target():
    goal = WritingGoal.objects.first()
    if goal is None:
        return 0
    return goal.target_chars


def send_morning_push():
    """08:30 동기부여 알림 발송."""
    title = '글쓰기 시작!'
    body = random.choice(MORNING_MESSAGES)
    sent = _broadcast(title, body)
    logger.info('Morning push sent to %d subscribers.', sent)


def send_evening_push():
    """22:00 피드백 알림 발송 - 당일 글자 수와 목표 비교."""
    char_count = _today_char_count()
    target = _current_goal_target()

    if target <= 0:
        title = '오늘의 글쓰기 결산'
        body = f'오늘 {char_count}자를 썼습니다. 목표를 설정하면 더 명확한 피드백을 드려요.'
    elif char_count >= target:
        title = '오늘 목표 달성!'
        body = f'목표 {target}자를 넘어 {char_count}자를 썼어요. 훌륭합니다!'
    else:
        shortfall = target - char_count
        title = '오늘 목표 미달'
        body = f'목표 {target}자 중 {char_count}자. {shortfall}자가 부족했어요. 내일은 더 잘해봐요.'

    sent = _broadcast(title, body)
    logger.info('Evening push sent to %d subscribers (chars=%d, target=%d).', sent, char_count, target)
