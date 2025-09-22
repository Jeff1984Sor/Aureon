from django.urls import path
from .views import (
    # Views de Casos
    CasoListView,
    CasoCreateView,
    CasoUpdateView,
    CasoDetailView,
    # Views de Pesquisa e Kanban
    CasoPesquisaView,
    KanbanView,
    TarefaListView,
    # Views de Ações (funções)
    add_andamento,
    add_tarefa,
    concluir_tarefa,
    reabrir_tarefa,
    deletar_tarefa,
    TimesheetListView,
    add_timesheet,
    delete_timesheet,
    # Views de Relatórios (funções)
    exportar_casos_excel,
    exportar_timesheet_excel,
    gerar_caso_pdf,
    # Views AJAX (funções)
    add_status_ajax,
    add_cobertura_ajax,
    add_motivo_ajax,
    add_analista_ajax,
)

urlpatterns = [
    # URLs principais do app 'casos'
    path('', CasoListView.as_view(), name='caso_list'),
    path('novo/', CasoCreateView.as_view(), name='caso_create'),
    path('pesquisa/', CasoPesquisaView.as_view(), name='caso_pesquisa'),
    path('kanban/', KanbanView.as_view(), name='kanban_board'),
    path('exportar/', exportar_casos_excel, name='caso_exportar_excel'),
    
    # URLs específicas de um caso (com <int:pk>)
    path('<int:pk>/', CasoDetailView.as_view(), name='caso_detail'),
    path('<int:pk>/editar/', CasoUpdateView.as_view(), name='caso_update'),
    path('<int:pk>/gerar_pdf/', gerar_caso_pdf, name='gerar_caso_pdf'),
    path('<int:pk>/exportar_excel/', exportar_timesheet_excel, name='exportar_timesheet_excel'),
    
    # URLs de Ações (com ID do caso ou da tarefa)
    path('<int:caso_pk>/add_andamento/', add_andamento, name='add_andamento'),
    path('<int:caso_pk>/add_tarefa/', add_tarefa, name='add_tarefa'),
    path('tarefas/', TarefaListView.as_view(), name='tarefa_list_all'),
     path('timesheets/', TimesheetListView.as_view(), name='timesheet_list_all'),
    path('<int:caso_pk>/add_timesheet/', add_timesheet, name='add_timesheet'),
    path('tarefa/<int:tarefa_pk>/concluir/', concluir_tarefa, name='concluir_tarefa'),
    path('tarefa/<int:tarefa_pk>/reabrir/', reabrir_tarefa, name='reabrir_tarefa'),
    path('tarefa/<int:tarefa_pk>/deletar/', deletar_tarefa, name='deletar_tarefa'),
    path('timesheet/<int:ts_pk>/delete/', delete_timesheet, name='delete_timesheet'),
    
    # URLs AJAX
    path('ajax/add-status/', add_status_ajax, name='add_status_ajax'),
    path('ajax/add-cobertura/', add_cobertura_ajax, name='add_cobertura_ajax'),
    path('ajax/add-motivo/', add_motivo_ajax, name='add_motivo_ajax'),
    path('ajax/add-analista/', add_analista_ajax, name='add_analista_ajax'),
]