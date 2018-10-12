.. _networking:

======================
Network virtualization
======================

.. _sec:networking:

Singularity 3.0 introduces full integration with 
`CNI <https://github.com/containernetworking/cni>`_, and several new features to
make network virtualization easy and convenient.  

Several new options have been added to the action commands (``exec``, ``run``, 
and ``shell``) to facilitate these features, and the ``--net`` option has been
updated as well.  These options can only be used by root.

``--net``
=========

Passing the ``--net`` flag will cause the container to join a new network
network namespace when it initiates.  Starting in Singularity 3.0 a new bridge 
interface will also be set up by default.

.. code-block:: none

    $ hostname -I
    10.0.2.15

    $ sudo singularity exec --net my_container.sif hostname -I
    10.22.0.4

``--dns``
=========

The ``--dns`` option allows you to specify a comma separated list of DNS servers
to add to the ``/etc/resolv.conf`` file.

.. code-block:: none

    $ nslookup sylabs.io | grep Server
    Server:		127.0.0.53

    $ sudo singularity exec --dns 8.8.8.8 ubuntu.sif nslookup sylabs.io | grep Server
    Server:		8.8.8.8
ß
``--hostname``
==============

The ``--hostname`` option accepts a string argument to change the hostname
within the container. 

    $ hostname
    ubuntu-bionic

    $ sudo singularity exec --hostname hal-9000 my_container.sif hostname
    hal-9000

    $ sudo singularity exec --dns 8.8.8.8 ubuntu.sif cat /etc/resolv.conf
    nameserver 8.8.8.8

``network``
===========

Accepted strings include:
vlan, veth, vcan, dummy, ifb, macvlan, macvtap, bridge (default), bond, ipoib, 
ip6tnl, ipip, sit, vxlan, gre, gretap, ip6gre, ip6gretap, vti, nlmon, 
bond_slave, ipvlan

specify desired network type separated by
commas, each network will bring up a
dedicated interface inside container
(default "bridge")

``network-args``
================

specify network arguments to pass to CNI plugins