# coding: utf-8

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import main
import accounts


class Test(models.Model):
    text = models.TextField(
        max_length=100,
        verbose_name=_('Название'),
        blank=False,
    )
    comment = models.TextField(
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

    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.pub_date = timezone.now()
        super(Test, self).save()
