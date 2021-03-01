from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model, logout, authenticate
from .forms import AddUserForm, LoginForm, UpdateUserForm, ProfileForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile, User
from course.models import Course
from accounts.decorators import allowed_users
from django.contrib.auth.decorators import login_required


def login_view(request):
    registered_user = get_user_model()
    login_form = LoginForm(request.POST or None) # login form refrencer
    register_form = AddUserForm(request.POST or None) # register form refrence

    if request.method == "POST":

        # if the post name(submit) is equals to the value(signin) than submit the register form
        if request.POST.get('submit') == 'signin':
           

            # if the data provided in the form is valid than save the form 
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user = register_form.save()
                raw_password = register_form.cleaned_data.get('password1')
                user = authenticate(request, email=user.email, password=raw_password)
                group = Group.objects.get(name='Student')
                user.groups.add(group)

                if user is not None:
                    login(request, user)
                    return redirect('login')

        # if the post name(submit) is equals to the value(login) than submit the login form
        elif request.POST.get('submit') == 'login':
            
            if login_form.is_valid():
                email =  login_form.cleaned_data.get('email')
                password =  login_form.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
       
                if user is not None:
                    login(request, user)
                    return redirect('edit-profile')
                else:
                    return redirect('login')
    
    contex ={
        'register_form': register_form,
        'login_form': login_form,
        
    }   
    return render(request, 'apps/login.html', contex)

# method for registration page
# def register_view(request):
#     register_form = AddUserForm(request.POST or None)

#     # if the data provided in the form is valid than save the form 
#     if register_form.is_valid():
#         user = register_form.save(commit=False)
#         user = register_form.save()
#         raw_password = register_form.cleaned_data.get('password1')

#         user = authenticate(request, email=user.email, password=raw_password)
#         group = Group.objects.get(name='Student')
#         user.groups.add(group)
#         if user is not None:
#             login(request, user)
#         return redirect('login')
    
#     return render(request, 'apps/login.html', {'register_form': register_form})

# method for login page
# def login_view(request):
#     registered_user = get_user_model()
#     login_form = LoginForm(request.POST or None)
#     if login_form.is_valid():
#         email =  login_form.cleaned_data.get('email')
#         password =  login_form.cleaned_data.get('password')
#         user = authenticate(email=email, password=password)
       
#         if user is not None:
#             login(request, user)
#             return redirect('edit-profile')
#         else:
#             return redirect('login')
        
#     return render(request, 'apps/login.html', {'login_form': login_form})

#method for teacher profile where we get the logged in user and render the courses the user has uploaded
@login_required(login_url='login')
def teacher_profile_view(request):
    user = request.user
    teacher_course = Course.objects.filter(user=user).order_by('-created')

    return render(request, "apps/teacherProfile.html", {'teacher_course': teacher_course})

#method for user profile page
@login_required(login_url='login')
def create_profile_view(request):

    # if the method is post than create a object for the form
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        create_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        #if the form is valid than save the form to database and redirect the user to profile page
        if create_form.is_valid() and user_form.is_valid():
            create_form.save()
            user_form.save()
            return redirect('teacher-profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        create_form = ProfileForm(instance=request.user.profile)

    contex = {
        'create_form': create_form,
        'user_form': user_form
    }    

    return render(request, 'apps/editProfile.html', contex)
