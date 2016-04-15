from django.shortcuts import render, redirect, render_to_response
from main.models import Subject, Question, Answer
from django.views.generic import ListView, TemplateView, DetailView, DeleteView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from main import dropdown


class MainCommunityTestingView(TemplateView):
    template_name = 'community_testing/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainCommunityTestingView, self).\
                  get_context_data(**kwargs)
        context['subjects'] = dropdown.create_dropdown(Subject.objects)
        return context


def construct_subject_breadcrubs(subject):
    string = str(subject)
    while subject.parent_subject is not None:
        subject = subject.parent_subject
        string = str(subject) + '/' + string
    return string


class CommunityTestView(TemplateView):
    template_name = 'community_testing/test.html'

    def get_context_data(self, **kwargs):
        context = super(CommunityTestView, self).get_context_data(**kwargs)
        context['subject_breadcrumbs'] = construct_subject_breadcrubs(
            Subject.objects.get(id=int(self.request.GET['subject_id'])))
        return context
