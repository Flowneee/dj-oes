# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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
        verbose_name=_('Вопрос'),
        blank=False,
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
        super(Question, self).save()

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

    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
        blank=True,
        null=True,
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
