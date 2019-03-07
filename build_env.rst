.. _build-environment:

=================
Build Environment
=================

.. _sec:buildenv:

--------
Overview
--------

It’s commonly the case that you want to customize your build
environment, such as specifying a custom cache directory for layers, or
sending your Docker Credentials to the registry endpoint. Here we will discuss those topics.

-------------
Cache Folders
-------------

To make download of layers for build and :ref:`pull <pull-command>` faster and less redundant, we
use a caching strategy. By default, the Singularity software will create
a set of folders in your ``$HOME`` directory for docker layers, Cloud library images and metadata, respectively:

.. code-block:: none

    $HOME/.singularity/cache/library
    $HOME/.singularity/cache/oci
    $HOME/.singularity/cache/oci-tmp

If you want replace the full path where you want to cache, set ``SINGULARITY_CACHEDIR`` to the desired path.
And by using the ``-E`` option, ``SINGULARITY_CACHEDIR`` will be passed along and be respected.
Remember that when you run commands as sudo this will use root’s home at ``/root`` and not your user’s home.

-----------------
Temporary Folders
-----------------

 .. _sec:temporaryfolders:

Singularity also uses some temporary directories to build the squashfs filesystem,
so this temp space needs to be large enough to hold the entire resulting Singularity image.
By default this happens in ``/tmp`` but can be overridden by setting ``SINGULARITY_TMPDIR`` to the full
path where you want the squashfs temp files to be stored. Remember you can also use ``-E`` option to pass and respect the definition of ``SINGULARITY_TMPDIR``.
Since images are typically built as root, be sure to set this variable in root’s environment.

If you are building an image on the fly, for example

.. code-block:: none

    singularity exec docker://busybox /bin/sh

Since all the oci blobs are converted into SIF format, by default a temporary runtime directory is created in ``.singularity/cache/oci-tmp/<sha256-code>/busybox_latest.sif``.

-----------
Pull Folder
-----------

For details about customizing the output location of :ref:`pull <pull-command>`, see the
:ref:`pull docs <pull-command>`. You have the similar ability to set it to be something
different, or to customize the name of the pulled image.

---------------------
Environment Variables
---------------------

#* If a flag is represented by both a CLI option and an environment variable, and both are set, the CLI option will always take precedence.
This is true for all environment variables except for ``SINGULARITY_BIND`` and ``SINGULARITY_BINDPATH`` which is combined with the ``--bind`` option, argument pair if both are present.
#* Environment variables overwrite default values in the CLI code
#* Any defaults in the CLI code are applied.

-----
Cache
-----

The location and usage of the cache is also determined by environment
variables.

**SINGULARITY_CACHEDIR** Is the base folder for caching layers and
singularity hub images. If not defined, it uses default of ``$HOME/.singularity``. If
defined, the defined location is used instead.

**SINGULARITY_PULLFOLDER** While this isn’t relevant for build, since
build is close to pull, we will include it here. By default, images
are pulled to the present working directory. The user can change this
variable to change that.

**SINGULARITY_TMPDIR** Is the base folder for squashfs image
temporary building. If not defined, it uses default of ``$TEMPDIR``. If defined,
the defined location is used instead.

Defaults
========

The following variables have defaults that can be customized by you via
environment variables at runtime.

Docker
------

**DOCKER_API_BASE** Set as ``index.docker.io``, which is the name of the registry. In
the first version of Singularity we parsed the Registry argument from
the build spec file, however now this is removed because it can be
obtained directly from the image name (eg, ``registry/namespace/repo:tag``). If you don’t specify a
registry name for your image, this default is used. If you have
trouble with your registry being detected from the image URI, use this
variable.

**DOCKER_API_VERSION** Is the version of the Docker Registry API
currently being used, by default now is ``v2``.
**DOCKER_OS** This is exposed via the exported environment variable ``SINGULARITY_DOCKER_OS``
and pertains to images that reveal a version 2 manifest with a
`manifest list <https://docs.docker.com/registry/spec/manifest-v2-2/#manifest-list>`_. In the case that the list is present, we must choose
an operating system (this variable) and an architecture (below). The
default is ``linux``.

**DOCKER_ARCHITECTURE** This is exposed via the exported environment
variable ``SINGULARITY_DOCKER_ARCHITECTURE``
and the same applies as for the ``DOCKER_OS`` with regards to being used in context
of a list of manifests. In the case that the list is present, we must
choose an architecture (this variable) and an os (above). The default
is ``amd64``, and other common ones include ``arm``, ``arm64``, ``ppc64le``, ``386``, and ``s390x``.
**NAMESPACE** Is the default namespace, ``library``.

**RUNSCRIPT_COMMAND** Is not obtained from the environment, but is a
hard coded default (“/bin/bash”). This is the fallback command used in
the case that the docker image does not have a CMD or ENTRYPOINT.
**TAG** Is the default tag, ``latest``.

**SINGULARITY_NOHTTPS** This is relevant if you want to use a
registry that doesn’t have https, and it speaks for itself. If you
export the variable ``SINGULARITY_NOHTTPS`` you can force the software to not use https when
interacting with a Docker registry. This use case is typically for use
of a local registry.
