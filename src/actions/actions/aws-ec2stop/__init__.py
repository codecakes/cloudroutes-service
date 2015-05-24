#!/usr/bin/python
######################################################################
# Cloud Routes Bridge
# -------------------------------------------------------------------
# Actions Module
######################################################################

import boto.ec2
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
        return actionEC2(redata, jdata, logger)
    else:
        return None


def actionEC2(redata, jdata, logger):
    ''' Perform EC2 Actions '''
    try:
        conn = boto.ec2.connect_to_region(
            redata['data']['region'],
            aws_access_key_id=redata['data']['aws_access_key'],
            aws_secret_access_key=redata['data']['aws_secret_key'])
        try:
            conn.stop_instances(instance_ids=[redata['data']['instance_id']])
            return True
        except:
            return False
    except:
        line = "aws-ec2stop: Could not connect to AWR for monitor %s" % jdata[
            'cid']
        logger.info(line)
        return False
