import json

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from Account.functions import send_email


@csrf_exempt
def email(request):
    """
    This view allows staffs to send emails to users.
    :param request:
    :return:
    """
    if request.user.is_staff:
        if request.method == 'GET':
            if 'users' in request.session:
                context = {"users": json.loads(request.session['users']),
                           "user": request.user}
                del request.session['users']
                return render(request, 'index.html', context)
            else:
                return redirect('admin/')
        if request.method == 'POST':
            message = request.POST['message']
            subject = request.POST['subject']
            count = 1
            attachments = []
            while f'attach_{count}' in request.FILES:
                from Account.models import Attachment
                attach = Attachment()
                attach.file = request.FILES[f'attach_{count}']
                attach.save()
                attachments.append(attach)
                count = count + 1
            emails = str(request.POST['email']).split(',')[:-1]
            send_email(None, subject, message, emails, None, attachments)
            from django.contrib import messages
            messages.success(request, "Selected Record(s) have been emailed successfully")
            return redirect('admin/Account/user/')
    else:
        return redirect('index')


def index(request):
    """
    The index page.
    :param request:
    :return:
    """
    return redirect('/admin')
