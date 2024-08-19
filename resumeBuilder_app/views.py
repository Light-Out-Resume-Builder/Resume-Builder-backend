from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, ResumeSerializer, LoginSerializer, LogoutSerializer, TemplateSerializer
from django.contrib.auth import authenticate
from .models import Template, Resume
from rest_framework import viewsets
import logging
logger = logging.getLogger(__name__)

class RegisterView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # Handling validation errors
        if not serializer.is_valid():
            logger.error(f"Validation Error in RegisterView: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = serializer.save()
            return Response({
                "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully. Continue to Login...",
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error in RegisterView: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = serializer.get_tokens_for_user(user)
        return Response({
            "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
            "tokens": tokens
        }, status=status.HTTP_200_OK)
    
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         serializer.is_valid(raise_exception=True)
    #         email = serializer.validated_data['email']
    #         password = serializer.validated_data['password']
    #         user = authenticate(email=email, password=password)

    #         if user is not None:
    #             return Response({
    #                 "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
    #                 "token": user.tokens()
    #             }, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         logger.error(f"Error during login: {str(e)}")
    #         return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    
class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optionally filter the queryset based on criteria
        return self.queryset


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter resumes to only include those belonging to the authenticated user
        return self.queryset.filter(user=self.request.user)

