===================
Persistent Overlays
===================

Persistent overlay directories allow you to overlay a writable file system on an
immutable read-only container for the illusion of read-write access.


--------
Overview
--------

A persistent overlay is a directory that “sits on top” of your compressed,
immutable SIF container. When you install new software or create and modify
files the overlay directory stores the changes.

If you want to use a SIF container as though it were writable, you can create a
directory to use as a persistent overlay. Then you can specify that you want to
use the directory as an overlay at runtime with the ``--overlay`` option.

You can use a persistent overlays with the following commands:

- ``run``
- ``exec``
- ``shell``
- ``instance.start``

-----
Usage
-----

To use a persistent overlay, you must first have a container.

.. code-block:: none

    $ sudo singularity build ubuntu.sif library://ubuntu

Then you must create a directory. (You can also use the ``--overlay`` option
with a legacy writable ext3 image.)

.. code-block:: none

    $ mkdir my_overlay

Now you can use this overlay directory with your container. Note that it is
necessary to be root to use an overlay directory.

.. code-block:: none

    $ sudo singularity shell --overlay my_overlay/ ubuntu.sif

    Singularity ubuntu.sif:~> touch /foo

    Singularity ubuntu.sif:~> apt-get update && apt-get install -y vim

    Singularity ubuntu.sif:~> which vim
    /usr/bin/vim

    Singularity ubuntu.sif:~> exit


You will find that your changes persist across sessions as though you were using
a writable container.

.. code-block:: none

    $ sudo singularity shell --overlay my_overlay/ ubuntu.sif

    Singularity ubuntu.sif:~> ls /foo
    /foo

    Singularity ubuntu.sif:~> which vim
    /usr/bin/vim

    Singularity ubuntu.sif:~> exit


If you mount your container without the ``--overlay`` directory, your changes
will be gone.

.. code-block:: none

    $ sudo singularity shell ubuntu.sif

    Singularity ubuntu.sif:~> ls /foo
    ls: cannot access 'foo': No such file or directory

    Singularity ubuntu.sif:~> which vim

    Singularity ubuntu.sif:~> exit
