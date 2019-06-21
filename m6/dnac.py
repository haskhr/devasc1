#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate HTTP requests to a REST API using the Python "requests"
library. Specifically, creates a simple SDK for Cisco DNA Center to get
a list of devices, as well as addition and removal.
"""

import json
import requests
from requests.auth import HTTPBasicAuth


class DNACTalker:
    """
    Homemade basic SDK for interacting with Cisco DNA Center.
    """

    def __init__(self, username, password, hostname):
        """
        Constructor requires username and password for initial login to
        collect a token. Token is then stored as part of a reusable
        HTTP headers dictionary for future API calls.
        """

        # Store basic information and collect token
        self.hostname = hostname
        temp_headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"https://{self.hostname}/dna/system/api/v1/auth/token",
            auth=HTTPBasicAuth(username=username, password=password),
            headers=temp_headers,
        )

        # Generate reusable headers dict with token for authentication
        token = response.json()["Token"]
        self.headers = {
            "X-Auth-Token": token,
            "Content-type": "application/json",
        }

    def get_device_list(self):
        """
        Return a dictionary of devices managed by DNA center.
        """

        response = requests.get(
            f"https://{self.hostname}/dna/intent/api/v1/network-device",
            headers=self.headers,
        )
        return response.json()

    def _get_task_status(self, response):
        """
        Internal method used to grab the status of an outstanding task such as
        adding or removing devices.
        """
        task_id = response.json()["response"]["taskId"]
        get_response = requests.get(
            f"https://{self.hostname}/dna/intent/api/v1/task/{task_id}",
            headers=self.headers,
        )
        return get_response.json()

    def add_device(self, device_dict):
        """
        Add a new device based on a large dictionary containing the required
        information for a device to be added.
        """
        add_response = requests.post(
            f"https://{self.hostname}/dna/intent/api/v1/network-device",
            data=json.dumps(device_dict),
            headers=self.headers,
        )
        return self._get_task_status(add_response)

    def delete_device(self, device):
        """
        Delete a device based on a dictionary gathered from the
        get_device_list() method.
        """
        dev_id = device["id"]
        delete_response = requests.delete(
            f"https://{self.hostname}/dna/intent/api/v1/network-device/{dev_id}",
            headers=self.headers,
        )
        return self._get_task_status(delete_response)

    def print_resp_status(self, response):
        """
        Pretty-printer based on a response dict that will reveal whether an add
        or delete operation succeeded or failed. If it fails, the failure reason
        is also printed.
        """
        sub_resp = response["response"]
        if sub_resp["isError"]:
            print(f"{self.hostname}: Error - {sub_resp['failureReason']}")
        else:
            print(f"{self.hostname}: Operation successful")


def main():
    """
    Execution starts here.
    """

    # Instantiate a new DNACTalker object with the public Cisco credentials
    # and DNA center standbox hostname. These may change, so be sure to check!
    dnactalker = DNACTalker("devnetuser", "Cisco123!", "sandboxdnac.cisco.com")

    # Defining a test IP addresses for a device we will add to and
    # remove from DNA center.
    test_ip = "192.0.2.85"

    # Collect the device list, then iterate over each device and print out
    # the device type along with the numeric ID.
    devices = dnactalker.get_device_list()
    for device in devices["response"]:
        print(f'Type: {device["type"]}  ID: {device["id"]}')

    # Define a dict with all parameters needed for the new node. This data
    # doesn't really matter, but many of these are required fields because
    # DNA center can manage some legacy nodes using SNMP and SSH/CLI.
    print("Adding new node")
    device_dict = {
        "ipAddress": [test_ip],
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

    # Add the device and print out the result using the DNACTalker methods.
    added_device = dnactalker.add_device(device_dict)
    dnactalker.print_resp_status(added_device)

    # Ensure new node was added by checking the IP, then delete it.
    # There are more advanced ways of doing it, but this "for" loop
    # illustrates the concept without any fanfare.
    devices = dnactalker.get_device_list()
    for device in devices["response"]:
        if device["managementIpAddress"] == test_ip:
            # We found our new IP in the list, which we expected because
            # the addition was successful. Let's remove this device
            # and ensure it succeeds.
            print(f"Deleting node with ID: {device['id']}")
            deleted_device = dnactalker.delete_device(device)
            dnactalker.print_resp_status(deleted_device)
            break


if __name__ == "__main__":
    main()
