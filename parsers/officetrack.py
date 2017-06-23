# -*- coding: utf-8 -*-
from base64 import b64decode
import logging
import logging.handlers
import os
import time

from lxml import etree

logger = logging.getLogger(__name__)

def getFormName(_xml):
    _FormName = _xml.find('Form/Name')
    if _FormName is not None:
        _FormNameText = _FormName.text
        return _FormNameText
    else:
        return None


def saveXML(_attach, _mail, _TypeForm, _FormVersion, _source):
    _date = _mail.split('.')[0]
    _id = _mail.split('.')[1]

    if '/' in _TypeForm:
        xml_dir = _TypeForm.lower()
        _TypeForm = _TypeForm.split('/')[1]
    else:
        xml_dir = _TypeForm.lower()

    _mailname = (_TypeForm + '_' +
             _FormVersion + '_' +
             time.strftime('%Y%m%d_%H%M%S_%Z', time.localtime(int(_date))) +
             '_' + _id
             )

    filename = '/opt/files/xmls/' + xml_dir + '/' + _mailname + '.xml'

    try:
        with open(filename, 'wb') as f:
            try:
                f.write(_attach)
                _mail_dir = os.path.dirname(_source).replace('/new', '/OfficeTrack/')
                _mailfilename = _mail_dir + _mailname + '.mail'
                return _mailfilename
            except:
                pass
    except:
        return _source

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
    print(_source)
    attach = b64decode(_mail.attachments_list[0]['payload'])
    xml = etree.fromstring(attach)
    FormName = getFormName(xml)

    if FormName is None:
        _TypeForm = 'outros'
        _FormVersion = '01'
        Filename = os.path.basename(_source)
        return saveXML(attach, Filename, _TypeForm, _FormVersion, _source)

    split_FormName = FormName.split('|')
    len_split_FormName = len(split_FormName)

    if len_split_FormName == 1:
        if 'AÇÕES' in FormName:
            _TypeForm = 'antigas/melhorias'
            _FormVersion = 'P01'
        elif 'AJUSTE' in FormName:
            _TypeForm = 'antigas/ajuste915'
            _FormVersion = 'P01'
        elif 'ASBUILT' in FormName:
            _TypeForm = 'antigas/asbuilt'
            _FormVersion = 'P01'
        elif 'CORRETIVA' in FormName:
            _TypeForm = 'antigas/corretivas'
            _FormVersion = 'P01'
        elif 'ICR' in FormName:
            _TypeForm = 'antigas/icr'
            _FormVersion = 'P01'
        elif 'INSTALAÇÃO' in FormName:
            _TypeForm = 'antigas/instalacaoposto'
            _FormVersion = 'P01'
        elif 'INVENTÁRIO' in FormName:
            _TypeForm = 'antigas/inventario'
            _FormVersion = 'P01'
        elif 'PLANO' in FormName:
            _TypeForm = 'antigas/planoverao'
            _FormVersion = 'P01'
        elif 'PREVENTIVA' in FormName:
            _TypeForm = 'antigas/preventivas'
            _FormVersion = 'P01'
        elif 'RETIRADA' in FormName:
            _TypeForm = 'antigas/retirada58'
            _FormVersion = 'P01'
        elif 'SINALIZAÇÃO' in FormName:
            _TypeForm = 'antigas/sinalizacao'
            _FormVersion = 'P01'
        elif 'SURVEY' in FormName:
            _TypeForm = 'antigas/survey'
            _FormVersion = 'P01'
        elif 'NÃO':
            _TypeForm = 'TND'
            _FormVersion = 'P01'
        else:
            _TypeForm = 'outros'
            _FormVersion = 'P01'
        Filename = os.path.basename(_source)
        return saveXML(attach, Filename, _TypeForm, _FormVersion, _source)
    elif len_split_FormName == 2:
        if 'Manutenção Corretiva' in FormName:
            _TypeForm = 'MCO'
            _FormVersion = FormName.split('|')[1].strip()
        else:
            _TypeForm = 'outros'
            _FormVersion = 'P01'
        Filename = os.path.basename(_source)
        return saveXML(attach, Filename, _TypeForm, _FormVersion, _source)
    elif len_split_FormName > 2:
        _TypeForm = FormName.split('|')[1].strip()
        _FormVersion = FormName.split('|')[2].strip()
        Filename = os.path.basename(_source)
        return saveXML(attach, Filename, _TypeForm, _FormVersion, _source)
