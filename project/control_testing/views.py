import json

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseNotFound

from django_ajax.mixin import AJAXMixin

from accounts.models import User
from tutor.models import Test
from public_testing.views import construct_subject_breadcrumbs,\
    create_test_result_content_from_json
from main.models import Subject, Question, Answer
from project.settings import DEBUG_OUTPUT, debug_print
from .models import ControlTestResult


class ControlTestingListView(TemplateView):
    template_name = 'control_testing/main.html'

    def get_context_data(self, **kwargs):
        context = super(ControlTestingListView, self).\
                  get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['avaliable_tests'] = Test.objects.filter(
            study_groups__icontains=request.user.study_group,
        )
        return render(request, self.template_name, context)


class ControlTestDetailsView(TemplateView):
    template_name = 'control_testing/control_test_details_before_testing.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        test = Test.objects.get(id=int(request.GET['test_id']))
        if request.user.study_group.lower() not in test.study_groups.lower():
            return HttpResponseNotFound('<h1>Error 404: Not found!</h1>')
        context['subject_breadcrumbs'] = construct_subject_breadcrumbs(
            test.subject
        )
        print(context['subject_breadcrumbs'])
        context['test'] = test
        return render(request, self.template_name, context)


def get_control_test_content_from_json(test_json):
    content = []
    for i in test_json:
        temp = {}
        temp['question'] = Question.objects.get(id=i['question'])
        temp['answers'] = []
        if temp['question'].is_only_answer():
            temp['element_type'] = 'radio'
        else:
            temp['element_type'] = 'checkbox'

        for j in i['answers']:
            temp['answers'].append(Answer.objects.get(id=j))
        content.append(temp)
    return content


class ControlTestView(TemplateView):

    def get(self, request, *args, **kwargs):
        self.template_name = 'control_testing/control_test.html'
        context = self.get_context_data(**kwargs)
        debug_print(request.GET)
        test = Test.objects.get(id=int(request.GET['test_id']))
        test_json = json.loads(test.test_json)
        context['test_content'] = get_control_test_content_from_json(
            test_json
        )
        for i in test_json:
            i['selection'] = []

        context['test'] = test
        if request.user.study_group.lower() not in test.study_groups.lower():
            return HttpResponseNotFound('<h1>Error 404: Not found!</h1>')
        debug_print(context['test_content'])
        context['subject_breadcrumbs'] = construct_subject_breadcrumbs(
            test.subject
        )

        test_result, created = ControlTestResult.objects.update_or_create(
            user=request.user,
            test=test,
            subject=test.subject,
            defaults={
                'json_log': json.dumps(test_json),
            }
        )
        return render(request, self.template_name, context)


class AJAXControlTestResultsView(AJAXMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        self.template_name = 'control_testing/ajax_control_test_results.html'
        context = self.get_context_data(**kwargs)
        if DEBUG_OUTPUT:
            debug_print(request.POST)
        test = Test.objects.get(id=int(request.POST['test_id']))
        test_results = ControlTestResult.objects.get(
            user=request.user,
            test=test
        )

        test_json = json.loads(test_results.json_log)
        for i in test_json:
            selection = request.POST[str(i['question'])]
            if type(selection) == str:
                i['selection'].append(int(selection))
            else:
                for j in selection:
                    i['selection'].append(int(j))
        if DEBUG_OUTPUT:
            debug_print(test_json)
        test_results_content,\
            number_of_correct_answers = create_test_result_content_from_json(
                test_json
            )

        test_results.json_log = json.dumps(test_json)
        test_results.result = number_of_correct_answers
        context['test'] = test
        context['subject_breadcrumbs'] = construct_subject_breadcrumbs(
            test.subject
        )
        context['testing_date'] = test_results.date
        context['test_results_content'] = test_results_content
        context['number_of_correct_answers'] = number_of_correct_answers
        test_results.is_completed = True
        test_results.save()
        return render(request, self.template_name, context)
