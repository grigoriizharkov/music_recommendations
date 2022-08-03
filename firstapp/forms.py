from django import forms


class LinkForm(forms.Form):
    url = forms.CharField()
