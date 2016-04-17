# coding: utf-8

import json

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.views.generic import TemplateView

from main import dropdown
from main.models import Subject, Question
from .models import Test, get_test_json_from_test
from project.settings import DEBUG_OUTPUT, debug_print


def index_view(request):
    context = {}
    return render(request, 'tutor/tutor.html', context)


def get_subject_subtree_as_list(subject):
    subjects = [subject, ]
    for i in Subject.objects.filter(parent_subject=subject):
        subjects += get_subject_subtree_as_list(i)
    if DEBUG_OUTPUT:
        debug_print(subjects)
    return subjects


class TestForm(forms.ModelForm):

    class Meta(object):
        model = Test
        fields = ['text', 'comment', 'time_for_test', 'study_groups', 'questions']

    def __init__(self, *args, **kwargs):
        subject_id = kwargs.pop('subject_id')
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['questions'] = forms.ModelMultipleChoiceField(
            queryset=Question.objects.filter(
                subject__in=get_subject_subtree_as_list(
                    Subject.objects.get(pk=subject_id)
                )
            ),
            widget=forms.CheckboxSelectMultiple
        )


class TestCreateView(CreateView):
    form_class = TestForm
    template_name = 'main/add.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.subject = Subject.objects.get(
            pk=self.request.GET['subject_id']
        )
        instance.save()
        form.save_m2m()
        instance.test_json = json.dumps(get_test_json_from_test(instance))
        instance.save()
        return redirect(reverse_lazy('tutor_subject_list'))

    def get_form_kwargs(self):
        kwargs = super(TestCreateView, self).get_form_kwargs()
        try:
            self.request.GET['subject_id']
        except:
            kwargs['subject_id'] = 1
        else:
            kwargs['subject_id'] = self.request.GET['subject_id']
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(TestCreateView, self).get_context_data(**kwargs)
        try:
            self.request.GET['subject_id']
        except:
            subject_id = 1
        else:
            subject_id = self.request.GET['subject_id']
        subject = Subject.objects.get(pk=subject_id)
        ctx['template_title'] = "Новый тест по теме «" + subject.text + "»"
        return ctx


def TestView(request, test_id):
    test = Test.objects.get(pk=test_id)
    context = {
        'template_title': "Тест «" + test.text + "»",
        'obj': test,
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
