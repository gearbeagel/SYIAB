from django.contrib.humanize.templatetags import humanize
from django.shortcuts import render

from boxes.forms import BoxForm
from boxes.models import Box, Memory


# Create your views here.

def create_a_box(request):
    form = BoxForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            box = form.save(commit=False)
            box.creator = request.user
            box.save()
    return render(request, 'boxes/create_box.html', {'form': form})


def view_box(request, id):
    box = Box.objects.get(pk=id)
    date_created_h = humanize.naturaltime(box.date_created)
    date_opening_h = humanize.naturaltime(box.date_opening)
    memories = Memory.objects.filter(box=box)
    return render(request, 'boxes/view_box.html', {'box': box,
                                                   'memories': memories,
                                                   'date_created_h': date_created_h,
                                                   'date_opening_h': date_opening_h})

def create_memory(request, box_id):
    pass
