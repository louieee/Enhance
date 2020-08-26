import json
import os
from Enhance.settings import BASE_DIR
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import User, Attachment
from datetime import datetime


def created_24hrs_ago():
    """
    returns the number of users created over the past 24 hours
    :return:
    """
    return [x for x in User.objects.all() if (datetime.now().astimezone() - x.date_joined).days <= 1].__len__()


def created_last_week():
    """
    :returns the number of users created over the past one week
    :return:
    """
    return [x for x in User.objects.all() if (datetime.now().astimezone() - x.date_joined).days <= 7].__len__()


def created_last_month():
    """
    :returns the number of users created over the past one month
    :return:
    """
    return [x for x in User.objects.all() if
            (datetime.now().astimezone() - x.date_joined).days in range(0, 32)].__len__()


def created_last_year():
    """
    :returns the number of users created over the past one year.
    :return:
    """
    return [x for x in User.objects.all() if
            (datetime.now().astimezone() - x.date_joined).days in range(0, 367)].__len__()


def active_users():
    """
    :returns the number of active users.
    :return:
    """
    return User.objects.filter(is_active=True).count


def paid_users():
    """
    :returns the number of users that have paid.
    :return:
    """
    return User.objects.filter(paid=True).count


def send_email(user, title, message, to, link, attachments=None):
    """
    This function sends the email to the emails
    :return:
    """
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    if link is not None:
        html_message = render_to_string('Account/mailer.html',
                                        {"link": link, "message": message, "subject": title, "user": user})
    else:
        html_message = render_to_string('Account/mailer.html',
                                        {"message": message, "subject": title, "user": user})
    plain_message = strip_tags(html_message)
    from_email = 'admin@datefix.com'
    message = EmailMultiAlternatives(title, plain_message, from_email, [to])
    message.attach_alternative(html_message, 'text/html')
    if attachments is not None:
        for i in attachments:
            message.attach_file(i.file.url[1:])
            i.delete()
            os.remove(i.file.url[1:])
    message.send(True)


def mark_payed(model_admin, request, queryset):
    """
    marks selected users as paid.
    :return:
    """
    queryset.update(paid=True)
    messages.success(request, "Selected Record(s) are now marked paid.")


def mark_unpayed(model_admin, request, queryset):
    """"
    marks selected users as unpaid.
    """
    queryset.update(paid=False)
    messages.success(request, "Selected Record(s) are now marked not paid.")


def e_mail(model_admin, request, queryset):
    """
    redirects staff to the email page.
    :return:
    """
    request.session['users'] = json.dumps([x.email for x in queryset])
    return redirect('email')


def activate(model_admin, request, queryset):
    """
    marks selected users as active.
    :return:
    """
    queryset.update(is_active=True)
    messages.success(request, "Selected Record(s) are now active.")


def inactivate(model_admin, request, queryset):
    """
    marks selected users as inactive.
    """
    queryset.update(is_active=False)
    messages.success(request, "Selected Record(s) are now inactive.")
