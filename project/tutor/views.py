# coding: utf-8

from django.shortcuts import render, redirect
from .models import Test
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django import forms

from main import dropdown
from main.models import Subject, Question
from django.views.generic import TemplateView


def index_view(request):
    context = {}
    return render(request, 'tutor/tutor.html', context)


class TestForm(forms.ModelForm):

    class Meta(object):
        model = Test
        fields = ['text', 'comment', 'questions']

    def __init__(self, *args, **kwargs):
        subject_id = kwargs.pop('subject_id')
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['questions'] = forms.ModelMultipleChoiceField(
            queryset=Question.objects.filter(subject=Subject.objects.get(
                pk=subject_id)),
            widget=forms.CheckboxSelectMultiple)


class TestCreateView(CreateView):
    form_class = TestForm
    template_name = 'main/add.html'
    try:
        self.request.GET['subject_id']
    except:
        subject_id = 1
    else:
        subject_id = self.request.GET['subject_id']

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.subject = Subject.objects.get(pk=self.subject_id)
        instance.save()
        form.save_m2m()
        return redirect(reverse_lazy('tutor_subject_list'))

    def get_form_kwargs(self):
        kwargs = super(TestCreateView, self).get_form_kwargs()
        kwargs['subject_id'] = self.subject_id
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(TestCreateView, self).get_context_data(**kwargs)
        ctx['template_title'] = "Новый тест по теме «" + Subject.objects.get(
                pk=self.subject_id).text + "»"
        return ctx


def TestView(request, test_id):
    context = {
        'template_title': "Тест «" + Test.objects.get(pk=test_id).text + "»",
        'obj': Test.objects.get(pk=test_id),
        }
    return render(request, 'tutor/test.html', context)


class SubjectView(TemplateView):
    template_name = 'tutor/subject.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectView, self).\
                  get_context_data(**kwargs)
        context['subjects'] = dropdown.create_dropdown(Subject.objects,
                                                       indent=6)
        return context


class SubjectTestView(SubjectView):
    template_name = 'tutor/subject_choise.html'


def TestListView(request, subject_id):
    subject_test_list = Test.objects.filter(subject=subject_id)
    context = {
        'template_title': "Тесты по теме «" +
        Subject.objects.get(pk=subject_id).text + "»",
        'test_list': subject_test_list,
    }
    return render(request, 'tutor/test_list.html', context)
