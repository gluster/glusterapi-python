# python-gluster-mgmt-client
python-gluster-mgmt-client generates client libraries from an OpenAPI spec 3 api definition. The code generator used is [openapi-generator](https://github.com/OpenAPITools/openapi-generator) which is a fork project of swagger-codegen. Care must be taken when defining the api under OpenAPI spec 3 because the swagger parser is still under active development and definitions especially ones which use external refs must be written carefully. Also the multiple yaml/json files must be in the same directory as placing the yaml/json files in multiple directories will produce errors and is not supported by the parser as of now. The yaml/json api definitions are inside the config directory.
# Documentation
  * [Client library Generation](utils/client_library_generation.md)
  * [Library usage](docs/library_usage.md)
  
