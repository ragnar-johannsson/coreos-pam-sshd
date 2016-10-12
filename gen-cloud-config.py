#!/usr/bin/env python

import StringIO

FILENAME = 'cloud-config.yml'

UNITS= [
    ('sshd.socket', 'host-files/sshd.socket', 'restart', 'runtime: true'),
    ('pam-sshd.service', 'host-files/pam-sshd.service', 'start', ''),
]

FILES = [
    ('host-files/pam-sshd-prep', '/opt/pam-sshd-prep', "0755"),
    ('host-files/default.pam-sshd', '/etc/default/pam-sshd', "0644"),
    ('host-files/sshd_config', '/etc/ssh/sshd_config', "0644"),
]

HEADER = '''#cloud-config
coreos:
  units:'''

UNIT_HEADER = '''
- name: "%s"
  command: "%s"
  %s
  content: |
'''

WRITE_FILES_HEADER = '''
write_files:'''

FILES_HEADER = '''
- path: "%s"
  permissions: "%s"
  owner: "root"
  content: |
'''

def write(content, dst, indent):
    for line in content.readlines():
        level = (indent+len(line)) if (len(line) > 1) else 0
        dst.write("%*s" % (level, line))

with open(FILENAME, 'w') as config:
    write(StringIO.StringIO(HEADER), config, 0)
    for name, src_path, command, extras in UNITS:
        with open(src_path, 'r') as unit:
            write(StringIO.StringIO(UNIT_HEADER % (name, command, extras)), config, 4)
            write(unit, config, 8)

    write(StringIO.StringIO(WRITE_FILES_HEADER), config, 0)
    for src_path, dst_path, mode in FILES:
        with open(src_path, 'r') as src_file:
            write(StringIO.StringIO(FILES_HEADER % (dst_path, mode)), config, 2)
            write(src_file, config, 6)
