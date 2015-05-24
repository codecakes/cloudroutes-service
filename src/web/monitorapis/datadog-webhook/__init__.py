######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Datadog Monitor API modules
######################################################################

import json


def webCheck(request, monitor, urldata, rdb):
    ''' Process the webbased api call '''
    replydata = {
        'headers': {'Content-type': 'application/json'}
    }
    rdata = {}
    jdata = request.json

    # Adding this because i'm lazy and didn't feel like modifying all the
    # references
    cid = urldata['cid']
    atype = urldata['atype']

    # Delete the Monitor
    monitor.get(cid, rdb)
    if jdata['check_key'] == monitor.url and atype == monitor.ctype:
        if "Triggered" in jdata['title']:
            monitor.healthcheck = "false"
            result = monitor.webCheck(rdb)
            if result:
                rdata['result'] = "success"
            else:
                rdata['result'] = "failed"
        elif "No data" in jdata['title']:
            monitor.healthcheck = "false"
            result = monitor.webCheck(rdb)
            if result:
                rdata['result'] = "success"
            else:
                rdata['result'] = "failed"
        elif "Recovered" in jdata['title']:
            monitor.healthcheck = "true"
            result = monitor.webCheck(rdb)
            if result:
                rdata['result'] = "success"
            else:
                rdata['result'] = "failed"
        else:
            rdata['result'] = "unknown request"
    else:
        rdata['result'] = "invalid key"

    replydata['data'] = json.dumps(rdata)

    return replydata
