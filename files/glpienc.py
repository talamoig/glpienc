#!/bin/env python
import MySQLdb
import sqlite3
import sys
import os

if len(sys.argv)!=2:
    sys.stderr.write("Usage: %s <hostname>\n"%sys.argv[0])
    sys.exit(1)

configfiles=['/etc/glpienc/config.py', 'config.py']

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
    query="SELECT glpi_computers.name FROM glpi_computers WHERE is_template=0 AND is_deleted=0"
    cur.execute(query)
    rows=cur.fetchall()
    rows=[r[0] for r in rows]
    return rows

def yaml_fromdb(cur,host):
    query="SELECT glpi_computers.name,glpi_states.name,glpi_groups.name \
FROM glpi_computers, glpi_groups, glpi_states \
WHERE is_template=0 AND is_deleted=0 \
AND glpi_computers.name='%s' \
AND glpi_computers.groups_id=glpi_groups.id AND glpi_states.id=glpi_computers.states_id"%host
    cur.execute(query)
    rows=cur.fetchall()
    yaml=""
    if len(rows)==0:
        sys.stderr.write("Warning: host '%s' not found in the db\n"%host)
        return '---\n'
    if len(rows)>1:
        sys.stderr.write("query for host %s returned %s results. Expecting 1\n"%(host,len(rows)))
        sys.stderr.write("hostname 1:"+rows[0][0])
        sys.stderr.write("hostname 1:"+rows[1][0])
        sys.exit(1)
    host=rows[0][0]
    env=rows[0][1].replace(' ','-')
    role=rows[0][2]
    yaml="---\n   environment: %s"%env
    if role!=None:
        yaml=yaml+"\n   classes:"
        yaml=yaml+"\n     - role::%s"%role
    return yaml

def sqlite_cursor():
    global fallbackfile
    global sqlite_con
    sqlite_con=sqlite3.connect(fallbackfile)
    return sqlite_con.cursor()

def yaml_fromsqlite(cur,host):
    cur.execute("SELECT yaml FROM hostyaml WHERE host='%s'"%host)
    data = cur.fetchone()
    return data[0]

def update_sqlite(cur,host,yaml):
    cur.execute("REPLACE INTO hostyaml VALUES('%s','%s')"%(host,yaml))

host=sys.argv[1]
if domainremove:
    host=host.split('.')[0]

try:
    sqlite_cur=sqlite_cursor()
except sqlite3.OperationalError as e:
    print e[1]
    sys.exit(1)

try:
    cur=mysql_cursor()
    hostlist=hostlist_fromdb(cur)
    for h in hostlist:
        yaml=yaml_fromdb(cur,h)
        update_sqlite(sqlite_cur,h,yaml)
except MySQLdb.OperationalError as e:
    sys.stderr.write("Connecting to the DB failed with the following error:\n")
    sys.stderr.write(e[1]+"\n")
    sys.stderr.write("Falling-back to SQLLite backup\n")

yaml=yaml_fromsqlite(sqlite_cur,host)
print yaml
sqlite_con.commit()
sqlite_con.close()
