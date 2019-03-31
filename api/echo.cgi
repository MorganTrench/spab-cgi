#!/home1/therevpr/opt/python27/bin/python
import sys
import cgi
import json
import sqlite3
import cgitb
import datetime
# enable displaying debug information in html
# cosider commenting this out for deployment
cgitb.enable()

print "Content-type: text/plain\n\n"
data = json.load(sys.stdin)
print json.dumps(data)
