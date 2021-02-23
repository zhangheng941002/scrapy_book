from rest_framework import serializers

from .models import *


class BookAllInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAllInfoModel
        fields = '__all__'
        depth = 1


class BookTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTypeModel
        fields = '__all__'
        depth = 1


class BookModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = BookModel
        fields = '__all__'
        depth = 1


class BookChapterSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = BookChapterModel
        fields = ("book_id", "chapter_name", "num", "create_date")
        depth = 3


class ChapterContentSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = BookChapterModel
        fields = '__all__'
        depth = 3
