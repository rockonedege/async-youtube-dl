# coding=utf-8
__author__ = 'ttan'
import logging
import sys
from pathlib import Path

def init(root = 'temp', console_log_level = logging.DEBUG, file_log_level = logging.INFO):


  datefmt='%d/%b/%Y %H:%M:%S'

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  # logger.setLevel(logging.INFO)

  # create console handler with a higher log level
  # http://stackoverflow.com/questions/1383254/logging-streamhandler-and-standard-streams

  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.DEBUG)
  ch.setFormatter(logging.Formatter("[%(levelname)s|%(filename)s|%(asctime)s|%(thread)d]:  %(message)s", datefmt=datefmt))
  logger.addHandler(ch)


  LOG_ROOT = Path(__file__).absolute().parent/root
  LOG_ROOT.mkdir(exist_ok=True, parents=True)

  LOG_FILE = LOG_ROOT/'app.log'

  fh = logging.FileHandler(str(LOG_FILE), encoding='utf-8')
  fh.setLevel(console_log_level)
  fh.setFormatter(logging.Formatter("[%(levelname)s|%(asctime)s|%(filename)s]:  %(message)s", datefmt=datefmt))
  logger.addHandler(fh)
