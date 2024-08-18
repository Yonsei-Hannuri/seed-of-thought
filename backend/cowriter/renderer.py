import inflection
from rest_framework.renderers import JSONRenderer

class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 변환 함수
        def camelize(data):
            if isinstance(data, dict):
                return {inflection.camelize(key, False): camelize(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [camelize(item) for item in data]
            return data

        camelized_data = camelize(data)
        return super().render(camelized_data, accepted_media_type, renderer_context)

