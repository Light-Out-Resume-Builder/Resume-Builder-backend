from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken 
from .managers import UserManager


class User(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager() 

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    

class Template(models.Model):
    TEMPLATE_CHOICES = [
        ('Basic', 'Basic'),
        ('Modern', 'Modern'),
        ('Professional', 'Professional'),
        ('Creative', 'Creative'),
    ]

    template_type = models.CharField(max_length=50, choices=TEMPLATE_CHOICES)
    is_cover_letter = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.get_template_type_display()} ({'Cover Letter' if self.is_cover_letter else 'Resume'})"

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Resume"

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experiences')
    position_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    work_summary = models.TextField(blank=True, null=True)

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    school_name = models.CharField(max_length=100)
    school_location = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)

class Reference(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    full_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

class AdditionalSection(models.Model):
    SECTION_CHOICES = [
        ('Languages', 'Languages'),
        ('Certification', 'Certification'),
        ('Volunteering', 'Volunteering'),
        ('Links', 'Links'),
        ('Custom Section', 'Custom Section'),
        ('Accomplishments', 'Accomplishments'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='additional_sections')
    section_type = models.CharField(max_length=50, choices=SECTION_CHOICES)
    content = models.TextField()

class CoverLetter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cover_letters')
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Cover Letter Specific Details
    years_of_experience = models.IntegerField(blank=True, null=True)
    specific_job = models.BooleanField(default=False)
    job_type = models.CharField(max_length=100, blank=True, null=True)
    standout_points = models.TextField(blank=True, null=True)
    relevant_experience = models.TextField(blank=True, null=True)
    preferred_work_type = models.CharField(max_length=100, blank=True, null=True)
    
    # User and Employer Details
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100)
    user_phone_number = models.CharField(max_length=20)
    user_email = models.EmailField()
    user_address = models.CharField(max_length=255)
    
    employer_company_name = models.CharField(max_length=100)
    employer_hiring_manager_name = models.CharField(max_length=100)
    employer_address = models.CharField(max_length=255)
    
    # Letter Details
    letter_date = models.DateField()
    letter_body = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Cover Letter"

