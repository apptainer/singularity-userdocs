
.. _bind-paths-and-mounts:

=====================
Bind Paths and Mounts
=====================

.. _sec:bindpaths:

If `enabled by the system administrator <https://singularity-admindoc.readthedocs.io/en/latest/the_singularity_config_file.html#user-bind-control-boolean-default-yes>`_, 
Singularity allows you to map directories on your host system to directories 
within your container using bind mounts. This allows you to read and write data 
on the host system with ease.

--------
Overview
--------

When Singularity ‘swaps’ the host operating system for the one inside your 
container, the host file systems becomes inaccessible. But you may want to read 
and write files on the host system from within the container. To enable this 
functionality, Singularity will bind directories back into the container via two 
primary methods: system-defined bind paths and user-defined bind paths.

-------------------------
System-defined bind paths
-------------------------

The system administrator has the ability to define what bind paths will be 
included automatically inside each container. Some bind paths are automatically 
derived (e.g. a user’s home directory) and some are statically defined (e.g. 
bind paths in the Singularity configuration file). In the default 
configuration, the directories ``$HOME`` , ``/tmp`` , ``/proc`` , ``/sys`` , 
``/dev``, and ``$PWD`` are among the system-defined bind paths.

-------------------------
User-defined bind paths
-------------------------

If the system administrator has `enabled user control of binds <https://singularity-admindoc.readthedocs.io/en/latest/the_singularity_config_file.html#user-bind-control-boolean-default-yes>`_, 
you will be able to request your own bind paths within your container.

Many of the Singularity commands such as ``run``, ``exec`` , and ``shell`` will 
accept the ``--bind/-B`` command-line option to specify bind paths, and will 
also honor the ``$SINGULARITY_BIND`` (or ``$SINGULARITY_BINDPATH``) environment 
variable. The argument for this option  is a comma-delimited string of bind path 
specifications in the format  ``src[:dest[:opts]]``, where ``src`` and ``dest`` 
are paths outside and inside  of the container respectively. If ``dest`` is not 
given, it is set equal to  ``src``. Mount options (``opts``) may be specified as 
``ro`` (read-only) or ``rw`` (read/write, which is the default). The 
``--bind/-B`` option can be specified multiple times, or a comma-delimited 
string of bind path specifications can be used.

Specifying bind paths
=====================

Here’s an example of using the ``--bind`` option and binding ``/data`` on the 
host to ``/mnt`` in the container (``/mnt`` does not need to already exist in 
the container):

.. code-block:: none

    $ ls /data
    bar  foo

    $ singularity exec --bind /data:/mnt my_container.sif ls /mnt
    bar  foo

You can bind multiple directories in a single command with this syntax:

.. code-block:: none

    $ singularity shell --bind /opt,/data:/mnt my_container.sif

This will bind ``/opt`` on the host to ``/opt`` in the container and ``/data`` 
on the host to ``/mnt`` in the container. 

Using the environment variable instead of the command line argument, this would 
be:

.. code-block:: none

    $ export SINGULARITY_BIND="/opt,/data:/mnt"

    $ singularity shell my_container.sif

Using the environment variable ``$SINGULARITY_BIND``, you can bind paths even 
when you are running your container as an executable file with a runscript. If 
you bind many directories into your Singularity containers and they don’t 
change, you could even benefit by setting this variable in your ``.bashrc`` 
file.

A note on using ``--bind`` with the ``--writable`` flag
=======================================================

To mount a bind path inside the container, a *bind point* must be defined 
within the container. The bind point is a directory within the container that 
Singularity can use as a destination to bind a directory on the host system. 

Starting in version 3.0, Singularity will do its best to bind mount requested 
paths into a container regardless of whether the appropriate bind point exists 
within the container.  Singularity can often carry out this operation even in 
the absence of the "overlay fs" feature.  

However, binding paths to non-existent points within the container can result in 
unexpected behavior when used in conjuction with the ``--writable`` flag, and is 
therefore disallowed. If you need to specify bind paths in combination with the 
``--writable`` flag, please ensure that the appropriate bind points exist within 
the container. If they do not already exist, it will be necessary to modify the 
container and create them.