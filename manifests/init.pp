class glpienc (
  $dbuser,
  $dbhost,
  $dbpasswd,
  $dbname,
  $puppetrole,
  $statusasenv    = true,
  $domainremove   = false,
  $enablefallback = true,
  $fallbackfile   = '/var/local/glpienc/glpienc.db',
)
{
  file{'/etc/glpienc':
    ensure => directory,
  }

  file{'/var/local/glpienc':
    ensure => directory,
  }

  file{'/var/local/glpienc/sqlite-schema.sql':
    ensure => present,
    source => 'puppet:///modules/glpienc/sqlite-schema.sql',
  }
  
  file{'/etc/glpienc/config.py':
    ensure  => present,
    content => template('glpienc/config.erb'),
    require => File['/etc/glpienc']
  }
  
  file{'/usr/bin/glpienc.py':
    ensure  => present,
    mode    => '0755',
    source  => 'puppet:///modules/glpienc/glpienc.py',
  }
  
}
