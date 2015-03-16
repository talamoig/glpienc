#!/bin/env python
import MySQLdb
import sys

execfile('config.py')

if len(sys.argv)!=2:
    print "Usage: %s <hostname>"%sys.argv[0]
    sys.exit(1)

host=sys.argv[1]

db = MySQLdb.connect(host=dbhost, # your host, usually localhost
                     user=dbuser, # your username
                      passwd=dbpasswd, # your password
                      db=dbname) # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

query="SELECT glpi_computers.name,glpi_states.name,glpi_plugin_customfields_computers.puppetrole \
FROM glpi_plugin_customfields_computers,glpi_computers,glpi_states \
WHERE glpi_states.id=glpi_computers.states_id \
AND glpi_computers.name='%s' \
AND glpi_plugin_customfields_computers.id=glpi_computers.id"%host
#print query
#sys.exit(0)
cur.execute(query)

# print all the first cell of all the rows
#print "a"
rows=cur.fetchall()
if len(rows)!=1:
    sys.stderr.write("query returned %s results. Expecting 1\n"%len(rows))
    sys.exit(1)
host=rows[0][0]
env=rows[0][1]
role=rows[0][2]
print "---"
print "   environment: %s"%env
print "   role: %s"%role
