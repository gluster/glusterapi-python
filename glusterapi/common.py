
import datetime
import hashlib
from uuid import UUID

import jwt
import requests

from glusterapi.exceptions import GlusterApiError
from glusterapi.exceptions import GlusterApiInvalidInputs


def validate_uuid(brick_id, version=4):
    try:
        UUID(brick_id, version=version)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False
    return True

def validate_peer_id(peerid):
    if validate_uuid(peerid) is False:
        raise GlusterApiInvalidInputs("Invalid peer id specified")

def validate_volume_name(vol_name):
    vol_name = vol_name.strip()
    if not vol_name:
        raise GlusterApiInvalidInputs("Volume name cannot be empty")


class BaseAPI(object):
    def __init__(self, endpoint='http://127.0.0.1:24007', user=None,
                 secret=None, verify=False):
        self.base_url = endpoint
        self.user = user
        self.secret = secret
        self.verify = verify

    def set_token_in_header(self, method, uri, headers=None):

        if self.user is None or self.secret is None:
            return None
        if headers is None:
            headers = dict()
        claims = dict()
        claims['iss'] = self.user

        # Issued at time
        claims['iat'] = datetime.datetime.utcnow()

        # Expiration time
        claims['exp'] = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=1)

        # URI tampering protection
        val = b'%s&%s' % (method.encode('utf8'), uri.encode('utf8'))
        claims['qsh'] = hashlib.sha256(val).hexdigest()

        token = jwt.encode(claims, self.secret, algorithm='HS256')
        headers['Authorization'] = b'bearer ' + token

        return headers

    def _get(self, url, param=None):
        headers = self.set_token_in_header('GET', url)
        return requests.get(self.base_url + url, headers=headers,
                            verify=self.verify, params=param)

    def _post(self, url, data):
        headers = self.set_token_in_header('POST', url)
        return requests.post(self.base_url + url, data=data, headers=headers,
                             verify=self.verify)

    def _delete(self, url, data):
        headers = self.set_token_in_header('DELETE', url)
        return requests.delete(self.base_url + url, data=data, headers=headers,
                               verify=self.verify)

    def _put(self, url, data):
        headers = self.set_token_in_header('PUT', url)
        return requests.put(self.base_url + url, data=data, headers=headers,
                            verify=self.verify)

    @staticmethod
    def _handle_request(func, expected_status_code, *args, **kwargs):
        resp = func(*args, **kwargs)
        if resp.status_code != expected_status_code:
            # TODO: Add additional error details
            raise GlusterApiError()

        if resp.status_code == 204:
            return resp.status_code, {}

        return resp.status_code, resp.json()
