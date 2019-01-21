from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper

from .models import ParecerDisciplina, ProtocoloAvulso, Requerimento, RequerimentoMatricula

class ParecerDisciplinaFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ParecerDisciplinaFormsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.template = 'bootstrap4/table_inline_formset.html'

class ProtocoloAvulsoForm(forms.ModelForm):
    requerimentos = forms.ModelChoiceField(queryset=Requerimento.objects.all())

    class Meta:
        model = ProtocoloAvulso
        fields = ['unidade', 'secao', 'requerimentos']

class RequerimentoMatriculaForm(forms.ModelForm):
    class Meta:
        model = RequerimentoMatricula
        fields = ['aluno', 'unidade', 'docente']

ParecerDisciplinaFormset = inlineformset_factory(RequerimentoMatricula, ParecerDisciplina, fields = ['disciplina', 'turma', 'parecer'], extra=3, can_delete=False)

RequerimentoFormset = inlineformset_factory(ProtocoloAvulso, Requerimento, fields = '__all__', extra=2, can_delete=False)
