from django.shortcuts import render

from boxes.forms import BoxForm
from boxes.models import Box


# Create your views here.

def create_a_box(request):
    form = BoxForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            box = form.save(commit=False)
            box.creator = request.user
            box.save()
    return render(request, 'box_creation/create_box.html', {'form': form})