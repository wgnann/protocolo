from django.urls import path

from . import views

# precisa adicionar o include no urls.py do django
urlpatterns = [
    path('', views.index, name='index'),
    path('aluno/', views.AlunoList.as_view(), name='aluno_lista'),
    path('aluno/novo', views.AlunoCreate.as_view(), name='aluno_novo'),
    path('aluno/<int:pk>/', views.AlunoDetail.as_view(), name='aluno_info'),
    path('requerimento/<int:pk>/', views.RequerimentoDetail.as_view(), name='requerimento_info'),
    path('requerimento/alteracao/novo', views.RequerimentoAlteracaoCreate.as_view(), name='requerimento_alteracao_novo'),
]
