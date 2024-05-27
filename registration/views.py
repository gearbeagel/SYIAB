
from django.contrib.auth import logout
from django.contrib.humanize.templatetags import humanize
from django.shortcuts import render, redirect

from boxes.models import Box


def home(request):
    context = {}
    message = ''
    context['message'] = message
    if request.user.is_authenticated:
        boxes = Box.objects.filter(creator=request.user).all().order_by('-date_created')
        if boxes:
            for box in boxes:
                box.humanized_opening_date = humanize.naturaltime(box.date_opening)
            context['boxes'] = boxes
    return render(request, 'main.html', context)


def registration_view(request):
    return render(request, "registration/registration_view.html")


def logout_view(request):
    logout(request)
    return redirect("home")

