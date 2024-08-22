from . import views
from django.urls import path
from .views import  ResumeViewSet, TemplateViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [

    path('template/', TemplateViewSet.as_view({
        'get': 'list',      # To Handles GET requests to list all templates
        'post': 'create'    # To Handles POST requests to create a new template
    }), name="template-list"),

    path('template/<int:pk>/', TemplateViewSet.as_view({
        'get': 'retrieve',  # To Handles GET requests to retrieve a single template by ID
        'put': 'update',    # To Handles PUT requests to update a template by ID
        'delete': 'destroy' # To Handles DELETE requests to delete a template by ID
    }), name="template-detail"),
    

    path('resume/', ResumeViewSet.as_view({
        'get': 'list',      # To Handles GET requests to list all resumes
        'post': 'create'    # To Handles POST requests to create a new resume
    }), name="resume-list"),

    path('resume/<int:pk>/', ResumeViewSet.as_view({
        'get': 'retrieve',  # To Handles GET requests to retrieve a single resume by ID
        'put': 'update',    # To Handles PUT requests to update a resume by ID
        'delete': 'destroy' # To Handles DELETE requests to delete a resume by ID
    }), name="resume-detail"),
    
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginView.as_view(),name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]