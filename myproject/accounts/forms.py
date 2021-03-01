from django import forms
from .models import User, Profile
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from crispy_forms.helper import FormHelper

#Form to add user detail for registration 
class AddUserForm(forms.ModelForm):

    # method to make sure that the label is not shown in the template form field
    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 

    """
    New User Form. Requires password confirmation.
    """
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'full_name','placeholder':'Full Name'}), 
        label='')

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'email','placeholder':'Email'}), 
        label='')

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
        label='')
    
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Comfirm password'}),
        label='')
  
   

    # group = forms.ModelChoiceField(queryset=Group.objects.filter(name='Student'), required=True) #getting the groups from admin as a choice field

    class Meta:
        model = User
        fields = ['email', 'full_name']
    
    

    # to make sure the password and the confirm password are equal
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    # to make sure the added detail of the user in form is saved in database
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # user.groups.add(self.cleaned_data['group']) # saving the user to the group as per thie choice. 
        return user
    
    

# This form is use if the user wants to make changes to the registered detail
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'full_name']

    # Password can't be changed in the admin
    def clean_password(self):
        return self.initial["password"]

# this form is use to show the login form to the user
class LoginForm(forms.Form): 
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'email','placeholder':'Email'}), 
        label='')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
        label='')

    class Meta:
        fields = ['email', 'password']

    # this method is use to sure that the information matches the database information. if not it raises an error
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("User does not exist")
        return super(LoginForm, self).clean(*args, **kwargs)

# this form is created for the user to edit their profile
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_img', 'phone_number', 'address', 'gender', 'about']