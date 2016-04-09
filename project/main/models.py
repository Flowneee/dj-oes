# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subject(models.Model):

    text = models.TextField(
        verbose_name=_('Тема'),
        blank=False,
    )
    parent_subject = models.ForeignKey(
        'self',
        verbose_name=_('Надтема'),
        related_name='child_subjects',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Тема')
        verbose_name_plural = _('Темы')
    def __str__(self):
        return self.text    

    def __str__(self):
        return self.text


class Question(models.Model):

    text = models.TextField(
        verbose_name=_('Вопрос'),
        blank=False,
    )
    subject = models.ForeignKey(
        'main.Subject',
        verbose_name=_('Тема'),
        related_name='subject_questions',
    )

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
    def __str__(self):
        return self.text         

    def __str__(self):
        return self.text


class Answer(models.Model):

    text = models.TextField(
        verbose_name=_('Ответ'),
        blank=False,
    )
    question = models.ForeignKey(
        'main.Question',
        verbose_name=_('Вопрос'),
        related_name='question_answers',
    )
    is_true = models.BooleanField(
        verbose_name=_('Правильный'),
        blank=False,
    )

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    def __str__(self):
        return self.text
