#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from mailparser import MailParser
from servicenow import parserServiceNow as parseSN


def parsemail(_mailfile):
    source = _mailfile
    mail = MailParser()
    mail.parse_from_file(_mailfile)
    if 'semparar@service-now.com' in mail.from_:
        parseSN(_mailfile, mail)


# Função Principal
def main(mailfile):
    parsemail(mailfile)


if __name__ == '__main__':
    main(sys.argv[1])
