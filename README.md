# o que é
Esta é uma tentativa de escrever um substituto para um sistema de protocolos.

# instalação
Procedimentos para a instalação do sistema de protocolos para desenvolvimento e testes.

## virtualenv

    virtualenv venv -p python3
    source venv/bin/activate

**OBS:** sempre que qualquer coisa relacionada ao projeto for executada, esse passo é necessário (caso já não tenha sido executado).

## packages

    pip install django django-crispy-forms django-extensions django-filter django-select2

## django

    django-admin start startproject jango

### configuração
em **jango/jango/settings.py**, acrescentar depois de INSTALLED_APPS

    INSTALLED_APPS += [
    	'protocolo.apps.ProtocoloConfig',
    	'django_extensions',
    	'django_select2',
    	'django_filters',
    	'crispy_forms',
    ]
    
    CRISPY_TEMPLATE_PACK = 'bootstrap4'

ainda no **settings.py**, substituir

    LANGUAGE_CODE = 'pt-br'
    TIME_ZONE = 'America/Sao_Paulo'

em **jango/jango/urls.py**, **antes** de urlpatterns importar o **include**
    from django.urls import path, include

em **urls.py**, acrescentar **depois** de urlpatterns

    urlpatterns += [
        path('protocolo/', include('protocolo.urls')),
        path('select2/', include('django_select2.urls')),
    ]

## outras dependências

### migrations
    cd venv/jango/protocolo
    mkdir -p migrations
    > migrations/__init__.py
    cd ..
    python manage.py makemigrations
    python manage.py migrate

### conteúdo estático

    cd venv/jango/protocolo
    mkdir -p static/js
    wget -P static/js/ https://code.jquery.com/jquery-3.3.1.min.js

### criando usuário do /admin

    cd venv/jango
    python manage.py createsuperuser

## rodando
    cd venv/jango
    python manage.py runserver

Daí, basta acessar:

 - localhost:8000/admin
 - localhost:8000/protocolo
