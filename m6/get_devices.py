#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to get the list of
devices from Cisco DNA Center using the REST API.
"""

import requests


def main():
    """
    Execution begins here.
    """

    # Declare useful local variables to simplify request process
    api_path = "https://sandboxdnac.cisco.com/dna"
    auth = ("devnetuser", "Cisco123!")
    headers = {"Content-Type": "application/json"}

    # Issue HTTP POST request to the proper URL to request a token
    auth_resp = requests.post(
        f"{api_path}/system/api/v1/auth/token", auth=auth, headers=headers
    )

    # If successful, print token. Else, print failure info
    if auth_resp.ok:
        token = auth_resp.json()["Token"]
        # print(token)
    else:
        print(f"Token request failed with code {auth_resp.status_code}")
        print(f"Failure body: {auth_resp.text}")

    # Add a new header to carry our token in future HTTP requests
    headers.update({"X-Auth-Token": token})

    # Issue HTTP GET request to get list of network devices
    # For brevity, not going to perform error checking again
    get_resp = requests.get(
        f"{api_path}/intent/api/v1/network-device", headers=headers
    )

    # Debugging output to learn the JSON structure, then quit
    # import json; print(json.dumps(get_resp.json(), indent=2))

    # Iterate over list of dictionaries and print device ID and management IP
    if get_resp.ok:
        for device in get_resp.json()["response"]:
            print(f"ID: {device['id']}  IP: {device['managementIpAddress']}")
    else:
        print(f"Device collection failed with code {get_resp.status_code}")
        print(f"Failure body: {get_resp.text}")


if __name__ == "__main__":
    main()
