from django.contrib import admin
from .models import Cliente, Telefone

class TelefoneInline(admin.TabularInline):
    model = Telefone
    extra = 1

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_razao_social', 'email', 'cidade')
    search_fields = ('nome_razao_social', 'email')
    inlines = [TelefoneInline]