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
    class Meta:
        model = BookModel
        fields = '__all__'
        depth = 1


class BookChapterSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = BookChapterModel
        fields = '__all__'
        depth = 3


class BookChapterListSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = BookChapterModel
        fields = '__all__'
        depth = 3
