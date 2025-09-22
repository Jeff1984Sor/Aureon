from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Caso, RegraWorkflow, Tarefa, Andamento, FaseWorkflow

# Importa a nossa nova função de notificação do app 'notificacoes'
from notificacoes.utils import disparar_notificacao_workflow

# ==============================================================================
# ROBÔ 1: Acionado APENAS na CRIAÇÃO de um Caso
# Objetivo: Aplicar o workflow inicial e criar as tarefas da primeira fase.
# ==============================================================================
@receiver(post_save, sender=Caso)
def aplicar_workflow_no_caso(sender, instance, created, **kwargs):
    """ Este signal aplica o workflow inicial. """
    
    # Se for uma edição (update), NÃO FAZ NADA.
    if not created:
        return

    try:
        regra = RegraWorkflow.objects.get(cliente=instance.cliente, produto=instance.produto)
        workflow = regra.workflow
        primeira_fase = workflow.fases.order_by('ordem').first()
        if primeira_fase:
            instance.fase_atual_workflow = primeira_fase
            instance.save(update_fields=['fase_atual_workflow'])
            for tarefa_padrao in primeira_fase.tarefas_padrao.all():
                Tarefa.objects.create(
                    caso=instance, tipo_tarefa=tarefa_padrao.tipo_tarefa, status='P',
                    responsavel=tarefa_padrao.responsavel_override, origem_fase_workflow=primeira_fase
                )
    except RegraWorkflow.DoesNotExist:
        print(f"WORKFLOW: Nenhuma regra encontrada para o caso #{instance.id}.")

# ==============================================================================
# ROBÔ 2: Acionado QUANDO UMA TAREFA É SALVA
# Objetivo: Verificar se a fase terminou, avançar e DISPARAR NOTIFICAÇÃO.
# ==============================================================================
@receiver(post_save, sender=Tarefa)
def avancar_workflow_ao_concluir_tarefas(sender, instance, **kwargs):
    """
    Este signal avança o workflow e chama o sistema de notificação.
    """
    tarefa_concluida = instance
    
    if tarefa_concluida.status != 'C' or not tarefa_concluida.origem_fase_workflow:
        return

    caso = tarefa_concluida.caso
    fase_concluida = tarefa_concluida.origem_fase_workflow
    
    tarefas_pendentes = Tarefa.objects.filter(
        caso=caso,
        origem_fase_workflow=fase_concluida
    ).exclude(status='C').exists()

    if tarefas_pendentes:
        return
    
    workflow = fase_concluida.workflow
    proxima_fase = workflow.fases.filter(ordem__gt=fase_concluida.ordem).order_by('ordem').first()
    
    if proxima_fase:
        # Guarda a fase antiga antes de mudar
        fase_origem_para_notificacao = caso.fase_atual_workflow

        # Avança o caso
        caso.fase_atual_workflow = proxima_fase
        if proxima_fase.atualiza_status_para:
            caso.status = proxima_fase.atualiza_status_para
        caso.save()

        # Cria as novas tarefas
        for tarefa_padrao in proxima_fase.tarefas_padrao.all():
            Tarefa.objects.create(
                caso=caso, tipo_tarefa=tarefa_padrao.tipo_tarefa, status='P',
                responsavel=tarefa_padrao.responsavel_override, origem_fase_workflow=proxima_fase
            )
        
        # Cria Andamento
        Andamento.objects.create(
            caso=caso, data_andamento=timezone.now().date(),
            descricao=f"Workflow avançou para a fase: '{proxima_fase.nome}'.",
            usuario_criacao=None
        )

        # --- DISPARA A NOTIFICAÇÃO POR E-MAIL ---
        disparar_notificacao_workflow(
            caso=caso,
            fase_origem=fase_origem_para_notificacao,
            fase_destino=proxima_fase
        )

    else:
        # O workflow terminou
        Andamento.objects.create(
            caso=caso,
            data_andamento=timezone.now().date(),
            descricao="Fluxo de trabalho concluído.",
            usuario_criacao=None
        )