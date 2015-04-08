class glpienc (
  $dbuser,
  $dbhost,
  $dbpasswd,
  $dbname,
  $puppetrole,
  $domainremove = false,
)
{
  file{'/etc/glpienc':
    ensure => directory,
  }
  
  file{'/etc/glpienc/config.py':
    ensure  => present,
    content => template('glpienc/config.erb'),
    require => File['/etc/glpienc']
  }
  
  file{'/usr/bin/glpienc.py':
    ensure  => present,
    mode    => 0755,
    source  => 'puppet:///modules/glpienc/glpienc.py',
  }
  
}
