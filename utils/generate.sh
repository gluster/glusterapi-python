#!/bin/bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${0}")" && pwd)"
cd ~
if [ ! -d "${GENPATH}" ]
  then
	echo "Unable to find openapi-generator..Please make sure it is intstalled and the GENPATH environment variable is set
Instructions for installation:
1) git clone https://github.com/openapitools/openapi-generator
2) cd openapi-generator/
3) mvn clean package
	
Now set the GENPATH Variable as the absolute path of the generator, run the following in cmd line 
export GENPATH=<path of openapi-generator>, for example export GENPATH=\$HOME/openapi-generator. Add the same in .bashrc if you don't want to
run the command every time."
        exit 0
else
        cd $GENPATH
fi


dest_dir=${2}

#The following line invokes openapi-generator that generates client library
#Make sure theres a config.json file in your current working directory
java -jar modules/openapi-generator-cli/target/openapi-generator-cli.jar generate -i "${1}" -g python -o "${dest_dir}" -c "${SCRIPT_DIR}/config.json"


#Just some string cleanup for later concatenation i.e removing the forward-slash character if present
if [ "${dest_dir: -1}" = "/" ]
  then
	dest_dir="${dest_dir: : -1}"
fi


#Renaming a not so aesthetic file name into something moderately aesthetic
mv "${dest_dir}/glusterapi/api/default_api.py" "${dest_dir}/glusterapi/api/client.py"


#One liner to recurively substitute some ugly names to something good looking for the SDK using sed
find ${dest_dir}/glusterapi -type f -print0 | xargs -0 sed -i -e 's/DefaultApi/Client/g' -e 's/default_api/client/g' -e 's/unknown_base_type/body/g'
cp -t "${dest_dir}/glusterapi/" "${SCRIPT_DIR}/auth.py" "${SCRIPT_DIR}/enable_auth.sh"
exit 0
