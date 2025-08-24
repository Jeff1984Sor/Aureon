from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font, Alignment


from .models import Caso, Status, Cobertura, Motivo,Timesheet, Cliente, Advogado, Status, Analista
from .forms import CasoForm, AndamentoForm,Tarefa,TarefaForm,TimesheetForm


class CasoListView(LoginRequiredMixin, ListView):
    model = Caso
    template_name = 'casos/caso_list.html'
    context_object_name = 'casos'
    paginate_by = 10

class CasoUpdateView(LoginRequiredMixin, UpdateView):
    model = Caso
    form_class = CasoForm
    template_name = 'casos/caso_form.html' # Reutiliza o mesmo template
    success_url = reverse_lazy('caso_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Caso'
        return context
    
class CasoCreateView(LoginRequiredMixin, CreateView):
    model = Caso
    form_class = CasoForm
    template_name = 'casos/caso_form.html'
    success_url = reverse_lazy('caso_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Adicionar Novo Caso'
        return context

class CasoDetailView(LoginRequiredMixin, DetailView):
    model = Caso
    template_name = 'casos/caso_detail.html'
    context_object_name = 'caso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['andamento_form'] = AndamentoForm()
        context['tarefa_form'] = TarefaForm()
        context['timesheet_form'] = TimesheetForm()
        return context

# --- VIEWS AJAX ---

@login_required
def add_status_ajax(request):
    if request.method == 'POST':
        nome_status = request.POST.get('nome')
        if nome_status:
            status, created = Status.objects.get_or_create(nome=nome_status)
            return JsonResponse({'id': status.id, 'nome': status.nome})
    return JsonResponse({'error': 'Requisição inválida'}, status=400)

@login_required
def add_cobertura_ajax(request):
    if request.method == 'POST':
        nome_cobertura = request.POST.get('nome')
        if nome_cobertura:
            cobertura, created = Cobertura.objects.get_or_create(nome=nome_cobertura)
            return JsonResponse({'id': cobertura.id, 'nome': cobertura.nome})
    return JsonResponse({'error': 'Requisição inválida'}, status=400)

@login_required
def add_motivo_ajax(request):
    if request.method == 'POST':
        nome_motivo = request.POST.get('nome')
        if nome_motivo:
            motivo, created = Motivo.objects.get_or_create(nome=nome_motivo)
            return JsonResponse({'id': motivo.id, 'nome': motivo.nome})
    return JsonResponse({'error': 'Requisição inválida'}, status=400)

@login_required
def add_analista_ajax(request):
    if request.method == 'POST':
        nome_analista = request.POST.get('nome')
        if nome_analista:
            analista, created = Analista.objects.get_or_create(nome=nome_analista)
            return JsonResponse({'id': analista.id, 'nome': analista.nome})
    return JsonResponse({'error': 'Requisição inválida'}, status=400)

# --- VIEW PARA ADICIONAR ANDAMENTO ---

@login_required
def add_andamento(request, caso_pk):
    caso = get_object_or_404(Caso, pk=caso_pk)
    if request.method == 'POST':
        form = AndamentoForm(request.POST)
        if form.is_valid():
            andamento = form.save(commit=False)
            andamento.caso = caso
            andamento.usuario_criacao = request.user
            andamento.save()
    
    # Linha corrigida, com a indentação correta
    return redirect('caso_detail', pk=caso_pk)

@login_required
def add_tarefa(request, caso_pk):
    caso = get_object_or_404(Caso, pk=caso_pk)
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.caso = caso
            # O criador é o responsável por padrão
            if not tarefa.responsavel:
                tarefa.responsavel = request.user
            tarefa.save()
    return redirect('caso_detail', pk=caso_pk)

@login_required
def concluir_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    if request.method == 'POST':
        tarefa.status = 'C' # 'C' de Concluída
        tarefa.data_conclusao = timezone.now()
        tarefa.save()
    # Redireciona de volta para a página de detalhes do caso ao qual a tarefa pertence
    next_url = request.POST.get('next', reverse('caso_detail', kwargs={'pk': tarefa.caso.pk}))
    return redirect(next_url)

@login_required
def deletar_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    caso_pk = tarefa.caso.pk # Guarda o ID do caso antes de deletar a tarefa
    if request.method == 'POST':
        tarefa.delete()
    # Redireciona de volta para a página de detalhes do caso
    redirect_url = reverse('caso_detail', kwargs={'pk': caso_pk}) + '#tarefas-tab-pane'
    return redirect('caso_detail', pk=caso_pk)

@login_required
def reabrir_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    if request.method == 'POST':
        tarefa.status = 'P' # Pendente
        tarefa.data_conclusao = None # Limpa a data de conclusão
        tarefa.save()
    
    next_url = request.POST.get('next', reverse('caso_detail', kwargs={'pk': tarefa.caso.pk}))
    return redirect(next_url)

@login_required
def deletar_tarefa(request, tarefa_pk):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_pk)
    caso_pk = tarefa.caso.pk
    if request.method == 'POST':
        tarefa.delete()
    
    next_url = request.POST.get('next', reverse('caso_detail', kwargs={'pk': caso_pk}))
    return redirect(next_url)

class TarefaListView(LoginRequiredMixin, ListView):
    model = Tarefa
    template_name = 'casos/tarefa_list.html' # Um novo template para esta visão
    context_object_name = 'tarefas'
    paginate_by = 20 # Tarefas podem ser muitas, paginação é importante

    def get_queryset(self):
        # Começamos com todas as tarefas
        # select_related otimiza a busca, pegando os dados do caso, tipo e responsável
        # em uma única consulta ao banco de dados. Muito eficiente!
        queryset = Tarefa.objects.select_related('caso', 'tipo_tarefa', 'responsavel').all()

        # Filtro por Responsável (pessoa)
        responsavel_id = self.request.GET.get('responsavel')
        if responsavel_id:
            queryset = queryset.filter(responsavel_id=responsavel_id)

        # Filtro por Data de Criação
        data_de = self.request.GET.get('data_de')
        data_ate = self.request.GET.get('data_ate')
        if data_de:
            queryset = queryset.filter(data_criacao__date__gte=data_de)
        if data_ate:
            queryset = queryset.filter(data_criacao__date__lte=data_ate)

        # Filtro por Status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-data_criacao') # Mais recentes primeiro

    def get_context_data(self, **kwargs):
        # Adiciona dados extras ao template
        context = super().get_context_data(**kwargs)
        # Passa a lista de todos os usuários para o template, para popular o filtro
        context['responsaveis'] = User.objects.all().order_by('username')
        # Passa as opções de status para o template
        context['status_choices'] = Tarefa.STATUS_TAREFA_CHOICES
        return context
@login_required
def add_timesheet(request, caso_pk):
    caso = get_object_or_404(Caso, pk=caso_pk)
    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.caso = caso
            
            # Converte HH:MM para Duration
            tempo_str = form.cleaned_data['tempo_str']
            horas, minutos = map(int, tempo_str.split(':'))
            timesheet.tempo = timedelta(hours=horas, minutes=minutos)
            
            timesheet.save()
    return redirect(reverse('caso_detail', kwargs={'pk': caso_pk}) + '#timesheet-tab-pane')

# As views de Editar e Deletar são mais complexas para fazer na mesma página.
# Por enquanto, vamos criar apenas a de Deletar, que é mais simples.
@login_required
def delete_timesheet(request, ts_pk):
    timesheet = get_object_or_404(Timesheet, pk=ts_pk)
    caso_pk = timesheet.caso.pk
    if request.method == 'POST':
        timesheet.delete()
    return redirect(reverse('caso_detail', kwargs={'pk': caso_pk}) + '#timesheet-tab-pane')

@login_required
def exportar_timesheet_excel(request, caso_pk):
    caso = get_object_or_404(Caso, pk=caso_pk)
    timesheets = caso.timesheets.all().order_by('data_execucao')

    # Cria um arquivo Excel em memória
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f'Timesheet Caso {caso.id}'

    # --- CABEÇALHOS ---
    headers = ['Data Execução', 'Profissional', 'Tempo Gasto (HH:MM)', 'Descrição da Atividade']
    sheet.append(headers)
    
    # Estilo para os cabeçalhos (negrito)
    bold_font = Font(bold=True)
    for cell in sheet[1]:
        cell.font = bold_font
        cell.alignment = Alignment(horizontal='center')

    # --- DADOS ---
    total_duration = timedelta()
    for ts in timesheets:
        total_duration += ts.tempo
        
        # Formata a duração para HH:MM
        total_seconds = int(ts.tempo.total_seconds())
        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        tempo_formatado = f"{horas:02d}:{minutos:02d}"

        sheet.append([
            ts.data_execucao,
            ts.profissional.username,
            tempo_formatado,
            ts.descricao
        ])

    # --- LINHA DE TOTAL ---
    total_total_seconds = int(total_duration.total_seconds())
    total_horas = total_total_seconds // 3600
    total_minutos = (total_total_seconds % 3600) // 60
    total_formatado = f"{total_horas:02d}:{total_minutos:02d}"
    
    sheet.append([]) # Linha em branco
    sheet.append(['', '', 'Total de Horas:', total_formatado])
    # Estilo para o total
    total_cell = sheet.cell(row=sheet.max_row, column=3)
    total_cell.font = bold_font
    total_cell_valor = sheet.cell(row=sheet.max_row, column=4)
    total_cell_valor.font = bold_font
    
    # --- PREPARA A RESPOSTA HTTP ---
    # Nome do arquivo que será baixado
    filename = f'Relatorio_Timesheet_Caso_{caso.id}_{caso.titulo_caso}.xlsx'
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Salva o workbook na resposta
    workbook.save(response)

    return response

class CasoPesquisaView(LoginRequiredMixin, ListView):
    model = Caso
    template_name = 'casos/caso_pesquisa.html'
    context_object_name = 'casos'
    paginate_by = 25

    def get_queryset(self):
        queryset = Caso.objects.select_related(
            'cliente', 'status', 'advogado_responsavel', 'analista'
        ).all()

        # Filtro de texto livre (busca em vários campos)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(titulo_caso__icontains=q) |
                Q(numero_sinistro__icontains=q) |
                Q(numero_apolice__icontains=q) |
                Q(cliente__nome_razao_social__icontains=q) |
                Q(segurado__icontains=q) |
                Q(terceiro__icontains=q)
            )

        # Filtros de Combos (Dropdowns)
        filtros = {
            'cliente_id': self.request.GET.get('cliente'),
            'status_id': self.request.GET.get('status'),
            'advogado_responsavel_id': self.request.GET.get('advogado'),
            'analista_id': self.request.GET.get('analista'),
        }
        # Remove filtros vazios e aplica os que têm valor
        filtros_validos = {k: v for k, v in filtros.items() if v}
        if filtros_validos:
            queryset = queryset.filter(**filtros_validos)
        
        return queryset.order_by('-data_entrada')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Pesquisa Avançada de Casos"
        # Passa os dados para popular os combos de filtro no template
        context['clientes'] = Cliente.objects.all().order_by('nome_razao_social')
        context['advogados'] = Advogado.objects.all().order_by('nome')
        context['status_list'] = Status.objects.all().order_by('nome')
        context['analistas'] = Analista.objects.all().order_by('nome')
        return context
    
