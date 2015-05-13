# GLPIEnc - Puppet ENC from GLPI

This code makes possible to use [GLPI](http://www.glpi-project.org/spip.php?lang=en) as an [ENC](https://docs.puppetlabs.com/guides/external_nodes.html) for Puppet.

The basic idea is that:
 
 - a `node` in Puppet is a `computer` in GLPI;
 - the `environment` of a node in Puppet is the `state` (eg. `production`, `new`, `dev`, `retired`) of the computer in GLPI;
 - `role` in Puppet is a [custom field](http://www.glpi-project.org/wiki/doku.php?id=en:plugins:customfields_use) in GLPI (eg. `puppetrole`).

If you have a running GLPI with the *custom fields* plugin,
the necessary informations for the given host `hostname` can be extracted directly from the GLPI database with the following query:

    SELECT glpi_computers.name,
           glpi_states.name,
           glpi_plugin_customfields_computers.puppetrole 
      FROM glpi_plugin_customfields_computers,
           glpi_computers,
           glpi_states
     WHERE glpi_states.id=glpi_computers.states_id
       AND glpi_computers.name='hostname'
       AND glpi_plugin_customfields_computers.id=glpi_computers.id;


*glpienc* is provided as a puppet module, that will be usually installed on the puppet master.

To install it you need information access to the GLPI database, ie:

 - `dbhost`: the host hosting the GLPI MySQL database;
 - `dbuser`: the user to access the db;
 - `dbpasswd`: its password;
 - `dbname`: the database name (tipically `glpi`);
 - `puppetrole`: the name of the *custom field* used for storing puppet roles.

Consider that is safer to create a special DB user for this task, giving it select-only access to the DB.

There is also the optional parameter `domainremove`, that defaults to `false`.
If this parameter is set to `true`
the query against the database will be made only for the hostname part, without the domain part, ie. if 
you invoke the ENC against `my-hostname.domain.at.com` the query on the database will be performed for
`my-hostname` only. This is an useful option since puppet uses FQDN while maybe you don't keep the FQDN
inside GLPI (tipical inside a single domain case).

*glpienc* has also a fallback mechanism, ie. every time it is invoked if it can access the GLPI database
will make a copy of it on a SQLite database file. It will not copy everything but just the *yaml* associated
to a host.
So, as soon as it cannot access the GLPI database, *glpienc* will fallback to the SQLite database for retrieving
the hosts yaml.

To install inside puppet:

    class {'glpienc':
   	  dbuser       => 'glpi-user',
	  dbhost       => 'glpi-host',
	  dbpasswd     => 'glpi-passwd',
	  dbname       => 'glpi',
	  puppetrole   => 'puppetrole',
	  domainremove => true,
    }

The default location of the fallback file is `/var/local/glpienc/glpienc.db` but you can change by passing
the `fallbackfile` parameter on the class.

### Requirements

MySQL SQLite 3 Python libraries.