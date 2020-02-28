#!/usr/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/csc675-775-03-fall2019-07/application/")

from AirportApp import app as application
application.secret_key = 'asdsafasfad'
