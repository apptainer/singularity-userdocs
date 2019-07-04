
.. _appendix:

Appendi
========


.. TODO oci & oci-archive along with http & https

.. _singularity-environment-variables:


Singularity's environment variables
-----------------------------------

Singularity 3.0 comes with some environment variables you can set or modify depending on your needs.
You can see them listed alphabetically below with their respective functionality.

``A``
^^^^^

#. **SINGULARITY_ADD_CAPS**: To specify a list (comma separated string) of capabilities to be added. Default is an empty string.

#. **SINGULARITY_ALL**: List all the users and groups capabilities.

#. **SINGULARITY_ALLOW_SETUID**: To specify that setuid binaries should or not be allowed in the container. (root only) Default is set to false.

#. **SINGULARITY_APP** and **SINGULARITY_APPNAME**: Sets the name of an application to be run inside a container.

#. **SINGULARITY_APPLY_CGROUPS**: Used to apply cgroups from an input file for container processes. (it requires root privileges)

``B``
^^^^^

#. **SINGULARITY_BINDPATH** and **SINGULARITY_BIND**: Comma separated string ``source:<dest>`` list of paths to bind between the host and the container.

#. **SINGULARITY_BOOT**: Set to false by default, considers if executing ``/sbin/init`` when container boots (root only).

#. **SINGULARITY_BUILDER**: To specify the remote builder service URL. Defaults to our remote builder.

``C``
^^^^^

#. **SINGULARITY_CACHEDIR**: Specifies the directory for image downloads to be cached in.

#. **SINGULARITY_CLEANENV**: Specifies if the environment should be cleaned or not before running the container. Default is set to false.

#. **SINGULARITY_CONTAIN**: To use minimal ``/dev`` and empty other directories (e.g. ``/tmp`` and ``$HOME``) instead of sharing filesystems from your host. Default is set to false.

#. **SINGULARITY_CONTAINALL**: To contain not only file systems, but also PID, IPC, and environment. Default is set to false.

#. **SINGULARITY_CONTAINLIBS**: Used to specify a string of file names (comma separated string) to bind to the ``/.singularity.d/libs`` directory.

``D``
^^^^^

#. **SINGULARITY_DEFFILE**: Shows the Singularity recipe that was used to generate the image.

#. **SINGULARITY_DESC**: Contains a description of the capabilities.

#. **SINGULARITY_DETACHED**: To submit a build job and print the build ID (no real-time logs and also requires ``--remote``). Default is set to false.

#. **SINGULARITY_DNS**: A list of the DNS server addresses separated by commas to be added in ``resolv.conf``.

#. **SINGULARITY_DOCKER_LOGIN**: To specify the interactive prompt for docker authentication.

#. **SINGULARITY_DOCKER_USERNAME**: To specify a username for docker authentication.

#. **SINGULARITY_DOCKER_PASSWORD**: To specify the password for docker authentication.

#. **SINGULARITY_DROP_CAPS**: To specify a list (comma separated string) of capabilities to be dropped. Default is an empty string.

``E``
^^^^^

#. **SINGULARITY_ENVIRONMENT**: Contains all the environment variables that have been exported in your container.
#. **SINGULARITYENV_***: Allows you to transpose variables into the container at runtime. You can see more in detail how to use this variable in our :ref:`environment and metadata section <environment-and-metadata>`.
#. **SINGULARITYENV_APPEND_PATH**: Used to append directories to the end of the ``$PATH`` environment variable. You can see more in detail on how to use this variable in our :ref:`environment and metadata section <environment-and-metadata>`.
#. **SINGULARITYENV_PATH**: A specified path to override the ``$PATH`` environment variable within the container. You can see more in detail on how to use this variable in our :ref:`environment and metadata section <environment-and-metadata>`.
#. **SINGULARITYENV_PREPEND_PATH**: Used to prepend directories to the beginning of `$PATH`` environment variable. You can see more in detail on how to use this variable in our :ref:`environment and metadata section <environment-and-metadata>`.

``F``
^^^^^

#. **SINGULARITY_FAKEROOT**: Set to false by default, considers running the container in a new user namespace as uid 0 (experimental).

#. **SINGULARITY_FORCE**: Forces to kill the instance.

``G``
^^^^^

#. **SINGULARITY_GROUP**: Used to specify a string of capabilities for the given group.

``H``
^^^^^

