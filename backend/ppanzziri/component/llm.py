import json
import os
import re
from abc import ABC, abstractmethod

import anthropic


class WritingAnalyzer(ABC):
    """글 분석 컴포넌트 추상 클래스. 구현체는 요약과 키워드를 반환한다."""

    @abstractmethod
    def analyze(self, content):
        """
        :param content: 분석 대상 글 (str)
        :return: {'summary': str, 'keywords': [str, ...]}
        """
        raise NotImplementedError


class ClaudeWritingAnalyzer(WritingAnalyzer):
    """Claude API로 글 요약과 키워드를 추출한다."""

    _MODEL = 'claude-opus-4-6'
    _MAX_TOKENS = 1024
    _PROMPT_TEMPLATE = (
        '다음 글을 분석하여 JSON 형식으로만 응답하세요. 다른 설명은 포함하지 마세요.\n'
        '응답 형식: {{"summary": "한 줄 요약", "keywords": ["키워드1", "키워드2", "키워드3"]}}\n'
        '- summary: 50자 이내 한 줄 요약\n'
        '- keywords: 핵심 키워드 3~5개\n\n'
        '글:\n{content}'
    )

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            api_key = os.getenv('ANTHROPIC_API_KEY', '').strip()
            if not api_key:
                raise RuntimeError('ANTHROPIC_API_KEY is not configured.')
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def analyze(self, content):
        client = self._get_client()
        message = client.messages.create(
            model=self._MODEL,
            max_tokens=self._MAX_TOKENS,
            thinking={'type': 'adaptive'},
            messages=[
                {
                    'role': 'user',
                    'content': self._PROMPT_TEMPLATE.format(content=content),
                }
            ],
        )
        return self._parse_response(message)

    @staticmethod
    def _parse_response(message):
        response_text = ''
        for block in message.content:
            if block.type == 'text':
                response_text = block.text
                break

        parsed = ClaudeWritingAnalyzer._extract_json(response_text)
        summary = str(parsed.get('summary', '')).strip()
        keywords_raw = parsed.get('keywords', [])
        if not isinstance(keywords_raw, list):
            keywords_raw = []
        keywords = [str(k).strip() for k in keywords_raw if str(k).strip()]
        return {'summary': summary, 'keywords': keywords}

    @staticmethod
    def _extract_json(text):
        if not text:
            return {}
        try:
            return json.loads(text)
        except (TypeError, ValueError):
            pass

        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            return {}
        try:
            return json.loads(match.group(0))
        except (TypeError, ValueError):
            return {}


llm_client = ClaudeWritingAnalyzer()
