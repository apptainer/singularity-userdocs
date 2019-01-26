========
Appendix
========

.. _build-library-module:

---------------------------
``library`` bootstrap agent
---------------------------

.. _sec:build-library-module:


Overview
========

You can use an existing container on the Container Library as your “base,” and
then add customization. This allows you to build multiple images from the same
starting point. For example, you may want to build several containers with the
same custom python installation, the same custom compiler toolchain, or the same
base MPI installation. Instead of building these from scratch each time, you
could create a base container on the Container Library and then build new
containers from that existing base container adding customizations in ``%post``,
``%environment``, ``%runscript``, etc.

Keywords
========

.. code-block:: singularity

    Bootstrap: library

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    From: <entity>/<collection>/<container>:<tag>

The From keyword is mandatory. It specifies the container to use as a base.
``entity`` is optional and defaults to ``library``. ``collection`` is
optional and defaults to ``default``. This is the correct namespace to use for
some official containers (``alpine`` for example). ``tag`` is also optional and
will default to ``latest``.

.. code-block:: singularity

    Library: http://custom/library

The Library keyword is optional. It will default to
``https://library.sylabs.io``.


.. _build-docker-module:

--------------------------
``docker`` bootstrap agent
--------------------------

.. _sec:build-docker-module:

Overview
========

Docker images are comprised of layers that are assembled at runtime to create an
image. You can use Docker layers to create a base image, and then add your own
custom software. For example, you might use Docker’s Ubuntu image layers to
create an Ubuntu Singularity container. You could do the same with CentOS,
Debian, Arch, Suse, Alpine, BusyBox, etc.

Or maybe you want a container that already has software installed. For instance,
maybe you want to build a container that uses CUDA and cuDNN to leverage the
GPU, but you don’t want to install from scratch. You can start with one of the
``nvidia/cuda`` containers and install your software on top of that.

Or perhaps you have already invested in Docker and created your own Docker
containers. If so, you can seamlessly convert them to Singularity with the
``docker`` bootstrap module.

Keywords
========

.. code-block:: singularity

    Bootstrap: docker

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    From: <registry>/<namespace>/<container>:<tag>@<digest>

The From keyword is mandatory. It specifies the container to use as a base.
``registry`` is optional and defaults to ``index.docker.io``. ``namespace`` is
optional and defaults to ``library``. This is the correct namespace to use for
some official containers (ubuntu for example). ``tag`` is also optional and will
default to ``latest``

See :ref:`Singularity and Docker <singularity-and-docker>` for more detailed
info on using Docker registries.

.. code-block:: singularity

    Registry: http://custom_registry

The Registry keyword is optional. It will default to ``index.docker.io``.

.. code-block:: singularity

    Namespace: namespace

The Namespace keyword is optional. It will default to ``library``.

.. code-block:: singularity

    IncludeCmd: yes

The IncludeCmd keyword is optional. If included, and if a ``%runscript`` is not
specified, a Docker ``CMD`` will take precedence over ``ENTRYPOINT`` and will be
used as a runscript. Note that the ``IncludeCmd`` keyword is considered valid if
it is not empty! This means that ``IncludeCmd: yes`` and ``IncludeCmd: no`` are
identical. In both cases the ``IncludeCmd`` keyword is not empty, so the Docker
``CMD`` will take precedence over an ``ENTRYPOINT``.

 See :ref:`Singularity and Docker <singularity-and-docker>` for more info on
 order of operations for determining a runscript.

Notes
=====

Docker containers are stored as a collection of tarballs called layers. When
building from a Docker container the layers must be downloaded and then
assembled in the proper order to produce a viable file system. Then the file
system must be converted to Singularity Image File (sif) format.

Building from Docker Hub is not considered reproducible because if any of the
layers of the image are changed, the container will change. If reproducibility
is important to your workflow, consider hosting a base container on the
Container Library and building from it instead.

For detailed information about setting your build environment see
:ref:`Build Customization <build-environment>`.

.. _build-shub:

------------------------
``shub`` bootstrap agent
------------------------

.. _sec:build-shub:

Overview
========

