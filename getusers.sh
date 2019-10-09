#!/bin/bash

appid=""
org=""
password=""
user=""

while [ $# -gt 0 ]; do
	case "$1" in
		--appid=*)
			appid="${1#*=}"
			;;
		--org=*)
			org="${1#*=}"
			;;
		--password=*)
			password="${1#*=}"
			;;
		--user=*)
			user="${1#*=}"
			;;
    	*)
    		echo "bad option'"$1"'"
			echo " "
			exit 1
  esac
  shift
done

if [ -z $appid ]; then echo "missing application ID.  Use --appid"; exit; fi
if [ -z $org ]; then echo "missing organization name.  Use --org"; exit; fi
if [ -z $password ]; then echo "missing user password. Use --password"; exit; fi
if [ -z $user ]; then echo "missing --user"; exit; fi


# change this if using self-hosted - just put the IP address of your server, on port 4444:
#
# like:    http://192.168.1.138:4444
#
server="https://${org}1.yadle.com"


version="v2"


echo -en "Authenticating..."
auth=$(curl --silent -X POST \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=${user}&password=${password}" \
	"${server}/yadle/${version}/auth/login")

prop="error"
temp=`echo ${auth} | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w $prop`
e=${temp##*|}


if [ "$e" == "Unauthorized" ]; then
	echo "[FAILED]"
	exit
fi

echo "[OK]"

# extract password and token for future API calls
#
prop="password"
temp=`echo ${auth} | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w $prop`
password=${temp##*|}

prop="token"
temp=`echo ${auth} | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w $prop`
token=${temp##*|}

# GET list of users info
#
r=$(curl  --silent -X GET \
  -H "authorization: Bearer ${token}:${password}" \
  -H "x-app-id: ${appid}" \
  "${server}/yadle/${version}/user/_all")

# user document is in ${r}
echo ${r} | python -m json.tool

