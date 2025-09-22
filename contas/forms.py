# contas/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # Usa o User padrão do Django

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User # Aponta para o User padrão
        # Adiciona os campos de email e nome ao formulário de cadastro
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona a classe do Bootstrap a todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})