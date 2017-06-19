#!/home/cezar.santanna/.virtualenvs/abastece/bin/python
# -*- coding: utf-8 -*-
from io import StringIO
from datetime import datetime
from lxml import html
from html2text import HTML2Text


def parserINC(_source, mail):
    print('Incidende------------------------------------------------')
    print('To: %s' % mail.to_)
    print('From: %s' % mail.from_)
    print('Subject: %s' % mail.subject)
    h = HTML2Text()
    h.ignore_links = True
    html = StringIO(h.handle(mail.body))
    i = 0
    for line in html:
        if 'Service Now' in line:
            print('Linha [%s]: %s' % (i, line))
        elif '**Usuario final afetado**' in line:
            print('Linha [%s]: %s' % (i, line))
        elif '**Descriçao Resumida**' in line:
            print('Linha [%s]: %s' % (i, line))
        elif '**Descriçao**' in line:
            print('Linha [%s]: %s' % (i, line))
        i = i + 1
    pass



def parserREQ(_source, mail):
    """
    print('Requisição-----------------------------------------------')
    print('To: %s' % mail.to_)
    print('From: %s' % mail.from_)
    print('Subject: %s' % mail.subject)
    h = HTML2Text()
    h.ignore_links = True
    html = StringIO(h.handle(mail.body))
    i = 0
    for line in html:
        if '**' in line:
            print('Linha [%s]: %s' % (i, line))
        i = i + 1
    """
    pass


def parserTASK(_source, mail):
    """
    print('Tarefa---------------------------------------------------')
    print('To: %s' % mail.to_)
    print('From: %s' % mail.from_)
    print('Subject: %s' % mail.subject)
    h = HTML2Text()
    h.ignore_links = True
    html = StringIO(h.handle(mail.body))
    i = 0
    for line in html:
        if '**' in line:
            print('Linha [%s]: %s' % (i, line))
        i = i + 1
    """
    pass


def parserServiceNow(_source, mail):
    if 'INC' in mail.subject:
        return parserINC(_source, mail)
    elif 'TASK' in mail.subject:
        return parserTASK(_source, mail)
    elif 'REQ' in mail.subject:
        return parserREQ(_source, mail)
    else:
        return _source.replace('/new/', '/ServiceNow/Others/not_parsed/')
