from django.contrib.auth import authenticate, get_user_model
from timeclock.auth import PinAuth
from django import forms


class MyLoginForm(forms.Form):
    pin = forms.IntegerField(label=('pin'), widget=forms.PasswordInput())

    error_messages = {
            'invalid_login': ("Unknown pin: "),
            'inactive': ("Inactive user"),
            }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)


    def clean(self):
        pin = self.cleaned_data.get('pin')
        if pin:
            self.user_cache = authenticate( self.request, pin=pin,)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                    )


    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )


