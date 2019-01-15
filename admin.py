from django.contrib import admin

from .models import *

class ParecerDisciplinaInline(admin.TabularInline):
    extra = 2
    fields = ['disciplina', 'turma', 'parecer']
    model = ParecerDisciplina
    verbose_name = "disciplina"

class DisciplinaAdmin(admin.ModelAdmin):
    fields = ['sigla', 'nome']

class RequerimentoAlteracaoAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Informações do aluno",  {'fields':
            [('aluno', 'unidade'), ('disciplina', 'turma')]
        }),
        ("Informações do parecer", {'fields':
            ['docente', 'data_parecer', ('frequencia', 'nota'), 'observacao']
        })
    ]

class RequerimentoMatriculaAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Informações do aluno", {'fields': [('aluno', 'unidade')]}),
        ("Informações do parecer", {'fields':
            ['docente', 'data_parecer', 'observacao']
        })
    ]
    inlines = [ParecerDisciplinaInline]

class RequerimentoOutrosAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Informações do aluno", {'fields':
            [('aluno', 'unidade'), 'solicitacao']
        }),
        ("Informações do parecer", {'fields':
            ['docente', 'data_parecer', 'parecer', 'observacao']
        })
    ]

class ProtocoloAvulsoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Aluno)
admin.site.register(Docente)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Unidade)
admin.site.register(RequerimentoAlteracao, RequerimentoAlteracaoAdmin)
admin.site.register(RequerimentoMatricula, RequerimentoMatriculaAdmin)
admin.site.register(RequerimentoOutros, RequerimentoOutrosAdmin)
admin.site.register(ProtocoloAvulso, ProtocoloAvulsoAdmin)
