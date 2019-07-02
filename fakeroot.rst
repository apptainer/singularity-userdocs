.. _fakeroot:

================
Fakeroot feature
================

--------
Overview
--------

Fakeroot feature (or commonly referred as rootless mode) allows an unprivileged user
to run a container as a **"fake root"** user by leveraging
`user namespace UID/GID mapping <http://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_.

.. note:: 

	This feature requires a Linux kernel >= 3.8, but the recommended version is >= 3.18

A **"fake root"** user has almost the same administrative rights as root but only **inside the container**
and the **requested namespaces**, which means that this user:

  - can set different user/group ownership for files or directories he owns
  - can change user/group identity with su/sudo commands
  - has full privileges inside the requested namespaces (network, ipc, uts)

---------------------
Restrictions/security
---------------------

Filesystem
==========

A **"fake root"** user can't access or modify files and directories for which he doesn't
have already access or rights on the host filesystem, so a **"fake root"** user won't be able
to access to host file like ``/etc/shadow`` or host ``/root`` directory.

Additionally, all files or directories created with **"fake root"** user are owned like
``root:root`` inside container and are owned like ``user:group`` outside of container.
Let's see the following example, in this case "user" is authorized to use the fakeroot feature
and can use 65536 UIDs starting at 131072 (same thing for GIDs).

+----------------------+-----------------------+
| UID inside container | UID outside container |
+======================+=======================+
| 0 (root)             | 1000 (user)           |
+----------------------+-----------------------+
| 1 (daemon)           | 131072 (non-existent) |
+----------------------+-----------------------+
| 2 (bin)              | 131073 (non-existent) |
+----------------------+-----------------------+
| ...                  | ...                   |
+----------------------+-----------------------+
| 65536                | 196607                |
+----------------------+-----------------------+

Which means if **"fake root"** user creates a file a ``bin`` user in container, this file will
be owned by ``131073:131073`` outside of container. The responsibility relies on the administrator
to ensure that there is no overlap with the current user's UID/GID on the system.

Network
=======

Restrictions are also applied for network, if ``singularity`` is executed without ``--net`` flag,
the **"fake root"** user won't be able to use ``ping`` or bind a container service on a port below
than 1024.

With ``--net`` the **"fake root"** user has full privileges in this dedicated network, inside
the container network he can bind on privileged ports below 1024, use ping, manage firewall rules,
listen traffic ...
And everything done in this dedicated network won't affect the host network.

.. note:: 
    Of course an unprivileged user could not map host ports below than 1024 by using:
    ``--network-args="portmap=80:80/tcp"``

-----
Usage
-----

By default fakeroot feature is disabled for all users, it requires that your username is added in
``fakeroot allowed users`` list in ``singularity.conf``, if you can't add it yourself, ask to an
administrator.

Then you could use it with ``--fakeroot`` or ``-f`` option, this option is available with singularity commands :

  - ``shell``
  - ``exec``
  - ``run``
  - ``instance start``
  - ``build``

Build
=====

With fakeroot an unprivileged user can now build image from a definition file with few restrictions, bootstrap
methods requiring to create block devices (like ``/dev/null``) won't work as **"fake root"** user is not allowed to
create block devices, so bootstrap methods like ``debootstrap``, ``yum``, ``zypper`` doesn't work with ``--fakeroot``
option.

Examples
========

Build from a definition file:
-----------------------------

.. code-block:: none

    singularity build --fakeroot /tmp/test.sif /tmp/test.def

Ping from container:
--------------------

.. code-block:: none

    singularity exec --fakeroot --net docker://alpine ping -c1 8.8.8.8

HTTP server:
------------

.. code-block:: none

    singularity run --fakeroot --net --network-args="portmap=8080:80/tcp" -w docker://nginx