You can use an existing container on Singularity Hub as your “base,” and then
add customization. This allows you to build multiple images from the same
starting point. For example, you may want to build several containers with the
same custom python installation, the same custom compiler toolchain, or the same
base MPI installation. Instead of building these from scratch each time, you
could create a base container on Singularity Hub and then build new containers
from that existing base container adding customizations in ``%post`` ,
``%environment``, ``%runscript``, etc.

Keywords
========

.. code-block:: singularity

    Bootstrap: shub

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    From: shub://<registry>/<username>/<container-name>:<tag>@digest

The From keyword is mandatory. It specifies the container to use as a base.
``registry is optional and defaults to ``singularity-hub.org``. ``tag`` and
``digest`` are also optional. ``tag`` defaults to ``latest`` and ``digest`` can
be left blank if you want the latest build.

Notes
=====

When bootstrapping from a Singularity Hub image, all previous definition files
that led to the creation of the current image will be stored in a directory
within the container called ``/.singularity.d/bootstrap_history``. Singularity
will also alert you if environment variables have been changed between the base
image and the new image during bootstrap.

.. _build-localimage:

------------------------------
``localimage`` bootstrap agent
------------------------------

.. _sec:build-localimage:

This module allows you to build a container from an existing Singularity
container on your host system. The name is somewhat misleading because your
container can be in either image or directory format.

Overview
========

You can use an existing container image as your “base”, and then add
customization. This allows you to build multiple images from the same starting
point. For example, you may want to build several containers with the same
custom python installation, the same custom compiler toolchain, or the same base
MPI installation. Instead of building these from scratch each time, you could
start with the appropriate local base container and then customize the new
container in ``%post``, ``%environment``, ``%runscript``, etc.

Keywords
========

.. code-block:: singularity

    Bootstrap: localimage

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    From: /path/to/container/file/or/directory

The From keyword is mandatory. It specifies the local container to use as a
base.

Notes
=====

When building from a local container, all previous definition files that led to
the creation of the current container will be stored in a directory within the
container called ``/.singularity.d/bootstrap_history``. Singularity will also
alert you if environment variables have been changed between the base image and
the new image during bootstrap.

.. _build-yum:

-----------------------
``yum`` bootstrap agent
-----------------------

.. _sec:build-yum:

This module allows you to build a Red Hat/CentOS/Scientific Linux style
container from a mirror URI.

Overview
========

Use the ``yum`` module to specify a base for a CentOS-like container. You must
also specify the URI for the mirror you would like to use.

Keywords
========

.. code-block:: singularity

    Bootstrap: yum

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    OSVersion: 7

The OSVersion keyword is optional. It specifies the OS version you would like to
use. It is only required if you have specified a %{OSVERSION} variable in the
``MirrorURL`` keyword.

.. code-block:: singularity

    MirrorURL: http://mirror.centos.org/centos-%{OSVERSION}/%{OSVERSION}/os/$basearch/

The MirrorURL keyword is mandatory. It specifies the URI to use as a mirror to
download the OS. If you define the ``OSVersion`` keyword, than you can use it in
the URI as in the example above.

.. code-block:: singularity

    Include: yum

The Include keyword is optional. It allows you to install additional packages
into the core operating system. It is a best practice to supply only the bare
essentials such that the ``%post`` section has what it needs to properly
complete the build. One common package you may want to install when using the
``yum`` build module is YUM itself.

Notes
=====

There is a major limitation with using YUM to bootstrap a container. The RPM
database that exists within the container will be created using the RPM library
and Berkeley DB implementation that exists on the host system. If the RPM
implementation inside the container is not compatible with the RPM database that
was used to create the container, RPM and YUM commands inside the container may
fail. This issue can be easily demonstrated by bootstrapping an older RHEL
compatible image by a newer one (e.g. bootstrap a Centos 5 or 6 container from a
Centos 7 host).

In order to use the ``debootstrap`` build module, you must have ``yum``
installed on your system. It may seem counter-intuitive to install YUM on a
system that uses a different package manager, but you can do so. For instance,
on Ubuntu you can install it like so:

.. code-block:: none

    $ sudo apt-get update && sudo apt-get install yum

.. _build-debootstrap:

---------------------------
``debootstrap`` build agent
---------------------------

