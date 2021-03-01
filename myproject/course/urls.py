from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='dashboard'),
    path('courseView/', views.course_view, name='courses'),
    path('searchView/', views.search_view, name='search'),
    path('contentAdd/', views.content_add_view, name= 'content-add'),
    path('verification/', views.verification_view, name='verify'),
    path('<int:id>/contentEdit/', views.content_edit_view, name='content-edit'),
    path('<int:pk>/contentDelete/', views.content_delete_view, name='content-delete'),
    path('lecture/<int:lecture_id>/', views.tutorial_detail_view, name="tutorial"), 

]