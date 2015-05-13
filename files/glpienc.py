#!/bin/env python
import MySQLdb
import sqlite3
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

def mysql_cursor():
    global dbhost
    global dbyser
    global dbpasswd
    global dbname
    db = MySQLdb.connect(host=dbhost, # your host, usually localhost
                         user=dbuser, # your username
                         passwd=dbpasswd, # your password
                         db=dbname) # name of the data base
    return db.cursor() 

def hostlist_fromdb(cur):
    query="SELECT glpi_computers.name FROM glpi_computers"
    cur.execute(query)
    rows.cur.fetchall()
    return rows

def yaml_fromdb(cur,host):
    global puppetrole
    query="SELECT glpi_computers.name,glpi_states.name,glpi_plugin_customfields_computers.%s \
FROM glpi_plugin_customfields_computers,glpi_computers,glpi_states \
WHERE glpi_states.id=glpi_computers.states_id \
AND glpi_computers.name='%s' \
AND glpi_plugin_customfields_computers.id=glpi_computers.id"%(puppetrole,host)
    cur.execute(query)
    rows=cur.fetchall()
    yaml=""
    if len(rows)!=1:
        sys.stderr.write("query returned %s results. Expecting 1\n"%len(rows))
        sys.exit(1)
    host=rows[0][0]
    env=rows[0][1].replace(' ','-')
    role=rows[0][2]
    yaml="---\n   environment: %s"%env
    if role!=None:
        yaml=yaml+"\n   classes: %s"%role
        yaml=yaml+"\n   parameters:"
        yaml=yaml+"\n      role: %s"%role.split('::')[1]
    return yaml

def sqlite_cursor():
    global falbackfile
    con=sqlite3.connect(fallbackfile)
    return con.cursor()

def yaml_fromsqlite(cur,host):
    global cur
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    return data

source=''
try:
    cur=connect_to_mysql()
    source='mysql'
except MySQLdb.OperationalError as e:
    source='sqlite'
    sys.stderr.write("Connecting to the DB failed with the following error:\n")
    sys.stderr.write(e[1]+"\n")
    sys.stderr.write("Falling-back to SQLLite backup\n")

host=sys.argv[1]
if domainremove:
    host=host.split('.')[0]

if source=='mysql':
    yaml=yaml_fromdb(cur,host)
if source='sqlite':
    cur=sqlite_cursor()
    yaml=yaml_fromsqlite(cur,host)
    
# replace into hostyaml values ('sdsdff','sdsdff');
