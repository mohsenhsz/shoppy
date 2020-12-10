from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('email', 'full_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserRegisterationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Confirm', max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError("Your passwords didn't match")
