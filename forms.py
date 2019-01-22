from django import forms
from django.forms.models import inlineformset_factory

from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from crispy_forms.helper import FormHelper

from .models import ParecerDisciplina, ProtocoloAvulso, Requerimento, RequerimentoMatricula, Unidade

class ParecerDisciplinaFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ParecerDisciplinaFormsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.template = 'bootstrap4/table_inline_formset.html'

class ProtocoloAvulsoForm(forms.ModelForm):
    requerimento = forms.ModelMultipleChoiceField(
        queryset=Requerimento.objects.filter(protocolo_avulso__isnull=True),
        widget=ModelSelect2MultipleWidget(model=Requerimento,
            search_fields=['aluno__nome__icontains'],
            dependent_fields={'unidade': 'unidade'}))

    class Meta:
        model = ProtocoloAvulso
        fields = ['unidade', 'secao', 'requerimento']
        widgets = {'unidade': ModelSelect2Widget(model=Unidade,
            search_fields=['nome__icontains'])}

class RequerimentoMatriculaForm(forms.ModelForm):
    class Meta:
        model = RequerimentoMatricula
        fields = ['aluno', 'unidade', 'docente']

ParecerDisciplinaFormset = inlineformset_factory(RequerimentoMatricula, ParecerDisciplina, fields = ['disciplina', 'turma', 'parecer'], extra=3, can_delete=False)
