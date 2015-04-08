#!/bin/env python
import MySQLdb
import sys
import os

if len(sys.argv)!=2:
    sys.stderr.write("Usage: %s <hostname>\n"%sys.argv[0])
    sys.exit(1)

configfiles=['/etc/glpienc/config.py','config.py']

configured=False
for conffile in configfiles:
    if os.path.isfile(conffile):
        configured=True
        execfile(conffile)
        break

if not configured:
    files=' '.join(configfiles)
    sys.stderr.write("Could not ready any of the following configuration files: %s\n"%files)
    sys.exit(1)

db = MySQLdb.connect(host=dbhost, # your host, usually localhost
                     user=dbuser, # your username
                     passwd=dbpasswd, # your password
                     db=dbname) # name of the data base

cur = db.cursor() 

host=sys.argv[1]
if domainremove:
    host=host.split('.')[0]

query="SELECT glpi_computers.name,glpi_states.name,glpi_plugin_customfields_computers.%s \
FROM glpi_plugin_customfields_computers,glpi_computers,glpi_states \
WHERE glpi_states.id=glpi_computers.states_id \
AND glpi_computers.name='%s' \
AND glpi_plugin_customfields_computers.id=glpi_computers.id"%(puppetrole,host)

cur.execute(query)

# print all the first cell of all the rows
#print "a"
rows=cur.fetchall()
if len(rows)!=1:
    sys.stderr.write("query returned %s results. Expecting 1\n"%len(rows))
    sys.exit(1)
host=rows[0][0]
env=rows[0][1].replace(' ','-')
role=rows[0][2]
print "---"
print "   environment: %s"%env
if role!=None:
    print "   classes: %s"%role
