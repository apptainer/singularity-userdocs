.. _build-environment:

=================
Build Environment
=================

.. _sec:buildenv:

--------
Overview
--------

You may wish to customize your build
environment by doing things such as specifying a custom cache directory for images or
sending your Docker Credentials to the registry endpoint. Here we will discuss these and other topics
related to the build environment.

-------------
Cache Folders
-------------

To make downloading images for build and :ref:`pull <pull-command>` faster and
less redundant, Singularity uses a caching strategy. By default, Singularity
will create a set of folders in your ``$HOME`` directory for Cloud library
images, Docker images, Shub images, Docker layers, net images, and oras images,
respectively:

.. code-block:: none

    $HOME/.singularity/cache/library
    $HOME/.singularity/cache/oci-tmp
    $HOME/.singularity/cache/shub
    $HOME/.singularity/cache/oci
    $HOME/.singularity/cache/net
    $HOME/.singularity/cache/oras


If you want to cache in a different directory, set ``SINGULARITY_CACHEDIR`` to
the desired path. By using the ``-E`` option with the ``sudo`` command,
``SINGULARITY_CACHEDIR`` will be passed along to root's environment and
respected during the build. Remember that when you run commands as root
images will be cached in root’s home at ``/root`` and not your user’s home.

--------------
Cache commands
--------------

Since v3.1, Singularity has introduced a new ``cache`` command to manage you
cache.

.. note::

    Running the cache commands with sudo privilege will consider cache location as ``/root/.singularity/cache``. The default location for cache without sudo privilege is ``~/.singularity/cache``.
    Make sure that if you build a container with sudo privilege, you will need to consider the sudo location from the cache, and not the default.

    For example, running the following command with sudo privilege (considering the sudo privilege location for cache ``/root/.singularity/cache``):

    .. code-block:: none

        $ sudo singularity cache list --verbose
        NAME                   DATE CREATED           SIZE             TYPE
        ubuntu_latest.sif      2019-01-31 14:59:32    28.11 Mb         library
        ubuntu_18.04.sif       2019-01-31 14:58:44    27.98 Mb         library

    and then cleaning the cache without sudo privilege (``singularity cache clean -a``) will not work, since the default cache location is ``~/.singularity/cache``.
    In this case you would need to run the clean command with sudo privilege:

    .. code-block:: none

        $ sudo singularity cache clean --force

Listing Cache
=============

Since the default for ``list`` is a summary, you will need to supply a 
additional ``--verbose`` flag to get a list format:

.. code-block:: none

    $ singularity cache list --verbose
    NAME                     DATE CREATED           SIZE             TYPE
    alpine_3.9.sif           2020-01-20 12:10:48    2.72 MB          library
    alpine_latest.sif        2020-01-20 12:10:48    2.72 MB          library
    alpine_3.8.sif           2020-01-20 12:10:49    2.18 MB          library
    busybox_latest.sif       2020-01-20 12:10:48    672.70 kB        library
    alpine_3.8.sif           2020-01-20 12:10:54    2.19 MB          oci
    busybox_latest.sif       2020-01-20 12:11:07    782.34 kB        oci
    alpine_latest.sif        2020-01-20 12:11:19    2.77 MB          oci
    busybox_latest.sif       2020-01-20 12:10:47    618.53 kB        shub
    0d716090a9745a91272d29   2020-01-20 12:11:13    0.58 kB          blob
    15f9a1d6490941630beb39   2020-01-20 12:11:04    0.35 kB          blob
    20f3ac4aaa6fdf5e7f49a0   2020-01-20 12:10:52    0.58 kB          blob
    343ebab94a7674da181c6e   2020-01-20 12:11:15    0.35 kB          blob
    48e59556946cccb00d1073   2020-01-20 12:10:52    0.35 kB          blob
    b075e856be427655d946bf   2020-01-20 12:11:00    0.57 kB          blob
    bdbbaa22dec6b7fe23106d   2020-01-20 12:10:51    760.98 kB        blob
    c87736221ed0bcaa60b8e9   2020-01-20 12:10:51    2.21 MB          blob
    c9b1b535fdd91a9855fb7f   2020-01-20 12:10:51    2.80 MB          blob
    
    There are 8 container file(s) using 14.66 MB and 9 oci blob file(s) using 5.77 MB of space
    Total space used: 20.43 MB

You can also clean a specific cache type, choosing between: ``library``,
``oci-tmp``, ``shub``, ``oci``, ``net``, and ``oras`` (separated by commas)

.. code-block:: none

    # clean only library cache
    $ singularity cache --force clean --type=library

    # clean only oci cache
    $ singularity cache --force clean --type=oci

    # clean only blob cache
    $ singularity cache --force clean --type=blob

    # clean only library, and oci cache
    $ singularity cache --force clean --type=library,oci

.. note::

    This feature of passing additional types with comma-separated arguments can
    also be used with the ``singularity cache list``.

