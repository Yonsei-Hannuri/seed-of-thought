import hannuri.integration.cowriter
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

import hannuri.integration

from cowriter.serializer import *
from cowriter.models import *
from cowriter.message import *
from cowriter.renderer import CamelCaseJSONRenderer
from cowriter.parser import CamelCaseJSONParser
from cowriter.component import llm
from cowriter.agent import promptAgent
from cowriter.utils import is_valid_sentence


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.filter(del_yn=False).order_by('-subject_id')
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser, JSONParser] 

    def retrieve(self, request, *args, **kwargs):
        subject_id = kwargs.get('pk')
        subject_url = request.query_params.get('subjectUrl', None)
        subject = Subject.objects.filter(pk=subject_id).first()

        if not subject:
            res = None
            # if subject_url:
            #     response = requests.get(subject_url)
            #     if response.status_code == 200:
            #         res = response.json()
            # print(response)
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(subject_url)
            query_params = parse_qs(parsed_url.query)
            session_ids = query_params.get('sessionId')
            if not session_ids:
                return Response('존재하지 않는 자원', status=status.HTTP_404_NOT_FOUND)
            session_id = session_ids[0]
            res = hannuri.integration.cowriter.get_subject(session_id)
            if res is None: 
                subject = Subject(pk=subject_id, subject_url=subject_url)
                subject.save()
            else:
                subject = Subject(
                    pk=subject_id, 
                    subject_url=subject_url,
                    subject_title = res.get('subjectTitle'),
                    subject_content = res.get('subjectContent'),
                    subject_purpose = res.get('subjectPurpose'),
                )
                subject.save()
        
        serializer = self.get_serializer(subject)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.del_yn = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EssayViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.filter(del_yn=False).order_by('-created_dt')
    serializer_class = EssaySerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser, JSONParser] 

    def get_queryset(self):
        user = self.request.user
        action = self.request.query_params.get('action', None)
        if action == 'recent-subject-essay':
          subject_id = self.request.query_params.get('subject-id', None)
          return Essay.objects.filter(owner=user.email, del_yn=False, subject_id=subject_id).order_by('-created_dt')
        else:
            return Essay.objects.filter(owner=user.email, del_yn=False).order_by('-created_dt')

    def retrieve(self, request, *args, **kwargs):
        action = request.query_params.get('action', None)
        if action == "title-recommend":
            essay_id = kwargs.get('pk')
            essay = Essay.objects.filter(pk=essay_id).first()
            paras = essay.paragraph.filter(del_yn=False)
            if len(paras) == 0 :
                raise ValidationError("단락이 없어 제목을 생성할 수 없습니다.")
            essay_contents = '\n'.join([para.paragraph_content for para in paras])
            return Response({"titleRecommend" : promptAgent.recommend_title(essay_contents)})
        else:
            return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs): 
        request.data['owner'] = request.user.email
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        action = request.query_params.get('action', None)
        if not action:
            return Response(NO_ACTION_DEFINED, status=status.HTTP_400_BAD_REQUEST)
        
        if action.lower() == "title":
            if not request.data["title"]:
                return Response('title 프로퍼티가 필요합니다.', status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(self.get_object(), partial=True, data={"essay_title": request.data["title"]})
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        if action.lower() == "complete":
            if not request.data["complete"]:
                return Response('complete(true/false) 프로퍼티가 필요합니다.', status=status.HTTP_400_BAD_REQUEST)
            complete_yn = True if request.data["complete"].lower() == 'true' else False
            serializer = self.get_serializer(self.get_object(), partial=True, data={"complete_yn":complete_yn})
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(NOT_DEFINED_ACTION, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.del_yn = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EssayMindmapViewSet(viewsets.ModelViewSet):
    queryset = EssayMindmap.objects.order_by('-created_dt')
    serializer_class = EssayMindmapSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser, JSONParser] 

    def get_queryset(self):
        essay_id = self.kwargs['essay_id']
        return EssayMindmap.objects.filter(essay_id=essay_id)

    def create(self, request, *args, **kwargs):
        essay_id = kwargs['essay_id']
        mindmap = request.data
        if not isinstance(mindmap, list):
            return Response({"error": "Expected a list of items on 'mindmap' property"}, status=status.HTTP_400_BAD_REQUEST)
        edges = []
        for edge in mindmap:
            edge["keyword1"] = edge["keyword1"].strip()
            edge["keyword2"] = edge["keyword2"].strip()
            keywords = [edge["keyword1"] if edge["keyword1"] < edge["keyword2"] else edge["keyword2"],
                        edge["keyword2"] if edge["keyword1"] < edge["keyword2"] else edge["keyword1"]]
            keyword_records = [None, None]
            for index in range(2):
                keyword_record = Keyword.objects.filter(keyword_nm=keywords[index]).first()
                if not keyword_record:
                    keyword_record = Keyword.objects.create(keyword_nm=keywords[index])
                keyword_records[index] = keyword_record
            edges.append(
                {
                    "essay_id": essay_id, 
                    "keyword1": keyword_records[0].keyword_id, 
                    "keyword2": keyword_records[1].keyword_id
                }
            )
        serializer = self.get_serializer(data=edges, many=True)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            EssayMindmap.objects.filter(essay_id=essay_id).delete()
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ParagraphViewSet(viewsets.ModelViewSet):
    queryset = Paragraph.objects.filter(del_yn=False).order_by('-created_dt')
    serializer_class = ParagraphSerializer  
    permission_classes = [IsAuthenticated]
    renderer_classes = [CamelCaseJSONRenderer]
    parser_classes = [CamelCaseJSONParser, JSONParser] 

    DUMMY_ORDER = 10000

    def get_queryset(self):
        essay_id = self.kwargs['essay_id']
        return Paragraph.objects.filter(essay_id=essay_id, del_yn=False).order_by("order")

    def create(self, request, *args, **kwargs): 
        request.data['essay_id'] = kwargs['essay_id']
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        place_before = self.request.data["place_before"]
        with transaction.atomic():
            new_paragraph = serializer.save(order = ParagraphViewSet.DUMMY_ORDER)
            self._update_paragraph_order(new_paragraph, place_before)
            ParagraphHist.objects.create(
                paragraph_id = new_paragraph,
                change_type = "INITIAL",
                paragraph_content = new_paragraph.paragraph_content
            )

    def update(self, request, *args, **kwargs):
        action = request.query_params.get('action', None)
        if not action:
            return Response(NO_ACTION_DEFINED, status=status.HTTP_400_BAD_REQUEST)
        
        if action == 'regenerate':
            instance = self.get_object()
            command = request.data["command"]
            if command == 'INITIAL':
                revised_content = promptAgent.initial_gen_paragraph(instance.paragraph_content)
            else:
                if not is_valid_sentence(command):
                    raise ValidationError("더욱 자세한 요청을 입력해주세요.")
                revised_content = promptAgent.modify_paragaph_command(instance.paragraph_content, command)

            serializer = self.get_serializer(instance, partial=True, data={"paragraph_content": revised_content})
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                self.perform_update(serializer)
                ParagraphHist.objects.create(
                    paragraph_id = instance,
                    change_type = "REGENERATE",
                    change_command = command,
                    paragraph_content = revised_content
                )
            return Response(serializer.data)
        elif action == 'manual':
            instance = self.get_object()
            content = request.data["content"]
            serializer = self.get_serializer(instance, partial=True, data={"paragraph_content": content})
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                self.perform_update(serializer)
                ParagraphHist.objects.create(
                    paragraph_id = instance,
                    change_type = "MANUAL",
                    paragraph_content = content
                )
            return Response(serializer.data)
        elif action == 'order':
            instance = self.get_object()
            place_before = request.data["place_before"]
            self._update_paragraph_order(instance, place_before)
            return Response(self.get_serializer(instance).data)
    
        return Response(NOT_DEFINED_ACTION, status=status.HTTP_400_BAD_REQUEST)
    

    
    def _update_paragraph_order(self, paragraph, place_before):
        cur_order = paragraph.order
        if cur_order == place_before - 1 or cur_order == place_before:
            return Response("순서 변화가 없었습니다.")
        paragraphs = [paragraph for paragraph in Paragraph.objects.filter(essay_id=paragraph.essay_id, del_yn=False).all().order_by('order')]
        if ParagraphViewSet.DUMMY_ORDER == cur_order:
            paragraph = paragraphs.pop()
        else:
            paragraph = paragraphs.pop(cur_order)
        if cur_order < place_before:
            paragraphs.insert(place_before-1, paragraph)
        else:
            paragraphs.insert(place_before, paragraph)
        for i in range(len(paragraphs)):
            paragraphs[i].order = i
        Paragraph.objects.bulk_update(paragraphs, ['order'])
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.del_yn = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)