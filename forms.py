from django import forms
from django.forms.models import inlineformset_factory

from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from crispy_forms.helper import FormHelper

from .models import ParecerDisciplina, ProtocoloAvulso, Requerimento, RequerimentoAlteracao, RequerimentoMatricula, RequerimentoOutros, Unidade

class ParecerDisciplinaFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ParecerDisciplinaFormsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.template = 'bootstrap4/table_inline_formset.html'

class ProtocoloAvulsoForm(forms.ModelForm):
    requerimento = forms.ModelMultipleChoiceField(
        queryset=Requerimento.objects.filter(protocolo_avulso__isnull=True),
        widget=ModelSelect2MultipleWidget(
            model=Requerimento,
            search_fields=['aluno__nome__icontains'],
            dependent_fields={'unidade': 'unidade'}
        )
    )

    class Meta:
        model = ProtocoloAvulso
        fields = ['unidade', 'secao', 'requerimento']
        widgets = {
            'unidade': ModelSelect2Widget(
                model=Unidade,
                search_fields=['nome__icontains']
            )
        }

class RequerimentoAlteracaoForm(forms.ModelForm):
    class Meta:
        model = RequerimentoAlteracao
        fields = ['aluno', 'unidade', 'disciplina', 'turma', 'docente', 'subtipo']
        widgets = {'subtipo': forms.HiddenInput}

class RequerimentoAlteracaoUpdateForm(forms.ModelForm):
    class Meta:
        model = RequerimentoAlteracao
        fields = ['nota', 'frequencia', 'observacao', 'subtipo', 'data_parecer']
        widgets = {
            'subtipo': forms.HiddenInput,
            'data_parecer': forms.HiddenInput,
        }

class RequerimentoMatriculaForm(forms.ModelForm):
    class Meta:
        model = RequerimentoMatricula
        fields = ['aluno', 'unidade', 'docente', 'subtipo']
        widgets = {'subtipo': forms.HiddenInput}

class RequerimentoOutrosForm(forms.ModelForm):
    class Meta:
        model = RequerimentoOutros
        fields = ['aluno', 'unidade', 'solicitacao', 'docente', 'subtipo']
        widgets = {'subtipo': forms.HiddenInput}

class RequerimentoOutrosUpdateForm(forms.ModelForm):
    class Meta:
        model = RequerimentoOutros
        fields = ['parecer', 'observacao', 'subtipo', 'data_parecer']
        widgets = {
            'subtipo': forms.HiddenInput,
            'data_parecer': forms.HiddenInput,
        }

ParecerDisciplinaFormset = inlineformset_factory(RequerimentoMatricula, ParecerDisciplina, fields = ['disciplina', 'turma'], extra=3, can_delete=False)
