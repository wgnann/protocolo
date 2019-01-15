from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
    
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
    nusp = models.CharField(max_length=20, unique=True)

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
        return "%s - %s" % (
            self.sigla,
            self.nome
        )

class Unidade(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class ProtocoloAvulso(models.Model):
    data_saida = models.DateTimeField(auto_now=True)
    secao = models.CharField(max_length=255)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "protocolos avulsos"

    def __str__(self):
        return "%s - %s - %s" % (
            str(self.id),
            self.unidade.nome,
            self.secao
        )

class Requerimento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    # implementaremos auto_now=True no save()
    data_entrada = models.DateTimeField(editable=False)
    data_parecer = models.DateTimeField(blank=True, null=True)
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT)
    # implementaremos unicidade anual no save()
    indice_anual = models.PositiveIntegerField(editable=False)
    observacao = models.TextField(blank=True)
    protocolo_avulso = models.ForeignKey(ProtocoloAvulso, on_delete=models.PROTECT)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT)

    # está vulnerável a race conditions! 
    def save(self, *args, **kwargs):
        if not self.data_entrada:
            self.data_entrada = timezone.now()

        if not self.indice_anual:
            ultimo = Requerimento.objects.filter(data_entrada__year = self.data_entrada.year).order_by('indice_anual').last()
            if ultimo:
                self.indice_anual = ultimo.indice_anual + 1
            else:
                self.indice_anual = 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s - %s - %s" % (
            self.aluno.nusp,
            self.aluno.nome,
            self.data_entrada.date()
    )

class RequerimentoAlteracao(Requerimento):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    frequencia = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True
    )
    nota = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True
    )
    turma = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "requerimento alterações"

class RequerimentoMatricula(Requerimento):
    disciplinas = models.ManyToManyField(Disciplina, through='ParecerDisciplina')
RequerimentoDispensa = RequerimentoMatricula

class RequerimentoOutros(Requerimento):
    parecer = models.CharField(
        max_length=2,
        choices=OPCOES_DO_PARECER,
        default=PENDENTE,
    )
    solicitacao = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "requerimento outros"

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

