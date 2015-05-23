#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'dominikmajda'

from webcrawlers.royters import RoytersManager
from webcrawlers.telegraph import TelegraphManager
from webcrawlers.zarohedge import ZeroHedgeManager
from webcrawlers.thestreet import TheStreetManager
from time import time
from datetime import datetime
import atexit


######################
#      Variables     #
######################

LOG_NAME = "log" + str(datetime.now())
DUMP_FOLDER = "dump/"
STOP_CONDITION = 30000
i = 13446;

# Crate all sites manager

telegraph = datetime(2014, 11, 6, 12, 44, 57, 557000)
routers = datetime(2015, 4, 28, 12, 44, 57, 557000)
#
telegraphManager = TelegraphManager(date=telegraph)
roytersManager = RoytersManager(date=routers)
# telegraphManager = TelegraphManager()
# roytersManager = RoytersManager()
zerohedgeManager = ZeroHedgeManager()
thestreetManager = TheStreetManager()

# Start logging
log = open(LOG_NAME, 'w')

######################
#       Methods      #
######################

def compare_dates(date1, date2):
    if date1.year==date2.year and date1.month==date2.month and date1.day==date2.day:
        return True
    else:
        return False

def log_url_failre(crawler):
    log.write("Failure at: " + crawler.url + "\n")

def time_log():
    print "\n" + str(i) + ' articles in ' + str(time()-start_time) + "\n\n"
    log.write("\n" + str(i) + ' articles in ' + str(time()-start_time) + "\n\n")

def close_all():
    log.write("Closing state:\n")

    # Dump crawlers state
    log.write("Telegraph date: " + str(telegraphManager.date) + "\n")
    log.write("ZeroHedge date: " + str(zerohedgeManager.date) + "\n")
    log.write("Routers date: " + str(roytersManager.date) + "\n")
    log.write("TheStreet page: " + str(thestreetManager.page) + "\n")

    log.close()

def dump(manager, prefix):
    global i
    crawler = manager.get_next_link()
    if crawler.dump(DUMP_FOLDER + str(i) + prefix, verbose=True, add_links=True):
        # Increase stop condition
        i+=1
    else:
        log_url_failre(crawler)


######################
# It all starts here #
######################

# Make time start - for testing purpose
start_time = time()
crawlers_date = datetime.now()

# Create log file and exit hook
atexit.register(close_all)
log = open(LOG_NAME, 'w')

# Start here
while (i<STOP_CONDITION):

    dump(telegraphManager, "_telegraph")
    dump(roytersManager, "_routers")
    # dump(zerohedgeManager, "_zero")
    # dump(thestreetManager, "_thestreet")

    # Testing time
    if i%100==0:
        time_log()


