from django import forms
from .models import Subject, Question, Answer

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('text', 'parent_subject',)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'subject',)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', 'question', 'is_true',)