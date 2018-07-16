"""Accounts related models."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    MALE = 'male'
    FEMALE = 'female'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    MR, MISS, MRS, MS, DR = ('Mr', 'Miss', 'Mrs', 'Ms', 'Dr')
    TITLE_CHOICES = (
        (MR, _("Mr")),
        (MISS, _("Miss")),
        (MRS, _("Mrs")),
        (MS, _("Ms")),
        (DR, _("Dr")),
    )

    title = models.CharField(
        pgettext_lazy(u"Treatment Pronouns for the customer", u"Title"),
        max_length=64, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(_("First name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True)

    date_or_birth = models.DateField(_('date of birth'), null=True, blank=True)
    gender = models.CharField(
        _('gender'),
        max_length=16,
        blank=True, null=True,
        choices=GENDER_CHOICES,
    )
    email = models.EmailField(_('email address'), unique=True)
    phone_number = PhoneNumberField(
        _("Phone number"), blank=True,
        help_text=_("In case we need to call you"))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.name or self.email

    def get_full_name(self):
        return self.name

    def clean(self):
        super(User, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def join_fields(self, fields, separator=u", "):
        """
        Join a sequence of fields using the specified separator
        """
        field_values = []
        for field in fields:
            # Title is special case
            if field == 'title':
                value = self.get_title_display()
            else:
                value = getattr(self, field)
            field_values.append(value)
        return separator.join(filter(bool, field_values))

    @property
    def salutation(self):
        """
        Name (including title)
        """
        return self.join_fields(
            ('title', 'first_name', 'last_name'),
            separator=u" ")

    @property
    def name(self):
        return self.join_fields(('first_name', 'last_name'), separator=u" ")

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)