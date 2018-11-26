# Client Library Generation

This guide demonstrates how to setup the client system(installation of dependencies) and also how to generate the client code using the script generate.sh 

## Setup

Before running generate.sh please make sure that the following are installed:

 ### Apache Maven
 Install maven:
  ```
  yum install maven
  ```
 ### Java;
 Install java:
 ```
 yum install java
 ```
 ### Install openapi-generator
 ```
 git clone https://github.com/openapitools/openapi-generator
 cd openapi-generator/
 mvn clean package
 ```
## Running the script
Before running the script make sure to set the GENPATH environtment variable:
 ```
 export GENPATH=<path of openapi-generator> (for example export GENPATH=$HOME/openapi-generator)
 ```
Add the same in .bashrc if you don't want to run the command every time.

Run the generate.sh script in the utils directory with the source yaml/json as initial argument and the directory where the code should be generated to as the other argument. 
 ```
 cd utils
 ./generate.sh <absolute path to the yaml/json file> <destination directory>
 
  ```
Example:
 ```
 cd utils
 ./generate.sh ~/python-gluster-mgmt-client/config/yaml/peer_volume_api_yaml/api.yml ~/api/
 ```
