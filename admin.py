from django.contrib import admin

from .models import *

class ParecerDisciplinaInline(admin.TabularInline):
    extra = 2
    fields = ['disciplina', 'turma', 'parecer']
    model = ParecerDisciplina
    verbose_name = "disciplina"

class RequerimentoMatriculaAdmin(admin.ModelAdmin):
    inlines = [ParecerDisciplinaInline]

admin.site.register(Aluno)
admin.site.register(Docente)
admin.site.register(Disciplina)
admin.site.register(Unidade)
admin.site.register(RequerimentoAlteracao)
admin.site.register(RequerimentoMatricula, RequerimentoMatriculaAdmin)
admin.site.register(RequerimentoOutros)
admin.site.register(ProtocoloAvulso)
