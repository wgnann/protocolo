from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django import forms

from crispy_forms.helper import FormHelper

from .forms import ParecerDisciplinaFormset, ParecerDisciplinaFormsetHelper, ProtocoloAvulsoForm, RequerimentoMatriculaForm
from .models import Aluno, ProtocoloAvulso, Requerimento, RequerimentoAlteracao

def index(request):
    return render(request, 'protocolo/index.html', {})

# ListViews
class AlunoList(ListView):
    model = Aluno

class RequerimentoList(ListView):
    model = Requerimento

class RequerimentoAlteracaoList(ListView):
    model = RequerimentoAlteracao

# CreateViews
class CrispyCreateView(CreateView):
    def __init__(self, *args, **kwargs):
        super(CrispyCreateView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_context_data(self, **kwargs):
        context = super(CrispyCreateView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context

class AlunoCreate(CrispyCreateView):
    model = Aluno
    fields = ['nome', 'nusp']

class RequerimentoAlteracaoCreate(CrispyCreateView):
    model = RequerimentoAlteracao
    fields = ['aluno', 'unidade', 'disciplina', 'turma', 'docente']

# DetailViews
class AlunoDetail(DetailView):
    model = Aluno

class ProtocoloAvulsoDetail(DetailView):
    model = ProtocoloAvulso

# Resto
def protocoloavulso_novo(request):
    if request.method == 'POST':
        form = ProtocoloAvulsoForm(request.POST)
        if form.is_valid():
            protocolo_avulso = form.save()
            requerimentos = form.cleaned_data.get('requerimento')
            requerimentos.update(protocolo_avulso=protocolo_avulso)
            return HttpResponse(request)
    else:
        form = ProtocoloAvulsoForm()

    helper = FormHelper()
    helper.form_tag = False
    context = {
        'form': form,
        'helper': helper
    }
    template = "protocolo/protocoloavulso_form.html"
    return render(request, template, context)

def requerimentomatricula_novo(request):
    if request.method == 'POST':
        form = RequerimentoMatriculaForm(request.POST)
        formset = ParecerDisciplinaFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            requerimento = form.save()
            formset.instance = requerimento
            formset.save()
            return redirect(requerimento.get_absolute_url())
    else:
        form = RequerimentoMatriculaForm()
        formset = ParecerDisciplinaFormset()

    helper = FormHelper()
    helper.form_tag = False
    helperset = ParecerDisciplinaFormsetHelper()
    context = {
        'form': form,
        'formset': formset,
        'helper': helper,
        'helperset': helperset
    }
    template = "protocolo/requerimentomatricula_form.html"
    return render(request, template, context)

def requerimento_info(request, pk):
    parent = get_object_or_404(Requerimento, pk=pk)
    requerimento = parent.tipo()
    context = {'requerimento': requerimento}
    template = "protocolo/"+requerimento._meta.model_name+"_detail.html"
    return render(request, template, context)

