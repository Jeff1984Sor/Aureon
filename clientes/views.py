# No topo do arquivo, adicione CreateView e reverse_lazy às importações
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm # <-- Importe o formulário que acabamos de criar
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.db.models import Q

# Esta view você já tem. Deixe ela como está.
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10 # Opcional: Adiciona paginação para listas grandes

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome_razao_social') # Começa com todos os clientes, ordenados por nome
        
        # Pega o termo de busca da URL (o 'q' do nosso formulário)
        search_term = self.request.GET.get('q')
        
        if search_term:
            # Se um termo de busca foi enviado, filtra o queryset
            # __icontains faz a busca "case-insensitive" (não diferencia maiúsculas de minúsculas)
            queryset = queryset.filter(
                Q(nome_razao_social__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(cidade__icontains=search_term) |
                Q(uf__icontains=search_term) |
                Q(cep__icontains=search_term)
                # Adicione mais campos aqui se desejar
            )
        
        return queryset

# --- ADICIONE ESTA NOVA VIEW ABAIXO ---

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html' # O arquivo HTML que vamos criar a seguir
    success_url = reverse_lazy('cliente_list') # Para onde ir depois de salvar com sucesso

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente' # O nome que usaremos no template para acessar o objeto

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html' # Reutiliza o mesmo template do create
    success_url = reverse_lazy('cliente_list')

    # Opcional: passa um título para o template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Cliente'
        return context
class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html' # Um template para confirmar
    success_url = reverse_lazy('cliente_list')