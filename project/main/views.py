# coding: utf-8

from django.shortcuts import render, redirect
from .models import Subject, Question, Answer
from .forms import SubjectForm, QuestionForm, AnswerForm
from django.views.generic import TemplateView

def subject_new_view(request): # временное решение
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            # return redirect('main_database')
        else:
            (form) = SubjectForm()
            return render(request, 'main/subject_edit.html',
                          {'form': form})


def question_new_view(request): # временное решение
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            subject = form.save()
            # return redirect('main_database')
        else:
            form = QuestionForm()
            return render(request, 'main/question_edit.html',
                          {'form': form})


def answer_new_view(request): # временное решение
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            subject = form.save()
            # return redirect('main_database')
        else:
            form = AnswerForm()
            return render(request, 'main/answer_edit.html',
                          {'form': form})


def index_view(request): # затычка
    return render(request, 'main/index.html')


class SearchView(TemplateView): # затычка
    template_name = 'main/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        return context
