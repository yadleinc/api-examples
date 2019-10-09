#
#	Copyright (c) 2016-2019 Datawhere Inc.  All rights reserved.
#
#	This software is the confidential and proprietary information
# 	("Confidential Information") of Datawhere Inc.("Datawhere")  You
#	shall not disclose such Confidential Information and shall use it
#	only in accordance with the terms of the license agreement you
#	entered into with Datawhere.
#
#	DATAWHERE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
#	SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
# 	BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR  PURPOSE, OR NON-INFRINGEMENT. DATAWHERE
#	SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT
#	OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

#
# The code below does the following things:
# 1) authenticates (logs in to your yadle account)
# 2) gets a list of all users
# 3) outputs the results
#
# The getUsers function has the following signature:
#
# def getUsers(bearer, appid, server, skip, limit, quiet, terms):
#
# The arguments:
# bearer  	(required) An authentication token. Use the bearer
#			token returned from the logIn() function upon a valid login
#
# appid  	(required) This is one of your organization's valid app id's.
#         	If you do not know your app id, contact a Yadle representative
#
# apiserver (required) The url of you organization's Yadle API server
#
# skip  	(optional) The point in the results returned to you should start.
#        	For example, if you set skip=10, then the returned results will
#        	skip the first 10 users, start with the 11th user result.
#        	Use in combination with 'limit' to page through results.
#
# limit  	(optional) How many results should be return returned.
#         	The default is all. Use in combination with 'skip'
#         	to page through results. E.g. if you called with
#         	skip=20 and limit=20, you would be given results 21-40,
#         	because it would skip the first 20 users and would give you the next 20
#
#
# Command line usage:
# While the code below can be used as a module, it can also be launched from the command line.
# The following arguments are required:
#   --apiserver
#   --user
#   --password
#   --appid
#
# The following arguments are optional:
#   --skip
#   --limit
#
#   Example usage:
#	python getusers.py \
#		--apiserver="https://yadle11.yadle.com" \
#		--user=yadle \   		<-- Yadle user account that is making the API call
#		--password=xxxxxxx \	<-- password for Yadle user account
#		--appid="api_xxxxxxxxxxxxxxxxxxxx" \
#		--limit=5 \
#		--skip=2



import requests
import json
import pprint
import traceback, sys
import argparse



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


def getUsers(bearer, appid, apiserver, skip, limit):
	skipString = ""
	limitString = ""
	quietString = ""

	if skip is not None:
		skipString = "skip={0}".format(skip)

	if limit is not None:
		limitString = "limit={0}".format(limit)

	url = "{0}/yadle/v2/user/_all?{1}&{2}".format(apiserver, skipString, limitString)

	headers = {
		'x-app-id': appid,
		'Authorization': bearer,
		'cache-control': "no-cache"
	}

	response = requests.request("GET", url, headers=headers)
	users = json.loads(response.text)

	for u in users['rows']:
		print(u['id'],u['firstName'],u['lastName'], u['status'])


	#pprint.pprint(users)

	return users



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--apiserver", required=True)
	parser.add_argument("--user", required=True)
	parser.add_argument("--password", required=True)
	parser.add_argument("--appid", required=True)
	parser.add_argument("--skip", required=False)
	parser.add_argument("--limit", required=False)

	args = parser.parse_args()

	# log in and get the bearer that will be used to authenticate for subsequent API calls.
	bearer = logIn(args.apiserver, args.user, args.password)


	# get list of users
	#
	getUsers(
		bearer=bearer,
		appid=args.appid,
		apiserver=args.apiserver,
		skip=args.skip,
		limit=args.limit)



if __name__ == "__main__":
    main()



