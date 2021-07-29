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
        self.logger = logging.getLogger(memberName + 'Logger')
        self.logger.setLevel(logging.ERROR)
        self.logger.addHandler(logging.FileHandler(errLogName))
        
    def writeErrorlog(self, title, content):
        self.logger.error(title + ' : ' + datetime.datetime.now().strftime('%Y-%m%d %H:%M:%S'))
        self.logger.error(content)
        self.logger.error('----------------------------------------')
        
