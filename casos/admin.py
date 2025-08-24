from django.contrib import admin
from .models import (
    Advogado, Status, Cobertura, Motivo, Analista, Produto, Caso, TipoTarefa, Tarefa
)

@admin.register(Advogado)
class AdvogadoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Cobertura)
class CoberturaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Motivo)
class MotivoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Analista)
class AnalistaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(TipoTarefa)
class TipoTarefaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'prazo_dias', 'tipo_prazo', 'recorrente')
    list_filter = ('tipo_prazo', 'recorrente')

class TarefaInline(admin.TabularInline):
    model = Tarefa
    extra = 0
    fields = ('tipo_tarefa', 'status', 'responsavel', 'data_conclusao')

# --- VERSÃO UNIFICADA E CORRETA DO CASO ADMIN ---
@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    # Adicionamos o list_display que estava no primeiro bloco
    list_display = (
        'id', 'titulo_caso', 'cliente', 'status', 
        'advogado_responsavel', 'data_entrada'
    )
    
    # E mantivemos todas as outras configurações
    inlines = [TarefaInline]
    
    list_filter = (
        'status', 'advogado_responsavel', 'analista', 'data_entrada'
    )
    
    search_fields = (
        'titulo_caso', 'numero_sinistro', 'cliente__nome_razao_social'
    )
    
    fieldsets = (
        ('Informações Principais', {'fields': ('titulo_caso', 'cliente', 'status', 'numero_sinistro', 'numero_apolice', 'numero_aviso')}),
        ('Partes Envolvidas & Cobertura', {'fields': ('segurado', 'terceiro', 'cobertura', 'motivo', 'produto')}),
        ('Responsáveis e Prazos', {'fields': ('advogado_responsavel', 'analista', 'data_entrada', 'previsao_conclusao', 'prazo_regulacao_dias')}),
        ('Valores', {'fields': ('valor_causa', 'valor_prejuizo_apurado', 'horas_trabalhadas')}),
        ('Datas de Relatórios', {'fields': ('data_relatorio_preliminar', 'data_relatorio_final')}),
        ('Detalhes Adicionais', {'fields': ('numero_caso_lo', 'resumo_caso', 'observacao')}),
    )