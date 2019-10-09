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
# def disable(bearer, appid, server, skip, limit, quiet, terms):
#
# The arguments:
# bearer - (required) An authentication token. Use the bearer
#          token returned from the logIn() function upon a valid login
#
# appid - (required) This is one of your organization's valid app id's.
#         If you do not know your app id, contact a Yadle representative
#
# apiserver - (required) The url of you organization's Yadle API server
#
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
#
#   Example usage:
#	python adduser.py \
#		--apiserver="https://yadle11.yadle.com" \
#		--user=yadle \
#		--password=xxxxxxx \
#		--appid="api_xxxxxxxxxxxxxxxxxxxx" \
#		--newuser=someone@domain.com



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


def addUser(bearer, appid, apiserver, email, firstname, lastname):

	url = "{0}/yadle/v2/user/invite".format(apiserver)

	headers = {
		'x-app-id': appid,
		'Authorization': bearer,
		'cache-control': "no-cache"
	}

	payload = {
		'firstName': firstname,
		'lastName': lastname,
		'email': email
	}


	response = requests.request("POST", url, data=payload, headers=headers)

	pprint.pprint(response)

	return



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--apiserver", required=True)
	parser.add_argument("--user", required=True)
	parser.add_argument("--password", required=True)
	parser.add_argument("--appid", required=True)
	parser.add_argument("--email", required=True)
	parser.add_argument("--firstname", required=True)
	parser.add_argument("--lastname", required=True)

	args = parser.parse_args()

	# log in and get the bearer that will be used to authenticate for subsequent API calls.
	bearer = logIn(args.apiserver, args.user, args.password)

	addUser(
		bearer=bearer,
		appid=args.appid,
		apiserver=args.apiserver,
		email=args.email,
		firstname=args.firstname,
		lastname=args.lastname)


if __name__ == "__main__":
    main()



