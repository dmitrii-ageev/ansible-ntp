import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_os_type(host):
    assert host.system_info.type == 'linux', 'Only the Linux operating system is supported!'


def test_package(host):
    # Get the scheduler daemon name
    package_name = 'ntp'
    service_name = 'ntpd'

    # Check if the system has cron daemon installed, enabled, up and running
    assert host.package(package_name).is_installed, 'The %s package should be installed.' % package_name
    assert host.service(service_name).is_running, 'The %s daemon should be running.' % service_name
    assert host.service(service_name).is_enabled, 'The %s service should be enabled.' % service_name

    # Check if a system configuration file exists
    system_configuration = host.file('/etc/sysconfig/%s' % service_name)
    assert system_configuration.exists, 'The system configuration file should exists.'

    # Logrotate package should be installed
    assert host.package('logrotate').is_installed, 'The logrotate package should be installed.'
    # Check logrotate file
    logrotate_configuration = host.file('/etc/logrotate.d/%s' % package_name)
    assert logrotate_configuration.exists, 'The logrotate configuration file should exists.'

    # Check ntpstats directory
    assert host.file('/var/lib/ntpstats').exists, 'The ntpstats directory should exists.'


def test_configuration(host):
    # Configuration file must be in place
    configuration = host.file('/etc/ntp.conf')
    assert configuration.exists, 'The configuration file should exists.'
    assert configuration.user == 'ntp'
    assert configuration.group == 'ntp'
    assert configuration.mode == 0o640

    # Check group and user
    group = host.group('ntp')
    assert group.exists, 'The daemon group should exists.'

    user = host.user('ntp')
    assert user.exists, 'The daemon user should exists.'
