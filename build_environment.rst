.. _build-environment:

=================
Build Environment
=================

.. _sec:buildenv:

It’s commonly the case that you want to customize your build
environment, such as specifying a custom cache directory for layers, or
sending your Docker Credentials to the registry endpoint. Here we will
discuss those things

-------------
Cache Folders
-------------

To make download of layers for build and :ref:`pull <pull-command>` faster and less redundant, we
use a caching strategy. By default, the Singularity software will create
a set of folders in your ``$HOME`` directory for docker layers, Singularity Hub
images, and Docker metadata, respectively:

.. code-block:: none

    $HOME/.singularity

    $HOME/.singularity/docker

    $HOME/.singularity/shub

    $HOME/.singularity/metadata


Fear not, you have control to customize this behavior! If you don’t want
the cache to be created (and a temporary directory will be used), set ``SINGULARITY_DISABLE_CACHE`` to
True/yes, or if you want to move it elsewhere, set ``SINGULARITY_CACHEDIR`` to the full path
where you want to cache. Remember that when you run commands as sudo
this will use root’s home at ``/root`` and not your user’s home.

-----------------
Temporary Folders
-----------------

 .. _sec:temporaryfolders:

Singularity also uses some temporary directories to build the squashfs filesystem,
so this temp space needs to be large enough to hold the entire resulting Singularity image.
By default this happens in ``/tmp`` but can be overridden by setting ``SINGULARITY_TMPDIR`` to the full
path where you want the squashfs temp files to be stored. Since images
are typically built as root, be sure to set this variable in root’s
environment.

If you are building an image on the fly, for example

.. code-block:: none

    singularity exec docker://busybox /bin/sh

by default a temporary runtime directory is created that looks like ``/tmp/.singularity-runtime.xxxxxxxx``.

This can be problematic for some ``/tmp`` directories that are hosted at
Jetstream/OpenStack, Azure, and possibly EC2, which are very small. If
you need to change the location of this runtime, then **export** the
variable ``SINGULARITY_LOCALCACHEDIR``.

.. code-block:: none

    SINGULARITY_LOCALCACHEDIR=/tmp/pancakes

    export SINGULARITY_LOCALCACHEDIR

    singularity exec docker://busybox /bin/sh


The above runtime folder would be created under ``/tmp/pancakes/.singularity-runtime.xxxxxxxx``

-----------
Pull Folder
-----------

For details about customizing the output location of :ref:`pull <pull-command>`, see the
:ref:`pull docs <pull-command>`. You have the similar ability to set it to be something
different, or to customize the name of the pulled image.

---------------------
Environment Variables
---------------------

All environmental variables are parsed by Singularity python helper
functions, and specifically the file `defaults.py <https://github.com/singularityware/singularity/blob/2.6.0/libexec/python/defaults.py>`_ is a gateway
between variables defined at runtime, and pre-defined defaults. By way
of import from the file, variables set at runtime do not change if
re-imported. This was done intentionally to prevent changes during the
execution, and could be changed if needed. For all variables, the
order of operations works as follows:

#. First preference goes to environment variable set at runtime

#. Second preference goes to default defined in this file

#. Then, if neither is found, null is returned except in the case that ``required=True``.
   A ``required=True`` variable not found will system exit with an error.

#. Variables that should not be displayed in debug logger are set with ``silent=True``,
   and are only reported to be defined.

For boolean variables, the following are acceptable for True, with any
kind of capitalization or not:

.. code-block:: none

    ("yes", "true", "t", "1","y")

-----
Cache
-----

The location and usage of the cache is also determined by environment
variables.

**SINGULARITY_DISABLE_CACHE** If you want to disable the cache, this
means is that the layers are written to a temporary directory. Thus,
if you want to disable cache and write to a temporary folder, simply
set ``SINGULARITY_DISABLE_CACHE`` to any true/yes value. By default, the cache is not disabled.

**SINGULARITY_CACHEDIR** Is the base folder for caching layers and
singularity hub images. If not defined, it uses default of ``$HOME/.singularity``. If
defined, the defined location is used instead.

If ``SINGULARITY_DISABLE_CACHE`` is set to True, this value is ignored in favor of a temporary
directory. For specific sub-types of things to cache, subdirectories
are created (by python), including ``$SINGULARITY_CACHEDIR/docker`` for docker layers and ``$SINGULARITY_CACHEDIR/shub`` for
Singularity Hub images. If the cache is not created, the Python script
creates it.

**SINGULARITY_PULLFOLDER** While this isn’t relevant for build, since
build is close to pull, we will include it here. By default, images
are pulled to the present working directory. The user can change this
variable to change that.

**SINGULARITY_TMPDIR** Is the base folder for squashfs image
temporary building. If not defined, it uses default of ``$TEMPDIR``. If defined,
the defined location is used instead.

**SINGULARITY_LOCALCACHEDIR** Is the temporary folder (default ``/tmp``) to
generate runtime folders (containers “on the fly”) typically a ``run``, ``exec`` , or ``shell``
or a ``docker://`` image. This is different from where downloaded layers are cached
(``$SINGULARITY_CACHEDIR``) or pulled (``SINGULARITY_PULLFOLDER``) or where a (non on-the-fly build) happens ( ``$SINGULARITY_TMPDIR`` ). See
`temporary folders <#temporary-folders>`_ above for an example. You can generally determine the value of this
setting by running a command with ``--debug`` , and seeing the last line “Removing
directory:”

.. code-block:: none

    singularity --debug run docker://busybox echo "pizza!"

    ...

    DEBUG   [U=1000,P=960]     s_rmdir()                                 Removing directory: /tmp/.singularity-runtime.oArO0k

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

Singularity Hub
---------------

**SHUB_API_BASE** The default base for the Singularity Hub API,
which is ``https://singularity-hub.org/api``. If you deploy your own registry, you don’t need
to change this, you can again specify the registry name in the URI.

General
=======

**SINGULARITY_PYTHREADS** The Python modules use threads (workers) to
download layer files for Docker, and change permissions. By default,
we will use 9 workers, unless the environment variable ``SINGULARITY_PYTHREADS`` is defined.
**SINGULARITY_COMMAND_ASIS** By default, we want to make sure the container running process gets passed forward as the current process,
so we want to prefix whatever the Docker command or entrypoint is with
``exec``. We also want to make sure that following arguments get passed, so we
append ``"$@"``. Thus, some entrypoint or cmd might look like this:

.. code-block:: none

    /usr/bin/python

and we would parse it into the runscript as:

.. code-block:: none

    exec /usr/bin/python "$@"

However, it might be the case that the user does not want this. For this
reason, we have the environmental variable ``RUNSCRIPT_COMMAND_ASIS``. If defined as
yes/y/1/True/true, etc., then the runscript will remain as ``/usr/bin/python``.
