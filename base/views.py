from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Department, Student, Course, Lecturer, VerificationCode, Session, StudentCourse,Attendance
from .forms import  LecturerForm, DepartmentForm, CourseForm
from django.contrib.auth import authenticate, login, logout
import string
import secrets
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone




# Create your views here.


def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user based on reference, username, and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User credentials are valid, log in the user
            login(request, user)
            # Check if the user has a related Student object
            if Student.objects.filter(user=user).exists():
                return redirect('verify')  # Redirect to the verify code page for students
            elif Lecturer.objects.filter(user=user).exists():
                return redirect('login') 
        else:
            # User credentials are invalid, show an error message
            error_message = 'Invalid login credentials. Please try again.'
            return render(request, 'base/login_page.html', {'error_message': error_message})
   

    return render(request, 'base/login_page.html')

def Lecturer_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user based on reference, username, and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User credentials are valid, log in the user
            login(request, user)
               # Check if the user has a related Student object
            if Student.objects.filter(user=user).exists():
                return redirect('login')  # Redirect to the verify code page for students
            elif Lecturer.objects.filter(user=user).exists():
               return redirect('lecturer_home')  # Redirect to the dashboard or any desired page after successful login
        else:
            # User credentials are invalid, show an error message
            error_message = 'Invalid login credentials. Please try again.'
            return render(request, 'base/lecturer_login.html', {'error_message': error_message})
     
     return render(request, 'base/lecturer_login.html')
    

def StudentHome(request, code):
    # Check if the user is authenticated (logged in)
    if request.user.is_authenticated:
        # Get the currently logged-in student
        student = Student.objects.get(user=request.user)
        
        if request.method == "POST":
            
            
            return redirect('attendancepage', code=code)
        # You can now access the student's attributes like student.name, student.roll_number, etc.
        
        context = {'student': student}
        return render(request, 'base/home_page.html', context)
    else:
        # Handle the case when the user is not logged in
        # You might want to redirect to a login page or show an error message.
        # For example:
        
        return render(request, 'base/login_page.html')



def generate_verification_code(lecturer, course, session, expiration_minutes):
    # Your code to generate the verification code
    alphabet = string.ascii_letters + string.digits
    verification_code = ''.join(secrets.choice(alphabet) for i in range(6))

    # Calculate expiration timestamp
    current_time = timezone.now()
    expiration_time = current_time + timedelta(minutes=expiration_minutes)

    # Store the verification code with the associated lecturer, course, and expiration time
    code = VerificationCode.objects.create(
        code=verification_code,
        lecturer=lecturer,
        course=course,
        session=session,
        expiration_time=expiration_time,
    )
    return code


@login_required
def VerifyCode(request):
    error_message = None
    current_time = timezone.now()

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            verification_code = VerificationCode.objects.get(code=code, used=False)
            session = verification_code.session
        except VerificationCode.DoesNotExist:
            error_message = 'Invalid Verification code. Please try again.'
        else:
            if verification_code.expiration_time <= current_time:
                verification_code.used = True
                verification_code.save()
                error_message = 'Verification code has expired.'
            else:
                session.expiration_time = current_time + timedelta(minutes=5)
                verification_code.used = False
                session.save()  # Save the session
                verification_code.save()  # Save the verification code

                if not request.user.is_staff:
                    student = Student.objects.get(user=request.user)

                    try:
                        student_course = StudentCourse.objects.get(student=student, course=verification_code.course)
                    except StudentCourse.DoesNotExist:
                        error_message = f"You are not enrolled in {verification_code.course}. Invalid login credentials. Please try again."
                    else:
                        # Perform verification here
                        # ...

                        messages.success(request, 'Verification successful. You can now log in.')
                        return redirect('student_home', code=code)

    return render(request, 'base/verify_code.html', {'error_message': error_message})




def MarkAttendance(request, code):
    verification_code = get_object_or_404(VerificationCode, code=code)
    lecturer = verification_code.lecturer
    course = verification_code.course
    session = verification_code.session
    student_course = StudentCourse.objects.get(student=request.user.student, course=course)  # Use get() here

    time = session.expiration_time
    time_remaining = (time - timezone.now()).total_seconds()
    if time_remaining <= 0:
        return redirect('login')

    if request.method == 'POST':
        # Check if the student is eligible to mark attendance
        if time_remaining > 0:  # No need for this check again, it's already done above
            # Mark attendance for the student
            attendance, created = Attendance.objects.get_or_create(
                StudentCourse=student_course,
                session=session,
                defaults={'attended': True}
            )
            if not created:
                attendance.attended = True
                attendance.save()
        return redirect('closing')
    
    context = {
        'verification_code': verification_code,
        'lecturer': lecturer,
        'course': course,
        'session': session,
        'time_remaining': time_remaining,
    }

    return render(request, 'base/attendance_page.html', context)


def Closing(request):

    return render(request, 'base/closing.html')



