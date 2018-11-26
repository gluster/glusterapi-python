 Snapshot APIs example usage:
 ```
 import glusterapi
 from glusterapi.api.client import Client
 client = Client()
 
 # The method names and parameters depend on the yaml/json api definition
 # The api methods being used below are called from the library obtained from running generate.sh using api.json in snapshot_json directory
 
 # Create a snapshot:
 glusterapi.snapshot_create(create={'volname':'testvol1', 'snapname': 'testsnap1')
 
 # Activate a snapshot:
 glusterapi.snapshot_activate('testsnap1')
 
 # Clone a snapshot:
 glusterapi.snapshot_clone('testsnap1', clone={'clonename':'clone1'})
 
 # Get snapshot information:
 glusterapi.snapshot_info('testsnap1')
 
 # Get all snapshot information:
 glusterapi.snapshot_list_all()
 
 # Restore a snapshot:
 glusterapi.snapshot_restore('testsnap1')
 
 # Get snapshot status:
 glusterapi.snapshot_status('testsnap1')
 
 # Deactivate a snapshot:
 glusterapi.snapshot_deactivate('testsnap1')
 
 # Delete a snapshot:
 glusterapi.snapshot_delete('testsnap1')
 ```
