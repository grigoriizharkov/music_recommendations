from django import forms


class UserForm(forms.Form):
    url = forms.CharField(label="Ссылка", help_text="")
    number = forms.IntegerField(label="Число песен", min_value=1, max_value=20, help_text="(от 1 до 20)")
