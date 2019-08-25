from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [
            'user',
            'image',
            'content',
        ]

    def clean_content(self):
        if len(self.cleaned_data['content']) < 10:
            raise forms.ValidationError('content is too small')
