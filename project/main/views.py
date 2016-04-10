# coding: utf-8

from django.shortcuts import render, redirect
from .models import Subject, Question, Answer
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

class SubjectCreateView(CreateView):
    model = Subject
    fields = ['text','parent_subject',]
    template_name = 'main/add_subject.html'
    def form_valid(self, form):
        instance = form.save(commit=False)
        '''
        Заполнение остальных полей
        '''
        instance.save()
        return redirect(reverse_lazy('subject_new'))

class QuestionCreateView(CreateView):
    model = Question
    fields = ['text','subject',]
    template_name = 'main/add_question.html'
    def form_valid(self, form):
        instance = form.save(commit=False)
        '''
        Заполнение остальных полей
        '''
        instance.save()
        return redirect(reverse_lazy('question_new'))

class AnswerCreateView(CreateView):
    model = Answer
    fields = ['text','question','is_true',]
    template_name = 'main/add_answer.html'
    def form_valid(self, form):
        instance = form.save(commit=False)
        '''
        Заполнение остальных полей
        '''
        instance.save()
        return redirect(reverse_lazy('answer_new'))


def index_view(request): # затычка
    return render(request, 'main/index.html')


class SearchView(TemplateView): # затычка
    template_name = 'main/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        return context
