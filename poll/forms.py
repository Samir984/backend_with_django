from django import forms
from .models import Poll
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question','option_1','option_2','option_3','option_4']




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']