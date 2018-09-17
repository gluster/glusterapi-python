"""
Test module.

The module tests for peer functionalities.
"""
from urlparse import urlparse
import json
import pytest

from glusterapi import Client


class GlusterdConfig(object):
    """GlusterdConfig Class to test the bindings."""

    #TODO: Add setupclass() and teardownclass() functions
    hostname = ''
    node_list = []
    node_peerid_map = {}

    @classmethod
    def set_node_list(cls, node):
        """Set the node list."""
        cls.node_list.append(node)

    @classmethod
    def set_peer_id(cls, node, resp_id):
        """Set the peer id."""
        cls.node_peerid_map[node] = resp_id

    @classmethod
    def get_peer_id(cls, node):
        """Retrieve the peer id."""
        return cls.node_peerid_map.get(node, "")

    @property
    def get_node_list(self):
        """Retrieve the node list."""
        return self.node_list


Peer = GlusterdConfig()


@pytest.fixture(scope='module')
def gd2client():
    """Initialise all the class member variables."""
    config = json.loads(open('config.json').read())
    endpoint = config["glusterd2"]["endpoint"]
    user = config["glusterd2"]["user"]
    secret = config["glusterd2"]["secret"]
    verify = config["glusterd2"]["verify"]

    # Check for controller node and skip it for probing.
    for node in config["peer"]:
        if node["hostname"].split(':')[0] == urlparse(endpoint).netloc.split(':')[0]:
            continue
        Peer.set_node_list(node["hostname"])
    return Client(endpoint=endpoint, user=user, secret=secret, verify=verify)


def test_peer_add(gd2client):
    """Test for peer addition."""
    node_list = Peer.get_node_list
    for node in node_list:
        _, resp = gd2client.peer_add(host=node)
        # store  peerID of nodes in class variable
        Peer.set_peer_id(node, resp['id'])
        assert bool(resp)


def test_peer_status(gd2client):
    """Test for peer status."""
    status, _ = gd2client.peer_status()
    assert status == 200


def test_peer_remove(gd2client):
    """Test for peer removal."""
    node_list = Peer.get_node_list
    for node in node_list:
        _, resp = gd2client.peer_remove(peerid=Peer.get_peer_id(node))
        assert not bool(resp)


def test_georep_create_delete(gd2client):
    """Test for georep session operations."""
    m_bricks = []
    _, resp = gd2client.peer_status()
    peer_id = resp[0]["id"]
    for i in range(3):
        temp_path = "/usr/local/var/lib/glusterd2/bricks/brick" + str(i)
        brick_path = peer_id + ":" + temp_path
        m_bricks.append(brick_path)
    mastervol = "testmastervol"
    gd2client.volume_create(m_bricks, volume_name=mastervol,
                                        transport="tcp", replica=0, disperse=0,
                                        disperse_data=0, disperse_redundancy=0,
                                        arbiter=0, force=True, options=None,
                                        metadata=None)
    gd2client.volume_start("testmastervol", False)
    r_bricks = []
    for i in range(3, 5):
        temp_path = "/usr/local/var/lib/glusterd2/bricks/brick" + str(i)
        brick_path = peer_id + ":" + temp_path
        r_bricks.append(brick_path)
    config = json.loads(open('config.json').read())
    georep_endpoint = config["glusterd2"]["endpoint"]
    georep_user = config["glusterd2"]["user"]
    georep_secret = config["glusterd2"]["secret"]
    georep_verify = config["glusterd2"]["verify"]
    remotevol="testremotevol"
    client=Client(endpoint=georep_endpoint, user=georep_user, secret=georep_secret, verify=georep_verify)
    client.volume_create(r_bricks, volume_name=remotevol,
                                        transport="tcp", replica=0, disperse=0,
                                        disperse_data=0, disperse_redundancy=0,
                                        arbiter=0, force=True, options=None,
                                        metadata=None)
    client.volume_start("testremotevol", False)
    remotehostinfo = urlparse(georep_endpoint).netloc.split(':')
    remotehost = remotehostinfo[0]
    remoteport = remotehostinfo[1]
    _, resp = gd2client.georep_create(mastervol, remotehost, remoteport, remotevol,
                                      remoteuser="root", remote_endpoint="",
                                      remote_endpoint_user=client.user,
                                      remote_endpoint_secret=client.secret,
                                      remote_endpoint_verify=client.verify)

    # start geo-rep session
    _, _ = gd2client.georep_start(mastervol, remotehost, remotevol,
                                  force=False)

    # stop geo-rep session
    _, _ = gd2client.georep_stop(mastervol, remotehost, remotevol,
                                 force=False)

    # get status of geo-rep session
    _, _ = gd2client.georep_status(mastervol, remotehost, remotevol)

    # delete geo-rep session
    _, _ = gd2client.georep_delete(mastervol, remotehost, remotevol,
                                   force=False)

    # delete the volumes
    _, _ = gd2client.volume_delete("testmastervol")
    _, _ = gd2client.volume_delete("testremotevol")

