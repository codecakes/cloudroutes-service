#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import stathat
import time

def action(**kwargs):
    ''' This method is called to action a reaction '''
    # This method can be used for legacy reactions that have
    # a different function based on true/false
    logger = kwargs['logger']
    if "false" in kwargs['jdata']['check']['status']:
        return false(kwargs['redata'], kwargs['jdata'],
            kwargs['rdb'], kwargs['r_server'], logger)
    if "true" in kwargs['jdata']['check']['status']:
        return true(kwargs['redata'], kwargs['jdata'],
            kwargs['rdb'], kwargs['r_server'], logger)

def false(redata, jdata, rdb, r_server, logger):
    ''' This method will be called when a monitor has false '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'true':
        run = False

    if run:
        if redata['data']['continuous'] == "True":
            callStathat(redata, jdata, logger)
            return True
        else:
            if jdata['check']['prev_status'] != "false":
                callStathat(redata, jdata, logger)
                return True
            else:
                line = "stathat: Skipping stathat call as monitor %s was previously false" % jdata['cid']
                logger.info(line)
                return None
    else:
        return None


def true(redata, jdata, rdb, r_server, logger):
    ''' This method will be called when a monitor has passed '''
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] == 'false':
        run = False

    if run:
        if redata['data']['continuous'] == "True":
            callStathat(redata, jdata, logger)
            return True
        else:
            if jdata['check']['prev_status'] != "true":
                callStathat(redata, jdata, logger)
                return True
            else:
                line = "stathat: Skipping stathat call as monitor %s was previously true" % jdata['cid']
                logger.info(line)
                return None
    else:
        return None


# Local

def callStathat(redata, jdata, logger):
    ''' Actually perform the stathat call '''
    if redata['data']['stat_type'] == "count":
        stathat.ez_count(
            redata['data']['ez_key'],
            redata['data']['stat_name'], redata['data']['value'])
        line = "stathat: Sent stathat counter for monitor %s" % jdata['cid']
        logger.info(line)
    elif redata['data']['stat_type'] == "value":
        stathat.ez_value(
            redata['data']['ez_key'],
            redata['data']['stat_name'], redata['data']['value'])
        line = "stathat: Sent stathat value for monitor %s" % jdata['cid']
        logger.info(line)
    else:
        line = "stathat: Unknown stat type defined in reaction %s" % redata[
            'id']
        logger.error(line)
