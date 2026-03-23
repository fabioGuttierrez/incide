from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        help_text='Usado para notificações de pagamento e recuperação de conta.',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(
        label='Nome',
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome'}),
    )
    last_name = forms.CharField(
        label='Sobrenome',
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Seu sobrenome'}),
    )
    email = forms.EmailField(
        label='E-mail',
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
    )
    phone = forms.CharField(
        label='Telefone',
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '(11) 99999-9999'}),
    )

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_user = current_user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self._current_user:
            qs = User.objects.filter(email=email).exclude(pk=self._current_user.pk)
            if qs.exists():
                raise forms.ValidationError('Este e-mail já está cadastrado por outro usuário.')
        return email
