from django.contrib import messages
from django.contrib.humanize.templatetags import humanize
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from boxes.forms import BoxForm, MemoryForm
from boxes.models import Box, Memory
from boxes.serializers import BoxSerializer, MemorySerializer


# Create your views here.

def create_a_box(request):
    context = {}
    form = BoxForm(request.POST)
    context['form'] = form
    if request.method != "POST":
        return render(request, 'boxes/create_edit_box.html', context)
    if form.is_valid():
        box = form.save(commit=False)
        box.creator = request.user
        if form.cleaned_data['date_opening'] < timezone.now():
            message = "The date can't be in the past :/"
            messages.error(request, message)
            print(message)
            return render(request, 'boxes/create_edit_box.html', context)
        box.save()
        message = "Your box has been created."
        messages.success(request, message, extra_tags='success')
        return redirect('home')
    else:
        return render(request, 'boxes/create_edit_box.html', context)


def view_box(request, box_id):
    box = Box.objects.get(pk=box_id)
    date_created_h = humanize.naturaltime(box.date_created)
    date_opening_h = humanize.naturaltime(box.date_opening)
    memories = Memory.objects.filter(box=box).all()
    return render(request, 'boxes/view_box.html', {'box': box,
                                                   'memories': memories,
                                                   'date_created_h': date_created_h,
                                                   'date_opening_h': date_opening_h})


def create_memory(request, box_id):
    context = {}
    box = get_object_or_404(Box, pk=box_id)
    form = MemoryForm()
    message = ''
    context['form'] = form
    if request.method != 'POST':
        return render(request, 'boxes/create_edit_memory.html', context)
    form = MemoryForm(request.POST, request.FILES)
    if form.is_valid():
        memory = form.save(commit=False)
        memory.box = box
        memory.save()
        message = "Your memory has been created."
        messages.success(request, message, extra_tags='success')
        return redirect('view_box', box_id=box.pk)


def view_memory(request, box_id, memory_id):
    context = {}
    memory = get_object_or_404(Memory, pk=memory_id)
    box = get_object_or_404(Box, pk=box_id)
    context['box'] = box
    context['memory'] = memory
    return render(request, 'boxes/view_memory.html', context)


def delete_memory(request, box_id, memory_id):
    memory = get_object_or_404(Memory, pk=memory_id)
    box = get_object_or_404(Box, pk=box_id)
    memory.delete()
    message = "Your memory has been deleted."
    messages.info(request, message)
    return redirect('view_box', box_id=box.pk)


def delete_box(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    box.delete()
    message = "Your box has been deleted."
    messages.info(request, message)
    return redirect('home')


def lock_box(request, box_id):
    box = get_object_or_404(Box, pk=box_id)

    if box is None:
        pass

    box.status = Box.Statuses.LOCKED
    box.save()

    message = 'Your box has been locked successfully!'
    messages.success(request, message)
    return redirect('home')


def edit_box(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    if not box:
        pass
    form = BoxForm(request.POST, instance=box)
    context = {'box': box, 'form': form}
    if form.is_valid():
        form.save()
        message = "Your box has been edited."
        messages.success(request, message, extra_tags='success')
        return redirect('view_box', box_id=box.pk)
    return render(request, 'boxes/create_edit_box.html', context)


# DRF ViewSet for API
class BoxViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        box = get_object_or_404(Box, pk=pk)
        serializer = BoxSerializer(box)
        return Response(serializer.data)

    def create(self, request):
        serializer = BoxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        box = get_object_or_404(Box, pk=pk)
        serializer = BoxSerializer(box, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        box = get_object_or_404(Box, pk=pk)
        box.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemoryViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        memory = get_object_or_404(Memory, pk=pk)
        serializer = MemorySerializer(memory)
        return Response(serializer.data)

    def create(self, request):
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        memory = get_object_or_404(Memory, pk=pk)
        serializer = MemorySerializer(memory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        memory = get_object_or_404(Memory, pk=pk)
        memory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
