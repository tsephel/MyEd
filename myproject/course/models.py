from django.db import models
from django.conf import settings
from io import BytesIO  #basic input/output operation
from PIL import Image #Imported to compress images
from django.core.files import File #to store files
from django.core.exceptions import ValidationError

# Create your models here.

#Validate file size and limit upload size
def validate_file_size(value):
    file_size = value.size

    if file_size > 10485760:
        raise ValidationError('The maximum file size that can be uploaded is 10MB')
    else:
        return value

# Model with fields created for category page
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model with fields created for course page 
class Course(models.Model):
    skill = (
        ('beginner', 'Beginner'),
        ('intermidate', 'Intermidate'),
        ('advance', 'Advance'),
        )
    title = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='poster/', help_text = "Please upload a cover picture for your lecture slides.")
    skills = models.CharField(max_length=25,choices=skill)
    powerpoint_slides = models.FileField(upload_to='powerpoint/', null=True, blank=True, help_text = "Please upload your powerpoint slides here.")
    powerpoint_url = models.URLField( null=True, blank=True, help_text = "Please upload your powerpoint slides here.")
    price = models.IntegerField(null=True, blank=True, help_text = "Leave the table blank if the course is free of cost.")
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
   
    def __str__(self):
        return self.title

# Model with fields created for verification page
class Verification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qualification = models.FileField(upload_to = 'documents/', null=True, help_text= 'Upload a proof for your verification to become an instructor.')
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
# Model with fields created for lecture page 
class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture_title = models.CharField(max_length=500, help_text= 'eg: Lecture 1: Introduction to computer')
    lecture_content = models.FileField(null=True, blank=True, upload_to='lecture video/', help_text='Upload your lecture video here', validators=[validate_file_size])
    youtube_url = models.URLField(null=True, blank=True, help_text='Link of youtube url that you want to upload')

    def __str__(self):
        return self.lecture_title

# Model with fields created for comment page
class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE, related_name="replies") # this implies tha recursive relation to the reply field
    comment = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{}-{}'.format(self.course.title, str(self.user.full_name))
