# mail_receiver
Processa a fila de arquivos de e-mail, via cron.d, categorizando como:
 1 - E-mail vindos do Servidor OfficeTrack com arquivos XML anexados
 2 - E-mail vindos do ServiceNow com as informações das TASKs ou INCs atribuídos a Temos
 3 - Outros e-mails
 
Na categoria 1 são realizadas as seguintes ações:
  1 - Extração do XML anexo
  2 - Salvamento arquivo XML dentro da pasta /opt/files/xmls/to_process/OfficeTrack em caso de sucesso
  3 - Salva e-mail completo dentro da pasta /opt/files/mails/OfficeTrack/processed/ em caso de sucesso (comprimido)
  4 - Salva e-mail completo dentro da pasta /opt/files/mails/OfficeTrack/error/ em caso de falha

Na categoria 2 são realizadas as seguintes ações:
  1 - Extração das informações do corpo do e-mail
  2 - Salvamento das informações em XML dentro da pasta /opt/files/xmls/to_process/ServiceNow em caso de sucesso
  3 - Salva e-mail completo dentro da pasta /opt/files/mails/ServiceNow/processed/ em caso de sucesso (comprimido)
  4 - Salva e-mail completo dentro da pasta /opt/files/mails/ServiceNow/error/ em caso de falha

Na categoria 3 são realizadas as seguintes ações:
  1 - Salva e-mail completo dentro da pasta opt/files/mails/Outros/ (comprimidos)
  2 - via cron.d todos os arquivos com mais de 31 dias são apagados