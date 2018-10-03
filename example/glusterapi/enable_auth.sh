#!/bin/bash

set -eu

sed -i 's/from __future__ import absolute_import/from . import auth/g' configuration.py
echo 'from __future__ import absolute_import' | cat - configuration.py > temp && mv temp configuration.py

sed -i 's/self.update_params_for_auth(header_params, query_params, auth_settings)/self.update_params_for_auth(resource_path, method, header_params, query_params, auth_settings)/g' api_client.py
sed -i 's/update_params_for_auth(self, headers, querys, auth_settings)/update_params_for_auth(self, resource_path, method, headers, querys, auth_settings)/g' api_client.py
sed -i 's/self.configuration.auth_settings()/self.configuration.auth_settings(resource_path, method)/g' api_client.py

sed -i 's/def auth_settings(self)/def auth_settings(self, resource_path, method)/g' configuration.py
sed -i 's/self.get_basic_auth_token()/auth.Auth(\"glustercli\",resource_path, method)/g' configuration.py
