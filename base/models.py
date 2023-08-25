# models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Department(models.Model):
    dno = models.PositiveIntegerField(unique=True)
    dname = models.CharField(max_length=100)
    

    def __str__(self):
        return self.dname


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    SN = models.PositiveIntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=40)
    code = models.PositiveIntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE) 
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name



class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()  
    time = models.TimeField()
    expiration_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=5))  # Initial expiration time
    sessions = models.PositiveIntegerField(default=15)
    
    def is_attended(self):
        return self.attendance_set.filter(attended=True).exists()

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        if not self.time:
            self.time = timezone.now().time()
        super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reference = models.PositiveIntegerField(unique=True)
    index = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=60)
    year = models.PositiveIntegerField()
    Total_strike = models.PositiveIntegerField(default=0)
    
    programme = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    strike = models.PositiveIntegerField(default=0)

@receiver(post_save, sender=Student)
def assign_program_courses(sender, instance, created, **kwargs):
    if created:
        if instance.programme:
            courses = Course.objects.filter(department=instance.programme)
            for course in courses:
                StudentCourse.objects.create(student=instance, course=course)


class VerificationCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code


# Signal to automatically create 15 sessions for each course after course creation
@receiver(post_save, sender=Course)
def create_sessions(sender, instance, created, **kwargs):
    if created:
        for i in range(15):
            session = Session.objects.create(
                course=instance,
                date=timezone.now().date(),  # Set the date to current date
                time=timezone.now().time(),  # Set the time to current time
                expiration_time=timezone.now() + timezone.timedelta(minutes=5)  # Initial expiration time
            )


class Attendance(models.Model):
    StudentCourse = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.attended:
            self.StudentCourse.strike += 0
        else:
            self.StudentCourse.strike += 1
        self.StudentCourse.save()
        super(Attendance, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - Session {self.session.sessions}"