from django.contrib import admin
from django.urls import path
from . import views  


urlpatterns = [
   path('', views.student_login, name="login"),
   path('lecturer_login/', views.Lecturer_login, name="lecturer_login"),
   path('studenthome/<str:code>/', views.StudentHome, name="student_home"),
   path('lecturerhome/', views.LecturerHome, name="lecturer_home"),
   path('generate/<str:code>/', views.GeneratePage, name='generate'),
   path('generate_verification_code/', views.generate_verification_code, name='generate_verification_code'),
   path('verification/', views.VerifyCode, name="verify"),
   path('attendance/<str:code>/', views.MarkAttendance, name="attendancepage"),
   path('closing/', views.Closing, name='closing'),
   path('get_sessions_for_course/', views.get_sessions_for_course, name='get_sessions_for_course'),
   path('table/', views.TablePage, name="table"),
   path('tablehome/', views.TableHome, name="table_home"),
   path('students', views.StudentsTable, name="students_table"),
   path('permission', views.PermissionTable, name="permission_table"),
   path('Help/', views.Help, name="help"),
   
]
