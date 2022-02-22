from rest_framework import serializers
from hannuri.models import *

class UserSerializer(serializers.ModelSerializer):
    detgori = serializers.HyperlinkedRelatedField(many=True, view_name='detgori-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'generation' ,'color', 'detgori', 'is_staff']

class SeasonSerializer(serializers.ModelSerializer):
    session = serializers.HyperlinkedRelatedField(many=True, view_name='session-detail', read_only=True)
    socialActivity = serializers.HyperlinkedRelatedField(many=True, view_name='socialactivity-detail', read_only=True)
    googleFolderId = serializers.ReadOnlyField()

    class Meta:
        model = Season
        fields = ['id', 'year', 'semester', 'title', 'leader', 'sessioner', 'socializer', 'session', 'socialActivity', 'googleFolderId']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    readfile = serializers.HyperlinkedRelatedField(many=True, view_name='sessionreadfile-detail', read_only=True)
    detgori = serializers.HyperlinkedRelatedField(many=True, view_name='detgori-detail', read_only=True)
    googleFolderId = serializers.ReadOnlyField()

    class Meta:
        model = Session
        fields = ['id', 'season', 'week', 'title', 'readfile', 'detgori', 'googleFolderId']

class SessionReadfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionReadfile
        fields = ['id', 'parentSession',  'googleId']

class DetgoriSerializer(serializers.ModelSerializer):
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='detgoricomment-detail', read_only=True)
    authorId = serializers.ReadOnlyField(source='author.id')
    authorName = serializers.ReadOnlyField(source='author.name')
    authorColor = serializers.ReadOnlyField(source='author.color')
    googleId = serializers.ReadOnlyField()

    class Meta:
        model = Detgori
        fields = ['id', 'parentSession', 'title', 'authorId', 'authorColor','authorName', 'date', 'comments', 'googleId',]

class DetgoriCommentSerializer(serializers.ModelSerializer):
    commentReplys = serializers.HyperlinkedRelatedField(many=True, view_name='detgoricommentreply-detail', read_only=True)
    authorId = serializers.ReadOnlyField(source='author.id')
    authorName = serializers.ReadOnlyField(source='author.name')
    authorColor = serializers.ReadOnlyField(source='author.color')
    class Meta:
        model = DetgoriComment
        fields = ['id', 'parentDetgori', 'authorId', 'authorName','authorColor', 'date', 'text', 'commentReplys']

class DetgoriCommentReplySerializer(serializers.ModelSerializer):
    authorId = serializers.ReadOnlyField(source='author.id')
    authorName = serializers.ReadOnlyField(source='author.name')
    authorColor = serializers.ReadOnlyField(source='author.color')
    class Meta:
        model = DetgoriCommentReply
        fields = ['id', 'parentComment', 'authorId', 'authorName','authorColor', 'date', 'text']

class SocialActivitySerializer(serializers.ModelSerializer):
    googleFolderId = serializers.ReadOnlyField()
    imgs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='googleId'
     )

    class Meta:
        model = SocialActivity
        fields = ['season', 'title', 'date', 'summary', 'googleFolderId', 'imgs']

#class SocialActivityImgSerializer(serializers.ModelSerializer):
#    googleId = serializers.ReadOnlyField()
#    class Meta:
#        model = SocialActivityImg
#        fields = ['id', 'googleId']
#

class FreeNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeNote
        fields = ['id', 'text', 'page', 'position']