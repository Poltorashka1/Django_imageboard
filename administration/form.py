from django import forms


class Search(forms.Form):
    search = forms.CharField(max_length=50, label='Поиск')
