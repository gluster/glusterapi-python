Peer and Volume management APIs example usage:
```
 import glusterapi
 from glusterapi.api.client import Client
 client = Client()
 
 # The method names and parameters depend on the yaml/json api definition
 # The api methods being used below are called from the library obtained from running generate.sh using api.json in peer_volume_api_json directory 
 
 # Add a peer to the TSP
 client.add_peer(add={'addresses':['192.168.56.102']})
 
 # Get peer information
 client.get_peer('0c5bc279-397a-4535-be32-301c16dbbc69')
 
 # Get information of all peers in the TSP
 client.get_peers()
 
 # Edit peer information
 client.edit_peer('0c5bc279-397a-4535-be32-301c16dbbc69', edit={'zone':'3203f226-b37f-42da-83fe-0fe8d043d995'})
 
 # Delete Peer
 client.delete_peer('0c5bc279-397a-4535-be32-301c16dbbc69')
 
 # This is for creating volume via manual provisioning
 client.volume_create(body = {'name':'gv1', 'type':'replicate', 'replica':3, 'bricks': [['peerid':'0c5bc279-397a-4535-be32-301c16dbbc69', 'path':'/exports/bricks/gv1/brick1/brick'], ['peerid':'7aafd270-b9b2-40b2-ba0e-7289f7d025c0', 'path':'/exports/bricks/gv1/brick2/brick'], ['peerid':'57470e13-2f9c-4404-9179-fb2ba38cc1d8', 'path': '/exports/bricks/gv1/brick3/brick']]})
 
 # This is for creating volume via intelligent volume provisioning. Make sure the device is registered first
 client.volume_create(body = {'name':'gv1', 'size':1000, replica:3})
 
 # Get the volume information
 client.volume_info()
 
 # Start the specified volume
 client.volume_start('gv1')
 
 # Stop the specified volume
 client.volume_stop('gv1')
 
 ```