def LecturerHome(request):
    if request.user.is_authenticated:
        lecturer = Lecturer.objects.get(user=request.user)
        courses = Course.objects.filter(lecturer=lecturer)

        # Get the first course in the list of courses
        default_course = courses.first()

        # Filter the sessions for the default course and lecturer
        sessions = Session.objects.filter(course=default_course)
        available_sessions = [session for session in sessions if not session.is_attended()]

        if request.method == 'POST':
            selected_course_id = request.POST.get('course')
            selected_course = get_object_or_404(Course, id=selected_course_id)
            
            selected_session_id = request.POST.get('session')
            selected_session = get_object_or_404(Session, id=selected_session_id)

            expiration_minutes = 3
            # Generate a verification code
            code = generate_verification_code(lecturer, selected_course, selected_session, expiration_minutes)

            

            # Pass the filtered sessions to the context
            return redirect('generate', code=code.code)

        context = {'lecturer': lecturer, 'courses': courses, 'available_sessions': available_sessions, }
        return render(request, 'base/Staff_page.html', context)
    else:
        return render(request, 'base/lecturer_login.html')



def get_sessions_for_course(request):
    if request.method == 'GET':
        selected_course_id = request.GET.get('course_id')
        selected_course = get_object_or_404(Course, id=selected_course_id)
        
        sessions = Session.objects.filter(course=selected_course)
        available_sessions = [session.id for session in sessions if not session.is_attended()]

        data = {
            'available_sessions': available_sessions,
        }
        
        return JsonResponse(data)
      
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def GeneratePage(request, code):
    # Retrieve the VerificationCode object with the given code
    verification_code = get_object_or_404(VerificationCode, code=code)

    context = {'code': code, 'verification_code': verification_code}
    return render(request, 'base/generate.html', context)




def TablePage(request):

    students_table_url = reverse("students_table")
    table_home_url = reverse("table_home")
    permission_table_url = reverse("permission_table")
    context = {'table_home_url':table_home_url, 'students_table_url': students_table_url, 'permission_table_url': permission_table_url }
    
    return render(request, 'base/table.html', context)


def TableHome(request):

    context = {}
    return render(request, 'base/home.html', context)


def StudentsTable(request):
    # Get the lecturer associated with the current user
    lecturer = Lecturer.objects.get(user=request.user)

    # Get all courses related to the lecturer
    courses = Course.objects.filter(lecturer=lecturer)

    # Get all students enrolled in the courses related to the lecturer
    students = Student.objects.filter(studentcourse__course__in=courses)

    # Prepare a dictionary to store student information and strikes
    student_info = {}
    for student in students:
        # Get the StudentCourse object for the student and course combination
        student_course = StudentCourse.objects.get(student=student, course__in=courses)
        
        # Get the strikes for that StudentCourse object
        strikes = student_course.strike
        
        # Store student information and strikes in the dictionary
        student_info[student] = {
            'course': student_course.course,
            'strikes': strikes,
            'student': student,
        }

    context = {'student_info': student_info}
    return render(request, 'base/Students.html', context)


def PermissionTable(request):
    # Get the lecturer associated with the current user
    lecturer = Lecturer.objects.get(user=request.user)

    # Get all courses related to the lecturer
    courses = Course.objects.filter(lecturer=lecturer)

    # Get all students enrolled in the courses related to the lecturer
    students = Student.objects.filter(studentcourse__course__in=courses)

    # Prepare a dictionary to store student information and strikes
    student_info = {}
    for student in students:
        # Get the StudentCourse object for the student and course combination
        student_course = StudentCourse.objects.get(student=student, course__in=courses)
        
        # Get the strikes for that StudentCourse object
        strikes = student_course.strike
        
        # Store student information and strikes in the dictionary
        student_info[student] = {
            'course': student_course.course,
            'strikes': strikes,
            'student': student,
        }

    q = request.GET.get('q', '')
    course_filter = request.GET.get('courseFilter')
    # Other filter parameters similarly

    if q:
        students = students.filter(index__icontains=q)
    if course_filter:
        students = students.filter(studentcourse__course__id=course_filter)
    # Other filtering conditions

    context = {'student_info': student_info, 'q': q}
    return render(request, 'base/permission.html', context)

# def CreateStudent(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         reference = request.POST.get('reference')
#         password = request.POST.get('password')
        
#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'User does not exist')

#     login = Course.objects.all()
#     context = {'login': login}
#     return render(request, 'base/login_page.html', context)    

def Help(request):
    return render(request, 'base/help.html')    


# def SForm(request):
#     form = StudentForm()
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()

#     context = {'form': form}
#     return render(request, 'base/Sforms.html', context)

def DForm(request):
    form = DepartmentForm()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'base/dform.html', context)

def CForm(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'base/cform.html', context)

def LForm(request):
    form = LecturerForm()
    if request.method == 'POST':
        form = LecturerForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'base/Lform.html', context)