#. **SINGULARITY_HELPFILE**: Specifies the runscript helpfile, if it exists.

#. **SINGULARITY_HOME** : A home directory specification, it could be a source or destination path. The source path is the home directory outside the container and the destination overrides the home directory within the container.

#. **SINGULARITY_HOSTNAME**: The container's hostname.

``I``
^^^^^

#. **SINGULARITY_IMAGE**: Filename of the container.

``J``
^^^^^

#. **SINGULARITY_JSON**: Specifies the structured json of the def file, every node as each section in the def file.

``K``
^^^^^

#. **SINGULARITY_KEEP_PRIVS**: To let root user keep privileges in the container. Default is set to false.

``L``
^^^^^

#. **SINGULARITY_LABELS**: Specifies the labels associated with the image.

#. **SINGULARITY_LIBRARY**: Specifies the library to pull from. Default is set to our Cloud Library.

``N``
^^^^^

#. **SINGULARITY_NAME**: Specifies a custom image name.

#. **SINGULARITY_NETWORK**: Used to specify a desired network. If more than one parameters is used, addresses should be separated by commas, where each network will bring up a dedicated interface inside the container.

#. **SINGULARITY_NETWORK_ARGS**: To specify the network arguments to pass to CNI plugins.

#. **SINGULARITY_NOCLEANUP**: To not clean up the bundle after a failed build, this can be helpful for debugging. Default is set to false.

#. **SINGULARITY_NOHTTPS**: Sets to either false or true to avoid using HTTPS for communicating with the local docker registry. Default is set to false.

#. **SINGULARITY_NO_HOME**: Considers not mounting users home directory if home is not the current working directory. Default is set to false.

#. **SINGULARITY_NO_INIT** and **SINGULARITY_NOSHIMINIT**: Considers not starting the ``shim`` process with ``--pid``.

#. **SINGULARITY_NO_NV**: Flag to disable Nvidia support. Opposite of ``SINGULARITY_NV``.

#. **SINGULARITY_NO_PRIVS**: To drop all the privileges from root user in the container. Default is set to false.

#. **SINGULARITY_NV**: To enable experimental Nvidia support. Default is set to false.

``O``
^^^^^

#. **SINGULARITY_OVERLAY** and **SINGULARITY_OVERLAYIMAGE**: To indicate the use of an overlay file system image for persistent data storage or as read-only layer of container.

``P``
^^^^^

#. **SINGULARITY_PWD** and **SINGULARITY_TARGET_PWD**: The initial working directory for payload process inside the container.

``R``
^^^^^

#. **SINGULARITY_REMOTE**: To build an image remotely. (Does not require root) Default is set to false.

#. **SINGULARITY_ROOTFS**: To reference the system file location.

#. **SINGULARITY_RUNSCRIPT**: Specifies the runscript of the image.

``S``
^^^^^

#. **SINGULARITY_SANDBOX**: To specify that the format of the image should be a sandbox. Default is set to false.

#. **SINGULARITY_SCRATCH** and **SINGULARITY_SCRATCHDIR**: Used to include a scratch directory within the container that is linked to a temporary directory. (use -W to force location)

#. **SINGULARITY_SECTION**: To specify a comma separated string of all the sections to be run from the deffile (setup, post, files, environment, test, labels, none)

#. **SINGULARITY_SECURITY**: Used to enable security features. (SELinux, Apparmor, Seccomp)

#. **SINGULARITY_SECRET**: Lists all the private keys instead of the default which display the public ones.

#. **SINGULARITY_SHELL**: The path to the program to be used as an interactive shell.

#. **SINGULARITY_SIGNAL**: Specifies a signal sent to the instance.

``T``
^^^^^

#. **SINGULARITY_TEST**: Specifies the test script for the image.

#. **SINGULARITY_TMPDIR**: Used with the ``build`` command, to consider a temporary location for the build.

``U``
^^^^^

#. **SINGULARITY_UNSHARE_PID**: To specify that the container will run in a new PID namespace. Default is set to false.

#. **SINGULARITY_UNSHARE_IPC**: To specify that the container will run in a new IPC namespace. Default is set to false.

#. **SINGULARITY_UNSHARE_NET**: To specify that the container will run in a new network namespace (sets up a bridge network interface by default). Default is set to false.

#. **SINGULARITY_UNSHARE_UTS**: To specify that the container will run in a new UTS namespace. Default is set to false.

