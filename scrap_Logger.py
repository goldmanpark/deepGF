import os
import logging
import datetime
from pathlib import Path

# error Log directory setting
# Log directory structure with example:
# /LOG
#   -/ERROR
#       -20210725_134030_SOWON.log
#   -/COMPLETE
#       -20210725_141032_SOWON.log

class ScrapLogger:
    def __init__(self, memberName):
        Path(os.getcwd() + '/LOG').mkdir(parents=True, exist_ok=True)
        Path(os.getcwd() + '/LOG/ERROR').mkdir(parents=True, exist_ok=True)
        Path(os.getcwd() + '/LOG/COMPLETE').mkdir(parents=True, exist_ok=True)

        errLogName = os.getcwd() + '/LOG/ERROR/' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + memberName + '.log'
        self.errlog = logging.getLogger(memberName + 'errlog')
        self.errlog.setLevel(logging.ERROR)
        self.errlog.addHandler(logging.FileHandler(errLogName))
        
        infoLogName = os.getcwd() + '/LOG/COMPLETE/' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + memberName + '.log'
        self.infolog = logging.getLogger(memberName + 'infolog')
        self.infolog.setLevel(logging.INFO)
        self.infolog.addHandler(logging.FileHandler(infoLogName))

    def writeErrorlog(self, title, content):
        self.errlog.error(title + ' : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.errlog.error(content)
        self.errlog.error('----------------------------------------')

    def writeProcesslog(self, title, content):
        self.infolog.info(title + ' : ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.infolog.info(content)
        self.infolog.info('----------------------------------------')     
