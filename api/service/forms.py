from django import forms
from service.models import ServiceModels


class PostFormService(forms.ModelForm):
    class Meta:
        model = ServiceModels
        fields = "__all__"
