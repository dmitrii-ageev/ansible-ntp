import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_os_type(host):
    assert host.system_info.type == 'linux', 'Only the Linux operating system is supported!'


def test_package(host):
    # Set the package and daemon name
    package_name = 'ntp'
    service_name = 'ntpd'

    # Check if the system has cron daemon installed, enabled, up and running
    assert not host.service(service_name).is_running, 'The %s daemon should be stopped.' % service_name
    assert not host.service(service_name).is_enabled, 'The %s service should be disabled.' % service_name
    assert not host.package(package_name).is_installed, 'The %s package should be removed.' % package_name

    # Check if a system configuration file exists
    system_configuration = host.file('/etc/sysconfig/%s' % service_name)
    assert not system_configuration.exists, 'The system configuration file should be removed.'

    # Logrotate package should still be installed
    assert host.package('logrotate').is_installed, 'The logrotate package should be installed.'
    # Check logrotate file
    logrotate_configuration = host.file('/etc/logrotate.d/%s' % package_name)
    assert not logrotate_configuration.exists, 'The logrotate configuration file should be removed.'

    # Check ntpstats directory
    assert not host.file('/var/lib/ntpstats').exists, 'The ntpstats directory should be removed.'


def test_configuration(host):
    # A configuration file must be removed
    configuration = host.file('/etc/ntp.conf')
    assert not configuration.exists, 'The configuration file should be removed.'


def test_logs(host):
    # Check for logs
    log = host.file('/var/log/ntp')
    assert not log.exists, 'The log directory should be removed.'
