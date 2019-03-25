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
# 2) does a search
# 3) outputs the results
# 
# The search function has the following signature:
#
# def search(bearer, appid, server, skip, limit, quiet, terms):
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
# skip - (optional) The point from which the search results 
#        returned to you should start.
#        For example, if you set skip=10, then the returned results will 
#        skip the first 10 start with the 11th search result.
#        Use in combination with 'limit' to page through results.
#
# limit - (optional) How many results an individual search should return. 
#         The default is 10. Use in combination with 'skip'
#         to page through results. E.g. if you searched with
#         skip=20 and limit=20, you would be given results 21-40,
#         because it would skip the first 20 results and give you the next 20
# 
# quiet - (optional) If quiet is set to True or 'true', the search will only return 
#         a list of file ids. Otherwise, it will return full file objects
#         with metadata.         
#
# terms - (optional) An object containing the key "terms" and its value as a 
#         string of terms you'd like to search by. 
#         Observe the following rules:
#          - The entire string must be wrapped in single quotes. 
#          - Separate terms are separated by a space
#          - Multi-word search terms must be wrapped in double quotes.
#          - tags must begin with a hash (#)
#          - multi-word tags must begin with a hash followed by 
#            the multi-word term wrapped in double quotes.   
#          e.g.: 
#           { "terms": ' "red car" honda #"3d model" ' }
#            searches red car, honda, and #3d model
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
# The following arguments are optional:
#   --skip
#   --limit
#   --quiet
#   --terms
#
#   Example usage:
#   python yadle_search.py \
#       --apiserver=https://exampleOrg1.yadle.com \
#       --user=exampleUser \
#       --password=examplePassword \
#       --appid=exampleAppId \
#       --quiet=true \
#       --limit=20 \
#       --skip=80 \
#       --terms='"star trek" #"3d model"'


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

def search(bearer, appid, apiserver, skip, limit, quiet, terms):
    skipString = ""
    limitString = ""
    quietString = ""

    if skip is not None:
        skipString = "skip={0}".format(skip)
    
    if limit is not None:
        limitString = "limit={0}".format(limit)

    if quiet == True or quiet == 'true':
        quietString = "quiet=true"

    url = "{0}/yadle/v2/search?{1}&{2}&{3}".format(apiserver, skipString, limitString, quietString)

    print(url)
        
    headers = {
        'x-app-id': appid,
        'Authorization': bearer,
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=terms, headers=headers)

    res = json.loads(response.text)

    pprint.pprint(res)

    # loop through individual files
    # for file in res['rows']:
    #     print("           ")
    #     pprint.pprint(file)                
    #     print("           ")

    return res



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apiserver", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--appid", required=True)
    parser.add_argument("--quiet", required=False)
    parser.add_argument("--skip", required=False)
    parser.add_argument("--limit", required=False)
    parser.add_argument("--terms", required=False)
    args = parser.parse_args()

    terms = {
        "terms": args.terms    
    }

    print(terms)

    # log in and get the bearer that will be used to authenticate search requests
    bearer = logIn(args.apiserver, args.user, args.password)


    search(
        bearer=bearer, 
        appid=args.appid, 
        apiserver=args.apiserver, 
        skip=args.skip, 
        limit=args.limit, 
        quiet=args.quiet,
        terms=terms)


if __name__ == "__main__":
    main()


