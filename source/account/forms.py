from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,  Post


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", required=True)

    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = ( 'username', 'email', 'first_name', 'phone_number', 'gender',
            'bio', 'avatar' )


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields =['image','description']
       widgets = {
            'image':forms.FileInput(attrs={'class':'form-control','id':'image'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
       }


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="")