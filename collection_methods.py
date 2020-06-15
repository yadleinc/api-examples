""" Examples demonstrating how to use the Yadle collections API.

    The first four functions below are convenience functions for the purpose of this demo.
    All subsequent function are examples of how to actually use the collections API.

    The main() function at the bottom contains an actual example of using the collections API.
    It gets the Yadle file ids of all of the files in a given directory and adds them to a collection.
    Than, just for the sake of example, it removes a few files, adds one file back to the collection,
    renames the collection, and finally, deletes the collection.

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

def get_file_instances_in_directory(device_id, directory, org, server, bearer, app_id):
    try:
        device_path = device_id + '_' + directory

        view_name = org + '_catalog'

        headers = {
            'authorization': bearer,
            'x-app-id': app_id
        }

        querystring = { 'key': device_path, 'reduce': 'false' }

        url = server + '/yadle/v2/utility/view/' + view_name + '/_design/path_to_id/_view/path_to_id3'

        response = requests.request("GET", url, headers = headers, params = querystring)

        print('INFO: get_indexed_file_list_in_directory: ' + url + ' querystring: ' + str(querystring))

        if not response:
            print('INFO: Invalid response ' + url + ' ' + str(response))
            return response.text

        response_json = response.json()
        print('INFO: response_json: ' + str(response_json))

        return response_json

    except:
        print('ERROR: ' + traceback.format_exc())
        return None

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

def get_matching_file_instances(files, collection_dir, server, bearer, app_id):
    """
    Because Yadle tracks any and all copies of a file, we need to make sure we're only 
    using instances of a file that are in the given directory. This function iterates
    over all instances of a file and returns only the instances that are in the
    given directory (collection_dir).
    """
    files_to_add = {}
    for file_info in files:
        print(file_info)
        file_doc = get_file_info(file_info['id'], server, bearer, app_id)

        for device_id in file_doc['device']:

            for path_id in file_doc['device'][device_id]['files']:

                if file_doc['device'][device_id]['files'][path_id]['dir'] == collection_dir:
                    if file_info['id'] not in files_to_add:
                        files_to_add[file_info['id']] = {}

                    if device_id not in files_to_add[file_info['id']]:
                        files_to_add[file_info['id']][device_id] = []

                    files_to_add[file_info['id']][device_id].append(path_id)

    return files_to_add


def create_collection(collection_name, body, server, bearer, app_id):

    """ The http message body when using creating or updating a collection 
    should look like this:
    {
        "{file_id1}": {
            "{device_id1}": ["{path_id1}"]
        },
        "{file_id2}": {
            "{device_id1}": ["{path_id2}", "{path_id3}"],
            "{device_id2}": ["{path_id4}", "{path_id5}", "{path_id6}"]
        }
    }
    """

    # Add files to a collection
    url = "{0}/yadle/v2/collection/{1}".format(server, collection_name)

    headers = {
    'x-app-id': app_id,
    'Authorization': bearer,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, json=body)

    print(json.loads(response.text))
    return json.loads(response.text)

def get_collection(collection_name, server, bearer, app_id):
    # Get collection documents
    url = "{0}/yadle/v2/collection/{1}".format(server, collection_name)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    print(json.loads(response.text))
    return json.loads(response.text)

def get_all_collections(collection_name, server, bearer, app_id):
    # Get collection documents
    url = "{0}/yadle/v2/collection/_all".format(server, collection_name)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    return json.loads(response.text)

def remove_members_from_collection(collection_name, body, server, bearer, app_id):
    # Delete files from a collection
    url = "{0}/yadle/v2/collection/{1}".format(server, collection_name)

    headers = {
    'x-app-id': app_id,
    'Authorization': bearer,
    'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, json=body)

    print(json.loads(response.text))
    return json.loads(response.text)

def add_members_to_collection(collection_name, body, server, bearer, app_id):
    # Add files to a collection
    url = "{0}/yadle/v2/collection/{1}".format(server, collection_name)

    headers = {
    'x-app-id': app_id,
    'Authorization': bearer,
    'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, json=body)

    print(json.loads(response.text))
    return json.loads(response.text)

def rename_collection(collection_name, new_name, server, bearer, app_id):
    # Rename collection
    url = "{0}/yadle/v2/collection/{1}/new_name/{2}".format(server, collection_name, new_name)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request('PATCH', url, headers=headers)

    print(json.loads(response.text))

def delete_collection(collection_name, server, bearer, app_id):
    # Delete collection
    url = "{0}/yadle/v2/collection/{1}/entire".format(server, collection_name)

    headers = {
        'x-app-id': app_id,
        'Authorization': bearer,
        'Content-Type': 'application/json'
    }

    response = requests.request('DELETE', url, headers=headers)

    print(json.loads(response.text))
    return json.loads(response.text)



def main():
    
    # server and authentication information
    server = 'https://example1.yadle.com'
    username = "your_username"
    password = "your_password"
    bearer = logIn(server, username, password)
    app_id = 'your_app_id'


    collection_name = 'my_test_collection2'
    device_id = 'a_device_id'

    # Directory string must end with a slash.
    collection_dir = "/full/path/to/a/directory/"
    
    # get all of the files within (the first level of) a directory:
    files = get_file_instances_in_directory(
        device_id,
        collection_dir,
        'yadle1',
        server,
        bearer, 
        app_id)

    files_to_add = get_matching_file_instances(files, collection_dir, server, bearer, app_id)

    
    print('files_to_add: ')
    print(files_to_add)

    create_result = create_collection(collection_name, files_to_add, server, bearer, app_id)
    if 'error' in create_result:
        print('error creating collection, exiting')
        return


    # Just as an example, take three files from what was added above
    # and remove them from the collection
    file_id1 = list(files_to_add)[0]
    file_id2 = list(files_to_add)[1]
    file_id3 = list(files_to_add)[2]
    files_to_remove = {
        file_id1: files_to_add[file_id1],
        file_id2: files_to_add[file_id2],
        file_id3: files_to_add[file_id3]
    }
    remove_members_from_collection(collection_name, files_to_remove, server, bearer, app_id)
    

    # Add on of those files back into the collection
    files_to_re_add= {
        file_id3: files_to_add[file_id3]
    }
    add_members_to_collection(collection_name, files_to_re_add, server, bearer, app_id)


    # Get the collection
    test_collection = get_collection(collection_name, server, bearer, app_id)


    # Edit the name of the collection
    new_name = 'MyTestCollection2'
    rename_collection(collection_name, new_name, server, bearer, app_id)


    # Delete the collection
    delete_collection(new_name, server, bearer, app_id)

if __name__ == '__main__':
    main()