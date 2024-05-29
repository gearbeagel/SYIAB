from django import forms
from django.contrib.auth.models import User
from .models import ProfilePicture


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    profile_picture = forms.ImageField(label='Profile Picture', required=False)

    def save(self, commit=True):
        user = super().save(commit=False)

        if 'profile_picture' in self.cleaned_data:
            profile_picture = self.cleaned_data['profile_picture']

            if profile_picture:
                profile_pic, created = ProfilePicture.objects.get_or_create(user=user)
                profile_pic.profile_picture = profile_picture
                profile_pic.save()

        if commit:
            user.save()
        return user
