#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
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
        return callDO(redata, jdata, logger)
    else:
        return None


def callDO(redata, jdata, logger):
    ''' Perform actual call '''
    headers = {'Authorization': 'Bearer ' + redata['data']['apikey'],
               'Content-Type': 'application/json'}
    url = "https://api.digitalocean.com/v2/droplets/%s/actions" % str(
        redata['data']['dropletid'])
    msg = {"type": "reboot"}
    payload = json.dumps(msg)
    try:
        req = requests.post(
            url, timeout=3.0, data=payload, headers=headers, verify=True)
    except:
        return False
    if req.status_code >= 200 and req.status_code < 300:
        line = "digitalocean-reboot: Reqeust to %s sent for monitor %s - Successful" % (url, jdata['cid'])
        logger.info(line)
        return True
    else:
        line = "digitalocean-reboot: Request to %s sent for monitor %s - False" % (url, jdata['cid'])
        logger.info(line)
        return False
