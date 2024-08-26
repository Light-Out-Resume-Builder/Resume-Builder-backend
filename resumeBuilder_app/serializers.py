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
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        return {'user': user}



class TemplateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Template
    fields = ['id', 'template_type', 'is_cover_letter']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id','user', 'template', 'created_at', 'first_name', 'last_name', 'job_title', 'address', 'email', 'phone_number', 'summary']

