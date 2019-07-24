#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to add a new device
to Cisco DNA Center using the REST API.
"""

import time
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

    # Create a dictionary to represent the new device to add
    new_device_dict = {
        "ipAddress": ["192.0.2.1"],
        "snmpVersion": "v2",
        "snmpROCommunity": "readonly",
        "snmpRWCommunity": "readwrite",
        "snmpRetry": "1",
        "snmpTimeout": "60",
        "cliTransport": "ssh",
        "userName": "nick",
        "password": "secret123!",
        "enablePassword": "secret456!",
    }

    # Issue HTTP POST request to add a new device with the
    # "new_device_dict" as the body of the request.
    add_resp = requests.post(
        f"{api_path}/intent/api/v1/network-device",
        json=new_device_dict,
        headers=headers,
    )

    if add_resp.ok:
        print(f"Request accepted: status code {add_resp.status_code}")

        # Wait 10 seconds
        time.sleep(10)

        # Query DNA center for the status of the specific task ID
        task = add_resp.json()["response"]["taskId"]
        task_resp = requests.get(
            f"{api_path}/intent/api/v1/task/{task}", headers=headers
        )

        # See if the task was completed successfully or not
        if task_resp.ok:
            task_data = task_resp.json()["response"]
            if not task_data["isError"]:
                print("New device successfully added")
            else:
                print(f"Async task error seen: {task_data['progress']}")
        else:
            print(f"Async GET failed: status code {task_resp.status_code}")

    else:
        # The initial HTTP POST failed; print details
        print(f"Device addition failed with code {add_resp.status_code}")
        print(f"Failure body: {add_resp.text}")


if __name__ == "__main__":
    main()
