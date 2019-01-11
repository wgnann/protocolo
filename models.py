from django.db import models
    
DEFERIDO = 'D'
INDEFERIDO = 'I'
PENDENTE = 'P'
OPCOES_DO_PARECER = (
    (DEFERIDO, 'Deferido'),
    (INDEFERIDO, 'Indeferido'),
    (PENDENTE, 'Pendente'),
)

class PessoaUSP(models.Model):
    nome = models.CharField(max_length=255)
    nusp = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

class Aluno(PessoaUSP):
    pass

class Docente(PessoaUSP):
    departamento = models.CharField(max_length = 10)

class Disciplina(models.Model):
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=10)

    def __str__(self):
        return self.nome

class Unidade(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Requerimento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    data_entrada = models.DateTimeField()
    data_parecer = models.DateTimeField()
    data_saida = models.DateTimeField()
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT)
    observacao = models.TextField()
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.aluno)

class RequerimentoAlteracao(Requerimento):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    frequencia = models.IntegerField()
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    turma = models.CharField(max_length=10)

class RequerimentoMatricula(Requerimento):
    disciplinas = models.ManyToManyField(Disciplina, through='ParecerDisciplina')
RequerimentoDispensa = RequerimentoMatricula

class RequerimentoOutros(Requerimento):
    parecer = models.CharField(
        max_length=2,
        choices=OPCOES_DO_PARECER,
        default=PENDENTE,
    )
    solicitacao = models.TextField()
RequerimentoRecurso = RequerimentoOutros
RequerimentoTrancamento = RequerimentoOutros

class ParecerDisciplina(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    parecer = models.CharField(
        max_length=2,
        choices=OPCOES_DO_PARECER,
        default=PENDENTE,
    )
    requerimento = models.ForeignKey(RequerimentoMatricula, on_delete=models.PROTECT)
    turma = models.CharField(max_length=10)

    def __str__(self):
       return self.disciplina 
