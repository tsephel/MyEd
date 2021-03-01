from django import forms
from .models import Course, Comment, Verification

#Form created for content add
class ContentAddForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title', 'category', 'poster', 'skills', 'powerpoint_slides', 'price']

        # widgets ={
        #     'title':forms.TextInput(attrs={'placeholder': 'Main title of the slide',}),
        #     'video_name':forms.TextInput(attrs={'placeholder': 'eg: Lecture 1: Intorduction to Computing'}),
            
        # }

#Form created to edit the content added
class ContentEditForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title', 'category', 'poster', 'skills', 'powerpoint_slides', 'price']

# Form created for verifying a user
class VerificationForm(forms.ModelForm):

    class Meta:
        model= Verification
        fields = ['qualification',]

#Form created to for user to comment on the course
class CommentForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment goes here!!!', 'rows':'2', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ('comment',)
