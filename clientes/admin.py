from django.contrib import admin
from .models import Cliente, Telefone

# Isso permite adicionar telefones na mesma tela de edição do cliente
class TelefoneInline(admin.TabularInline):
    model = Telefone
    extra = 1 # Mostra um campo extra para adicionar telefone por padrão

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_razao_social', 'email', 'tipo_pessoa', 'cidade', 'uf')
    inlines = [TelefoneInline] # Adiciona a seção de telefones
    search_fields = ('nome_razao_social', 'email')