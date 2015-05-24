#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import requests
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
        return call_linode(redata, jdata, logger)
    else:
        return None


def get_current_linodes(redata):
    ''' Perform actual call '''
    url = 'https://api.linode.com/'
    params = {
        "api_action": "linode.list",
        "api_key": str(redata['data']['api_key'])
    }
    try:
        req = requests.post(url, timeout=10.0, data=params, verify=True)
    except:
        return False
    return len(req.json()["DATA"])


def call_linode(redata, jdata, logger):
    ''' Perform actual call '''
    url = 'https://api.linode.com/'
    if int(redata['data']['upper_limit']) > get_current_linodes(redata):
        params = {
            "api_action": "linode.create",
            "DatacenterID": int(redata['data']['datacenter_id']),
            "PlanID": int(redata['data']['plan_id']),
            "api_key": str(redata['data']['api_key'])
        }
        try:
            req = requests.post(url, timeout=10.0, data=params, verify=True)
        except Exception as e:
            line = 'linode-create: Request to {0} sent for monitor {1} - \
                False (error making API call: {2})'.format(url, jdata['cid'], e)
            logger.info(line)
            return False
        if req.status_code >= 200 and req.status_code < 300:
            if len(req.json()['ERRORARRAY']) > 0:
                line = 'linode-create: Request to {0} sent for monitor {1} - \
                    False'.format(url, jdata['cid'])
                logger.info(line)
                return False
            else:
                line = 'linode-create: Request to {0} sent for monitor {1} - \
                    Successful'.format(url, jdata['cid'])
                logger.info(line)
            return True
    else:
        line = 'linode-create: Request to {0} sent for monitor {1} - \
            Skipped (upper_limit < current linodes)'.format(url, jdata['cid'])
        logger.info(line)
        return None
