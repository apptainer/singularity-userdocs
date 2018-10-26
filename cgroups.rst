.. _cgroups:

=========================================
Limiting container resources with cgroups
=========================================

Starting in Singularity 3.0, users have the ability to limit container resources
using cgroups.

--------
Overview
--------

Singularity cgroups support can be configured and utilized via a TOML file. An 
example file is typically installed at 
``/usr/local/etc/singularity/cgroups/cgroups.toml``.  You can copy and edit this
file to suit your needs.  Then when you need to limit your container resources, 
apply the settings in the TOML file by using the path as an argument to the 
``--apply-cgroups`` option like so:

.. code-block:: none

    $ singularity shell --apply-cgroups /path/to/cgroups.toml

The ``--apply-cgroups`` option can only be used with root privileges.

--------
Examples
--------

Limiting memory
===============

Limit the amount of memory that your container uses to 500MB (524288000 bytes).
First, create a ``cgroups.toml`` file like this and save it in your home
directory.

.. code-block:: none

    [memory]
        limit = 524288000

Start your container like so:

.. code-block:: code

    $ sudo singularity instance start --apply-cgroups /home/$USER/cgroups.toml \
        my_container.sif instance1

After that, you can verify that the container is only using 500MB of memory.  
(This example assumes that ``instance1`` is the only running instance.)

.. code-block:: code
    
    $ cat /sys/fs/cgroup/memory/singularity/*/memory.limit_in_bytes
    524288000

Limiting CPU
============

Limiting IO
===========

Cleanup
=======

After you are finished with one of these examples, be sure to cleanup your 
instance with the following command.  

.. code-block:: code

    $ sudo singularity instance stop instance1

