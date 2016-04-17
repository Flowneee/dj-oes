# coding: utf-8

from random import sample, randint
import json

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from django_ajax.mixin import AJAXMixin

from main import dropdown
from main.models import Subject, Question, Answer
from project.settings import DEBUG_OUTPUT, debug_print
from public_testing.models import PublicTestResult


class MainPublicTestingView(TemplateView):
    template_name = 'public_testing/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPublicTestingView, self).\
                  get_context_data(**kwargs)
        context['subjects'] = dropdown.create_dropdown(Subject.objects,
                                                       indent=6)
        return context


def construct_subject_breadcrumbs(subject):
    string = str(subject)
    while subject.parent_subject is not None:
        subject = subject.parent_subject
        string = str(subject) + '/' + string
    return string


def get_answers(question):
    answers = question.question_answers.all()
    out = []
    if question.is_only_answer():
        out.append(answers.get(is_true=True))
        out += sample(list(answers.filter(is_true=False)), 3)
    else:
        trues = list(answers.filter(is_true=True))
        print(len(trues))
        print(question)
        out += sample(trues, randint(1, len(trues)))
        if len(out) < 4:
            out += sample(list(answers.filter(is_true=False)), 4-len(out))
    return out


def get_questions(subject, difficulty, number=20):
    def get_all_questions(subject):
        questions = list(Question.objects.filter(subject=subject))
        for i in Subject.objects.filter(parent_subject=subject):
            questions += list(get_all_questions(i))
        return questions

    questions = list(get_all_questions(subject))
    questions = [i for i in questions if i.difficulty in difficulty]
    if DEBUG_OUTPUT:
        debug_print(questions)
    if len(questions) < number:
        number = len(questions)
    return sample(questions, number)


def get_public_test_by_subject(subject, difficulty, number=20):
    content = []
    content_json = []
    for q in get_questions(subject, difficulty, number):
        q_answers = get_answers(q)

        temp = {}
        temp_json = {}
        temp['question'] = q
        temp_json['question'] = q.id
        if temp['question'].is_only_answer():
            temp['element_type'] = 'radio'
        else:
            temp['element_type'] = 'checkbox'
        temp['answers'] = q_answers
        temp_json['answers'] = []
        q_answers_order = ''
        for a in q_answers:
            q_answers_order += '{0} '.format(a.id)
            temp_json['answers'].append(a.id)
        temp_json['selection'] = []
        temp['answers_order'] = q_answers_order
        content.append(temp)
        content_json.append(temp_json)

    debug_print(content)
    return content, content_json


