######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Papertrail Webhook Monitor module
######################################################################

import json


def webCheck(request, monitor, urldata, rdb):
    ''' Process the webbased api call '''
    replydata = {
        'headers': {'Content-type': 'application/json'}
    }
    rdata = {}

    # Ensure data matches a logentries post and not just random requests
    if request.method == "POST" and "payload" in request.form:
        request_verify = True
    else:
        request_verify = False

    # Verify and then send web check Monitor
    monitor.get(urldata['cid'], rdb)
    # Verify check_key and api_type matches monitor for cid
    if urldata['check_key'] == monitor.url and \
            urldata['atype'] == monitor.ctype:
        # Ensure action is false or true
        if urldata['action'] == "healthy":
            action = "true"
        elif urldata['action'] == "failed":
            action = "false"
        else:
            action = urldata['action']
        if action == "false" or action == "true":
            # Set new status (not saved until monitor.webCheck is performed
            monitor.healthcheck = action
            if request_verify is True:
                # Send web based health check to dcqueues
                result = monitor.webCheck(rdb)
            else:
                result = False
            if result:
                rdata['result'] = "success"
            else:
                rdata['result'] = "failed"
        else:
            rdata['result'] = "failed"
    else:
        rdata['result'] = "invalid key"
    replydata['data'] = json.dumps(rdata)
    return replydata
