from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm

class CalendarView(generic.ListView):
    model = Event
    template_name = 'students/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, self.request.user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

@login_required
def student_calendar(request):
    if not request.user.is_student:
        return HttpResponse("<h1>UNAUTHORISED</h1>")
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, d.month, request.user)
    html_cal = cal.formatmonth(withyear=True)
    context={}
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)
    return render(request,"students/calendar.html",context)

@login_required
def admin_calendar(request):
    if not request.user.is_admin:
        return HttpResponse("<h1>UNAUTHORISED</h1>")
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, d.month, request.user)
    html_cal = cal.formatmonth(withyear=True)
    context={}
    context['calendar'] = mark_safe(html_cal)
    context['prev_month'] = prev_month(d)
    context['next_month'] = next_month(d)
    return render(request,"admins/calendar.html",context)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, slug=None):
    instance = Event()
    if slug:
        type = 'delete'
        instance = Event.objects.get(slug=slug)
        if not request.user.is_admin and instance.user != request.user:
            return HttpResponse("<h1>UNAUTHORISED</h1>")
    else:
        type = None
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.save()
        if request.user.is_admin:
            return redirect('admins:calendar')
        if request.user.is_student:
            return redirect('students:calendar')
    if request.user.is_admin:
        return render(request,'admins/event.html',{'form':form,'type':type,'slug':slug})
    if request.user.is_student:
        return render(request, 'students/event.html', {'form': form,'type':type,'slug':slug})

@login_required
def event_delete(request, slug):
    instance = Event.objects.get(slug=slug)
    if not request.user.is_admin and instance.user != request.user:
        return HttpResponse("<h1>UNAUTHORISED</h1>")

    instance.delete()

    if request.user.is_admin:
        return redirect('admins:calendar')
    if request.user.is_student:
        return redirect('students:calendar')
