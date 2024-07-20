from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, ResumeSerializer, LoginSerializer, LogoutSerializer, TemplateSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework import permissions
from .models import Template, Resume
from rest_framework import viewsets



class RegisterView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            return Response({
                "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
                "token": user.tokens()
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    

class TemplateList(APIView):
#   permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    templates = Template.objects.all()
    serializer = TemplateSerializer(templates, many=True)
    return Response(serializer.data)

  def post(self, request):
    serializer = TemplateSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TemplateDetail(APIView):
#   permission_classes = [permissions.IsAuthenticated]

  def get_object(self, pk):
    try:
      return Template.objects.get(pk=pk)
    except Template.DoesNotExist:
      return None

  def get(self, request, pk):
    template = self.get_object(pk)
    if not template:
      return Response(status=HTTP_404_NOT_FOUND)
    serializer = TemplateSerializer(template)
    return Response(serializer.data)

  def put(self, request, pk):
    template = self.get_object(pk)
    if not template:
      return Response(status=HTTP_404_NOT_FOUND)
    serializer = TemplateSerializer(template, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    template = self.get_object(pk)
    if not template:
      return Response(status=HTTP_404_NOT_FOUND)
    template.delete()
    return Response(status=HTTP_204_NO_CONTENT)

class TemplateDownloadView(APIView):
  def get(self, request, pk):
    template = self.get_object(pk)
    if not template:
      return Response(status=HTTP_404_NOT_FOUND)
    serializer = TemplateSerializer(template)
    return Response(serializer.data)
  
class TemplatePreviewView(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
