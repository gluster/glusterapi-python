import httplib
import json
import socket
import requests

from glusterapi.common import BaseAPI, validate_volume_name
from glusterapi.exceptions import GlusterApiError
from glusterapi.exceptions import GlusterApiInvalidInputs


def extract_volume_ID(remotehost, remoteport, remote_endpoint, remotevol, headers):
    if int(remoteport) not in range(1, 65535):
        raise GlusterApiInvalidInputs("Incorrect port")
    try:
        socket.inet_aton(remotehost)
    except socket.error:
        raise GlusterApiInvalidInputs("Invalid Remote host IP Address")
    validate_volume_name(remotevol)
    if not remote_endpoint:
        client_url = "http://"+ remotehost + ":" + remoteport + "/v1/volumes"
    else:
        client_url = remote_endpoint + "/v1/volumes"
    try:
        resp = requests.get(client_url, headers=headers)
    except ValueError:
        raise GlusterApiInvalidInputs("Invalid URL: %s" % client_url)
    if resp.status_code == 200:
        try:
            remotevolid = resp.json()[1].get('id')
        except ValueError:
            raise GlusterApiError("Remote volume doesn't exist")
    else:
        raise GlusterApiError("Invalid Url Response")
    return remotevolid

def get_vol_IDs(self, mastervol, remotevol, remotehost):
    georep_status_url = "/v1/geo-replication"
    try:
        allsessions = self._get(georep_status_url)
    except ValueError:
        raise GlusterApiError("No active geo-replication sessions")
    mastervolid = ""
    remotevolid = ""
    for s in allsessions.json():
        if s.get("master_volume") == mastervol:
            mastervolid = s.get("master_volume_id")
    if mastervolid == "":
        raise GlusterApiInvalidInputs("Master volume doesn't exist")

    for s in allsessions.json():
        if s.get("remote_volume") == remotevol:
            for host in s.get("remote_hosts"):
                if host.get("host") == remotehost:
                    remotevolid = s.get("remote_volume_id")
    if remotevolid == "":
        raise GlusterApiInvalidInputs("Remote volume doesn't exist")
    return mastervolid, remotevolid


