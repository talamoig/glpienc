# Puppet ENC from GLPI

This code makes possible to use [GLPI](http://www.glpi-project.org/spip.php?lang=en) as an [ENC](https://docs.puppetlabs.com/guides/external_nodes.html) for Puppet.

The basic idea is that:
 
 - a `node` in Puppet is a `computer` in GLPI;
 - the `environment` of a node in Puppet is the `state` (eg. `production`, `new`, `dev`, `retired`) of the computer in GLPI;
 - `role` in Puppet is a [custom field](http://www.glpi-project.org/wiki/doku.php?id=en:plugins:customfields_use) in GLPI (eg. `puppetrole`).

If you have a running GLPI with the *custom fields* plugin:

 - installed
 - enabled
 - a custom field defined on Computers with `puppetrole` as System Name

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

### Requirements

MySQL Python library.