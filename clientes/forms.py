from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        
        # Excluímos 'empresa' e 'data_criacao' que são automáticos
        exclude = ['data_criacao']
        
        # Widgets com as classes do Bootstrap, sem os IDs extras para o CEP
        widgets = {
            'tipo_pessoa': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_pessoa'}),
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nome_contato': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nome_contato'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}), # ID removido
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}), # ID removido
            'numero_endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}), # ID removido
            'cidade': forms.TextInput(attrs={'class': 'form-control'}), # ID removido
            'uf': forms.TextInput(attrs={'class': 'form-control'}), # ID removido
        }

        labels = {
            'nome_razao_social': 'Nome / Razão Social',
            'numero_endereco': 'Número',
            'tipo_pessoa': 'Tipo de Pessoa',
            'nome_contato': 'Nome do Contato (para PJ)',
        }