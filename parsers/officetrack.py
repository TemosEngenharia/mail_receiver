"""
Esta API tem como função principal processar os arquivos XMLs do OfficeTrack
e inserir as informações no banco de dados da aplicação abastece
"""
# -*- coding: utf-8 -*-
import re
from base64 import b64decode
from datetime import datetime
from datetime import date
from lxml import etree


"""
Variáveis para acesso ao Banco de Dados
"""
dbHost = "127.0.0.1"
dbName = "temosportal"
dbUser = "temos"
dbPass = "tw28()KP"


def saveXML(_attach, _mail, _dest):
    if _dest == 'Corretiva':
        filename = '/opt/files/xmls/mco/MCO01_' + _mail + '.xml'
    elif _dest == 'Preventiva':
        filename = '/opt/files/xmls/preventivas/PRV01_' + _mail + '.xml'
    elif _dest == 'PunchIn':
        filename = '/opt/files/xmls/punchin/PIN01_' + _mail + '.xml'
    elif _dest == 'PunchOut':
        filename = '/opt/files/xmls/punchout/POU01_' + _mail + '.xml'
    elif _dest == 'StartTask':
        filename = '/opt/files/xmls/starttask/STA01_' + _mail + '.xml'
    elif _dest == 'CloseTask':
        filename = '/opt/files/xmls/closetask/CTA01_' + _mail + '.xml'
    elif _dest == 'TaskNotDone':
        filename = '/opt/files/xmls/tasknotdone/TND01_' + _mail + '.xml'
    else:
        filename = '/opt/files/xmls/outros/' + _mail + '.xml'
    with open(filename, 'wb') as f:
        f.write(_attach)


def getFormName(_xml):
    _FormName = _xml.find('Form/Name')
    if _FormName is not None:
        _FormNameText = _FormName.text
        if 'AÇÕES' in _FormNameText:
            _FormNameText = 'AÇÕES DE MELHORIAS'
        elif 'PREVENTIVA' in _FormNameText:
            _FormNameText = 'PREVENTIVA'
        elif 'CORRETIVA' in _FormNameText:
            _FormNameText = 'CORRETIVA'
        else:
            pass
        return _FormNameText
    else:
        return None


def getEntryType(_xml):
    """
    Método para coleta da variável EntryType incluída no arquivo XML do
    OfficeTrack, esta variável pode assumir diferentes valores dependendo do
    tipo de Entrada realizada pelo funcionário no aplicativo do OfficeTrack.
    As EntryTypes utilizadas pela aplicação Abastece são:
    EntryType 21: MS_PunchIn
    EntryType 22: MS_PunchOut
    EntryType 23: MS_StartTask
    EntryType 24: MS_EndTask
    EntryType 25: MS_ConfirmTask
    EntryType 26: MS_CloseTask
    EntryType 29: MS_TaskNotDone
    EntryType 33: MS_TaskForm
    EntryType 60: MS_FormFilled

    Caso não seja possível encontrar este valor no XML ou o valor encontrado
    não corresponder aos prédefinidos o valor None é retornado e deve ser
    tratado pelo processo chamador
    """
    _EntryType = _xml.find('EntryType')
    if _EntryType is not None:
        if (_EntryType.text == '21' or
            _EntryType.text == '22' or
            _EntryType.text == '23' or
            _EntryType.text == '24' or
            _EntryType.text == '25' or
            _EntryType.text == '26' or
            _EntryType.text == '29' or
            _EntryType.text == '33' or
            _EntryType.text == '60'):
            return _EntryType.text
        else:
            return None
    else:
        return None


def parserOfficeTrack(_source, _mail):
    attach = b64decode(_mail.attachments_list[0]['payload'])
    xml = etree.fromstring(attach)
    FormName = getFormName(xml)

    if 'new' in _source:
        Filename = _source.replace('/opt/odoo-prd/Maildir/new/', '')
    elif 'manual' in _source:
        Filename = _source.replace('/opt/odoo-prd/Maildir/manual/', '')

    if getEntryType(xml) == '21':
        saveXML(attach, Filename, 'PunchIn')
    elif getEntryType(xml) == '22':
        saveXML(attach, Filename, 'PunchOut')
    elif getEntryType(xml) == '23':
        saveXML(attach, Filename, 'StartTask')
    elif getEntryType(xml) == '24':
        saveXML(attach, Filename, 'Outro')
    elif getEntryType(xml) == '25':
        saveXML(attach, Filename, 'Outro')
    elif getEntryType(xml) == '26':
        saveXML(attach, Filename, 'CloseTask')
    elif getEntryType(xml) == '29':
        saveXML(attach, Filename, 'TaskNotDone')
    elif getEntryType(xml) == '33':
        FormName = getFormName(xml)
        if 'Manutenção Corretiva' in FormName:
            saveXML(attach, Filename, 'Corretiva')
        elif 'Manutenção Preventiva' in FormName:
            saveXML(attach, Filename, 'Preventiva')
        elif 'Survey Instalação' in FormName:
            saveXML(attach, Filename, 'SurveyInst')
        elif 'AsBuilt' in FormName:
            saveXML(attach, Filename, 'AsBuilt')
        else:
            saveXML(attach, Filename, 'Outro')
    elif getEntryType(xml) == '60':
        saveXML(attach, Filename, 'Outro')

    if '/new/' in _source:
        return _source.replace('/new/', '/OfficeTrack/')
    elif '/manual/' in _source:
        return _source.replace('/manual/', '/OfficeTrack/')