.. _sec:build-debootstrap:

This module allows you to build a Debian/Ubuntu style container from a mirror
URI.

Overview
========

Use the ``debootstrap`` module to specify a base for a Debian-like container.
You must also specify the OS version and a URI for the mirror you would like to
use.

Keywords
========

.. code-block:: singularity

    Bootstrap: debootstrap

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    OSVersion: xenial

The OSVersion keyword is mandatory. It specifies the OS version you would like
to use. For Ubuntu you can use code words like ``trusty`` (14.04), ``xenial``
(16.04), and ``yakkety`` (17.04). For Debian you can use values like ``stable``,
``oldstable``, ``testing``, and ``unstable`` or code words like ``wheezy`` (7),
``jesse`` (8), and ``stretch`` (9).

 .. code-block:: singularity

     MirrorURL:  http://us.archive.ubuntu.com/ubuntu/

The MirrorURL keyword is mandatory. It specifies a URI to use as a mirror when
downloading the OS.

.. code-block:: singularity

    Include: somepackage

The Include keyword is optional. It allows you to install additional packages
into the core operating system. It is a best practice to supply only the bare
essentials such that the ``%post`` section has what it needs to properly
complete the build.

Notes
=====

In order to use the ``debootstrap`` build module, you must have ``debootstrap``
installed on your system. On Ubuntu you can install it like so:

.. code-block:: none

    $ sudo apt-get update && sudo apt-get install debootstrap

On CentOS you can install it from the epel repos like so:

.. code-block:: none

    $ sudo yum update && sudo yum install epel-release && sudo yum install debootstrap.noarch

.. _build-arch:

------------------------
``arch`` bootstrap agent
------------------------

.. _sec:build-arch:

This module allows you to build a Arch Linux based container.

Overview
========

Use the ``arch`` module to specify a base for an Arch Linux based container.
Arch Linux uses the aptly named ``pacman`` package manager (all puns intended).


Keywords
========

.. code-block:: singularity

    Bootstrap: arch

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

The Arch Linux bootstrap module does not name any additional keywords at this
time. By defining the ``arch`` module, you have essentially given all of the
information necessary for that particular bootstrap module to build a core
operating system.

Notes
=====

Arch Linux is, by design, a very stripped down, light-weight OS. You may need to
perform a significant amount of configuration to get a usable OS. Please refer
to this
`README.md <https://github.com/singularityware/singularity/blob/master/examples/arch/README.md>`_
and the
`Arch Linux example <https://github.com/singularityware/singularity/blob/master/examples/arch/Singularity>`_
for more info.

.. _build-busybox:

---------------------------
``busybox`` bootstrap agent
---------------------------

.. _sec:build-busybox:

This module allows you to build a container based on BusyBox.

Overview
========

Use the ``busybox`` module to specify a BusyBox base for container. You must
also specify a URI for the mirror you would like to use.

Keywords
========

.. code-block:: singularity

    Bootstrap: busybox

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    MirrorURL: https://www.busybox.net/downloads/binaries/1.26.1-defconfig-multiarch/busybox-x86_64

The MirrorURL keyword is mandatory. It specifies a URI to use as a mirror when
downloading the OS.

Notes
=====

You can build a fully functional BusyBox container that only takes up ~600kB of
disk space!

.. _build-zypper:

--------------------------
``zypper`` bootstrap agent
--------------------------

.. _sec:build-zypper:

This module allows you to build a Suse style container from a mirror URI.

Overview
========

Use the ``zypper`` module to specify a base for a Suse-like container. You must
also specify a URI for the mirror you would like to use.

Keywords
========

.. code-block:: singularity

    Bootstrap: zypper

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    OSVersion: 42.2

The OSVersion keyword is optional. It specifies the OS version you would like to
use. It is only required if you have specified a %{OSVERSION} variable in the
``MirrorURL`` keyword.

.. code-block:: singularity

    Include: somepackage

The Include keyword is optional. It allows you to install additional packages
into the core operating system. It is a best practice to supply only the bare
essentials such that the ``%post`` section has what it needs to properly
complete the build. One common package you may want to install when using the
zypper build module is ``zypper`` itself.
