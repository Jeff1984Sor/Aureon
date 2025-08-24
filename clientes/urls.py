from django.urls import path
from .views import (
    ClienteListView,
    ClienteCreateView,
    UpdateView, # Esta importação estava errada antes, vamos corrigir
    ClienteUpdateView, # Importe a sua UpdateView correta
    ClienteDeleteView,
    ClienteDetailView  # <-- Importe a nova view
)

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list'),
    path('novo/', ClienteCreateView.as_view(), name='cliente_create'),
    
    # --- ADICIONE ESTA NOVA ROTA ABAIXO ---
    path('<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),

    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente_delete'),
]