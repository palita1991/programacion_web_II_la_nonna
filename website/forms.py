import re
from django import forms
from .models import SolicitudContacto
from django.contrib.auth.password_validation import validate_password

class ContactoForm(forms.ModelForm):
    class Meta:
        model = SolicitudContacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre y apellido',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@gmail.com',
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribí tu consulta...',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'-]+$", nombre):
            raise forms.ValidationError('El nombre no puede contener números ni caracteres especiales.')
        return nombre


class SolicitudPanelForm(ContactoForm):
    class Meta(ContactoForm.Meta):
        fields = ['nombre', 'email', 'mensaje', 'leida']
        widgets = {
            **ContactoForm.Meta.widgets,
            'leida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# =========================================
# AUTENTICACIÓN
# =========================================

class RegistroForm(forms.Form):
    nombre_apellido = forms.CharField(
        label='Nombre y apellido',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Matias Perez',
        }),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
        }),
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres',
        }),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repetí tu contraseña',
        }),
    )

    def clean_nombre_apellido(self):
        nombre = self.cleaned_data.get('nombre_apellido', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre y apellido debe tener al menos 3 caracteres.')
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'-]+$", nombre):
            raise forms.ValidationError('El nombre y apellido no puede contener números ni caracteres especiales.')
        return nombre

    def clean_email(self):
        return self.cleaned_data.get('email', '').strip().lower()

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            validate_password(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')

        return cleaned_data


class ValidarCuentaForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
        }),
    )
    codigo = forms.CharField(
        label='Código de validación',
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresá el código de 6 dígitos',
            'autocomplete': 'one-time-code',
        }),
    )

    def clean_email(self):
        return self.cleaned_data.get('email', '').strip().lower()

    def clean_codigo(self):
        return self.cleaned_data.get('codigo', '').strip()


class LoginEmailForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@correo.com',
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña',
        }),
    )

    def clean_email(self):
        return self.cleaned_data.get('email', '').strip().lower()