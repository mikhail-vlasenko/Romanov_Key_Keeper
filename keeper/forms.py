from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя:', max_length=100, required=True)
    first_name = forms.CharField(label='Имя:', max_length=100, required=True)
    last_name = forms.CharField(label='Фамилия:', max_length=100, required=True)
    password = forms.CharField(label='Пароль:', max_length=100, required=True)
    password2 = forms.CharField(label='Пароль снова:', max_length=100, required=True)
    card_id = forms.IntegerField(label='Номер карты:', required=True)
    reg_code = forms.CharField(label='Код для регистрации:', max_length=100, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя:', max_length=100, required=True)
    password = forms.CharField(label='Пароль:', max_length=100, required=True)


class CardForm(forms.Form):
    card = forms.IntegerField(label='Номер карты:', required=True)
    key_num = forms.IntegerField(label='Номер кабинета:', max_value=1000, required=True)


class TransferForm(forms.Form):
    username = forms.CharField(label='Имя пользователя, которому передать:', max_length=100, required=True)
    key_num = forms.IntegerField(label='Номер кабинета:', max_value=1000, required=True)
