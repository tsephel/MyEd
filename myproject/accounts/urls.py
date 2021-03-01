from . import views
from django.urls import path
from django.contrib.auth import views as auth_views # there are many views soo alwasy name it as something relevent so the names doest collide

urlpatterns = [
    path('login/', views.login_view, name='login'),
     #ts is a build in class base view that is provided by django which is imported from django auth
    #has pass the template name as an argument in as_view function
    path('logout/', auth_views.LogoutView.as_view(template_name="apps/logout.html"), name= 'logout'),
    path('teacherprofile/', views.teacher_profile_view, name='teacher-profile'),
    path('createprofile/', views.create_profile_view, name='edit-profile'),
    
]