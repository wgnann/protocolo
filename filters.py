import django_filters

from .models import Requerimento

class RequerimentoFilter(django_filters.FilterSet):
    class Meta:
        model = Requerimento
        fields = ['aluno']
