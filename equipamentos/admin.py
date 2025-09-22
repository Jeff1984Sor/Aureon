from django.contrib import admin
from .models import Equipamento, TipoItem, CategoriaItem, Marca, StatusItem

@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin): list_display = ('nome',)
@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin): list_display = ('nome',)
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin): list_display = ('nome',)
@admin.register(StatusItem)
class StatusItemAdmin(admin.ModelAdmin): list_display = ('nome',)

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('numero_item', 'tipo_item', 'marca', 'modelo', 'posse_status')
    list_filter = ('tipo_item', 'categoria_item', 'marca', 'status_item', 'posse_status')