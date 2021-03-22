"""
use the Prism REST API v3 to create Prism Central Categories
"""

import requests
import urllib3
import json
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from requests.auth import HTTPBasicAuth


def main():
    """
    main entry point into the 'app'
    every function needs a Docstring in order to follow best
    practices
    """
    # load the script configuration
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    PC_IP = os.getenv("PC_IP")
    PC_PORT = os.getenv("PC_PORT")
    PC_USERNAME = os.getenv("PC_USERNAME")
    PC_PASSWORD = os.getenv("PC_PASSWORD")

    print(f"Prism Central IP: {PC_IP}")
    print(f"Prism Central Port: {PC_PORT}")

    """
    disable insecure connection warnings
    please be advised and aware of the implications of doing this
    in a production environment!
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup a variable that can be used to store our JSON configuration
    raw_json = []

    # grab and decode the category details from the included JSON file
    with open("./categories.json", "r") as f:
        raw_json = json.loads(f.read())

    # start building the BATCH request
    print(
        "Building the BATCH request payload that will " "create the category keys ..."
    )
    batch_payload = {
        "action_on_failure": "CONTINUE",
        "execution_order": "SEQUENTIAL",
        "api_request_list": [],
        "api_version": "3.1",
    }

    for key in raw_json["categories"][0]["keys"]:
        # do something with the keys here
        # probably use the API to create the keys, as shown below
        category_key_payload = {
            "operation": "PUT",
            "path_and_params": f"/api/nutanix/v3/categories/{key}",
            "body": {
                "name": key,
                "description": key,
                "capabilities": {"cardinality": 64},
                "api_version": "3.1",
            },
        }

        # add the new API request to the batch payload's BODY
        batch_payload["api_request_list"].append(category_key_payload)

    # submit the BATCH request that will create the category keys
    print("Creating the category keys via API BATCH request ...")
    endpoint = f"https://{PC_IP}:{PC_PORT}/api/nutanix/v3/batch"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}

    # submit the BATCH request that will create the category keys
    try:
        results = requests.post(
            endpoint,
            data=json.dumps(batch_payload),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(PC_USERNAME, PC_PASSWORD),
        )

        # check the results of the request
        print(f"BATCH request HTTP status code: {results.status_code}")
        json_response = results.json()
        print(
            f"There are {len(json_response['api_response_list'])} "
            "responses from this request."
        )
        for response in json_response["api_response_list"]:
            print(
                f"Response code: {response['status']} | "
                f"path_and_params: {response['path_and_params']}"
            )
    except Exception as error:
        print(f"An unhandled exception has occurred: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()

    # start building the next BATCH request
    print("Building the BATCH request payload that will create the category values ...")
    batch_payload = {
        "action_on_failure": "CONTINUE",
        "execution_order": "SEQUENTIAL",
        "api_request_list": [],
        "api_version": "3.1",
    }

    for value in raw_json["categories"][0]["values"]:
        # do something with the values here
        # probably use the API to create values, as shown below
        category_value_payload = {
            "operation": "PUT",
            "path_and_params": "/api/nutanix/v3/categories/"
            f"{value['key']}/{value['value']}",
            "body": {
                "value": value["value"],
                "description": value["value"],
                "assignment_rule": {
                    "name": "assignment rule name created by API",
                    "description": "assignment rule value created by API",
                    "selection_criteria_list": [],
                },
                "api_version": "3.1",
            },
        }

        # add the new API request to the batch payload's BODY
        batch_payload["api_request_list"].append(category_value_payload)

    # submit the BATCH request that will create the category keys
    try:
        results = requests.post(
            endpoint,
            data=json.dumps(batch_payload),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(PC_USERNAME, PC_PASSWORD),
        )

        # check the results of the request
        print(f"BATCH request HTTP status code: {results.status_code}")
        json_response = results.json()
        print(
            f"There are {len(json_response['api_response_list'])} "
            "responses from this request."
        )
        for response in json_response["api_response_list"]:
            print(
                f"Response code: {response['status']} | "
                f"path_and_params: {response['path_and_params']}"
            )
    except Exception as error:
        print(f"An unhandled exception has occurred: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()


if __name__ == "__main__":
    main()
