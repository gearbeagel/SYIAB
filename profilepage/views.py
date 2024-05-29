import random

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from profilepage import utils
from profilepage.forms import ProfileForm
from profilepage.models import ProfilePicture


# Create your views here.
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile_picture = get_object_or_404(ProfilePicture, user=user)
    motivation = random.choice(utils.motivational_quotes).lower()

    context = {
        'user': user,
        'profile_picture': profile_picture,
        'motivation': motivation,
    }

    return render(request, 'profile/profile_page.html', context)


def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('view_profile', username=form.cleaned_data['username'])

    return render(request, 'profile/profile_settings.html', {'form': form})
