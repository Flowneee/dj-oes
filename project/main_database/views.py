from django.shortcuts import render, redirect
from .models import Subject, Question, Answer
from .forms import SubjectForm, QuestionForm, AnswerForm

def subject_new(request):
	if request.method == "POST":
		form = SubjectForm(request.POST)
		if form.is_valid():
			subject = form.save()
#			return redirect('main_database')
	else:
		form = SubjectForm()
	return render(request, 'main_database/subject_edit.html',{'form': form})

def question_new(request):
	if request.method == "POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			subject = form.save()
#			return redirect('main_database')
	else:	
		form = QuestionForm()
	return render(request, 'main_database/question_edit.html',{'form': form})

def answer_new(request):
	if request.method == "POST":
		form = AnswerForm(request.POST)
		if form.is_valid():
			subject = form.save()
#			return redirect('main_database')
	else:
		form = AnswerForm()
	return render(request, 'main_database/answer_edit.html',{'form': form})