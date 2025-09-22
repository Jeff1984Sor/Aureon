from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm

# ==============================================================================
# VIEW PARA LISTAR CLIENTES (AGORA FILTRADA POR EMPRESA)
# ==============================================================================
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        # Pega a empresa do usuário logado
        
        
        # Começa com apenas os clientes daquela empresa
        queryset = Cliente.objects.filter(empresa=empresa_usuario).order_by('nome_razao_social')
        
        # Aplica o filtro de busca textual, se houver
        search_term = self.request.GET.get('q')
        if search_term:
            queryset = queryset.filter(
                Q(nome_razao_social__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(cidade__icontains=search_term) |
                Q(uf__icontains=search_term) |
                Q(cep__icontains=search_term)
            )
        
        return queryset

# ==============================================================================
# VIEW PARA CRIAR CLIENTES (AGORA ATRIBUINDO A EMPRESA)
# ==============================================================================
class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Novo Cliente'
        return context

    def form_valid(self, form):
        # Antes de salvar, define a empresa do novo cliente
        # como sendo a mesma do usuário que está fazendo o cadastro.
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

# ==============================================================================
# VIEWS DE DETALHE, EDIÇÃO E EXCLUSÃO (AGORA FILTRADAS POR EMPRESA)
# ==============================================================================
class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'
    
    def get_queryset(self):
        # Garante que um usuário só possa ver detalhes de clientes da sua própria empresa
        return Cliente.objects.filter(empresa=self.request.user.empresa)

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Cliente'
        return context
        
    def get_queryset(self):
        # Garante que um usuário só possa editar clientes da sua própria empresa
        return Cliente.objects.filter(empresa=self.request.user.empresa)

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')
    
    def get_queryset(self):
        # Garante que um usuário só possa deletar clientes da sua própria empresa
        return Cliente.objects.filter(empresa=self.request.user.empresa)