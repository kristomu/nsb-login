nsb-login
=========
Automated login script for NSB wireless on-train networks (Norway)

Automatisk innloggingsskript for NSBs trådløse tognettverk

Usage
-----

First run configure.py. The program will ask you for your login and password,
and construct a login.cfg file. Then, when you're on a train and connected to
the NSB_INTERAKTIV network, run dologin.py.

The login script will print a JSON status block before starting to log in. It
will also print another status block at the end. If the two differ, you're
logged in, otherwise try again. You can also check whether you're logged in
by pinging a host that responds to ping, or by trying to visit a web page.
If you're logged in, both these actions will succeed as expected; if not,
the network will respectively block pings and redirect you to the captive
portal frontpage.

The script also prints and logs timing data, as well as the name of the 
location where you're logging in (usually something like 75-10, which I think
is an internal train ID).

Known bugs and limitations
--------------------------

* There's no error checking.
* The controller host is hard-coded, but the IP may change in the future
* Simply reporting the JSON status chunk is not terribly user friendly, and the script doesn't try again if it fails to log in.

Still, it's sufficiently usable for my purposes.
