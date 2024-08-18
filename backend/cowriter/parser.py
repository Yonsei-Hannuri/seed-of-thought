import inflection
from rest_framework.parsers import JSONParser

class CamelCaseJSONParser(JSONParser):
    def _camel_to_snake(self, data):
        if isinstance(data, dict):
            return {inflection.underscore(key): self._camel_to_snake(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._camel_to_snake(item) for item in data]
        return data

    def parse(self, stream, media_type=None, parser_context=None):
        # JSONParser의 기본 parse 호출
        data = super().parse(stream, media_type=media_type, parser_context=parser_context)

        # snake_case로 변환
        return self._camel_to_snake(data)