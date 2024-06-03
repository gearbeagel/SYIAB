from django import forms
from django.core.exceptions import ValidationError

from boxes.models import Box, Memory


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ('name', 'date_opening', 'category')

        widgets = {
            'date_opening': forms.DateInput(attrs={'type': 'datetime-local'}),
        }


class MemoryForm(forms.ModelForm):
    text_content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    image_content = forms.ImageField(required=False)
    video_content = forms.FileField(required=False)
    audio_content = forms.FileField(required=False)
    file_content = forms.FileField(required=False)

    class Meta:
        model = Memory
        fields = ['box', 'name', 'content_type', 'description', 'text_content', 'image_content', 'video_content', 'audio_content', 'file_content']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super(MemoryForm, self).__init__(*args, **kwargs)
        self.fields['image_content'].widget.attrs.update({'class': 'form-control-file', 'accept': 'image/*'})
        self.fields['video_content'].widget.attrs.update({'class': 'form-control-file', 'accept': 'video/*'})
        self.fields['audio_content'].widget.attrs.update({'class': 'form-control-file', 'accept': 'audio/*'})
        self.fields['box'].required = False