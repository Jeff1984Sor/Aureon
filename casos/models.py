from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from django.conf import settings
from django.db.models import Sum
from datetime import date, timedelta

# --- Modelos de Apoio (Tabelas de Opções) ---
class Advogado(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Status(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nome

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

# --- Modelo Principal: Caso ---
class Caso(models.Model):
    # ... (todos os seus campos de Caso, exatamente como estavam)
    numero_aviso = models.CharField(max_length=50, blank=True, null=True)
    numero_sinistro = models.CharField(max_length=50, blank=True, null=True)
    numero_apolice = models.CharField(max_length=50, blank=True, null=True)
    titulo_caso = models.CharField(max_length=200, verbose_name="Título do Caso")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='casos')
    advogado_responsavel = models.ForeignKey(Advogado, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Advogado Responsável")
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    cobertura = models.ForeignKey(Cobertura, on_delete=models.PROTECT, blank=True, null=True)
    motivo = models.ForeignKey(Motivo, on_delete=models.PROTECT, blank=True, null=True)
    analista = models.ForeignKey(Analista, on_delete=models.SET_NULL, blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, blank=True, null=True)
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
        return f"Caso {self.id} - {self.titulo_caso} ({self.cliente.nome_razao_social})"

    class Meta:
        ordering = ['-data_entrada']
    @property
    def total_horas_trabalhadas(self):
        """Soma a duração de todos os timesheets associados a este caso."""
        # .aggregate(total=Sum('tempo')) faz a soma de todos os 'tempo' dos timesheets
        # O resultado é um dicionário, como {'total': DurationObject}
        resultado = self.timesheets.aggregate(total=Sum('tempo'))
        total_duration = resultado.get('total')

        if total_duration:
            # Converte a duração total em horas e minutos
            total_seconds = int(total_duration.total_seconds())
            horas = total_seconds // 3600
            minutos = (total_seconds % 3600) // 60
            return f"{horas:02d}:{minutos:02d}" # Formata como HH:MM
        
        return "00:00" # Retorna 00:00 se não houver lançamentos

# --- Modelo de Andamento (AGORA FORA DA CLASSE CASO) ---
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

class TipoTarefa(models.Model):
    TIPO_PRAZO_CHOICES = (
        ('U', 'Dias Úteis'),
        ('C', 'Dias Corridos'),
    )
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Tipo de Tarefa")
    prazo_dias = models.IntegerField(verbose_name="Prazo Padrão (em dias)")
    tipo_prazo = models.CharField(max_length=1, choices=TIPO_PRAZO_CHOICES, default='U', verbose_name="Tipo de Prazo")
    recorrente = models.BooleanField(default=False, verbose_name="É uma tarefa recorrente?")

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    STATUS_TAREFA_CHOICES = (
        ('P', 'Pendente'),
        ('A', 'Em Andamento'),
        ('C', 'Concluída'),
    )
    
    # Relacionamentos
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='tarefas')
    tipo_tarefa = models.ForeignKey(TipoTarefa, on_delete=models.PROTECT, verbose_name="Tipo de Tarefa")
    
    # Controle da Tarefa
    status = models.CharField(max_length=1, choices=STATUS_TAREFA_CHOICES, default='P')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(blank=True, null=True, verbose_name="Data de Conclusão Real")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo_tarefa.nome} - Caso #{self.caso.id}"

    # Propriedade para calcular a data de conclusão prevista
    @property
    def data_conclusao_prevista(self):
        if self.tipo_tarefa.tipo_prazo == 'C': # Dias Corridos
            return self.data_criacao.date() + timedelta(days=self.tipo_tarefa.prazo_dias)
        else: # Dias Úteis
            dias_uteis_adicionados = 0
            data_atual = self.data_criacao.date()
            while dias_uteis_adicionados < self.tipo_tarefa.prazo_dias:
                data_atual += timedelta(days=1)
                if data_atual.weekday() < 5: # weekday() é 0-4 para Seg-Sex
                    dias_uteis_adicionados += 1
            return data_atual
    
    class Meta:
        ordering = ['data_criacao']

class Timesheet(models.Model):
    # Relacionamento: Cada lançamento pertence a UM caso.
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, related_name='timesheets')
    
    data_execucao = models.DateField(verbose_name="Data de Execução")
    
    # Relacionamento com o usuário que executou o trabalho
    profissional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Profissional")
    
    # Para armazenar HH:MM, usamos um campo de Duração. É o tipo ideal para isso.
    tempo = models.DurationField(verbose_name="Tempo Gasto (HH:MM)")
    
    descricao = models.TextField(verbose_name="Descrição da Atividade")
    
    # Metadados
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lançamento de {self.profissional.username} em {self.data_execucao.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-data_execucao']