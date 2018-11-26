Georep API example usage:
```
import glusterapi
from glusterapi.api.client import Client
client = Client()

# The method names and parameters depend on the yaml/json api definition
# The api methods being used below are called from the library obtained from running generate.sh using api.json in georep_json directory 

# Create a geo-rep session between two cluster volumes:
glusterapi.geo_replication_create('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188', create={'mastervol':'testvol1', 'remotehosts':['192.168.56.102'], 'remotevol':'testvol2'})

# Start the geo-rep session:
glusterapi.geo_replication_start('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Pause a geo-rep session:
glusterapi.geo_replication_pause('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Resume a geo-rep session:
glusterapi.geo_replication_resume('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Show the status of geo-rep sessions:
glusterapi.geo_replication_status_list()

# Show the status of a particular geo-rep session:
glusterapi.geo_replication_status('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Generate ssh public key:
glusterapi.geo_replication_ssh_key_generate('testvol1')

# Get ssh public key:
glusterapi.geo_replication_ssh_key_get('testvol1')

# Push/Distribute the ssh keys:
glusterapi.geo_replication_ssh_key_push('testvol2', ssh_public_key2={'peerid':'fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', 'gsyncd':<insert GsyncdKey>, 'tar':<insert Tarkey>})

# Get the configuration values for a particular geo-rep session:
glusterapi.geo_replication_config_get('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Reset the configuration values:
glusterapi.geo_replication_config_reset('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Set the configuration values:
glusterapi.geo_replication_config_set('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Stop a geo-rep session:
glusterapi.geo_replication_stop('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')

# Delete a geo-rep session:
glusterapi.geo_replication_delete('fba0a488-21a4-42b7-8a41-b27ebaa8e5f4', '25b4e313-7b36-445d-b524-c3daebb91188')




