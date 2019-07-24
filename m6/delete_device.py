#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate Python "requests" to delete an existing
device from Cisco DNA Center using the REST API.
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

    # Issue an HTTP GET to search for a specific device by IP address
    delete_ip = "192.0.2.1"
    get_resp = requests.get(
        f"{api_path}/intent/api/v1/network-device/ip-address/{delete_ip}",
        headers=headers,
    )

    # If the device was found, continue with deletion
    if get_resp.ok:
        delete_id = get_resp.json()["response"]["id"]
        print(f"Found device with mgmt IP {delete_ip} and ID {delete_id}")

        # Issue HTTP DELETE and specify the device ID. Like the HTTP POST
        # to add a device, this is an asynchronous operation
        delete_resp = requests.delete(
            f"{api_path}/intent/api/v1/network-device/{delete_id}",
            headers=headers,
        )

        # If delete succeeded, check task ID for completion
        if delete_resp.ok:
            print(f"Request accepted: status code {delete_resp.status_code}")

            # Wait 10 seconds
            time.sleep(10)

            # Query DNA center for the status of the specific task ID
            task = delete_resp.json()["response"]["taskId"]
            task_resp = requests.get(
                f"{api_path}/intent/api/v1/task/{task}", headers=headers
            )

            # See if the task was completed successfully or not
            if task_resp.ok:
                task_data = task_resp.json()["response"]
                if not task_data["isError"]:
                    print("Old device successfully deleted")
                else:
                    print(f"Async task error seen: {task_data['progress']}")
            else:
                print(f"Async GET failed: status code {task_resp.status_code}")

        else:
            # The initial HTTP DELETE failed; print details
            print(f"Device removal failed with code {delete_resp.status_code}")
            print(f"Failure body: {delete_resp.text}")

    else:
        print(f"Could not find device with mgmt IP {delete_ip}")
        print(f"Code: {get_resp.status_code}  Body: {get_resp.text}")


if __name__ == "__main__":
    main()