class PublicTestView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(PublicTestView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        subject = Subject.objects.get(id=int(self.request.GET['subject_id']))
        context['subject_breadcrumbs'] = construct_subject_breadcrumbs(subject)
        d = int(request.GET['difficulty'])
        difficulty = [d-1, d, d+1]
        test_content, test_json = get_public_test_by_subject(subject,
                                                             difficulty)
        test = PublicTestResult.objects.create(
            user=request.user,
            subject=subject,
            difficulty=d,
            json_log=json.dumps(test_json),
        )
        context['test_content'] = test_content
        context['test_id'] = test.id
        context['subject_id'] = subject.id
        self.template_name = 'public_testing/test_test.html'
        return render(request, self.template_name, context)


def create_test_result_content_from_json(test_json):
    ''' Return a ready-to-render content for test results of
    specified test_json and also return a number of correct answers '''
    test_results_content = []
    number_of_correct_answers = 0
    for i in test_json:
        temp = {}
        temp['question'] = Question.objects.get(id=i['question'])
        correct = True
        temp['answers'] = []
        if temp['question'].is_only_answer():
            temp['element_type'] = 'radio'
        else:
            temp['element_type'] = 'checkbox'

        # fill the answers field
        for j in i['answers']:
            t = {}
            t['answer'] = Answer.objects.get(id=int(j))

            # in this section setting up a style for every question
            # depending on is it true and user's choice
            if (j in i['selection']) and not t['answer'].is_true:
                t['text_style'] = 'text-danger'
                t['icon'] = False
                correct = False
                temp['answers'].append(t)
                continue
            if t['answer'].is_true:
                t['text_style'] = 'text-success'
                t['icon'] = True
                temp['answers'].append(t)
                continue
            t['text_style'] = ''
            t['icon'] = None
            # end section

            temp['answers'].append(t)
        if correct:
            temp['result'] = _('Верно!')
            number_of_correct_answers += 1
        else:
            temp['result'] = _('Неверно!')
        test_results_content.append(temp)
    return test_results_content, number_of_correct_answers


class AJAXPublicTestResultsView(AJAXMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        self.template_name = 'public_testing/ajax_test_results.html'
        context = self.get_context_data(**kwargs)
        debug_print(request.POST)
        test_results = PublicTestResult.objects.get(
            id=int(request.POST['test_id'])
        )

        # create json_log for current test
        test_json = json.loads(test_results.json_log)
        for i in test_json:
            selection = request.POST[str(i['question'])]
            if type(selection) == str:
                i['selection'].append(int(selection))
            else:
                for j in selection:
                    i['selection'].append(int(j))

        test_results_content,\
            number_of_correct_answers = create_test_result_content_from_json(
                test_json
            )

        test_results.json_log = json.dumps(test_json)
        context['test'] = test_results
        context['test_results_content'] = test_results_content
        context['number_of_correct_answers'] = number_of_correct_answers
        test_results.is_completed = True
        return render(request, self.template_name, context)











class AJAXGetPublicQuestionView(AJAXMixin, TemplateView):

    def get_context_data(self, **kwargs):

        def get_answers(question):
            answers = question.question_answers.all()
            out = []
            if question.is_only_answer():
                out.append(answers.get(is_true=True))
                out += sample(list(answers.filter(is_true=False)), 3)
            else:
                trues = list(answers.filter(is_true=True))
                out += sample(trues, randint(1, len(trues)))
                out += sample(list(answers.filter(is_true=False)), 4-len(out))
            return out

        def get_question(subject):

            def get_questions(subject):
                questions = list(Question.objects.filter(subject=subject))
                for i in Subject.objects.filter(parent_subject=subject):
                    questions += list(get_questions(i))
                return questions

            questions = list(get_questions(subject))

            if DEBUG_OUTPUT:
                debug_print(questions)

            return questions[randint(0, len(questions)-1)]

        context = super(AJAXGetPublicQuestionView, self).\
                  get_context_data(**kwargs)

        # get random question from current subject and select random answers
        context['question'] = get_question(Subject.objects.get(
            id=int(self.request.GET['subject_id'])
        ))
        context['answers'] = get_answers(context['question'])

        # create answers order string to pass it later to result request
        answ_order = ''
        for i in context['answers']:
            answ_order += (str(i.id) + ' ')

        context['answers_order'] = answ_order.strip()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.template_name = 'public_testing/ajax_question.html'
        js_ctx = {}

        # check is answer have multiple answer and selecr proper element type
        if context['question'].is_only_answer():
            context['element_type'] = 'radio'
        else:
            context['element_type'] = 'checkbox'

        js_ctx['template'] = render(self.request, self.template_name, context)

        return js_ctx


class AJAXAnswerPublicQuestionView(AJAXMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.template_name = 'public_testing/ajax_question_result.html'
        js_ctx = {}
        answers_from_tested = []  # answers from student
        answers_to_template = []

        # check is answer have multiple answer and selecr proper element type
        question = Question.objects.get(id=int(request.POST['question_id']))
        if question.is_only_answer():
            context['element_type'] = 'radio'
        else:
            context['element_type'] = 'checkbox'

        # create list with answers from POST request
        if type(request.POST['answers']) == str:
            answers_from_tested.append(request.POST['answers'])
        else:
            answers_from_tested += request.POST['answers']

        all_answers = question.question_answers.all()
        answers_order = []
        for i in request.POST['answers_order'].split():
            answers_order.append(all_answers.get(id=int(i)))

        # fill list with answers to template
        is_answers_correct = True
        for i in answers_order:
            if (str(i.id) in answers_from_tested) and\
               i.is_true is False:
                answers_to_template.append([i, False, 'text-danger'])
                is_answers_correct = False
                continue
            if i.is_true:
                answers_to_template.append([i, True, 'text-success'])
                continue
            answers_to_template.append([i, None, ''])

        context['answers_to_template'] = answers_to_template
        context['question'] = question
        context['is_answers_correct'] = is_answers_correct
        context['subject_id'] = question.subject.id
        js_ctx['template'] = render(self.request, self.template_name, context)

        return js_ctx