#. **SINGULARITY_UPDATE**: To run the definition over an existing container (skips the header). Default is set to false.

#. **SINGULARITY_URL**: Specifies the key server ``URL``.

#. **SINGULARITY_USER**: Used to specify a string of capabilities for the given user.

#. **SINGULARITY_USERNS** and **SINGULARITY_UNSHARE_USERNS**: To specify that the container will run in a new user namespace, allowing Singularity to run completely unprivileged on recent kernels. This may not support every feature of Singularity. (Sandbox image only). Default is set to false.

``W``
^^^^^

#. **SINGULARITY_WORKDIR**: The working directory to be used for ``/tmp``, ``/var/tmp`` and ``$HOME`` (if ``-c`` or ``--contain`` was also used)

#. **SINGULARITY_WRITABLE**: By default, all Singularity containers are available as read only, this option makes the file system accessible as read/write. Default set to false.

#. **SINGULARITY_WRITABLE_TMPFS**: Makes the file system accessible as read-write with non-persistent data (with overlay support only). Default is set to false.


.. _buildmodules:

Build Modules
-------------

.. _build-library-module:


``library`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-library-module:


Overview
""""""""

You can use an existing container on the Container Library as your “base,” and
then add customization. This allows you to build multiple images from the same
starting point. For example, you may want to build several containers with the
same custom python installation, the same custom compiler toolchain, or the same
base MPI installation. Instead of building these from scratch each time, you
could create a base container on the Container Library and then build new
containers from that existing base container adding customizations in ``%post``,
``%environment``, ``%runscript``, etc.

Keywords
""""""""

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


``docker`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-docker-module:


Overview
""""""""

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
""""""""

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
"""""

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


``shub`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-shub:

Overview
""""""""

You can use an existing container on Singularity Hub as your “base,” and then
add customization. This allows you to build multiple images from the same
starting point. For example, you may want to build several containers with the
same custom python installation, the same custom compiler toolchain, or the same
base MPI installation. Instead of building these from scratch each time, you
could create a base container on Singularity Hub and then build new containers
from that existing base container adding customizations in ``%post`` ,
``%environment``, ``%runscript``, etc.

Keywords
""""""""

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
"""""

When bootstrapping from a Singularity Hub image, all previous definition files
that led to the creation of the current image will be stored in a directory
within the container called ``/.singularity.d/bootstrap_history``. Singularity
will also alert you if environment variables have been changed between the base
image and the new image during bootstrap.

.. _build-localimage:


``localimage`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-localimage:

This module allows you to build a container from an existing Singularity
container on your host system. The name is somewhat misleading because your
container can be in either image or directory format.

Overview
""""""""

You can use an existing container image as your “base”, and then add
customization. This allows you to build multiple images from the same starting
point. For example, you may want to build several containers with the same
custom python installation, the same custom compiler toolchain, or the same base
MPI installation. Instead of building these from scratch each time, you could
start with the appropriate local base container and then customize the new
container in ``%post``, ``%environment``, ``%runscript``, etc.

Keywords
""""""""

.. code-block:: singularity

    Bootstrap: localimage

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    From: /path/to/container/file/or/directory

The From keyword is mandatory. It specifies the local container to use as a
base.

Notes
"""""

When building from a local container, all previous definition files that led to
the creation of the current container will be stored in a directory within the
container called ``/.singularity.d/bootstrap_history``. Singularity will also
alert you if environment variables have been changed between the base image and
the new image during bootstrap.

.. _build-yum:


``yum`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-yum:

This module allows you to build a Red Hat/CentOS/Scientific Linux style
container from a mirror URI.

Overview
""""""""

Use the ``yum`` module to specify a base for a CentOS-like container. You must
also specify the URI for the mirror you would like to use.