class GeorepApis(BaseAPI):
    def georep_create(self, mastervol, remotehost, remoteport, remotevol,
                      remoteuser="root",
                      remote_endpoint="",
                      remote_endpoint_user=None,
                      remote_endpoint_secret=None,
                      remote_endpoint_verify=False):
        """
        Create Geo-replication Session.

        :param mastervol: (string) Master volume name
        :param remotehost: (string) Remote host
        :param remoteport: (string) Remote port
        :param remotevol: (string) Remote volume
        :param remoteuser: (string) Remote user
        :raises: GlusterAPIError or GlusterApiInvalidInputs on failure
        """
        validate_volume_name(mastervol)
        volumes_url = "/v1/volumes/"+str(mastervol)
        resp = self._get(volumes_url)
        peer_id = ""
        peers_url = "/v1/peers"
        peers_resp = self._get(peers_url)
        for _, peer in enumerate(peers_resp.json()):
            if str(peer.get("peer-addresses")[0]).split(":")[0] == remotehost:
                peer_id = peer.get("id")
        remotehostreq = []
        peer_req = {
            "peerid": peer_id,
            "host": remotehost
        }
        remotehostreq.append(peer_req)
        try:
            mastervolid = resp.json().get('id')
        except ValueError:
            raise GlusterApiError("Master volume %s doesn't exist" % mastervol)
        # Save old credentials for reinitialization of client
        old_endpoint = self.base_url
        old_user = self.user
        old_secret = self.secret
        old_verify = self.verify
        # Initialize session for remote cluster
        self.__init__(remote_endpoint, remote_endpoint_user,
                      remote_endpoint_secret, remote_endpoint_verify)
        headers = self.set_token_in_header('GET', volumes_url)
        remotevolid = extract_volume_ID(remotehost, remoteport, remote_endpoint, remotevol, headers)
        url = "/v1/geo-replication/%s/%s" % (mastervolid, remotevolid)
        req = {
            "mastervol": mastervol,
            "remotehosts": remotehostreq,
            "remotevol": remotevol,
            "remoteuser": remoteuser
        }
        # Reinitialize the client
        self.__init__(old_endpoint, old_user, old_secret, old_verify)
        return self._handle_request(self._post, httplib.CREATED,
                                    url, json.dumps(req))

    def georep_start(self, mastervol, remotehost, remotevol, force=False):
        """
        Start Geo-replication Session.

        :param mastervol: (string) Master volume name
        :param remotehost: (string) Remote host
        :param remotevol: (string) Remote volume
        :param force: (bool) Start Georep session with Force
        :raises: GlusterAPIError or GlusterApiInvalidInputs on failure
        """
        validate_volume_name(mastervol)
        mastervolid, remotevolid = get_vol_IDs(self, mastervol=mastervol, remotevol=remotevol, remotehost=remotehost)
        url = "/v1/geo-replication/%s/%s/start" % (mastervolid, remotevolid)
        req = {
            "force": force
        }
        return self._handle_request(self._post, httplib.OK,
                                    url, json.dumps(req))

    def georep_stop(self, mastervol, remotehost, remotevol, force=False):
        """
        Stop Geo-replication Session.

        :param mastervol: (string) Master volume name
        :param remotehost: (string) Remote host
        :param remotevol: (string) Remote volume
        :param force: (bool) Stop Georep session with Force
        :raises: GlusterAPIError or GlusterApiInvalidInputs on failure
        """
        validate_volume_name(mastervol)
        mastervolid, remotevolid = get_vol_IDs(mastervol=mastervol, remotevol=remotevol, remotehost=remotehost)
        url = "/v1/geo-replication/%s/%s/stop" % (mastervolid, remotevolid)
        req = {
            "force": force
        }
        return self._handle_request(self._post, httplib.OK,
                                    url, json.dumps(req))

    def georep_delete(self, mastervol, remotehost, remotevol, force=False):
        """
        Delete Geo-replication Session.

        :param mastervol: (string) Master volume name
        :param remotehost: (string) Remote host
        :param remotevol: (string) Remote volume
        :param force: (bool) Delete Georep session with Force
        :raises: GlusterAPIError or GlusterApiInvalidInputs on failure
        """
        validate_volume_name(mastervol)
        mastervolid, remotevolid = get_vol_IDs(mastervol=mastervol, remotevol=remotevol, remotehost=remotehost)
        url = "/v1/geo-replication/%s/%s" % (mastervolid, remotevolid)
        req = {
            "force": force
        }
        return self._handle_request(self._delete, httplib.NO_CONTENT,
                                    url, json.dumps(req))

    def georep_set(self, mastervol, remotehost, remotevol,
                   optname, optvalue, remoteuser="root"):
        """
        Set Geo-replication Session Option

        :param mastervol: (string) Master Volume Name
        :param remotehost: (string) Remote Host
        :param remotevol: (string) Remote Volume
        :param remoteuser: (string) Remote User
        :param optname: (string) Option Name
        :param optvalue: (string) Option Value
        :raises: GlusterAPIError or failure
        """
        pass

    def georep_get(self, mastervol, remotehost, remotevol,
                   remoteuser="root", optname=None):
        """
        Get Geo-replication Session Option

        :param mastervol: (string) Master Volume Name
        :param remotehost: (string) Remote Host
        :param remotevol: (string) Remote Volume
        :param remoteuser: (string) Remote User
        :param optname: (string) Option name
        :raises: GlusterAPIError or failure
        """
        pass

    def georep_reset(self, mastervol, remotehost,
                     remotevol, optname, remoteuser="root"):
        """
        Reset Geo-replication Session Option

        :param mastervol: (string) Master Volume Name
        :param remotehost: (string) Remote Host
        :param remotevol: (string) Remote Volume
        :param optname: (string) Option name
        :param remoteuser: (string) Remote User
        :raises: GlusterAPIError or failure
        """
        pass

    def georep_checkpoint(self, mastervol, remotehost,
                          remotevol, remoteuser="root"):
        """
        Set Geo-replication Session Checkpoint

        :param mastervol: (string) Master Volume Name
        :param remotehost: (string) Remote Host
        :param remotevol: (string) Remote Volume
        :param remoteuser: (string) Remote User
        :raises: GlusterAPIError or failure
        """
        return self.georep_set(mastervol, remotehost, remotevol,
                               "checkpoint", "now", remoteuser)

    def georep_status(self, mastervol=None, remotehost=None, remotevol=None):
        """
        Geo-replication Session Status.

        :param mastervol: (string) Master volume name
        :param remotehost: (string) Remote host
        :param remotevol: (string) Remote volume
        :raises: GlusterAPIError or GlusterApiInvalidInputs on failure
        """
        if mastervol and remotevol:
            validate_volume_name(mastervol)
            mastervolid, remotevolid = get_vol_IDs(self, mastervol=mastervol, remotevol=remotevol, remotehost=remotehost)
            url = "/v1/geo-replication/%s/%s" % (mastervolid, remotevolid)
        else:
            url = "/v1/geo-replication"
        return self._handle_request(self._get, httplib.OK, url, None)
