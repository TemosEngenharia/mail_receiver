import logging
import logging.handlers
import os
import sys

from conf.config import MailReceiverConf as Config
from parsers.mailparser import MailParser
from parsers.officetrack import parserOfficeTrack as parseOT
from parsers.servicenow import parserServiceNow as parseSN


config = Config()

logdir = config['log_dir']
mail_dir = config['mail_dir']

# Criando o log da aplicação
logger = logging.getLogger(__name__)

if config['log_level'] == 'INFO':
    logger.setLevel(logging.INFO)
elif config['log_level'] == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARN)

# Definido a Rotação do Arquivo de Log
logfile = logging.handlers.TimedRotatingFileHandler(
    logdir + 'mail_receiver.log',
    when = 'midnight',
    interval = 1,
    backupCount = 7,
    encoding = 'utf-8',
    )

# Definindo o Formato do Log
formatter = logging.Formatter(
    '%(asctime)s %(name)s|%(levelname)s|%(message)s',
    '%Y/%m/%d %H:%M:%S'
)

# Atribuindo o formato ao arquivo de log
logfile.setFormatter(formatter)

# Adicionando o arquivo de log ao logger
logger.addHandler(logfile)


def parsemail(_mailfile):
    source = _mailfile
    mail = MailParser()
    mail.parse_from_file(_mailfile)
    logger.info('From: %s' % mail.from_)
    logger.info('To: %s' % mail.to_)
    logger.info('Subject: %s' % mail.subject)
    if 'reports@latam.officeTrack.com' in mail.from_:
        destination = parseOT(_mailfile, mail)
        logger.info('OfficeTrack: Destination is %s' % destination)
        os.rename(source, destination)
    elif 'semparar@service-now.com' in mail.from_:
        # destination = parseSN(_mailfile, mail)
        destination = source.replace('/new/', '/ServiceNow/')
        logger.info('ServiceNow: Destination is %s' % destination)
        os.rename(source, destination)
    else:
        destination = source.replace('/new/', '/Error/')
        logger.info("Não identificado: Destination is %s, Subject is %s" % (destination, mail.subject))
        os.rename(source, destination)


# Função Principal
def main():
    try:
        files = [f for f in os.listdir(mail_dir) if os.path.isfile(os.path.join(mail_dir, f))]
        for mailfile in files:
            _mailfile = os.path.join(mail_dir, mailfile)
            parsemail(_mailfile)
    except:
        import traceback
        print('Whoops! Problem:', file = sys.stderr)
        traceback.print_exc(file = sys.stderr)
        logger.error("Mailfile %s, can't be parsed" % mailfile.replace('/new/', '/Error/'))
        destination = _mailfile.replace('/new/', '/Error/')
        os.rename(_mailfile, destination)
        pass
    finally:
        pass


if __name__ == '__main__':
    main()
