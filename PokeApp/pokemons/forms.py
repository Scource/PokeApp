from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username, email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(label=_("Email"),
                             widget=forms.EmailInput)
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
