from random import sample, randint

from django.views.generic import TemplateView
from django.shortcuts import render

from django_ajax.mixin import AJAXMixin

from main import dropdown
from main.models import Subject, Question


from project.settings import DEBUG_OUTPUT, debug_print


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


class PublicTestView(TemplateView):
    template_name = 'public_testing/test.html'

    def get_context_data(self, **kwargs):
        context = super(PublicTestView, self).get_context_data(**kwargs)
        context['subject_breadcrumbs'] = construct_subject_breadcrumbs(
            Subject.objects.get(id=int(self.request.GET['subject_id'])))
        context['subject_id'] = self.request.GET['subject_id']
        return context


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
