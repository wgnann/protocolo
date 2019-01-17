from django.shortcuts import get_object_or_404, render
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

class RequerimentoAlteracaoCreate(CreateView):
    model = RequerimentoAlteracao
    fields = ['aluno', 'unidade', 'disciplina', 'turma', 'docente']

def requerimento_info(request, pk):
    parent = get_object_or_404(Requerimento, pk=pk)
    requerimento = parent.tipo()
    context = {'requerimento': requerimento}
    template = "protocolo/"+requerimento._meta.model_name+"_detail.html"
    return render(request, template, context)
