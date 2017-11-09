#-*-coding:utf-8-*- 
__author__ = 'kerberos'
__date__ = '2017.6.20'

import os
import sys
from scrapy.cmdline import execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy","crawl","tieba"])
