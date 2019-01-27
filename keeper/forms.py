from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100, required=True)
    password = forms.CharField(label='Password:', max_length=100, required=True)
    password2 = forms.CharField(label='Password again:', max_length=100, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=100, required=True)
    password = forms.CharField(label='Password:', max_length=100, required=True)


class TakeKeyForm(forms.Form):
    user = forms.CharField(label='Username:', max_length=100, required=True)
    key_num = forms.IntegerField(label='Room number:', max_value=1000, required=True)
