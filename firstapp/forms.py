from django import forms


class UserForm(forms.Form):
    url = forms.CharField()
    number = forms.IntegerField(required=False, min_value=1, max_value=20)