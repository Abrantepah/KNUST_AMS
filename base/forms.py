from django.forms import ModelForm
from .models import Course, Lecturer, Department
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# class StudentForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = '__all__'

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class LecturerForm(ModelForm):
    class Meta:
        model = Lecturer
        fields = '__all__'        