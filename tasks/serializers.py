from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)  # 輸出 owner 的識別（使用 __str__）

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # 使用 create_user 來建立用戶（會自動進行密碼哈希）
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


