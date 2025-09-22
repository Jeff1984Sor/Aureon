from django import forms
from .models import Caso, Andamento, Tarefa, Timesheet

# ==============================================================================
# FORMULÁRIO PARA CRIAR UM CASO
# ==============================================================================

class CasoCreateForm(forms.ModelForm):
    """Este formulário é usado APENAS na tela de criação de um novo caso."""
    class Meta:
        model = Caso
        # Excluímos os campos que são automáticos, definidos pelo workflow, ou pela empresa do usuário.
        exclude = ['data_cadastro', 'fase_atual_workflow']
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'advogado_responsavel': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'cobertura': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'analista': forms.Select(attrs={'class': 'form-select'}),
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'numero_aviso': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_sinistro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_apolice': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_caso': forms.TextInput(attrs={'class': 'form-control'}),
            'segurado': forms.TextInput(attrs={'class': 'form-control'}),
            'terceiro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_caso_lo': forms.TextInput(attrs={'class': 'form-control'}),
            'data_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_relatorio_preliminar': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_relatorio_final': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'previsao_conclusao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valor_causa': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_prejuizo_apurado': forms.NumberInput(attrs={'class': 'form-control'}),
            'prazo_regulacao_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas_trabalhadas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'resumo_caso': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ==============================================================================
# FORMULÁRIO PARA EDITAR UM CASO
# ==============================================================================

class CasoUpdateForm(forms.ModelForm):
    """Este formulário é usado APENAS na tela de edição de um caso existente."""
    class Meta:
        model = Caso
        # Excluímos 'empresa', pois não deve ser alterada, e o campo automático.
        exclude = ['data_cadastro']
        
        widgets = {
            'fase_atual_workflow': forms.Select(attrs={'class': 'form-select', 'disabled': True}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'advogado_responsavel': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'cobertura': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'analista': forms.Select(attrs={'class': 'form-select'}),
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'numero_aviso': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_sinistro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_apolice': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo_caso': forms.TextInput(attrs={'class': 'form-control'}),
            'segurado': forms.TextInput(attrs={'class': 'form-control'}),
            'terceiro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_caso_lo': forms.TextInput(attrs={'class': 'form-control'}),
            'data_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_relatorio_preliminar': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_relatorio_final': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'previsao_conclusao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valor_causa': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_prejuizo_apurado': forms.NumberInput(attrs={'class': 'form-control'}),
            'prazo_regulacao_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'horas_trabalhadas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'resumo_caso': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        help_texts = {
            'fase_atual_workflow': 'A fase do workflow é controlada automaticamente.'
        }

# ==============================================================================
# OUTROS FORMULÁRIOS (NÃO PRECISAM DE MUDANÇA)
# ==============================================================================

class AndamentoForm(forms.ModelForm):
    class Meta:
        model = Andamento
        fields = ['data_andamento', 'descricao']
        widgets = {
            'data_andamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['tipo_tarefa', 'responsavel', 'observacao']
        widgets = {
            'tipo_tarefa': forms.Select(attrs={'class': 'form-select'}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TimesheetForm(forms.ModelForm):
    tempo_str = forms.CharField(
        label="Tempo Gasto (HH:MM)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 02:30'}),
        help_text="Informe o tempo no formato horas e minutos."
    )
    class Meta:
        model = Timesheet
        fields = ['data_execucao', 'profissional', 'tempo_str', 'descricao']
        widgets = {
            'data_execucao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'profissional': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TarefaConclusaoForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['descricao_conclusao']
        widgets = {
            'descricao_conclusao': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'required': True}
            ),
        }
        labels = {
            'descricao_conclusao': "Descreva o que foi feito para concluir esta tarefa"
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao_conclusao'].required = True