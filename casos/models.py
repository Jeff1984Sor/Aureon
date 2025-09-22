from django.db import models
from django.conf import settings
from django.db.models import Sum
from datetime import timedelta
from clientes.models import Cliente

# ==============================================================================
# MODELOS DE APOIO (ESTRUTURA SIMPLIFICADA)
# ==============================================================================

class Advogado(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário do Sistema")
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Status(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = "Status"

class Cobertura(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome

class Motivo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome

class Analista(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome
    
class TipoTarefa(models.Model):
    TIPO_PRAZO_CHOICES = (('U', 'Dias Úteis'), ('C', 'Dias Corridos'))
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Tipo de Tarefa")
    prazo_dias = models.IntegerField(verbose_name="Prazo Padrão (em dias)")
    tipo_prazo = models.CharField(max_length=1, choices=TIPO_PRAZO_CHOICES, default='U', verbose_name="Tipo de Prazo")
    recorrente = models.BooleanField(default=False, verbose_name="É uma tarefa recorrente?")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Tipo de Tarefa"
        verbose_name_plural = "Tipos de Tarefa"

# ==============================================================================
# MODELOS DE WORKFLOW
# ==============================================================================

class Workflow(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return self.nome

class FaseWorkflow(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='fases')
    nome = models.CharField(max_length=100)
    ordem = models.PositiveIntegerField()
    atualiza_status_para = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.workflow.nome} - {self.ordem}: {self.nome}"
    class Meta:
        ordering = ['workflow', 'ordem']
        unique_together = ('workflow', 'ordem')

class TarefaPadraoWorkflow(models.Model):
    fase = models.ForeignKey(FaseWorkflow, on_delete=models.CASCADE, related_name='tarefas_padrao')
    tipo_tarefa = models.ForeignKey(TipoTarefa, on_delete=models.PROTECT)
    responsavel_override = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.tipo_tarefa.nome

class RegraWorkflow(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    def __str__(self):
        return f"Regra: {self.cliente} + {self.produto}"
    class Meta:
        unique_together = ('cliente', 'produto')
        verbose_name = "Regra de Workflow"
        verbose_name_plural = "Regras de Workflow"

# ==============================================================================
# MODELO PRINCIPAL E RELACIONADOS
# ==============================================================================

class Caso(models.Model):
    numero_aviso = models.CharField(max_length=50, blank=True, null=True)
    numero_sinistro = models.CharField(max_length=50, blank=True, null=True)
    numero_apolice = models.CharField(max_length=50, blank=True, null=True)
    titulo_caso = models.CharField(max_length=200, verbose_name="Título do Caso")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='casos_do_cliente')
    advogado_responsavel = models.ForeignKey(Advogado, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Advogado Responsável")
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    fase_atual_workflow = models.ForeignKey(FaseWorkflow, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fase Atual do Workflow")
    cobertura = models.ForeignKey(Cobertura, on_delete=models.PROTECT, blank=True, null=True)
    motivo = models.ForeignKey(Motivo, on_delete=models.PROTECT, blank=True, null=True)
    analista = models.ForeignKey(Analista, on_delete=models.SET_NULL, blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    segurado = models.CharField(max_length=150, blank=True)
    terceiro = models.CharField(max_length=150, blank=True)
    data_entrada = models.DateField(verbose_name="Data de Entrada")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_relatorio_preliminar = models.DateField(blank=True, null=True, verbose_name="Data Relatório Preliminar")
    data_relatorio_final = models.DateField(blank=True, null=True, verbose_name="Data Relatório Final")
    previsao_conclusao = models.DateField(blank=True, null=True, verbose_name="Previsão de Conclusão")
    valor_causa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Valor da Causa")
    valor_prejuizo_apurado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Valor Prejuízo Apurado")
    prazo_regulacao_dias = models.IntegerField(blank=True, null=True, verbose_name="Prazo Regulação (Dias)")
    horas_trabalhadas = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Horas Trabalhadas")
    numero_caso_lo = models.CharField(max_length=50, blank=True, verbose_name="Número Caso LO")
    resumo_caso = models.TextField(blank=True, verbose_name="Resumo do Caso")
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"Caso #{self.id} - {self.titulo_caso}"
    
    @property
    def total_horas_trabalhadas(self):
        resultado = self.timesheets.aggregate(total=Sum('tempo'))
        total_duration = resultado.get('total')
        if total_duration:
            total_seconds = int(total_duration.total_seconds())
            horas = total_seconds // 3600
            minutos = (total_seconds % 3600) // 60
            return f"{horas:02d}:{minutos:02d}"
        return "00:00"
    class Meta:
        ordering = ['-data_entrada']

class Andamento(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='andamentos')
    data_andamento = models.DateField(verbose_name="Data do Andamento")
    descricao = models.TextField(verbose_name="Descrição")
    usuario_criacao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Andamento em {self.data_andamento.strftime('%d/%m/%Y')} para o Caso #{self.caso.id}"
    class Meta:
        ordering = ['-data_andamento', '-data_cadastro']

class Tarefa(models.Model):
    STATUS_TAREFA_CHOICES = (('P', 'Pendente'), ('A', 'Em Andamento'), ('C', 'Concluída'))
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='tarefas')
    tipo_tarefa = models.ForeignKey(TipoTarefa, on_delete=models.PROTECT, verbose_name="Tipo de Tarefa")
    status = models.CharField(max_length=1, choices=STATUS_TAREFA_CHOICES, default='P')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(blank=True, null=True, verbose_name="Data de Conclusão Real")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(blank=True)
    descricao_conclusao = models.TextField(blank=True, verbose_name="Descrição da Conclusão")
    origem_fase_workflow = models.ForeignKey(FaseWorkflow, on_delete=models.SET_NULL, null=True, blank=True, help_text="Fase do workflow que gerou esta tarefa.")
    def __str__(self):
        return f"{self.tipo_tarefa.nome} - Caso #{self.caso.id}"
    @property
    def data_conclusao_prevista(self):
        if self.tipo_tarefa.tipo_prazo == 'C':
            return self.data_criacao.date() + timedelta(days=self.tipo_tarefa.prazo_dias)
        else:
            dias_uteis_adicionados = 0
            data_atual = self.data_criacao.date()
            while dias_uteis_adicionados < self.tipo_tarefa.prazo_dias:
                data_atual += timedelta(days=1)
                if data_atual.weekday() < 5:
                    dias_uteis_adicionados += 1
            return data_atual
    class Meta:
        ordering = ['data_criacao']

class Timesheet(models.Model):
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='timesheets')
    data_execucao = models.DateField(verbose_name="Data de Execução")
    profissional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Profissional")
    tempo = models.DurationField(verbose_name="Tempo Gasto (HH:MM)")
    descricao = models.TextField(verbose_name="Descrição da Atividade")
    data_cadastro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Lançamento de {self.profissional.username} em {self.data_execucao.strftime('%d/%m/%Y')}"
    class Meta:
        ordering = ['-data_execucao']