from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from .models import Template, Resume

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")



class TemplateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Template
    fields = ['id', 'template_type', 'is_cover_letter']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id','user', 'template', 'created_at', 'first_name', 'last_name', 'job_title', 'address', 'email', 'phone_number', 'summary']

