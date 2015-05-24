#!/usr/bin/python
######################################################################
# Cloud Routes Actioner
# -------------------------------------------------------------------
# Actions Module
######################################################################

import requests
import json
import time


def action(**kwargs):
    ''' This method is called to action a reaction '''
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    run = True
    # Check for Trigger
    if redata['trigger'] > jdata['failcount']:
        run = False

    # Check for lastrun
    checktime = time.time() - float(redata['lastrun'])
    if checktime < redata['frequency']:
        run = False

    if redata['data']['call_on'] not in jdata['check']['status']:
        run = False

    if run:
        return call(redata, jdata, logger)
    else:
        return None


def call(redata, jdata, logger):
    ''' Perform actual call '''
    url = "https://api.commando.io/v1/recipes/%s/execute" % redata['data']['recipe_id']
    success = None
    groups = redata['data']['group_id'].split(",")
    for group in groups:
        payload = {
            'groups' : [ group ],
            'halt_on_stderr' : redata['data']['halt_on_stderr'],
            'notes' : 'Execution called by runbook.io'
        }
        try:
            req = requests.post(
                url,
                data=payload,
                auth=(redata['data']['user'], redata['data']['apikey']),
                timeout=3.0,
                verify=False)
        except:
            return False
        if req.status_code == 202:
            line = "commando-group: Reqeust to %s sent for monitor %s - Successful - %d" % (url, jdata['cid'], req.status_code)
            logger.info(line)
        else:
            line = "commando-group: Request to %s sent for monitor %s - False - %d" % (url, jdata['cid'], req.status_code)
            logger.info(line)
            line = "commando-group: Debug Reply %s" % req.text
            logger.debug(line)
            success = False
    if success is None:
        success = False
    return success
