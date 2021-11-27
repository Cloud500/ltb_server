from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Benutzername")
    password = forms.CharField(label="Passwort", widget=forms.PasswordInput)
