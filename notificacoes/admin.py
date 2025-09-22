from django.contrib import admin
from django import forms
from .models import ConfiguracaoEmail, TemplateEmail, RegraNotificacao

@admin.register(ConfiguracaoEmail)
class ConfiguracaoEmailAdmin(admin.ModelAdmin):
    list_display = ('apelido', 'email_host_user', 'ativo')

# --- 1. CRIAMOS UM FORMULÁRIO CUSTOMIZADO ---
class TemplateEmailAdminForm(forms.ModelForm):
    class Meta:
        model = TemplateEmail
        fields = '__all__'
        widgets = {
            # Aumenta a altura do campo 'corpo' para facilitar a edição
            'corpo': forms.Textarea(attrs={'rows': 20}),
        }

# --- 2. USAMOS O FORMULÁRIO NO NOSSO ADMIN ---
@admin.register(TemplateEmail)
class TemplateEmailAdmin(admin.ModelAdmin):
    form = TemplateEmailAdminForm # <-- Diz ao admin para usar nosso form customizado
    list_display = ('apelido', 'assunto', 'tipo_conteudo')

    # --- 3. A MÁGICA: Adicionamos a lista de variáveis ---
    fieldsets = (
        (None, {
            'fields': ('apelido', 'assunto', 'tipo_conteudo', 'corpo')
        }),
        ('Variáveis Disponíveis para o Template', {
            'fields': (), # Nenhum campo aqui
            'description': """
                <p>Você pode usar as seguintes variáveis no Assunto e no Corpo do E-mail. Elas serão substituídas pelos dados reais do caso.</p>
                <ul>
                    <li><code>{{ caso.id }}</code> - ID do Caso</li>
                    <li><code>{{ caso.titulo_caso }}</code> - Título do Caso</li>
                    <li><code>{{ caso.data_entrada }}</code> - Data de Entrada do Caso</li>
                    <li><code>{{ cliente.nome_razao_social }}</code> - Nome ou Razão Social do Cliente</li>
                    <li><code>{{ cliente.email }}</code> - Email do Cliente</li>
                    <li><code>{{ fase_origem.nome }}</code> - Nome da fase que foi concluída</li>
                    <li><code>{{ fase_destino.nome }}</code> - Nome da nova fase para a qual o caso avançou</li>
                </ul>
            """
        }),
    )

@admin.register(RegraNotificacao)
class RegraNotificacaoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'workflow')
    list_filter = ('workflow',)