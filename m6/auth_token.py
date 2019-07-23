#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to get an access token
from Cisco DNA Center using the REST API.
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
        print(token)
    else:
        print(f"Token request failed with code {auth_resp.status_code}")
        print(f"Failure body: {auth_resp.text}")


if __name__ == "__main__":
    main()
