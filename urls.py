from django.urls import path

from . import views

# precisa adicionar o include no urls.py do django
urlpatterns = [
    path('', views.index, name='index'),
    path('aluno/', views.AlunoList.as_view(), name='aluno_lista'),
    path('aluno/novo', views.AlunoCreate.as_view(), name='aluno_novo'),
    path('aluno/<int:pk>/', views.AlunoDetail.as_view(), name='aluno_info'),
    path('requerimento/', views.RequerimentoList.as_view(), name='requerimento_lista'),
    path('requerimento/<int:pk>/', views.requerimento_info, name='requerimento_info'),
    path('requerimento/alteracao/', views.RequerimentoAlteracaoList.as_view(), name='requerimento_alteracao_lista'),
    path('requerimento/alteracao/novo/', views.RequerimentoAlteracaoCreate.as_view(), name='requerimento_alteracao_novo'),
    path('requerimento/matricula/novo/', views.requerimentomatricula_novo, name='requerimento_matricula_novo'),
    path('protav/novo/', views.protocoloavulso_novo, name='protocolo_avulso_novo'),
    path('protav/<int:pk>/', views.ProtocoloAvulsoDetail.as_view(), name='protocolo_avulso_info'),
]
