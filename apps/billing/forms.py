from django import forms


def _digits_only(value: str) -> str:
    return ''.join(c for c in value if c.isdigit())


class CheckoutForm(forms.Form):
    cpf_cnpj = forms.CharField(
        label='CPF ou CNPJ',
        max_length=18,
        widget=forms.TextInput(attrs={
            'placeholder': '000.000.000-00 ou 00.000.000/0001-00',
            'class': 'w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500',
        }),
        help_text='Será utilizado apenas para emissão da cobrança.',
    )
    billing_cycle = forms.ChoiceField(
        label='Ciclo de cobrança',
        choices=[
            ('monthly', 'Mensal'),
            ('annual', 'Anual — 2 meses grátis'),
        ],
        widget=forms.RadioSelect(),
    )
    def clean_cpf_cnpj(self):
        value = self.cleaned_data['cpf_cnpj']
        digits = _digits_only(value)
        if len(digits) not in (11, 14):
            raise forms.ValidationError('Informe um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.')
        return digits
