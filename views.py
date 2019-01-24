from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django import forms

from crispy_forms.helper import FormHelper

from .filters import RequerimentoFilter
from .forms import ParecerDisciplinaFormset, ParecerDisciplinaFormsetHelper, ProtocoloAvulsoForm, RequerimentoAlteracaoForm, RequerimentoAlteracaoUpdateForm, RequerimentoMatriculaForm, RequerimentoOutrosForm, RequerimentoOutrosUpdateForm
from .models import Aluno, ProtocoloAvulso, Requerimento, RequerimentoAlteracao, RequerimentoMatricula, RequerimentoOutros


# CrispyViews
def CrispyFactory(Class):
    class CrispyGeneric(Class):
        def __init__(self, *args, **kwargs):
            super(CrispyGeneric, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False

        def get_context_data(self, **kwargs):
            context = super(CrispyGeneric, self).get_context_data(**kwargs)
            context['helper'] = self.helper
            return context
    return CrispyGeneric

CrispyCreateView = CrispyFactory(CreateView)
CrispyUpdateView = CrispyFactory(UpdateView)


# CreateViews
class AlunoCreate(CrispyCreateView):
    model = Aluno
    fields = ['nome', 'nusp']

class RequerimentoAlteracaoCreate(CrispyCreateView):
    model = RequerimentoAlteracao
    form_class = RequerimentoAlteracaoForm

#RequerimentoMatriculaCreate = requerimentomatricula_novo

class RequerimentoOutrosCreate(CrispyCreateView):
    model = RequerimentoOutros
    form_class = RequerimentoOutrosForm 


# DetailViews
class AlunoDetail(DetailView):
    model = Aluno

class RequerimentoAlteracaoDetail(DetailView):
    model = RequerimentoAlteracao

class RequerimentoMatriculaDetail(DetailView):
    model = RequerimentoMatricula

class RequerimentoOutrosDetail(DetailView):
    model = RequerimentoOutros

class ProtocoloAvulsoDetail(DetailView):
    model = ProtocoloAvulso


# ListViews
class AlunoList(ListView):
    model = Aluno

class RequerimentoList(ListView):
    model = Requerimento

class RequerimentoAlteracaoList(ListView):
    model = RequerimentoAlteracao

class RequerimentoMatriculaList(ListView):
    model = RequerimentoMatricula

class RequerimentoOutrosList(ListView):
    model = RequerimentoOutros


# UpdateViews
class RequerimentoAlteracaoUpdate(CrispyUpdateView):
    model = RequerimentoAlteracao
    form_class = RequerimentoAlteracaoUpdateForm

class RequerimentoOutrosUpdate(CrispyUpdateView):
    model = RequerimentoOutros
    form_class = RequerimentoOutrosUpdateForm


# Resto
def index(request):
    return render(request, 'protocolo/index.html', {})

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
    return redirect(requerimento.get_absolute_url())

def requerimento_parecer(request, pk):
    parent = get_object_or_404(Requerimento, pk=pk)
    requerimento = parent.tipo()
    return redirect(requerimento.parecer_url())
