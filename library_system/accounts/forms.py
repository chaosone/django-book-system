from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReaderRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=50)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
