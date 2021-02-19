from rest_framework import serializers
from .models import SmsDispatch, SystemCronTasks, MailDispatch, GroupSendBlack, ServiceConfig, AgentSalesRelations


class SmsDispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsDispatch
        fields = '__all__'
        depth = 0


class SystemCronTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemCronTasks
        fields = '__all__'
        depth = 0


class MailDispatchTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailDispatch
        fields = '__all__'
        depth = 0


class GroupSendBlackSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSendBlack
        fields = '__all__'
        depth = 1


class ServiceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceConfig
        fields = '__all__'
        depth = 1


class AgentSalesRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSalesRelations
        fields = '__all__'
        depth = 2