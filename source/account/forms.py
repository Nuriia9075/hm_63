from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", required=True)

    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = ( 'username', 'email', 'first_name', 'phone_number', 'gender',
            'bio', 'avatar' )
