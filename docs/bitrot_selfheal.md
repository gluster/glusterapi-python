Bitrot and Self-heal APIs example usage:
 ```
 import glusterapi
 from glusterapi.api.client import Client
 client = Client()
 
 # The method names and parameters depend on the yaml/json api definition
 # The api methods being used below are called from the library obtained from running generate.sh using api.json in bitrot_selfheal_json directory 
 
 # To enable bitrot detection for a given volume:
 glusterapi.bitrot_enable('testvol1')
 
 # Call the scrubber to verify the checksums for the volume:
 glusterapi.bitrot_scrub_ondemand('testvol1')
 
 # Show the scrubber status:
 glusterapi.bitrot_scrub_status('testvol1')
 
 # To disable bitrot detection for a given volume:
 glusterapi.bitrot_disable('testvol1')
 
 # Self Heal:
 glusterapi.self_heal('testvol1')
 
 # Brick info for self heal:
 glusterapi.self_heal_info('testvol1')
 ```
