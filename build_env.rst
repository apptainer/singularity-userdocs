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

To make downloading images for build and :ref:`pull <pull-command>` faster and less redundant, Singularity
uses a caching strategy. By default, Singularity will create
a set of folders in your ``$HOME`` directory for docker layers, Cloud library images, and metadata, respectively:

.. code-block:: none

    $HOME/.singularity/cache/library
    $HOME/.singularity/cache/oci
    $HOME/.singularity/cache/oci-tmp

If you want to cache in a different directory, set ``SINGULARITY_CACHEDIR`` to the desired path.
By using the ``-E`` option with the ``sudo`` command, ``SINGULARITY_CACHEDIR`` will be passed along 
to root's environment and respected during the build. 
Remember that when you run commands as root images will be cached in root’s home at ``/root`` and not your user’s home.

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

    singularity exec docker://busybox /bin/sh

This container is first built in ``/tmp``. Since all the oci blobs are converted into SIF format, 
by default a temporary runtime directory is created in:

.. code-block:: none

    $HOME/.singularity/cache/oci-tmp/<sha256-code>/busybox_latest.sif

In this case, the ``SINGULARITY_TMPDIR`` and ``SINGULARITY_CACHEDIR`` variables will also be respected.

-----------
Pull Folder
-----------

For details about customizing the output location of :ref:`pull <pull-command>`, see the
:ref:`pull docs <pull-command>`. You have the similar ability to set it to be something
different, or to customize the name of the pulled image.

---------------------
Environment Variables
---------------------

Environment varialbes 

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
