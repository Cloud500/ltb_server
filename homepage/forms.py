from django import forms


class LoginForm(forms.Form):
    """
    TODO: Docstring
    """
    username = forms.CharField(label="Benutzername")
    password = forms.CharField(label="Passwort", widget=forms.PasswordInput)
