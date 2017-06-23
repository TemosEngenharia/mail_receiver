from configparser import ConfigParser
import logging


def MailReceiverConf(_conf_file = '/etc/mail_receiver/mail_receiver.conf',
                     _section = 'Options'):
    logger = logging.getLogger(__name__)
    parser = ConfigParser()
    parser.read(_conf_file)
    mail_receiver_conf = {}
    if parser.has_section(_section):
        mail_receiver_conf = dict(parser.items(_section))
        return mail_receiver_conf
    else:
        raise Exception('Section {0} not found in the {1} file'.format(_section, _conf_file))

def OdooRPCConf(_conf_file = '/etc/odoo_prd/odoo_prd.conf',
                _section = 'option'):
    logger = logging.getLogger(__name__)
    parser = ConfigParser()
    if parser.has_section(_section):
        odoo_rpc_conf = dict(parser.items(_section))
        return odoo_rpc_conf
    else:
        raise Exception('Section {0} not found in the {1} file'.format(_section, _conf_file))
