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
directory, an ext3 file system image, or embed an ext3 file system image in SIF to use as a persistent overlay. Then you 
can specify that you want to use the directory or image as an overlay at runtime 
with the ``--overlay`` option, or ``--writable`` if you want to use the overlay embedded in SIF.

If you want to make changes to the image, but do not want them to persist, use the ``--writable-tmpfs`` option.

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

File system image overlay
=========================

You can use tools like ``dd`` and ``mkfs.ext3`` to create and format an empty ext3 file
system image:

.. code-block:: none

    $ dd if=/dev/zero of=overlay.img bs=1M count=500 && \
        mkfs.ext3 overlay.img

The second example creates an ext3 file system image with 500MBs of empty space.

Now you can use this overlay with your container, though filesystem permissions
still control where you can write.

.. code-block:: none

   $ sudo singularity shell --overlay overlay.img ubuntu.sif

Directory overlay
=================

Create a directory as usual:

.. code-block:: none

    $ mkdir my_overlay

.. note::

    For security reasons, you must be root to use a bare directory as an
    overlay. ext3 file system images can be used as overlays without root
    privileges.

The example below shows the directory overlay in action.

.. code-block:: none

    $ sudo singularity shell --overlay my_overlay/ ubuntu.sif

    Singularity ubuntu.sif:~> mkdir /data

    Singularity ubuntu.sif:~> chown user /data

    Singularity ubuntu.sif:~> apt-get update && apt-get install -y vim

    Singularity ubuntu.sif:~> which vim
    /usr/bin/vim

    Singularity ubuntu.sif:~> exit

Overlay embedded in SIF
=======================

It is possible to embed the overlay image in the SIF image.
In order to do that, you must first create a file system image.

.. code-block:: none

    $ dd if=/dev/zero of=overlay.img bs=1M count=500 && \
        mkfs.ext3 overlay.img

Then, you can add the overlay to the SIF image using the ``siftool`` functionality of Singularity.

.. code-block:: none

   $ singularity siftool add --datatype 4 --partfs 2 --parttype 4 --partarch 2 --groupid 1 ubuntu_latest.sif overlay.img

Below is the explanation what each parameter means, and how it can possibly affect the operation:

- ``datatype`` determines what kind of an object we attach, e.g. a definition file, environment variable, signature.
- ``partfs`` should be set according to the partition type, e.g. SquashFS, ext3, raw.
- ``parttype`` determines the type of partition. In our case it is being set to overlay.
- ``partarch`` must be set to the architecture against you're building. In this case it's ``amd64``.
- ``groupid`` is the ID of the container image group. In most cases there's no more than one group, therefore we can assume it is 1.

All of these options are documented within the CLI help. Access it by running ``singularity siftool add --help``.

After you've completed the steps above, you can shell into your container with the ``--writable`` option.

.. code-block:: none

        $ sudo singularity shell --writable ubuntu_latest.sif

Final note
==========

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
