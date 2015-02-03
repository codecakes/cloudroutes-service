#!/usr/bin/python
"""HTTP POST monitor."""

import re
import requests
import cStringIO

# currently the http get size limit is 2MB
# change the following function to allow for per user, size limit
def get_max_size():
    return 2*1024*1024


_HTTP_REQUEST_TIMEOUT = 10.0  # in seconds


# TODO: There should be a common lib where these utility functions can be
# stored. For now, we duplicate code :-(
def ParseHeaders(headers_str):
    headers = {}
    for header in str.splitlines(str(headers_str)):
        header = header.strip()
        # Ignore empty lines
        if not header:
            continue
        key, value = header.split(':')
        key = key.strip()
        value = value.strip()
        assert key
        assert value
        headers[key] = value
    return headers


def _check(jdata):
    url = jdata['data']['url']
    host = jdata['data']['host']
    payload = jdata['data']['payload'] or ''
    extra_headers = jdata['data']['extra_headers'] or ''
    status_codes = jdata['data']['status_codes'] or []
    response_regex = jdata['data']['response_regex'] or ''
    response_headers = jdata['data']['response_headers'] or ''
    assert url, "URL field not present"
    assert host, "Host field not present"
    headers = ParseHeaders(extra_headers)
    headers['host'] = host
    try:
        r = requests.post(url, timeout=_HTTP_REQUEST_TIMEOUT, headers=headers,
                          data=payload, verify=False, stream=True)
    except Exception as e:
        assert e, "Error making request"
        return False
    stream = cStringIO.StringIO()
    length = 0
    for chunk in r.iter_content(8192, decode_unicode=False):
        stream.write(chunk)
        length += len(chunk)
        if length > get_max_size():
            break
    retext = stream.getvalue()
    retext = unicode(retext)
    stream.close()
    status_codes = [int(code) for code in status_codes]
    assert not status_codes or \
        r.status_code in status_codes, "Invalid HTTP Response status code."
    assert re.search(response_regex, retext), "Response doesn't match"
    response_headers = ParseHeaders(response_headers)
    for header_name, header_value in response_headers.iteritems():
        assert header_name in r.headers, \
            "Header %s not found in response" % header_name
        assert header_value.lower() == r.headers[header_name].lower(), \
            "Header value for %s doesn't match" % header_name
    r.close()
    return True


def check(**kwargs):
    jdata = kwargs['jdata']
    logger = kwargs['logger']
    try:
        return _check(jdata)
    except Exception, e:
        logger.warning('http-post: {cid} - {message}'.format(
            cid=jdata['cid'], message=e.message))
        return False
