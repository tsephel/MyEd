from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.http import Http404 
from .models import Course, Lecture, Comment, Verification
from  accounts.models import Profile
from .forms import ContentAddForm, ContentEditForm, CommentForm, VerificationForm
from django.forms  import modelformset_factory
from django.contrib.auth import get_user_model
from accounts.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

#method to render all the latest courses in dashboard
def home_view(request): 
    course_count = Course.objects.all().count()
    student_count = Profile.objects.filter(user__groups__name__in=['Student']).count()
    teacher_count = Profile.objects.filter(user__groups__name__in=['Teacher']).count()

    context = {
        'course_count': course_count,
        'student_count': student_count,
        'teacher_count': teacher_count
    }

    
    return render(request, 'apps/dashboard.html', context)


@login_required(login_url='login')
# method to load all the courses in the course page
def course_view(request):
    latest_course = Course.objects.all().order_by('-created')

    context = {
        'latest_course': latest_course,
    }

    return render(request, 'apps/course.html', context)

@login_required(login_url='login')
# method to search for particualr courses in the course page
def search_view(request):
   
    query = request.GET.get('q')

    if query:
        search = Course.objects.filter(
            Q(title__icontains=query)|
            Q(user__full_name=query)|
            Q(price__icontains=query)
        )
    context = {
        'search': search,
    }

    return render(request, 'apps/search.html', context)


    

@login_required(login_url='login')
# method to load each lecture and the comments associated with the particular course as per the user
def tutorial_detail_view(request, lecture_id):
    tutorial = get_object_or_404(Course, pk=lecture_id) # here we get the id and all its componenet associated with it
    comments = Comment.objects.filter(course=tutorial, reply=None).order_by('-id') # here we are filtering the comment for the relevent post and getting the latest post at the top

    # if the request is post than create a foprm object
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)

        # if the form is valid than get the comment content and than create a comment object with the course detail, user detail and the comments detail and save it
        
        if comment_form.is_valid():
            comment = request.POST.get('comment') 
            reply_id = request.POST.get('comment_id')
            qs = None

            # for reply we first get the comment id
            # if there is reply than we get the reply id 
            if reply_id:
                qs = Comment.objects.get(id=reply_id)# to knw the reply of that comment by getting the reply id to the comment id

            comment = Comment.objects.create(course=tutorial, user=request.user, comment=comment, reply=qs)
            comment.save()

            return redirect('teacher-profile')
    
    
    else:
        comment_form = CommentForm()

    context = {
        'tutorial': tutorial,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'apps/lecture.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['Teacher']) # if the user is teacher than only the use can view the page
# method to add content to app by the user 
def content_add_view(request):
   
    LectureFormset = modelformset_factory(Lecture, fields=('lecture_title', 'lecture_content', 'youtube_url'))

    # if the request is post and the form is valid than save the form
    if request.method == 'POST':
        content_add_form = ContentAddForm(request.POST or None, request.FILES or None)
        formset = LectureFormset(request.POST or None, request.FILES or None)

        if content_add_form.is_valid() and formset.is_valid():
            course = content_add_form.save(commit=False)
            course.user = request.user
            course.save()

            # looping through the formset as we need multiple fields saving it in same form. here we get the data and than save it 
            for f in formset:
                try:
                    video = Lecture(course=course, lecture_title=f.cleaned_data.get('lecture_title'), lecture_content=f.cleaned_data.get('lecture_content'), youtube_url=f.cleaned_data.get('youtube_url'))
                    video.save()
                   
                except Exception as e:
                    break
            return redirect('teacher-profile')
    else:
        content_add_form = ContentAddForm()
        formset = LectureFormset(queryset=Lecture.objects.none())

    context = {
      
        'contentForm': content_add_form,
        'formset': formset,
    }
    
    return render(request, 'apps/contentAdd.html', context)


@login_required(login_url='login')
# method created for the verification from so that the user can upload the documents to become an instructor
def verification_view(request):
    if request.method == 'POST':
        
        verify_form = VerificationForm(request.POST or None, request.FILES or None)

        # if form is valid than we save the form in virutal database and we get the user and  than save the form in database
        if verify_form.is_valid():
            verify = verify_form.save(commit=False)
            verify.user = request.user
            verify.save()
    else:
        verify_form = VerificationForm() 
    
    context = {
        
        'verify_form': verify_form,
    }

    return render(request, 'apps/verification.html', context)




@login_required(login_url='login')
# Content Edit form
def content_edit_view(request, id):
    course = get_object_or_404(Course, pk=id)
    LectureFormset = modelformset_factory(Lecture, fields=('lecture_title', 'lecture_content', 'youtube_url'), extra=0)

    if course.user != request.user:
        raise Http404()

    if request.method == 'POST':
        content_edit_form = ContentEditForm(request.POST or None, request.FILES or None, instance=course)
        formset = LectureFormset(request.POST or None, request.FILES or None)

        if content_edit_form.is_valid(): 
            content_edit_form.save()
            data = Lecture.objects.filter(course=course)

            # give index of the item for a formset item strting form 0 and (f)the item itself 
            if formset.is_valid():
                for index, f in enumerate(formset):
                    if f.cleaned_data:
                        if f.cleaned_data['id'] is None:
                            video = Lecture(course=course, lecture_title=f.cleaned_data.get('lecture_title'), lecture_content=f.cleaned_data.get('lecture_content'), youtube_url=f.cleaned_data.get('youtube_url'))
                            video.save()
                        
                        else:
                            video = Lecture(course=course, lecture_title=f.cleaned_data.get('lecture_title'), lecture_content=f.cleaned_data.get('lecture_content'), youtube_url=f.cleaned_data.get('youtube_url'))              
                            d = Lecture.objects.get(id=data[index].id) #get slide id which was uploaded
                            d.lecture_title = video.lecture_title # changing the database tiitle with new title
                            d.lecture_content = video.lecture_content #changing the database content with new content
                            d.youtube_url = video.youtube_url # changing the database content with new content
                            d.save()

                return redirect('tutorial', course.id)

            else:
                print('formset is invalid')
    
        else:
            print("form is invalid")
          
    else:
        content_edit_form = ContentEditForm(instance=course)
        formset = LectureFormset(queryset=Lecture.objects.filter(course=course))

    context = {
        'contentForm': content_edit_form,
        'course': course,
        'formset': formset,
    }

    return render(request, 'apps/contentEdit.html', context)


@login_required(login_url='login')

# method for deleting the content that was uploaded. Here we get the id of the couser and if the method is post than we delete the object
def content_delete_view(request, pk):
    delete = get_object_or_404(Course, id=pk)
    if request.method == 'POST':
        delete.delete()
        return redirect('teacher-profile')

    return render(request, 'apps/contentDelete.html', {'delete': delete})


