import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myschool.settings')

import django
django.setup()

from students.models import Student
from results.models import Result, ExaminationName, Examination
from teachers.models import Teacher
from subjects.models import SubjectName,Subject
from standards.models import Standard, ClassTeacher
from accounts.models import User

def populate_users_for_teachers():
    print('Populating users!')
    for i in range(1,50):
        email = "t"+str(i)+"@gmail.com"
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email,password='Raghav.1',
                                            first_name='t',last_name=str(i))
            user.is_student = False
            user.is_teacher = True
            user.save()

def populate_teachers():
    print('Populating teachers!')
    for i in range(1,50):
        email = "t"+str(i)+"@gmail.com"
        user = User.objects.get(email=email)
        teacher = Teacher.objects.get_or_create(user=user)[0]
        teacher.save()


def populate_standards():
    print('Populating standardnames!')
    for i in range(1,11):
        standard = Standard.objects.get_or_create(name=str(i))[0]
        standard = standard.save()

def populate_classteachers():
    print('Populating standards')
    for i in range(1,11):
        standard = Standard.objects.get(name=str(i))
        user = User.objects.get(email="t"+str(i)+"@gmail.com")
        i=i+1
        teacher = Teacher.objects.get(user=user)
        teacher.is_class_teacher = True
        class_teacher = ClassTeacher.objects.get_or_create(standard=standard,teacher=teacher)[0]
        teacher = teacher.save()
        class_teacher.save()

def populate_subjectnames():
    subject_names = ['hindi','english','maths','science','social']
    print('Populating subjectnames!')
    i=1
    for name in subject_names:
        subjectName = SubjectName.objects.get_or_create(name=name)[0]
        subjectName.save()

def populate_subjects():
    i = 0
    teachers = Teacher.objects.all()
    subject_names = SubjectName.objects.all()
    standards = Standard.objects.all()
    for standard in standards:
        for subjectName in subject_names:
            teacher = teachers[i%10]
            print(teacher)
            subject = Subject.objects.get_or_create(name=subjectName,
                                                    standard=standard,
                                                    teacher=teacher)[0]
            subject.save()
            i = i + 1

def populate_users_for_students():
    print('Populating users!')
    for i in range(1,200):
        email = "s"+str(i)+"@gmail.com"
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email,password='Raghav.1',
                                            first_name='s',last_name=str(i))
            user.save()

def populate_students():
    print('Populating students!')
    for i in range(1,200):
        email = "s"+str(i)+"@gmail.com"
        user = User.objects.get(email=email)
        standard = Standard.objects.get(name=str(i%10+1))
        student = Student.objects.get_or_create(user=user,
                                                current_standard=standard,
                                                roll_number=i)[0]
        student.standards.add(standard)
        student.save()

def populate_examinationNames():
    exams = ['fa1','fa2','fa3','fa4','sa1','sa2','sa3']
    print('populating examination names!')
    for name in exams:
        exam = ExaminationName.objects.get_or_create(name=name)[0]
        exam.save()

def populate_examinations():
    exams = ['fa1','fa2','fa3','fa4','sa1','sa2','sa3']
    standards = Standard.objects.all()
    print('populating exams!')
    for name in exams:
        for standard in standards:
            exam = ExaminationName.objects.get(name=name)
            examination = Examination.objects.get_or_create(standard=standard,name=exam)[0]
            examination.save()

populate_users_for_teachers()
populate_teachers()
populate_standards()
populate_classteachers()
populate_subjectnames()
populate_subjects()
populate_users_for_students()
populate_students()
populate_examinationNames()
populate_examinations()
