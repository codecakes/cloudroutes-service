#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import time
import json

def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    rdb = kwargs['rdb']
    r_server = kwargs['r_server']
    logger = kwargs['logger']
    return logit(redata, jdata, rdb, r_server, logger)


def logit(redata, jdata, rdb, r_server, logger):
    ''' This method will be called to log monitor transaction history '''
    transaction = {
        'cid': jdata['cid'],
        'type': "reaction",
        'rid': redata['id'],
        'starttime': jdata['time_tracking']['control'],
        'zone': jdata['zone'],
        'uid': jdata['uid'],
        'url': jdata['url'],
        'trigger': redata['trigger'],
        'lastrun': redata['lastrun'],
        'rstatus': "executed",
        'status': jdata['check']['status'],
        'method': jdata['check']['method'],
        'time': time.time(),
        'cacheonly': redata['cacheonly'],
        'name': redata['name']
    }
    success = False
    cacheonly = False
    if redata['reaction_return'] is True:
        transaction['rstatus'] = 'Executed'
    elif redata['reaction_return'] is None:
        transaction['rstatus'] = 'Skipped'
    elif redata['reaction_return'] is False:
        transaction['rstatus'] = 'False'
    else:
        transaction['rstatus'] = 'Unknown'

    # Try to set rethinkdb first
    try:
        results = r.table('history').insert(transaction).run(rdb)
        if results['inserted'] == 1:
            success = True
            cacheonly = False
        else:
            success = False
    except (RqlDriverError, RqlRuntimeError) as e:
        success = False
        cacheonly = True
        line = "logit-reaction: RethinkDB is inaccessible cannot log %s, sending to redis" % jdata['cid']
        logger.info(line)
        line = "logit-reaction: RethinkDB Error: %s" % e.message
        logger.info(line)
        try:
            # Then set redis cache
            ldata = json.dumps(transaction)
            r_server.sadd("history", ldata)
            success = True
        except:
            line = "logit-reaction: Redis is inaccessible cannot log %s, via redis" % jdata['cid']
            logger.info(line)
            success = False
    return success
