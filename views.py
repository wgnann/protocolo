from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Aluno, Requerimento, RequerimentoAlteracao

def index(request):
    return render(request, 'protocolo/index.html', {})

class AlunoCreate(CreateView):
    model = Aluno
    fields = ['nome', 'nusp']

class AlunoDetail(DetailView):
    model = Aluno

class AlunoList(ListView):
    model = Aluno

class RequerimentoDetail(DetailView):
    model = Requerimento

class RequerimentoAlteracaoCreate(CreateView):
    model = RequerimentoAlteracao
    fields = ['aluno', 'unidade', 'disciplina', 'turma', 'docente']
