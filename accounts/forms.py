from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist.')

            # if not user.check_password(password):
            #    raise forms.ValidationError('Password is incorrect.')

            if not user.is_active:
                raise forms.ValidationError('This user is no longer active.')

            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username:
            user = User.objects.filter(username=username)

            if user.exists():
                raise forms.ValidationError('The username is already exists.')

        if email:
            user = User.objects.filter(email=email)

            if user.exists():
                raise forms.ValidationError('The email is already exists.')

        return super(UserRegisterForm, self).clean(*args, **kwargs)


    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email'
        ]
