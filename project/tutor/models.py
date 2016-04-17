# coding: utf-8
from __future__ import absolute_import

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

import main
import accounts
from project.settings import DEBUG_OUTPUT, debug_print


def get_test_json_from_test(test):
    content_json = []

    for q in test.questions.all():
        temp = {}
        temp['question'] = q.id
        temp['answers'] = []
        for a in q.question_answers.all():
            temp['answers'].append(a.id)
        content_json.append(temp)

    if DEBUG_OUTPUT:
        debug_print(content_json)
    return content_json


class Test(models.Model):
    text = models.TextField(
        max_length=100,
        verbose_name=_('Название'),
        blank=False,
    )
    comment = RichTextField(
        verbose_name=_('Комментарий'),
        blank=True,
    )
    subject = models.ForeignKey(
        main.models.Subject,
        verbose_name=_('Тема'),
        related_name='theme_tests',
        blank=False,
    )
    questions = models.ManyToManyField(
        main.models.Question,
        verbose_name=_('Включенные вопросы'),
        related_name='question_tests',
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
    )
    creator = models.ForeignKey(
        accounts.models.User,
        verbose_name=_('Создатель'),
        related_name='user_tests',
    )
    test_json = models.TextField(
        verbose_name=_('Тест в виде JSON'),
    )
    time_for_test = models.IntegerField(
        verbose_name=_('Время на прохождение теста (минут)'),
        default=45,
    )
    study_groups = models.TextField(
        verbose_name=_('Учебныe группы'),
        max_length=20, help_text=_('Введите названия групп, для которых '
                                   'доступен данный тест. Группы вводятся '
                                   'через запятую: ИСБО-03-13,ИСБО-02-13 .')
    )

    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.pub_date = timezone.now()
        super(Test, self).save()
