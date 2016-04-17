# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CustomManager(models.Manager):
    def create(self, **kwargs):
        now = timezone.now()
        return super(CustomManager, self).create(date=now, **kwargs)


class ControlTestResult(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Тестируемый'),
        blank=False, null=False,
    )
    test = models.ForeignKey(
        'tutor.Test',
        verbose_name=_('Тест'),
    )
    subject = models.ForeignKey(
        'main.Subject',
        verbose_name=_('Тема'),
    )
    json_log = models.TextField(
        verbose_name=_('Лог')
    )
    date = models.DateTimeField(
        verbose_name=_('Дата начала прохождения'),
        blank=False,
        null=False,
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
        verbose_name = _('Результат контрольного теста')
        verbose_name_plural = _('Результаты контрольных тестов')

    def __str__(self):
        return '{0} {1} {2}'.format(str(self.user), str(self.test),
                                    str(self.date))

    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super(ControlTestResult, self).save(*args, **kwargs)
