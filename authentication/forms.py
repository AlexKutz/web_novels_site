from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'Пользователь с таким именем уже зарегистрирован.')
        if email:
            if User.objects.filter(email__iexact=email).exists():
                self.add_error('email', 'Пользователь с такой почтой уже зарегистрирован.')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class EmailChangeForm(forms.Form):
    """A form that allow a user change or set their email"""
    error_messages = {
        'already_in_use': "Этот адрес электронной почты уже используется",
        'not_changed': "Адрес электронной почты совпадает с уже заданным.",
        'empty': "Пожалуйста, заполните обязательное поле",
    }

    new_email = forms.EmailField(
        label="Новый адрес электронной почты"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email(self):
        data = self.cleaned_data
        if not data.get('new_email'):
            raise forms.ValidationError(
                self.error_messages['empty'],
                code='required'
            )
        old_email = self.user.email
        new_email = self.cleaned_data.get('new_email')
        if new_email and not old_email:
            return new_email
        if new_email and old_email:
            if new_email == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='used'
                )
            return new_email

    def save(self, commit=True):
        email = self.cleaned_data["new_email"]
        self.user.is_active_email = False
        self.user.email = email
        if commit:
            self.user.save()
        return self.user
