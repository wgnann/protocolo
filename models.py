from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone

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
    def get_absolute_url(self):
        return reverse('aluno_info', kwargs={'pk': self.pk })

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
    protocolo_avulso = models.ForeignKey(
        ProtocoloAvulso,
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )
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

    # note que não poderemos ter mais de um grau de herança
    def tipo(self):
        for subclasse in Requerimento.__subclasses__():
            try:
                return getattr(self, subclasse._meta.model_name)
            except:
                pass

    def __str__(self):
        return "%s - %s - %s - %s" % (
            self.aluno.nusp,
            self.aluno.nome,
            self.unidade.nome,
            self.data_entrada.date()
    )

class RequerimentoAlteracao(Requerimento):
    ALTERACAO = 'A'
    BOLETIM = 'B'
    TIPO = (
        (ALTERACAO, 'Alteração de Frequência e Nota'),
        (BOLETIM, 'Boletim'),
    )

    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    frequencia = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True
    )
    nota = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True,
        null=True
    )
    subtipo = models.CharField(
        choices=TIPO,
        default=ALTERACAO,
        max_length=2,
    )
    turma = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('requerimento_alteracao_info', kwargs={'pk': self.pk })

    class Meta:
        verbose_name_plural = "requerimento alterações"

class RequerimentoMatricula(Requerimento):
    DISPENSA = 'D'
    MATRICULA = 'M'
    TIPO = (
        (DISPENSA, 'Dispensa'),
        (MATRICULA, 'Matrícula'),
    )

    disciplinas = models.ManyToManyField(Disciplina, through='ParecerDisciplina')
    subtipo = models.CharField(
        choices=TIPO,
        default=MATRICULA,
        max_length=2,
    )

    def get_absolute_url(self):
        return reverse('requerimento_matricula_info', kwargs={'pk': self.pk })

class RequerimentoOutros(Requerimento):
    OUTROS = 'O'
    RECURSO = 'R'
    TRANCAMENTO = 'T'
    TIPO = (
        (OUTROS, 'Outros'),
        (RECURSO, 'Recurso'),
        (TRANCAMENTO, 'Trancamento'),
    )
    parecer = models.CharField(
        choices=OPCOES_DO_PARECER,
        default=PENDENTE,
        max_length=2,
    )
    solicitacao = models.TextField(blank=True)
    subtipo = models.CharField(
        choices=TIPO,
        default=OUTROS,
        max_length=2,
    )

    def get_absolute_url(self):
        return reverse('requerimento_outros_info', kwargs={'pk': self.pk })

    class Meta:
        verbose_name_plural = "requerimento outros"

class ParecerDisciplina(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    parecer = models.CharField(
        choices=OPCOES_DO_PARECER,
        default=PENDENTE,
        max_length=2,
    )
    requerimento = models.ForeignKey(RequerimentoMatricula, on_delete=models.CASCADE)
    turma = models.CharField(max_length=10)

