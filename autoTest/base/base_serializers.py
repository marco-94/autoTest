"""
封装通用的列化器
"""
from rest_framework import serializers
from autoTest.base.base_model import BaseModel
import time


class BaseSerializer(serializers.ModelSerializer):
    """基类序列化器"""
    create_tm_format = serializers.DateTimeField(source="created_tm",
                                                 format="%Y-%m-%d %H:%M:%S",
                                                 required=False,
                                                 read_only=True,
                                                 help_text='创建时间(北京时间)')
    update_tm_format = serializers.DateTimeField(source="updated_tm",
                                                 format="%Y-%m-%d %H:%M:%S",
                                                 required=False,
                                                 read_only=True,
                                                 help_text='更新时间(北京时间)')

    created_tm = serializers.DateTimeField(required=False,
                                           read_only=True,
                                           help_text='创建时间(时间戳)')

    updated_tm = serializers.DateTimeField(required=False,
                                           read_only=True,
                                           help_text='更新时间(时间戳)')

    created_start_tm = serializers.IntegerField(write_only=True, required=False, help_text='创建开始时间')
    created_end_tm = serializers.IntegerField(write_only=True, required=False, help_text='创建结束时间')

    # 重写方法，返回时间戳
    def to_representation(self, instance):
        data = super().to_representation(instance)
        create_time = data.get("create_tm_format")
        update_time = data.get("update_tm_format")
        if create_time and update_time:
            create_time_stamp = str((time.mktime(time.strptime(create_time, '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]
            update_time_stamp = str((time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]
            data.update({"created_tm": create_time_stamp, "updated_tm": update_time_stamp})
            return data

    class Meta:
        model = BaseModel
        fields = ("created_tm", "updated_tm", "create_tm_format", "update_tm_format", "created_start_tm",
                  "created_end_tm")
