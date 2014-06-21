ip_assembler
============

This is a project that gathers together all IPs that are being reported as banned by the Wordpress plugins

* Better WP Security (now iThemes Security and not working any more)
* Login Security Solution

The IPs are taken from a mailbox where the plugins send their mails to. The mails are parsed, the IP(s) extracted and added to the database.

There is a "unification" of the IPs, that means the following IPs

* 10.10.10.10
* 10.10.10.11
* 10.10.10.12
* 10.10.10.13
* 10.10.10.14

will be merged to the "IP" 10.10.10.*. So instead of the 5 single IPs there will be only a single wildcard IP. This will work for at least 3 IPs being in a group.

You can specify the paths to Wordpress .htaccess files on the host the ip_assembler is running. This will result in adjusting all these .htaccess files if there
are new IPs added and the number of new IPs is greater than 10 (default) or settings.IP_ASSEMBLER_IP_CHANGED_THRESHOLD.

The number of IPs of the last update of .htaccess files is saved in settings.IP_ASSEMBLER_IP_CHANGED_FILE (default: /tmp/ipa-last).

For each IP, the following will be added

.. code-block:
    SetEnvIF REMOTE_ADDR <IP> DenyAccess
    SetEnvIF X-FORWARDED-FOR <IP> DenyAccess
    SetEnvIF X-CLUSTER-CLIENT-IP <IP> DenyAccess

The place where this will be put is determined by checking if "SetEnvIF REMOTE_ADDR ..." already is there. If so, this is the start position.
The last "SetEnvIF X-CLUSTER-CLIENT-IP" is the end position. Everything in between will be updated with the IPs from the database. If the .htaccess does not
contain these entries, than the content will be written to the beginning of the file.