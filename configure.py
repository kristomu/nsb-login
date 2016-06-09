import sys, ConfigParser, getpass, hashlib

print "What... is your username?",
username = raw_input()
password = getpass.getpass("What... is your password? ")
verification = getpass.getpass("Enter password again for verification: ")

if verification != password:
	print "Password mismatch."
	sys.exit(-1)

config = ConfigParser.ConfigParser()
config.add_section("login")
config.set("login", "username", username)		# todo proper write here
config.set("login", "shapassword", hashlib.sha1(password).hexdigest())

configfile = open("login.cfg", "w")
config.write(configfile)