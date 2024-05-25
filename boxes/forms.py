from django import forms
from boxes.models import Box

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ('name', 'creator', 'date_opening')
        exclude = ['creator']

        widgets = {
            'date_opening': forms.DateInput(attrs={'type': 'date'}),
        }