Keywords
""""""""

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
"""""

There is a major limitation with using YUM to bootstrap a container. The RPM
database that exists within the container will be created using the RPM library
and Berkeley DB implementation that exists on the host system. If the RPM
implementation inside the container is not compatible with the RPM database that
was used to create the container, RPM and YUM commands inside the container may
fail. This issue can be easily demonstrated by bootstrapping an older RHEL
compatible image by a newer one (e.g. bootstrap a Centos 5 or 6 container from a
Centos 7 host).

In order to use the ``yum`` build module, you must have ``yum``
installed on your system. It may seem counter-intuitive to install YUM on a
system that uses a different package manager, but you can do so. For instance,
on Ubuntu you can install it like so:

.. code-block:: none

    $ sudo apt-get update && sudo apt-get install yum

.. _build-debootstrap:


``debootstrap`` build agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-debootstrap:

This module allows you to build a Debian/Ubuntu style container from a mirror
URI.

Overview
""""""""

Use the ``debootstrap`` module to specify a base for a Debian-like container.
You must also specify the OS version and a URI for the mirror you would like to
use.

Keywords
""""""""

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
"""""

In order to use the ``debootstrap`` build module, you must have ``debootstrap``
installed on your system. On Ubuntu you can install it like so:

.. code-block:: none

    $ sudo apt-get update && sudo apt-get install debootstrap

On CentOS you can install it from the epel repos like so:

.. code-block:: none

    $ sudo yum update && sudo yum install epel-release && sudo yum install debootstrap.noarch


.. _build-arch:


``arch`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-arch:

This module allows you to build a Arch Linux based container.

Overview
""""""""

Use the ``arch`` module to specify a base for an Arch Linux based container.
Arch Linux uses the aptly named ``pacman`` package manager (all puns intended).


Keywords
""""""""

.. code-block:: singularity

    Bootstrap: arch

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

The Arch Linux bootstrap module does not name any additional keywords at this
time. By defining the ``arch`` module, you have essentially given all of the
information necessary for that particular bootstrap module to build a core
operating system.

Notes
"""""

Arch Linux is, by design, a very stripped down, light-weight OS. You may need to
perform a significant amount of configuration to get a usable OS. Please refer
to this
`README.md <https://github.com/singularityware/singularity/blob/master/examples/arch/README.md>`_
and the
`Arch Linux example <https://github.com/singularityware/singularity/blob/master/examples/arch/Singularity>`_
for more info.

.. _build-busybox:


``busybox`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-busybox:

This module allows you to build a container based on BusyBox.

Overview
""""""""

Use the ``busybox`` module to specify a BusyBox base for container. You must
also specify a URI for the mirror you would like to use.

Keywords
""""""""

.. code-block:: singularity

    Bootstrap: busybox

The Bootstrap keyword is always mandatory. It describes the bootstrap module to
use.

.. code-block:: singularity

    MirrorURL: https://www.busybox.net/downloads/binaries/1.26.1-defconfig-multiarch/busybox-x86_64

The MirrorURL keyword is mandatory. It specifies a URI to use as a mirror when
downloading the OS.

Notes
"""""

You can build a fully functional BusyBox container that only takes up ~600kB of
disk space!

.. _build-zypper:


``zypper`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec:build-zypper:

This module allows you to build a Suse style container from a mirror URI.

Overview
""""""""

Use the ``zypper`` module to specify a base for a Suse-like container. You must
also specify a URI for the mirror you would like to use.

Keywords
""""""""

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

.. _docker-daemon-archive:

``docker-daemon & docker-archive`` bootstrap agents
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For users using docker locally there are two options for creating Singularity
images without the need for a repository: ``docker-daemon://`` and ``docker-archive://``

Overview
""""""""

``docker-daemon`` allows you to build a SIF from locally running docker daemon
images while ``docker-archive`` let's you build from tar archives of images
pulled from docker.

Keywords
""""""""

.. code-block:: singularity

    From: /path/to/container/file/or/directory

The From keyword is mandatory and applies to these modules in the same nature
as described for other Bootstrap agents.

.. _scratch-agent:

``scratch`` bootstrap agent
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Through all the Bootstrap agents mentioned above, you were essentially building
over a base(parent) image pulled from either Library/Docker/Shub etc, but
Singularity offers support to create even the base images or minimal images to
create your custom containers.

Overview
""""""""

This module allows you to take full control of the content inside your container,
i.e., the user mentions the binaries/packages required for creation of the
container. The installation of any software, necessary config files can all be
mentioned in the ``%setup`` section of the definition file. This agent is
particularly useful for creating minimal image sizes and are more secure since
the creator is fully aware of what's inside the container (ideally only the
items required to run your application) and hence reduces the attack surface.
attack surface.

Keywords
""""""""

.. code-block:: singularity

    Bootstrap: scratch

Since you are building the image from scratch, it does not require and hence
does not support any keywords.

