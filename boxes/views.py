from django.contrib import messages
from django.contrib.humanize.templatetags import humanize
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from boxes.forms import BoxForm, MemoryForm
from boxes.models import Box, Memory


# Create your views here.

def create_a_box(request):
    context = {}
    form = BoxForm(request.POST)
    context['form'] = form
    if request.method == "POST":
        if form.is_valid():
            box = form.save(commit=False)
            box.creator = request.user
            if form.cleaned_data['date_opening'] < timezone.now():
                message = "The date can't be in the past :/"
                context['message'] = message
                return render(request, 'boxes/create_box.html', context)
            box.save()
            message = "Your box has been created."
            messages.success(request, message, extra_tags='success')
            return redirect('home')
    return render(request, 'boxes/create_box.html', context)


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
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.box = box
            memory.save()
            message = "Your memory has been created."
            messages.success(request, message, extra_tags='success')
            return redirect('view_box', box_id=box.pk)

    return render(request, 'boxes/create_memory.html', context)


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
    messages.success(request, message)
    return redirect('view_box', box_id=box.pk)


def delete_box(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    box.delete()
    message = "Your box has been deleted."
    messages.info(request, message)
    return redirect('home')
