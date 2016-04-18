# coding: utf-8
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.urlresolvers import reverse

import accounts
from ckeditor.fields import RichTextField


class CustomMainManager(models.Manager):
    def create(self, **kwargs):
        now = timezone.now()
        super(CustomMainManager, self).create(pub_date=now, **kwargs)


class Subject(models.Model):
    text = models.TextField(
        max_length=100,
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

    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
        blank=True,
        null=True,
    )

    creator = models.ForeignKey(
        accounts.models.User,
        verbose_name=_('Создатель'),
        related_name='user_subjects',
    )
    objects = CustomMainManager()

    class Meta:
        verbose_name = _('Тема')
        verbose_name_plural = _('Темы')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('subject-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.pub_date = timezone.now()
        super(Subject, self).save()


class Question(models.Model):

    text = models.TextField(
        max_length=100,
        verbose_name=_('Вопрос'),
        help_text="Запишите вопрос или основную его часть используя не более " +
        "100 символов при необходимости форматирования или большей длинны " +
        "вопроса, используйте поле «Текст вопроса»",
        blank=False,
    )

    text_full = RichTextField(
        verbose_name=_('Текст вопроса'),
        help_text="Если текст вопроса не умещается в заголовке или требуется " +
        "форматирование, используйте данное поле",
        blank=True,
        )

    subject = models.ForeignKey(
        'main.Subject',
        verbose_name=_('Тема'),
        related_name='subject_questions',
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
        blank=True,
        null=True,
    )
    DIFFICULTY = [
        (1, _('Легкий')),
        (2, _('Средний')),
        (3, _('Сложный')),
    ]
    difficulty = models.SmallIntegerField(
        verbose_name=_('Сложность вопроса'),
        choices=DIFFICULTY,
        default=1
    )
    is_approved = models.BooleanField(
        verbose_name=_('Отрецензирован'),
        default=False,
    )

    creator = models.ForeignKey(
        accounts.models.User,
        verbose_name=_('Создатель'),
        related_name='user_questions',
    )

    objects = CustomMainManager()

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('subject-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.pub_date = timezone.now()
        self.is_approved = self.creator.account_level in ['2', '3']
        super(Question, self).save()

    def is_only_answer(self):
        return len(self.question_answers.filter(is_true=True)) == 1


class Answer(models.Model):

    text = RichTextField(
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

    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
        blank=True,
        null=True,
    )

    creator = models.ForeignKey(
        accounts.models.User,
        verbose_name=_('Создатель'),
        related_name='user_answers',
    )

    objects = CustomMainManager()

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('subject-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.pub_date = timezone.now()
        super(Answer, self).save()
