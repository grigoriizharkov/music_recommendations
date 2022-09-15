from django import forms


class UserForm(forms.Form):
    url = forms.CharField(help_text="Ссылка вида https://music.yandex.ru/users/*username*/playlists/*playlist number*")
    number = forms.IntegerField(required=False, min_value=1, max_value=20, help_text="Число песен от 1 до 20")