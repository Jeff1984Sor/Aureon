from django.contrib import admin
import nested_admin
from .models import (
    Advogado, Status, Cobertura, Motivo, Analista, Produto, TipoTarefa,
    Workflow, FaseWorkflow, TarefaPadraoWorkflow, RegraWorkflow,
    Caso, Tarefa
)

@admin.register(Advogado)
class AdvogadoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin): list_display = ('nome',)
@admin.register(Cobertura)
class CoberturaAdmin(admin.ModelAdmin): list_display = ('nome',)
@admin.register(Motivo)
class MotivoAdmin(admin.ModelAdmin): list_display = ('nome',)
@admin.register(Analista)
class AnalistaAdmin(admin.ModelAdmin): list_display = ('nome',)
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin): list_display = ('nome',)

@admin.register(TipoTarefa)
class TipoTarefaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'prazo_dias', 'tipo_prazo')

class TarefaPadraoWorkflowInline(nested_admin.NestedTabularInline):
    model = TarefaPadraoWorkflow
    extra = 1

class FaseWorkflowInline(nested_admin.NestedTabularInline):
    model = FaseWorkflow
    extra = 1
    inlines = [TarefaPadraoWorkflowInline]

@admin.register(Workflow)
class WorkflowAdmin(nested_admin.NestedModelAdmin):
    list_display = ('nome',)
    inlines = [FaseWorkflowInline]

@admin.register(RegraWorkflow)
class RegraWorkflowAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'produto', 'workflow')

class TarefaInline(admin.TabularInline):
    model = Tarefa
    extra = 0

@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo_caso', 'cliente', 'status')
    inlines = [TarefaInline]