# ==============================================================================
# PESQUISA AVANÇADA E EXPORTAÇÃO
# ==============================================================================

def get_casos_filtrados(request):
    """Função auxiliar para reutilizar a lógica de filtro."""
    queryset = Caso.objects.select_related(
        'cliente', 'status', 'advogado_responsavel', 'analista'
    ).all()

    q = request.GET.get('q')
    if q:
        queryset = queryset.filter(
            Q(titulo_caso__icontains=q) |
            Q(numero_sinistro__icontains=q) |
            Q(numero_apolice__icontains=q) |
            Q(cliente__nome_razao_social__icontains=q) |
            Q(segurado__icontains=q) |
            Q(terceiro__icontains=q)
        )

    filtros = {
        'cliente_id': request.GET.get('cliente'),
        'status_id': request.GET.get('status'),
        'advogado_responsavel_id': request.GET.get('advogado'),
        'analista_id': request.GET.get('analista'),
    }
    filtros_validos = {k: v for k, v in filtros.items() if v}
    if filtros_validos:
        queryset = queryset.filter(**filtros_validos)
    
    return queryset.order_by('-data_entrada')

class CasoPesquisaView(LoginRequiredMixin, ListView):
    model = Caso
    template_name = 'casos/caso_pesquisa.html'
    context_object_name = 'casos'
    paginate_by = 25

    def get_queryset(self):
        return get_casos_filtrados(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Pesquisa Avançada de Casos"
        context['clientes'] = Cliente.objects.all().order_by('nome_razao_social')
        context['advogados'] = Advogado.objects.all().order_by('nome')
        context['status_list'] = Status.objects.all().order_by('nome')
        context['analistas'] = Analista.objects.all().order_by('nome')
        return context

@login_required
def exportar_casos_excel(request):
    queryset = get_casos_filtrados(request)
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Relatorio Completo de Casos'
    
    headers = [
        'ID do Caso', 'Título', 'Cliente', 'Status', 'Data de Entrada', 'Data de Cadastro',
        'Número do Aviso', 'Número do Sinistro', 'Número da Apólice',
        'Advogado Responsável', 'Analista', 'Segurado', 'Terceiro',
        'Cobertura', 'Motivo', 'Produto', 'Valor da Causa', 'Valor Prejuízo Apurado',
        'Data Relatório Preliminar', 'Data Relatório Final', 'Previsão de Conclusão',
        'Prazo Regulação (Dias)', 'Horas Trabalhadas', 'Número Caso LO',
        'Resumo do Caso', 'Observação'
    ]
    sheet.append(headers)
    bold_font = Font(bold=True)
    for cell in sheet[1]:
        cell.font = bold_font
        cell.alignment = Alignment(horizontal='center')

    for caso in queryset:
        # --- A CORREÇÃO ESTÁ AQUI ---
        # Cria uma versão "ingênua" da data de cadastro, sem timezone
        data_cadastro_sem_tz = caso.data_cadastro.replace(tzinfo=None) if caso.data_cadastro else None

        sheet.append([
            caso.id,
            caso.titulo_caso,
            caso.cliente.nome_razao_social,
            caso.status.nome if caso.status else '',
            caso.data_entrada,
            data_cadastro_sem_tz, # <-- Usamos a variável corrigida
            caso.numero_aviso,
            caso.numero_sinistro,
            caso.numero_apolice,
            caso.advogado_responsavel.nome if caso.advogado_responsavel else '',
            caso.analista.nome if caso.analista else '',
            caso.segurado,
            caso.terceiro,
            caso.cobertura.nome if caso.cobertura else '',
            caso.motivo.nome if caso.motivo else '',
            caso.produto.nome if caso.produto else '',
            caso.valor_causa,
            caso.valor_prejuizo_apurado,
            caso.data_relatorio_preliminar,
            caso.data_relatorio_final,
            caso.previsao_conclusao,
            caso.prazo_regulacao_dias,
            caso.horas_trabalhadas,
            caso.numero_caso_lo,
            caso.resumo_caso,
            caso.observacao,
        ])
    
    filename = 'Relatorio_Completo_Casos_Aureon.xlsx'
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    workbook.save(response)
    return response