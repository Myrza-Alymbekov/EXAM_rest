from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import News, Comment, NewsStatus, CommentStatus, Status


class NewsSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status')

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status')
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'news']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"


class NewsStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsStatus
        exclude = []

