import sys
import os
from argparse import ArgumentParser
from datetime import datetime, timedelta
from urllib.parse import urlparse
import jwt
import hashlib

def Auth(user, url, method):
    url = "/v1" + url
    secret_file = "/var/lib/glusterd2/auth"
    try:
        with open(secret_file) as f:
            secret = f.read()
    except IOError as err:
        sys.stderr.write("Unable to open secret file\n")
        sys.stderr.write("Error: %s\n" % err)
        sys.exit(1)
    claims = dict()
    claims['iss'] = user
    claims['iat'] = datetime.utcnow()
    claims['exp'] = datetime.utcnow() + timedelta(seconds=100)
    qsh = '%s&%s' % (method, url)
    qsh = qsh.encode('utf8')
    claims['qsh'] = hashlib.sha256(qsh).hexdigest()
    token = jwt.encode(claims, secret, algorithm='HS256')
    header = b'bearer ' + token
    head_com = header.decode()
    return head_com
