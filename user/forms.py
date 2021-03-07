from django import forms
from .models import Profile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=16, label="Kullanıcı Adı",
                               help_text="Bu girdiğiniz kullanıcı adı benzersiz olmalıdır. Ve kullanıcıya özeldir."
                               )
    password = forms.CharField(min_length=8, max_length=20, label="Şifre", widget=forms.PasswordInput,
                               help_text="Lütfen güvenli bir şifre seçin! Kullanıcı adı ile benzer olmamasına dikkat edin(tahmin edilebilmesi kolaylaşıyor)."
                               )
    confirm = forms.CharField(min_length=8, max_length=20,
                              label="Şifrenizi onaylayın", widget=forms.PasswordInput)

    def clean(self):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Şifreler uyuşmuyor!")

        values = {
            "username": username,
            "password": password
        }

        return values


class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        # birth_date = forms.DateField(input_formats = settings.DATE_INPUT_FORMATS)
        fields = (
            'image',
            'bio',
            'location',
            'birth_date',
        )
