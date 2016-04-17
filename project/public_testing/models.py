# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CustomManager(models.Manager):
    def create(self, **kwargs):
        now = timezone.now()
        return super(CustomManager, self).create(date=now, **kwargs)


class PublicTestResult(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Тестируемый'),
        blank=False, null=False,
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
    subject = models.ForeignKey(
        'main.Subject',
        verbose_name=_('Тема'),
    )
    json_log = models.TextField(
        verbose_name=_('Лог')
    )
    date = models.DateTimeField(
        verbose_name=_('Дата прохождения'),
        blank=True,
        null=True,
    )
    result = models.IntegerField(
        verbose_name=_('Результат'),
        blank=False, null=False,
        default=0
    )
    is_completed = models.BooleanField(
        verbose_name=_('Завершен'),
        default=False,
    )

    objects = CustomManager()

    class Meta:
        verbose_name = _('Результат теста')
        verbose_name_plural = _('Результаты тестов')

    def __str__(self):
        return '{0} {1} {2}'.format(str(self.user),
                                    str(self.subject), str(self.date))

    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super(PublicTestResult, self).save(*args, **kwargs)
