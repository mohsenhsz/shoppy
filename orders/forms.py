from django import forms


class CopounForm(forms.Form):
    code = forms.CharField(label='code')
