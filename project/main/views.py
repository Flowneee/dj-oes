# coding: utf-8

from django.shortcuts import render, redirect, render_to_response
from .models import Subject, Question, Answer
from django.views.generic import ListView, TemplateView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django import forms
from main.forms import UploadCsvForm
from main import file_handlers
from ckeditor.widgets import CKEditorWidget
import accounts


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
        instance.creator = self.request.user
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


class QuestionForm(forms.ModelForm):

    class Meta(object):
        model = Question
        fields = ['text', 'text_full', 'subject', ]

    def __init__(self, *args, **kwargs):
        answer_q = kwargs.pop('answer_q')
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['new_subject'] = forms.CharField(
                label="Новая тема",
                help_text="Если необходимая тема отсутствует в списке, " +
                "введите название новой темы в данное поле и установите " +
                "родительскую тему в предыдущем поле",
                required=False,
            )
        ans = ['arg0', 'arg1', 'arg2', 'arg3', 'arg4',
                'arg5', 'arg6', 'arg7', 'arg8', 'arg9']
        ans_true = ['argt0', 'argt1', 'argt2', 'argt3', 'argt4',
                'argt5', 'argt6', 'argt7', 'argt8', 'argt9']
        i = 0
        while answer_q > i:
            self.fields[ans[i]] = forms.CharField(
                label="Ответ " + str(i+1),
                widget=CKEditorWidget())
            self.fields[ans_true[i]] = forms.BooleanField(
                label="Правильный",
                required=False,
            )
            i += 1



class QuestionListView(ListView):
    queryset = Question.objects.order_by('subject')
    template_name = 'main/question_list.html'
    template_title = "Список вопросов"

    def get_context_data(self, **kwargs):
        ctx = super(QuestionListView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = 'main/add.html'
    template_title = "Новый вопрос"

    def form_valid(self, form):
        try:
            int(self.request.GET['a'])
        except:
            answer_q = 4
        else:
            if int(self.request.GET['a']) < 10:
                answer_q = int(self.request.GET['a'])
            else:
                answer_q = 10

        instance = form.save(commit=False)
        if form.cleaned_data['new_subject'] != "":
            s = Subject(
                    text=form.cleaned_data['new_subject'],
                    parent_subject=instance.subject,
                    creator=self.request.user,
                )
            s.save()
            instance.subject = s

        instance.creator = self.request.user
        instance.save()
        ans = ['arg0', 'arg1', 'arg2', 'arg3', 'arg4',
                'arg5', 'arg6', 'arg7', 'arg8', 'arg9']
        ans_true = ['argt0', 'argt1', 'argt2', 'argt3', 'argt4',
                'argt5', 'argt6', 'argt7', 'argt8', 'argt9']
        i = 0
        while answer_q > i:
            a = Answer(
                text=form.cleaned_data[ans[i]],
                question=instance,
                creator=self.request.user,
                is_true=form.cleaned_data[ans_true[i]],
            )
            a.save()
            i += 1
        return redirect(reverse_lazy('question_list'))

    def get_context_data(self, **kwargs):
        ctx = super(QuestionCreateView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx

    def get_form_kwargs(self):
        kwargs = super(QuestionCreateView, self).get_form_kwargs()
        try:
            int(self.request.GET['a'])
        except:
            kwargs['answer_q'] = 4
        else:
            if int(self.request.GET['a']) < 10:
                kwargs['answer_q'] = int(self.request.GET['a'])
            else:
                kwargs['answer_q'] = 10
        return kwargs


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
        instance.creator = self.request.user
        instance.save()
        return redirect(reverse_lazy('answer_list'))

    def get_context_data(self, **kwargs):
        ctx = super(AnswerCreateView, self).get_context_data(**kwargs)
        ctx['template_title'] = self.template_title
        return ctx


def AnswerView(request, answer_id):
    context = {
        'answid': answer_id,
        'template_title': "Ответ на вопрос «" + Answer.objects.get(
            pk=answer_id).question.text + '»',
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
    return render(request, 'main/test_index.html', context)


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
            parse_csv(request.FILES['file'], request.user)
        print(self.parse_state)
        context["errors"] = self.errors
        context["parse_state"] = self.parse_state
        return render_to_response('main/upload_result.html', context)

    def get_context_data(self, **kwargs):
        context = super(UploadCsvView, self).get_context_data(**kwargs)
        context["form"] = UploadCsvForm()
        return context
