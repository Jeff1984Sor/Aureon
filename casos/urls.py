from django.urls import path
from .views import CasoListView, CasoCreateView, CasoDetailView,add_tarefa,reabrir_tarefa,Timesheet,CasoUpdateView,TarefaListView,concluir_tarefa,deletar_tarefa,add_andamento,add_status_ajax,add_cobertura_ajax,add_motivo_ajax, add_analista_ajax,add_timesheet,delete_timesheet,exportar_timesheet_excel,CasoPesquisaView,exportar_casos_excel

urlpatterns = [
    path('', CasoListView.as_view(), name='caso_list'),
    path('novo/', CasoCreateView.as_view(), name='caso_create'),
    path('<int:pk>/', CasoDetailView.as_view(), name='caso_detail'),
    path('ajax/add-status/', add_status_ajax, name='add_status_ajax'),
    path('ajax/add-cobertura/', add_cobertura_ajax, name='add_cobertura_ajax'),
    path('ajax/add-motivo/', add_motivo_ajax, name='add_motivo_ajax'),
    path('ajax/add-analista/', add_analista_ajax, name='add_analista_ajax'),
    path('<int:caso_pk>/add_andamento/', add_andamento, name='add_andamento'),
    path('<int:caso_pk>/add_tarefa/', add_tarefa, name='add_tarefa'),
    path('tarefa/<int:tarefa_pk>/concluir/', concluir_tarefa, name='concluir_tarefa'),
    path('tarefa/<int:tarefa_pk>/deletar/', deletar_tarefa, name='deletar_tarefa'),
    path('tarefa/<int:tarefa_pk>/reabrir/', reabrir_tarefa, name='reabrir_tarefa'), 
    path('tarefas/', TarefaListView.as_view(), name='tarefa_list_all'),
    path('<int:pk>/editar/', CasoUpdateView.as_view(), name='caso_update'),
    path('<int:caso_pk>/add_timesheet/', add_timesheet, name='add_timesheet'),
    path('timesheet/<int:ts_pk>/delete/', delete_timesheet, name='delete_timesheet'),
    path('<int:caso_pk>/exportar_excel/', exportar_timesheet_excel, name='exportar_timesheet_excel'),
    path('pesquisa/', CasoPesquisaView.as_view(), name='caso_pesquisa'),
    path('exportar/', exportar_casos_excel, name='caso_exportar_excel'),
]