from students.models import Student
from results.models import Result, Examination
from teachers.models import Teacher
from subjects.models import Subject
from standards.models import Standard, ClassTeacher
from accounts.models import User

def add_variable_to_context(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            try:
                student = Student.objects.get(user=request.user)
                return {'student':student}
            except Student.DoesNotExist:
                return {}
        if request.user.is_teacher:
            teacher = Teacher.objects.get(user=request.user)
            subjects = Subject.objects.filter(teacher=teacher)
            dict = {
                'teacher_cp':teacher,
                'subjects_cp':subjects
            }
            return dict
    return {}
