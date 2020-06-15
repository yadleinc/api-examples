""" Examples demonstrating how to use the Yadle aggregate API.

    This file contains several methods for interacting with the Yadle API.

    The main() function at the bottom contains an actual example of creating and
    modifying an aggregate.

    See https://api.yadle.com/ for full documentation of the Yadle API.
"""

import requests
import json
import traceback


def logIn(apiserver, username, password):
    url = "{0}/yadle/v2/auth/login".format(apiserver)
    payload = "username={0}&password={1}&undefined=".format(username, password)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
 
    # get Bearer
    res = json.loads(response.text)
    bearer = "Bearer {0}:{1}".format(res['token'], res['password'])
    return bearer


def get_file_info(file_id, server, bearer, app_id):
    
    url = "{0}/yadle/v2/file/{1}".format(server, file_id)
    payload = ""
    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, data=payload, headers=headers)

    if not response:
        print('ERROR: ' + url + ' returns a null response ' + str(response))
        print(str(json.loads(response.text)))
        return None

    return json.loads(response.text)



def create_aggregate(file_id, member_list, server, bearer, app_id):
    url = "{0}/yadle/v2/file/{1}/aggregate/new".format(server, file_id)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, json=member_list)

    print(json.loads(response.text))
    return json.loads(response.text)

def remove_aggregate_members(file_id, aggregate_id, members_to_remove, server, bearer, app_id):
    url = "{0}/yadle/v2/file/{1}/aggregate/{2}".format(server, file_id, aggregate_id)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, json=members_to_remove)

    print(json.loads(response.text))
    return json.loads(response.text)

def add_additional_aggregate_members(file_id, aggregate_id, files_to_add, server, bearer, app_id):
    url = "{0}/yadle/v2/file/{1}/aggregate/{2}".format(server, file_id, aggregate_id)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, json=files_to_add)

    print(json.loads(response.text))
    return json.loads(response.text)

def get_aggregate(file_id, aggregate_id, server, bearer, app_id):
    url = "{0}/yadle/v2/file/{1}/aggregate/{2}".format(server, file_id, aggregate_id)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    print(json.loads(response.text))
    return json.loads(response.text)

def get_all_aggregates(file_id, server, bearer, app_id):
    # get all aggregates associated with a file
    url = "{0}/yadle/v2/file/{1}/aggregate/_all".format(server, file_id)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    print(json.loads(response.text))
    return json.loads(response.text)

def edit_primary_file(file_id, aggregate_id, new_primary, server, bearer, app_id):
    # edit primary file of an aggregate. The new primary file must already 
    # be a member of the aggregate.
    url = "{0}/yadle/v2/file/{1}/aggregate/{2}/edit_primary".format(server, file_id, aggregate_id)
    
    # body must be an array containing a signle file id: the new pimary file.
    body = [new_primary]
    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, json=body)

    print(json.loads(response.text))
    return json.loads(response.text)

def delete_entire_aggregate(file_id, aggregate_id, server, bearer, app_id):
    # Delete an entire aggregate. Note: this does not affect any constituent files themselves.
    url = "{0}/yadle/v2/file/{1}/aggregate/{2}/entire".format(server, file_id, aggregate_id)
    
    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers)

    print(json.loads(response.text))
    return json.loads(response.text)


def main():
        
    # server and authentication information
    server = 'https://example1.yadle.com'
    username = "your_username"
    password = "your_password"
    bearer = logIn(server, username, password)
    app_id = 'your_app_id'


    aggregate_head = 'file_id1'
    aggregate_members = ['file_id2', 'file_id3', 'file_id4']

    response = create_aggregate(aggregate_head, aggregate_members, server, bearer, app_id)

    # Once the aggregate has been created, we will use the new aggregate id to interact with it.
    aggregate_id = response['aggregate_id']

    # View the aggregate.
    aggregate = get_aggregate(aggregate_head, aggregate_id, server, bearer, app_id)

    # Change which file is the primary fire (the one that will be displayed in search results).
    edit_response = edit_primary_file(aggregate_head, aggregate_id, aggregate_members[0], server, bearer, app_id)

    if edit_response['code'] == 200:
        # aggregate_head has changed:
        aggregate_head = aggregate_members[0]
    

    # As an example, remove a file from the aggregate.
    files_to_remove = [aggregate_members[2]]
    remove_aggregate_members(aggregate_head, aggregate_id, files_to_remove, server, bearer, app_id)

    # Add the same file back into the aggregate.
    add_additional_aggregate_members(aggregate_head, aggregate_id, files_to_remove, server, bearer, app_id)  

    # Delete the entire aggregate.
    delete_entire_aggregate(aggregate_head, aggregate_id, server, bearer, app_id)

if __name__ == '__main__':
    main()