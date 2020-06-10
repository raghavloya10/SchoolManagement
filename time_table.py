import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myschool.settings')

import django
django.setup()

import random,secrets
from random import seed,randint,shuffle,choice
from datetime import datetime

from collections import defaultdict
from students.models import Student
from results.models import Result, ExaminationName, Examination
from teachers.models import Teacher
from subjects.models import SubjectName,Subject
from standards.models import Standard, ClassTeacher
from accounts.models import User

standards = Standard.objects.all()
all_subjects = Subject.objects.all()
teachers = Teacher.objects.all()
subjects = {}
timetable = {}
alloted = {}
classes_per_week = {}
allowed_classes_per_day = {}
no_of_classes_per_day = 6
no_of_working_days = 5
no_of_subjects_for_a_standard = 5
standards_failed_count = 0
total_classes_in_the_week = no_of_working_days * no_of_classes_per_day
classes_per_day = {}
failed_attempts = set()
failed_attempts_1 = 0
failed_attempts_2 = 0
failed_attempts_2a = 0
failed_attempts_3 = 0
failed_attempts_3a = 0

def initialise():

    global standards_alloted,timetable, alloted, failed_attempts, failed_attempts_1
    global failed_attempts_2, failed_attempts_2a, failed_attempts_3a, failed_attempts_3

    for standard in standards:
        subjects[standard] = []
        timetable[standard] = [None]*total_classes_in_the_week

    for subject in all_subjects:
        standard = subject.standard
        subjects[standard] += [subject]
        classes_per_week[subject] = subject.classes_per_week
        allowed_classes_per_day[subject] = 2

    for teacher in teachers:
        alloted[teacher] = [None]*total_classes_in_the_week

    shuffle(list(standards))

def is_possible_basic(standard):
    total = 0
    for subject in subjects[standard]:
        total += classes_per_week[subject]
    if total != total_classes_in_the_week:
        print(total)
        print(subjects[standard])
        return False
    return True

def new_day(standard,i):

    # print("Day"+str(int(i/no_of_classes_per_day)+1))
    for subject in subjects[standard]:
            classes_per_day[subject] = 0

def start_of_the_day_index(i):
    k = int(i/no_of_classes_per_day)
    return k*no_of_classes_per_day

def nullify(standard,start,end):
    global standards_alloted,timetable, alloted, failed_attempts, failed_attempts_1
    global failed_attempts_2, failed_attempts_2a, failed_attempts_3a, failed_attempts_3

    for i in range(start,end):
        subject = timetable[standard][i]
        alloted[subject.teacher][i] = None
        timetable[standard][i] = None

def allocate_standard(standard):

    global standards_alloted,timetable, alloted, failed_attempts, failed_attempts_1
    global failed_attempts_2, failed_attempts_2a, failed_attempts_3a, failed_attempts_3

    # Check if the sum of all classes = class per week
    if not is_possible_basic(standard):
        return "Sum of subject classes is not equal to classes per week"
    # end check
    i=0

    while i<total_classes_in_the_week:
        # Start of a new day
        if i % no_of_classes_per_day == 0:
            new_day(standard,i)

        failed_attempts.clear()

        while True:

            #If no subject is possible
            if len(failed_attempts) == len(subjects[standard]):

                failed_attempts.clear()
                # try alloting the day randomly for around 10 times

                failed_attempts_1 += 1

                if failed_attempts_1 == 10:
                    failed_attempts_1 = 0
                    failed_attempts_2a += 1
                    if failed_attempts_2a == 10:
                        failed_attempts_2a = 0
                        failed_attempts_2 += 1

                k = start_of_the_day_index(i-no_of_classes_per_day*failed_attempts_2)

                if k >= 0:
                    nullify(standard,k,i)
                    i = k
                    break

                else:
                    nullify(standard,0,i)
                    failed_attempts_2 = 0
                    failed_attempts_3a += 1
                    if failed_attempts_3a == 10:
                        failed_attempts_3a = 0
                        failed_attempts_3 += 1
                    if failed_attempts_3 == 0:
                        i=0
                        break
                    if failed_attempts_3 >10:
                        return "Not at all possible"

                    previous_standard = None

                    # for j in range(failed_attempts_3):
                    #     previous_standard = list(standards).index(standard)-j
                    #     nullify(previous_standard,0,total_classes_in_the_week)
                    #
                    # return j

            k = randint(0,len(subjects[standard])-1)
            present_subject = subjects[standard][k]
            # print("i value - "+str(i)+str(present_subject))
            # print(present_subject)

            if present_subject in failed_attempts:
                continue;

            # Bounding fn 1: One day can have a subject only certain no of times

            # if classes_per_day[present_subject] == allowed_classes_per_day[present_subject]:
            #     failed_attempts.add(present_subject)
            #     # print("Too many for the day")
            #     continue

            teacher = present_subject.teacher

            # Bounding fn 2: Teacher cannot have 2 classes at a time
            if alloted[teacher][i] is not None:
                failed_attempts.add(present_subject)
                # print("teacher is already allotted")
                continue

            # print(str(i)+str(present_subject))

            alloted[teacher][i] = present_subject
            timetable[standard][i] = present_subject
            classes_per_day[present_subject] += 1
            classes_per_week[present_subject] -= 1
            if classes_per_week[present_subject] == 0:
                # print("this for the week is done")
                allowed_classes_per_day[present_subject] = 0
            i+=1
            break

    return "Successful {}".format(standard)

def generate():

    global standards_alloted,timetable, alloted, failed_attempts, failed_attempts_1
    global failed_attempts_2, failed_attempts_2a, failed_attempts_3a, failed_attempts_3

    initialise()

    global standards

    print(timetable)

    i = 0

    while i<len(standards):

        standard = standards[i]
        k = allocate_standard(standard)
        if k == "Successful {}".format(standard):
            i += 1
            continue
        elif k == "Not at all possible":
            return k
        else:
            i -= k
            continue

    return "Completely Successful"

    # for standard in standards:
    #     print("standard is "+str(standard))
    #     for i in range(1,31):
    #         print(timetable[standard][i])

print(generate())

for standard in standards:
    print("standard -> {}".format(standard))
    for i in range(total_classes_in_the_week):
        print("{} -> {}".format(str(i),timetable[standard][i]))

for i in range(10):
    teacher = teachers[i]
    print("teacher -> {}".format(teacher))
    for i in range(total_classes_in_the_week):
        print("{} -> {}".format(str(i),alloted[teacher][i]))
