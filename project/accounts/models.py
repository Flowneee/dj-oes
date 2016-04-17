# coding: utf-8

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager, Group)
from django.core.validators import RegexValidator, EmailValidator


class NameValidator(RegexValidator):
    regex = r'[а-яА-Я]{1,}'
    message = _('Это поле может содержать только символы кириллицы.')


class UserManager(BaseUserManager):

    def _create_user(self, email, first_name, last_name, account_level,
                     is_active, is_staff, is_superuser,
                     password, **extra_fields):
        now = timezone.now()
        if not first_name:
            raise ValueError(_('Имя обязательно'))
        if not last_name:
            raise ValueError(_('Фамилия обязательна'))
        if not email:
            raise ValueError(_('Адрес электронной почты обязателен'))
        if account_level == '3':
            is_active = True
            is_staff = True
            is_superuser = True
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, account_level=account_level,
                          date_joined=now, is_staff=is_staff,
                          is_superuser=is_superuser, is_active=is_active,
                          last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, account_level='1',
                    is_active=False, is_staff=False, is_superuser=False,
                    password=None, **extra_fields):
        return self._create_user(first_name, last_name, account_level,
                                 is_active, is_staff, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, 'Root', 'Root', '3', True, True, True,
                                 password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name=_('Адрес электронной почты'),
        max_length=254,
        validators=[EmailValidator(message=_('Введите корректный e-mail.')), ],
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_('Имя'), max_length=75,
        validators=[NameValidator(), ]
    )
    last_name = models.CharField(
        verbose_name=_('Фамилия'), max_length=75,
        validators=[NameValidator(), ]
    )
    patronymic = models.CharField(
        verbose_name=_('Отчество'),
        max_length=75, blank=True,
        null=True,
        validators=[NameValidator(), ]
    )
    study_group = models.CharField(
        verbose_name=_('Учебная группа'),
        max_length=20, blank=True,
        null=True,
    )
    # birth_date = models.DateField(
    #     verbose_name=_('Дата рождения'),
    #     validators=[BirthDateValidator(), ],
    # )
    ACCOUNT_LEVEL = [
        ('0', _('Гость')),
        ('1', _('Студент')),
        ('2', _('Преподаватель')),
        ('3', _('Администратор')),
    ]
    account_level = models.CharField(
        verbose_name=_('Тип аккаунта'),
        max_length=1,
        choices=ACCOUNT_LEVEL,
        default='0'
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Присоединился'),
        default=timezone.now
    )
    is_staff = models.BooleanField(
        verbose_name=_('Администратор'),
        default=False,
        help_text=_('Имеет ли пользователь доступ к '
                    'панели администратора.')
    )
    is_active = models.BooleanField(
        verbose_name=_('Активен'),
        default=True,
        help_text=_('Является ли пользователь активным. '
                    'Вместо удаления аккаунта снимите выбор с этого поля.')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def get_full_name(self):
        return ('{0} {1} {2}'.format(self.last_name, self.first_name,
                                     self.patronymic)).strip()

    def get_short_name(self):
        short_name = '{0} {1}.'.format(self.last_name, str(self.first_name)[0])
        if (str(self.patronymic) != ''):
            short_name += str(self.patronymic)[0] + '.'
        return short_name.strip()

    def __str__(self):
        return self.get_short_name() + ' ({0})'.format(self.email)


class ProxyGroup(Group):

    class Meta:
        proxy = True
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural


class UserRating(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        verbose_name=_('Пользователь'),
        blank=False, null=False,
        related_name='user_ratings',
    )
    subject = models.ForeignKey(
        'main.Subject',
        verbose_name=_('Тема'),
        blank=False, null=False,
    )
    value = models.IntegerField(
        verbose_name=_('Значение'),
        blank=False, null=False,
        default=0,
    )

    class Meta:
        verbose_name = _('Рейтинг пользователя по теме')
        verbose_name_plural = _('Рейтинги пользователей')
        unique_together = ('user', 'subject')

    def __str__(self):
        return self.user.get_short_name + ' ' + str(self.subject) + str(self.value)
