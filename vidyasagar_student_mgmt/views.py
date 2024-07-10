from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from app.emailbackend import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from app.models import customuser, Course
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def BASE(request):
    return render(request,'base.html')

def LOGIN(request):
    return render(request,'login.html')


def doLogin(request):
    if request.method == "POST":
        user= EmailBackEnd.authenticate(request,
                                        username=request.POST.get('email'),
                                        password= request.POST.get('password'),
                                        )
        if user!= None:
            login(request, user)
            user_type = user.user_type
            if user_type =='1':
                return redirect('hod_home')
            elif user_type =='2':
                return redirect('staff_home')
            elif user_type =='3':
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login! Check Your Credentials")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login! Check Your Credentials")
            return redirect('login')


    return None


def doLogout(request):
    logout(request)
    return redirect('login')


def PROFILE(request):
    user= customuser.objects.get(id= request.user.id)

    context = {
        "user": user,
    }

    return render(request, 'profile.html')


def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            user = customuser.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name

            if password !=None and password != "" :
                user.set_password(password)

            user.save()
            messages.success(request, 'Your Profile Updated Successfully !!')
            return redirect('profile')
        except customuser.DoesNotExist:
            messages.error(request, 'User does not exist!')
        except Exception as e:
            messages.error(request, f'Failed to update profile! Error: {e}')

    return render(request, 'profile.html')


    return render(request, 'profile.html')

# views.py



def admin_manage_timetable(request, student_id):
    student = get_object_or_404(User, id=student_id)
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.user = student
            timetable.save()
            return redirect('admin_view_student', student_id=student.id)
    else:
        form = TimetableForm()
    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'admin_manage_timetable.html', context)
