
from django.contrib import admin
from .models import Category, Course, Lecture, Comment, Verification


admin.site.site_header = 'MyEd Admin Panel'

#Here we register all the models for account app which we have created so that it is displayed in admin page
class LectureTabularInline(admin.TabularInline):
    model = Lecture   
    extra = 0

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    inlines = [LectureTabularInline]
    list_display = ['title', 'user', 'category', 'skills', 'created']
    list_filter =['user', 'category']
    search_fields = ['title', 'category__name', 'user__full_name']
    class Meta:
        model = Course


class LectureAdmin(admin.ModelAdmin):
    list_display = ["lecture_title" , "course"]
    list_filter = ['course',]
    search_fields = ['course__title', 'lecture_title']

class CommnetAdmin(admin.ModelAdmin):
    pass

class VerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'verify']
    list_filter = ['verify',]


admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Comment, CommnetAdmin)
admin.site.register(Verification, VerificationAdmin)
