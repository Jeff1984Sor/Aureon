from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_pessoa', 'nome_razao_social', 'email', 'nome_contato',
            'cep', 'logradouro', 'numero_endereco', 'complemento',
            'bairro', 'cidade', 'uf'
        ]
        
        # É aqui que a mágica acontece. Adicionamos classes e IDs do Bootstrap.
        widgets = {
            'tipo_pessoa': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_pessoa'}),
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nome_contato': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nome_contato'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cep'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_logradouro'}),
            'numero_endereco': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_numero_endereco'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cidade'}),
            'uf': forms.Select(attrs={'class': 'form-select', 'id': 'id_uf'}), # Corrigido para Select, já que UF é um campo de escolha
        }

        # Opcional: Adicionar labels mais amigáveis
        labels = {
            'nome_razao_social': 'Nome / Razão Social',
            'numero_endereco': 'Número',
            'tipo_pessoa': 'Tipo de Pessoa',
            'nome_contato': 'Nome do Contato (para PJ)',
        }