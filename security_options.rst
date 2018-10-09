.. _security-options:

================
Security Options
================

.. _sec:security_options:

Singularity 3.0 introduces many new security related options to the container 
runtime.  This document will describe the new methods users have for specifying
the security scope and context when running Singularity containers.

------------------
Linux Capabilities
------------------

Singularity provides full support for granting and revoking Linux capabilities 
on a user or group basis.  For example, let us suppose that an admin has 
decided to grant a user capabilities to open raw sockets so that they can use
``ping`` in a container where the binary is controlled via capabilities (i.e. a
recent version of CentOS).  

To do so, the admin would issue a command such as this:

.. code-block:: none

    $ sudo singularity capability add --user david CAP_NET_RAW

This means the user ``david`` has just been granted permissions (through Linux
capabilities) to open raw sockets within Singularity containers.

To take advantage of this new capability, the user ``david`` must also request
the capability when executing a container with the ``--add-caps`` flag like so:

.. code-block:: none

    $ singularity exec --add-caps CAP_NET_RAW library://centos ping -c 1 8.8.8.8
    PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
    64 bytes from 8.8.8.8: icmp_seq=1 ttl=128 time=18.3 ms

    --- 8.8.8.8 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 18.320/18.320/18.320/0.000 ms

If the admin decides that it is no longer necessary to allow the user ``dave``
to open raw sockets within Singularity containers, they can revoke the 
appropriate Linux capability like so:

.. code-block:: none

    $ sudo singularity capability drop --user david CAP_NET_RAW

-------------------------------
Security related action options
-------------------------------

Singularity 3.0 introduces many new flags that can be passed to the action
commands; ``shell``, ``exec``, and ``run`` allowed fine grained control of
security related considerations.  

``--add-caps``
==============

As explained above, ``--add-caps`` will "activate" Linux capabilities when a 
container is initiated, providing those capabilities have been granted to the 
user by an administrator using the ``capability add`` command.

``--allow-setuid``
==================

The SetUID bit allows a program to be executed as the user that owns the binary.
The most well-known SetUID binaries are owned by root and allow a user to
execute a command with elevated priviledges.  But other SetUID binaries may 
allow a user to execute a command as a service account.  

By defualt SetUID is disallowed within Singularity containers as a security 
precaution.  But the root user can override this precaution and allow SetUID
binaries to behave as expected within a Singularity container with the 
``--allow-setuid`` option like so:

.. code-block:: none

    $ sudo singularity shell --allow-setuid some_container.sif 

``--apply-cgroups``
===================

``--keep-privs``
================

``--drop-privs``
================

``--security``
==============