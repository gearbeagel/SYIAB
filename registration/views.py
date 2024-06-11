from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.humanize.templatetags import humanize
from django.shortcuts import render, redirect

from boxes.models import Box
from registration.forms import RegistrationForm, LoginForm


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
    registration_form = RegistrationForm()

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            username = registration_form.cleaned_data.get('username')
            raw_password = registration_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful. You are now logged in!')
                return redirect('home')
            else:
                messages.error(request, 'Failed to authenticate after registration.')
        else:
            for field, errors in registration_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    return render(request, "registration/registration_view.html", {'registration_form': registration_form})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            for field, errors in login_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        login_form = LoginForm()

    return render(request, "registration/login_view.html", {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect("home")
