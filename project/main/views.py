# coding: utf-8

from django.shortcuts import render, redirect, render_to_response
from .models import Subject, Question, Answer
from django.views.generic import ListView, TemplateView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from main.forms import UploadCsvForm
from main import file_handlers


class SubjectListView(ListView):
    queryset = Subject.objects.order_by('parent_subject')
    template_name = 'main/subject_list.html'
    template_title = "Список тем"

    def get_context_data(self, **kwargs):
        ctx = super(SubjectListView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


class SubjectCreateView(CreateView):
    model = Subject
    fields = ['text', 'parent_subject', ]
    template_name = 'main/add.html'
    template_title = "Новая тема"

    def form_valid(self, form):
        instance = form.save(commit=False)
        '''
        Заполнение остальных полей
        '''
        instance.save()
        return redirect(reverse_lazy('subject_list'))

    def get_context_data(self, **kwargs):
        ctx = super(SubjectCreateView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


def SubjectView(request, subject_id):
    context = {
        'subjid': subject_id,
        'template_title': "Тема «" + Subject.objects.get(pk=subject_id).text + "»",
        'obj': Subject.objects.get(pk=subject_id),
        'related': Question.objects.filter(subject=subject_id),
        }
    return render(request, 'main/subject.html', context)


class QuestionListView(ListView):
    queryset = Question.objects.order_by('subject')
    template_name = 'main/question_list.html'
    template_title = "Список вопросов"

    def get_context_data(self, **kwargs):
        ctx = super(QuestionListView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


class QuestionCreateView(CreateView):
    model = Question
    fields = ['text' ,'subject', ]
    template_name = 'main/add.html'
    template_title = "Новый вопрос"

    def form_valid(self, form):
        instance = form.save(commit=False)
        '''
        Заполнение остальных полей
        '''
        instance.save()
        return redirect(reverse_lazy('question_list'))

    def get_context_data(self, **kwargs):
        ctx = super(QuestionCreateView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


def QuestionView(request, question_id):
    context = {
        'questid': question_id,
        'template_title': "Вопрос «" + Question.objects.get(pk=question_id).
        text + "»",
        'obj': Question.objects.get(pk=question_id),
        'related': Answer.objects.filter(question=question_id),
        }
    return render(request, 'main/question.html', context)


class AnswerListView(ListView):
    queryset = Answer.objects.order_by('question')
    template_name = 'main/answer_list.html'
    template_title = "Список ответов"

    def get_context_data(self, **kwargs):
        ctx = super(AnswerListView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


class AnswerCreateView(CreateView):
    model = Answer
    fields = ['text', 'question', 'is_true', ]
    template_name = 'main/add.html'
    template_title = "Новый ответ"

    def form_valid(self, form):
        instance = form.save(commit=False)
        '''
        Заполнение остальных полей
        '''
        instance.save()
        return redirect(reverse_lazy('answer_list'))

    def get_context_data(self, **kwargs):
        ctx = super(AnswerCreateView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


def AnswerView(request, answer_id):
    context = {
        'answid': answer_id,
        'template_title': "Ответ «" + Answer.objects.get(pk=answer_id).text + "»",
        'obj': Answer.objects.get(pk=answer_id),
        }
    return render(request, 'main/answer.html', context)


def index_view(request):
    latest_subject_list = Subject.objects.order_by('-pub_date')[:5]
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_answer_list = Answer.objects.order_by('-pub_date')[:5]
    context = {
        'latest_subjects': latest_subject_list,
        'latest_questions': latest_question_list,
        'latest_answers': latest_answer_list,
        }
    return render(request, 'main/index.html',context)


class SearchView(TemplateView): # затычка
    template_name = 'main/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        return context


class UploadCsvView(TemplateView):

    template_name = 'main/upload_csv.html'
    errors = []
    parse_state = 0

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
       # if context["form"].is_valid():
        self.parse_state, self.errors = file_handlers.\
            parse_csv(request.FILES['file'])
        print(self.parse_state)
        context["errors"] = self.errors
        context["parse_state"] = self.parse_state
        return render_to_response('main/upload_result.html', context)

    def get_context_data(self, **kwargs):
        context = super(UploadCsvView, self).get_context_data(**kwargs)
        context["form"] = UploadCsvForm()
        return context
