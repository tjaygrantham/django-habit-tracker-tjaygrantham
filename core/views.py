from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Habit, Record
from .forms import HabitForm, RecordForm
from django.contrib.auth.decorators import login_required
from lemminflect import getLemma, getInflection
from .templatetags.mytags import lemm, inflect
import json

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect(to='list_habits')
    return render(request, 'core/home.html')


@login_required
def list_habits(request):
    habits = request.user.habits.all()
    habit_form = HabitForm()
    return render(request, 'core/list_habits.html', {"habits": habits, "habit_form": habit_form})


@login_required
def show_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    record_form = RecordForm()
    record_list = [{
        'quantity': record.quantity,
        'added': record.added.strftime('%Y-%m-%d'),
    } for record in habit.records.all().order_by('added')]
    if request.user == habit.user:
        return render(request, 'core/show_habit.html', {"habit": habit, "record_form": record_form, "records": json.dumps(record_list)})
    return redirect(to='home')


@login_required
def add_habit(request):
    if request.method == 'GET':
        form = HabitForm()
    else:
        form = HabitForm(data=request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.action = habit.action.lower()
            habit.period = habit.period.lower()
            habit.unit = lemm(habit.unit, "NOUN")
            habit.save()
            return redirect(to='list_habits')
    return render(request, "core/add_habit.html", {"form": form})

@login_required
def add_record(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == 'GET':
        form = RecordForm()
    else:
        form = RecordForm(data=request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.habit = habit
            record.user = request.user
            if (not habit.lesser and record.quantity >= habit.goal) or (habit.lesser and record.quantity < habit.goal):
                record.goal_met = True
            else:
                record.goal_met = False
            try:
                record.save()
            except IntegrityError:
                print(f'There is already a record for { record.added }')
            return redirect(to='show_habit', pk=habit.pk)
    return render(request, "core/add_record.html", {"form": form, "habit": habit})

@login_required
def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if request.method == 'GET':
        form = HabitForm(instance=habit)
    else:
        form = HabitForm(data=request.POST, instance=habit)
        if form.is_valid():
            habit.save()
            return redirect(to='list_habits')
    return render(request, "core/edit_habit.html", {"form": form, "habit": habit})