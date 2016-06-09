from __future__ import print_function
import json, urllib2, ConfigParser, time, urllib
import requests
import logging
import random, time

## -- CONFIG BEGIN --

## Default hosts. Change if the situation changes.
## BLUESKY: Read the controller host name from the JSON status

default_frontend_url     = "http://interaktiv.nsb.no/"
default_controller_host  = "192.168.100.1"
default_controller_port  = "3990"

# -- END ---

def get_login_stream(status_reply, username, SHA1_password, 
		cookies = None, headers = None, proxies=None):
	login_URL_params = {'fnc': 'login', 'username': username,
		'password': SHA1_password, 'challenge': status_reply["challenge"],
		'client_ip': status_reply["redir"]["ipAddress"],
		'client_mac': status_reply["redir"]["macAddress"]}

	return requests.get(default_frontend_url, 
		params=login_URL_params, cookies=cookies, headers = headers, proxies=proxies)

def get_status(controller_host=default_controller_host, 
		controller_port=default_controller_port, cookies = None, 
		headers = None, proxies = None):
	# Add a random.random() to thwart caching. Is it required?
	callback_URL = "http://" + controller_host + ":" + controller_port + \
		"/json/status?" + str(random.random())

	callback_page_stream = requests.get(callback_URL, cookies=cookies, 
		headers=headers, proxies = proxies)
	callback_reply = json.loads(callback_page_stream.text)

	throwaway = ""

	for i in callback_page_stream.content:
		throwaway = i


	return callback_reply, callback_page_stream.cookies

def get_config_username_pwd():
	config = ConfigParser.ConfigParser()
	config.readfp(open('login.cfg'))
	username = config.get("login", "username")
	shapassword = config.get("login", "shapassword")

	return username, shapassword

# --- #

logfile = open("nsblogin.log", "a")

# The procedure goes like this:
#	1. Try to login: it doesn't matter with what username and password.
#		The NSB login site will give an incorrect login response with
#		a cookie. Save the cookie.
#	2. Get json status to get the challenge token to use in step 3. Provide
#		the cookies from step one. 
#	3. Now do a proper login with the correct username and SHA1 password,
#		and challenge token. If all goes well, you'll be logged in.

# I imagine the login script finagles the expected chilli challenge-
# response values server-side and then sends a redirect with them, but that
# kind of destroys the reason for using challenge-response to begin with...

# --------- step 1 ------------

# We need the cookies for some reason.

ctimepref = time.ctime() + ":\t" 

username, shapassword = get_config_username_pwd()

isite = "http://192.168.100.1:3990/login?username=foo@bar.baz&response="
idx = 1

before_invalid_login = time.time()

req = requests.get(isite)		# Nonstandard headers or cookies not reqd

print (ctimepref, "[TIME] First invalid login took", time.time()-before_invalid_login,"s.", file = logfile)

ord_cookies = req.history[idx].cookies  # YES !!!!
print ("Ordinary cookies: ", ord_cookies)

# --------- step 2 ------------

before_get_status = time.time()

callback_reply, callback_cookie = get_status(cookies=ord_cookies)

print (ctimepref, "[TIME] Getting status took", time.time()-before_get_status, "s.", file=logfile)

print (callback_reply)
print ("Callback cookie: ", callback_cookie)

print (ctimepref, "Received data from location", callback_reply["location"]["name"], file=logfile)

# --------- step 3 ------------

before_valid_login = time.time()

login_page = get_login_stream(callback_reply, username, shapassword,
	cookies=ord_cookies)

print (ctimepref, "[TIME] Valid login took", time.time()-before_valid_login,"s.", file=logfile)

# Finally, provide a new status report. If it's unlike the first, then
# you're logged in, otherwise you're not yet logged in.

print ("Getting status again...")

before_status = time.time()

print (get_status())

print (ctimepref, "[TIME] Finally getting status took", time.time() - before_status,"s.", file=logfile)
logfile.close()