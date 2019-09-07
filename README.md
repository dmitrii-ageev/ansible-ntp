dmitrii-ageev.ntp
=================

Ansible role for RHEL/CentOS. It installs the Network Time Protocol daemon (ntpd), 
software that maintains the system time in synchronization with time servers.

Requirements
------------

The role dmitrii-ageev.logrotate is used to configure logrotate settings.

Example Playbook
----------------

```
#
# playbook.yml
#
- name: Install NTP server
  hosts: server.domain.net
  become: true
  
  roles:
      - role: dmitrii-ageev.ntp
        ntp__service_options: "-I 127.0.0.1 -g -u {{ ntp__user }}:{{ ntp__group }} -p {{ ntp__pid_file }} -f {{ ntp__drift_file }}"
        ntp__restrict:
          - "-4 default kod notrap nomodify nopeer noquery"
          - "127.0.0.1"
          - "source notrap nomodify noquery"
        ntp__servers:
          - "0.centos.pool.ntp.org iburst"
          - "1.centos.pool.ntp.org iburst"
```

License
-------

GNU General Public License v2.0

Author Information
------------------

Dmitrii Ageev <d.ageev@gmail.com>

