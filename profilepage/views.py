import random

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from profilepage import utils
from profilepage.forms import ProfileForm
from profilepage.models import ProfilePicture
from profilepage.serializers import UserSerializer


def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile_picture, created = ProfilePicture.objects.get_or_create(user=user)
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


def delete_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        raise Http404("You do not have permission to delete this profile.")
    logout(request)
    user.delete()
    messages.success(request, 'Your profile has been deleted.')
    return redirect('home')


class ProfileViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UserSerializer(user)
        motivation = random.choice(utils.motivational_quotes).lower()
        data = serializer.data
        data['motivation'] = motivation
        return Response(data)

    @action(detail=True, methods=['put'])
    def edit(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        if user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        logout(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