Cleaning the Cache
==================

Most of the ``cache clean`` and ``cache list`` flags can be interchanged,
(``--name`` and ``--force`` is only reserved for ``cache clean``).

By default when running ``cache clean``, you will be prompted unless you
use the ``--force`` flag.

.. code-block:: none

    $ singularity cache clean --force

.. code-block:: none

    $ singularity cache clean --dry-run

-----------------
Temporary Folders
-----------------

.. _sec:temporaryfolders:

Singularity uses a temporary directory to build the squashfs filesystem,
and this temp space needs to be large enough to hold the entire resulting Singularity image.
By default this happens in ``/tmp`` but the location can be configured by setting ``SINGULARITY_TMPDIR`` to the full
path where you want the sandbox and squashfs temp files to be stored. Remember to use ``-E`` option to pass the value of ``SINGULARITY_TMPDIR``
to root's environment when executing the ``build`` command with ``sudo``.

When you run one of the action commands (i.e. ``run``, ``exec``, or ``shell``) with a container from the
container library or an OCI registry, Singularity builds the container in the temporary directory caches it
and runs it from the cached location.

Consider the following command:

.. code-block:: none

    $ singularity exec docker://busybox /bin/sh

This container is first built in ``/tmp``. Since all the oci blobs are converted into SIF format,
by default a temporary runtime directory is created in:

.. code-block:: none

    $HOME/.singularity/cache/oci-tmp/<sha256-code>/busybox_latest.sif

In this case, the ``SINGULARITY_TMPDIR`` and ``SINGULARITY_CACHEDIR`` variables will also be respected.

-----------
Pull Folder
-----------

To customize your pull default location you can do so by specifying Singularity in which folder to pull the image, assuming you own a folder called ``mycontainers`` inside your ``$HOME`` folder
, you would need to do something like the following:

.. code-block:: none

    $ singularity pull $HOME/mycontainers library://library/default/alpine

Singularity also allows you to modify the default cache location for pulling images. By default, the location of the pull folder is given by the environment variable ``SINGULARITY_CACHEDIR``.
``SINGULARITY_CACHEDIR`` by default points to ``$HOME/.singularity/cache`` but this path can be modified. You would need to set and export the ``SINGULARITY_CACHEDIR`` environment variable before pulling the image, like so:

.. code-block:: none

   $ export SINGULARITY_CACHEDIR=$HOME/mycontainers
   $ singularity pull library://library/default/alpine

And that will successfully pull that container image inside your new ``SINGULARITY_CACHEDIR`` location.

--------------------
Encrypted Containers
--------------------

Beginning in Singularity 3.4.0 it is possible to build and run encrypted
containers.  The containers are decrypted at runtime entirely in kernel space, 
meaning that no intermediate decrypted data is ever present on disk or in 
memory.  See :ref:`encrypted containers <encryption>` for more details.

---------------------
Environment Variables
---------------------

#. If a flag is represented by both a CLI option and an environment variable, and both are set, the CLI option will always take precedence. This is true for all environment variables except for ``SINGULARITY_BIND`` and ``SINGULARITY_BINDPATH`` which is combined with the ``--bind`` option, argument pair if both are present.

#. Environment variables overwrite default values in the CLI code

#. Any defaults in the CLI code are applied.


Defaults
========

The following variables have defaults that can be customized by you via
environment variables at runtime.

Docker
------

**SINGULARITY_DOCKER_LOGIN** Used for the interactive login for Docker Hub.

**SINGULARITY_DOCKER_USERNAME** Your Docker username.

**SINGULARITY_DOCKER_PASSWORD** Your Docker password.

**RUNSCRIPT_COMMAND** Is not obtained from the environment, but is a
hard coded default (“/bin/bash”). This is the fallback command used in
the case that the docker image does not have a CMD or ENTRYPOINT.
**TAG** Is the default tag, ``latest``.

**SINGULARITY_NOHTTPS** This is relevant if you want to use a
registry that doesn’t have https, and it speaks for itself. If you
export the variable ``SINGULARITY_NOHTTPS`` you can force the software to not use https when
interacting with a Docker registry. This use case is typically for use
of a local registry.

Library
-------

**SINGULARITY_BUILDER** Used to specify the remote builder service URL. The default value is our remote builder.

**SINGULARITY_LIBRARY** Used to specify the library to pull from. Default is set to our Cloud Library.

**SINGULARITY_REMOTE** Used to build an image remotely (This does not require root). The default is set to false.

Encryption
----------

**SINGULARITY_ENCRYPTION_PASSPHRASE** Used to pass a plaintext passphrase to encrypt a container file system (with the ``--encrypt`` flag). The default is empty.

**SINGULARITY_ENCRYPTION_PEM_PATH** Used to specify the location of a public key to use for container encryption (with the ``--encrypt`` flag). The default is empty.

