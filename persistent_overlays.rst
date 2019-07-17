===================
Persistent Overlays
===================

Persistent overlay directories allow you to overlay a writable file system on an
immutable read-only container for the illusion of read-write access.


--------
Overview
--------

A persistent overlay is a directory or file system image that “sits on top” of 
your compressed, immutable SIF container. When you install new software or 
create and modify files the overlay stores the changes.

If you want to use a SIF container as though it were writable, you can create a
directory or an ext3 file system image to use as a persistent overlay. Then you 
can specify that you want to use the directory or image as an overlay at runtime 
with the ``--overlay`` option.

You can use persistent overlays with the following commands:

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

Then you must create a directory or ext3 file system image to use as your 
overlay.

You can create a directory in the normal way:

.. code-block:: none

    $ mkdir my_overlay

Or tools like ``dd`` and ``mkfs.ext3`` to create and format an empty ext3 file
system image:

.. code-block:: none

    $ dd if=/dev/zero of=my_overlay bs=1M count=500 && \
        mkfs.ext3 my-overlay

The second example creates an ext3 file system image with 500MBs of empty space.

Now you can use this overlay with your container, though filesystem permissions
still control where you can write.  

.. note::

    For security reasons, you must be root to use a bare directory as an
    overlay. ext3 file system images can be used as overlays without root
    privileges.  

.. code-block:: none

    $ sudo singularity shell --overlay my_overlay/ ubuntu.sif

    Singularity ubuntu.sif:~> mkdir /data

    Singularity ubuntu.sif:~> chown user /data

    Singularity ubuntu.sif:~> apt-get update && apt-get install -y vim

    Singularity ubuntu.sif:~> which vim
    /usr/bin/vim

    Singularity ubuntu.sif:~> exit


You will find that your changes persist across sessions as though you were using
a writable container.

.. code-block:: none

    $ singularity shell --overlay my_overlay/ ubuntu.sif

    Singularity ubuntu.sif:~> ls -lasd /data
    4 drwxr-xr-x 2 user root 4096 Apr  9 10:21 /data

    Singularity ubuntu.sif:~> which vim
    /usr/bin/vim

    Singularity ubuntu.sif:~> exit


If you mount your container without the ``--overlay`` directory, your changes
will be gone.

.. code-block:: none

    $ singularity shell ubuntu.sif

    Singularity ubuntu.sif:~> ls /data
    ls: cannot access 'data': No such file or directory

    Singularity ubuntu.sif:~> which vim

    Singularity ubuntu.sif:~> exit

------------------------------
A note on resizing ext3 images
------------------------------

Singularity v2 provided built-in support for creating and resizing ext3 file 
system images, but with the adoption of SIF as the default container format,
this support was dropped.  

Luckily, you can use standard Linux tools to manipulate ext3 images. For
instance, to resize the 500MB file created above to 700MB one could use the 
``e2fsck`` and ``resize2fs`` utilities like so:

.. code-block:: none

    $ e2fsck -f my_overlay && \
        resize2fs my_overlay 700M

Hints for creating and manipulating ext3 images on your distribution are readily
available online and are not treated further in this manual.  