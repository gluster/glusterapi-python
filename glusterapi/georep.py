import httplib
import json
import socket
import requests

from glusterapi.common import BaseAPI, validate_volume_name
from glusterapi.exceptions import GlusterApiError
from glusterapi.exceptions import GlusterApiInvalidInputs


def extract_volume_ID(remotehost, remoteport, remotevol, headers):
    if remoteport not in range(1, 65535):
        raise GlusterApiInvalidInputs("Incorrect port")
    try:
        socket.inet_aton(remotehost)
    except socket.error:
        raise GlusterApiInvalidInputs("Invalid Remote host IP Address")
    validate_volume_name(remotevol)
    client_url = "http://"+ remotehost + ":" + remoteport + "/v1/volumes"
    try:
        resp = requests.get(client_url, headers=headers)
    except ValueError:
        raise GlusterApiInvalidInputs("Invalid URL: %s" % client_url)
    if resp.status_code == 200:
        remotevolid = resp.json().get(remotevol)
    else:
        raise GlusterApiError("Remote volume doesn't exist")
    return remotevolid

def get_vol_IDs(self, mastervol, remotevol, remotehost):
    georep_status_url = "/v1/geo-replication"
    try:
        allsessions = requests.get(self, georep_status_url)
    except ValueError:
        raise GlusterApiError("No active geo-replication sessions")
    for s in allsessions:
        if s.MasterID == mastervol:
            mastervolid = s.MasterID
    if mastervolid is None:
        raise GlusterApiInvalidInputs("Master volume doesn't exist")

    for s in allsessions:
        if s.RemoteVol == remotevol:
            for host in s.RemoteHosts:
                if host.Hostname == remotehost:
                    remotevolid = s.RemoteID
    if remotevolid is None:
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
        volumes_url = "/v1/volumes/"
        resp = self._get(self, volumes_url)
        try:
            mastervolid = resp.get(mastervol)
        except ValueError:
            raise GlusterApiError("Master volume %s doesn't exist" % mastervol)
        self.__init__(remote_endpoint, remote_endpoint_user,
                      remote_endpoint_secret, remote_endpoint_verify)
        headers = self._set_token_in_header('GET', volumes_url)
        remotevolid = extract_volume_ID(remotehost, remoteport, remotevol, headers)
        url = "/v1/geo-replication/%s/%s" % (mastervolid, remotevolid)
        req = {
            "mastervolume": mastervol,
            "remotehost": remotehost,
            "remoteport": remoteport,
            "remotevolume": remotevol,
            "remoteuser": remoteuser
        }
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
        mastervolid, remotevolid = get_vol_IDs(mastervol, remotevol, remotehost)
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
        mastervolid, remotevolid = get_vol_IDs(mastervol, remotevol, remotehost)
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
        mastervolid, remotevolid = get_vol_IDs(mastervol, remotevol, remotehost)
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
            mastervolid, remotevolid = get_vol_IDs(mastervol, remotevol, remotehost)
            url = "/v1/geo-replication/%s/%s" % (mastervolid, remotevolid)
        else:
            url = "/v1/geo-replication"
        return self._handle_request(self._get, httplib.OK, url, None)
