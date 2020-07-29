# from django.shortcuts import render,get_object_or_404,redirect
# from django.urls import reverse_lazy
# from django.utils import timezone
# from django.http import HttpResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
# from django.views.generic import (TemplateView,ListView,
#                                   DetailView, CreateView,
#                                   UpdateView, DeleteView)
# from django.contrib.auth import authenticate, get_user_model, login

# from students.models import Student
# from results.models import Result, Examination
# from teachers.models import Teacher
# from subjects.models import Subject
# from standards.models import Standard, ClassTeacher
# from accounts.models import User


# class StandardTemplateView(LoginRequiredMixin, TemplateView):
#     template_name = 'standards/class_teacher_home.html'

#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         if not user.is_teacher:
#             context['not_teacher'] = True
#         else:
#             teacher = Teacher.objects.get(user=user)
#             context['teacher'] = teacher
#             class_teacher = ClassTeacher.objects.get(teacher=teacher)
#             standard = class_teacher.standard
#             context['standard'] = standard
#             context['students'] = Student.objects.filter(current_standard=standard)

#         return context

# # @login_required
# # def class_teacher_view(request):
# #     user = request.user
# #     if not user.is_teacher:
# #         return HttpResponse('<h1>You are not a teacher</h1>')
# #     class_teacher = ClassTeacher.objects.get(pk=pk)
# #     standard = class_teacher.standard
# #     students = Student.objects.filter(standard=standard)
# #     subjects = Subject.objects.filter(standard=standard)
# #     teacher = class_teacher.teacher
# #
# #     if teacher.user != request.user :
# #         return HttpResponse('<h1>You are not allowed to access this page</h1>')
# #
# #     info = {}
# #
# #     for student in students:
# #         d1 = student.roll_number
# #         for subject in subjects:
# #             try:
# #                 result = Result.objects.get(student=student, subject=subject)
# #                 info.setdefault(d1, {})[subject] = result.marks_secured
# #             except Result.DoesNotExist:
# #                 info.setdefault(d1, {})[subject] = ""
# #
# #     my_dict = {
# #         'standard': standard,
# #         'teacher': teacher,
# #         'subjects': Subject.objects.filter(standard=standard),
# #         'students': students,
# #         'marks': info,
# #     }
# #
# #     return render(request,'teacher/class_teacher_home.html',context=my_dict)
# #
# # # class ClassTeacherTemplateView(LoginRequiredMixin, TemplateView):
# # #     template_name = 'teacher/class_teacher_home.html'
# # #
# # #     def get_context_data(self,**kwargs):
# # #         context = super().get_context_data(**kwargs)
# # #         pk = self.kwargs['pk']
# # #         class_teacher = ClassTeacher.objects.get(pk=pk)
# # #         teacher = class_teacher.teacher
# # #         standard = class_teacher.standard
# # #         if teacher.user != req.user :
# # #             return HttpResponse('<h1>You are not allowed to access this page</h1>')
# # #         context['standard'] = standard
# # #         context['teacher'] = teacher
# # #         context['subjects'] = Subject.objects.filter(standard=standard)
# # #         students = Student.objects.filter(standard=standard)
# # #         for student in students:
# # #             for subject in subjects:
# # #                 context[d1] = {}
# # #                 try:
# # #                     result = Result.objects.get(student=student, subject=subject)
# # #                     context[d1].update(str(result.subject): str(result.marks_secured))
# # #                 except Result.DoesNotExist:
# # #                     context[d1].update(str(result.subject): "")
