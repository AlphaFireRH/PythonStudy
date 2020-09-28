#!use/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from alive_progress import alive_bar
import onedrivesdk as sdk
from onedrivesdk.helpers import GetAuthCodeServer
from onedrivesdk.helpers.resource_discovery import ResourceDiscoveryRequest

redirect_uri = 'http://localhost:8080'
client_id = 'hao_ren@histonegames.onmicrosoft.com'
client_secret = 'Authentication()'
discovery_uri = 'https://api.office.com/discovery/'
auth_server_url = 'https://login.microsoftonline.com/common/oauth2/authorize'
auth_token_url = 'https://login.microsoftonline.com/common/oauth2/token'


def Authentication():
    http = sdk.HttpProvider()  # sdk.HttpProvider()
    auth = sdk.AuthProvider(
        http, client_id, auth_server_url=auth_server_url, auth_token_url=auth_token_url)
    auth_url = auth.get_auth_url(redirect_uri)
    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
    auth.authenticate(code, redirect_uri, client_secret,
                      resource=discovery_uri)
    # If you have access to more than one service, you'll need to decide
    # which ServiceInfo to use instead of just using the first one, as below.
    service_info = ResourceDiscoveryRequest(
    ).get_service_info(auth.access_token)[0]
    auth.redeem_refresh_token(service_info.service_resource_id)
    client = sdk.OneDriveClient(
        service_info.service_resource_id + '/_api/v2.0/', auth, http)


def main():
    Authentication()
    print("\n\n-------------Finish-------------\n\n")
    os.system("pause")


if __name__ == '__main__':
    main()
