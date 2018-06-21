========
Appendix
========

.. _build-docker-module:

-------------------
build-docker-module
-------------------

.. _sec:build-docker-module:

Overview
========

Docker images are comprised of layers that are assembled at runtime to create an image. You can use Docker layers to create a base
image, and then add your own custom software. For example, you might use Docker’s Ubuntu image layers to create an Ubuntu Singularity
container. You could do the same with CentOS, Debian, Arch, Suse, Alpine, BusyBox, etc.

Or maybe you want a container that already has software installed. For instance, maybe you want to build a container that uses CUDA
and cuDNN to leverage the GPU, but you don’t want to install from scratch. You can start with one of the ``nvidia/cuda`` containers and
install your software on top of that.

Or perhaps you have already invested in Docker and created your own Docker containers. If so, you can seamlessly convert them to
Singularity with the ``docker`` bootstrap module.

Keywords
========

.. code-block:: none

    Bootstrap: docker

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

.. code-block:: none

    From: <registry>/<namespace>/<container>:<tag>@<digest>

The From keyword is mandatory. It specifies the container to use as a base. ``registry`` is optional and defaults to ``index.docker.io``.
``namespace`` is optional and defaults to ``library``. This is the correct namespace to use for some official containers (ubuntu for example).
``tag`` is also optional and will default to ``latest``

See :ref:`Singularity and Docker <singularity-and-docker>` for more detailed info on using Docker registries.

.. code-block:: none

    Registry: http://custom_registry

The Registry keyword is optional. It will default to ``index.docker.io``.

.. code-block:: none

    Namespace: namespace

The Namespace keyword is optional. It will default to ``library``.

.. code-block:: none

    IncludeCmd: yes

The IncludeCmd keyword is optional. If included, and if a ``%runscript`` is not specified, a Docker ``CMD`` will take precedence over ``ENTRYPOINT``
and will be used as a runscript. Note that the ``IncludeCmd`` keyword is considered valid if it is not empty! This means that
 ``IncludeCmd: yes`` and ``IncludeCmd: no`` are identical. In both cases the ``IncludeCmd`` keyword is not empty, so the Docker ``CMD`` will take precedence
 over an ``ENTRYPOINT``.

 See :ref:`Singularity and Docker <singularity-and-docker>` for more info on order of operations for determining a runscript.


Notes
=====

Docker containers are stored as a collection of tarballs called layers. When building from a Docker container the layers must be downloaded and then
assembled in the proper order to produce a viable file system. Then the file system must be converted to squashfs or ext3 format.

Building from Docker Hub is not considered reproducible because if any of the layers of the image are changed, the container will change.
If reproducibility is important to you, consider hosting a base container on Singularity Hub and building from it instead.

For detailed information about setting your build environment see :ref:`Build Customization <build-environment>`.

.. _build-shub:

----------
build-shub
----------

.. _sec:build-shub:

Overview
========

You can use an existing container on Singularity Hub as your “base,” and then add customization. This allows you to build multiple images
from the same starting point. For example, you may want to build several containers with the same custom python installation, the same custom
compiler toolchain, or the same base MPI installation. Instead of building these from scratch each time, you could create a base container on
Singularity Hub and then build new containers from that existing base container adding customizations in ``%post`` , ``%environment``, ``%runscript``, etc.

Keywords
========

.. code-block:: none

    Bootstrap: shub

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

.. code-block:: none

    From: shub://<registry>/<username>/<container-name>:<tag>@digest

The From keyword is mandatory. It specifies the container to use as a base. ``registry is optional and defaults to ``singularity-hub.org``.
``tag`` and ``digest`` are also optional. ``tag`` defaults to ``latest`` and ``digest`` can be left blank if you want the latest build.

Notes
=====

When bootstrapping from a Singularity Hub image, all previous definition files that led to the creation of the current image will be stored
in a directory within the container called ``/.singularity.d/bootstrap_history``. Singularity will also alert you if environment variables have
been changed between the base image and the new image during bootstrap.

.. _build-localimage:

----------------
build-localimage
----------------

.. _sec:build-localimage:

This module allows you to build a container from an existing Singularity container on your host system. The name is somewhat misleading
because your container can be in either image or directory format.

Overview
========

You can use an existing container image as your “base,” and then add customization. This allows you to build multiple images from the same
starting point. For example, you may want to build several containers with the same custom python installation, the same custom compiler
toolchain, or the same base MPI installation. Instead of building these from scratch each time, you could start with the appropriate local
base container and then customize the new container in ``%post``, ``%environment``, ``%runscript``, etc.

Keywords
========

.. code-block:: none

    Bootstrap: localimage

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

.. code-block:: none

    From: /path/to/container/file/or/directory

The From keyword is mandatory. It specifies the local container to use as a base.

Notes
=====

When building from a local container, all previous definition files that led to the creation of the current container will be stored in a
directory within the container called ``/.singularity.d/bootstrap_history``. Singularity will also alert you if environment variables have been
changed between the base image and the new image during bootstrap.

.. _build-yum:

---------
build-yum
---------

.. _sec:build-yum:

This module allows you to build a Red Hat/CentOS/Scientific Linux style container from a mirror URI.

Overview
========

Use the ``yum`` module to specify a base for a CentOS-like container. You must also specify the URI for the mirror you would like to use.

Keywords
========

.. code-block:: none

    Bootstrap: yum

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

.. code-block:: none

    OSVersion: 7

The OSVersion keyword is optional. It specifies the OS version you would like to use. It is only required if you have specified a %{OSVERSION}
variable in the ``MirrorURL`` keyword.

.. code-block:: none

    MirrorURL: http://mirror.centos.org/centos-%{OSVERSION}/%{OSVERSION}/os/$basearch/

The MirrorURL keyword is mandatory. It specifies the URL to use as a mirror to download the OS. If you define the ``OSVersion`` keyword, than you
can use it in the URL as in the example above.

.. code-block:: none

    Include: yum

The Include keyword is optional. It allows you to install additional packages into the core operating system. It is a best practice to supply
only the bare essentials such that the ``%post`` section has what it needs to properly complete the build. One common package you may want to install
when using the ``yum`` build module is YUM itself.

Notes
=====

There is a major limitation with using YUM to bootstrap a container. The RPM database that exists within the container will be created using the
RPM library and Berkeley DB implementation that exists on the host system. If the RPM implementation inside the container is not compatible with
the RPM database that was used to create the container, RPM and YUM commands inside the container may fail. This issue can be easily demonstrated
by bootstrapping an older RHEL compatible image by a newer one (e.g. bootstrap a Centos 5 or 6 container from a Centos 7 host).

In order to use the ``debootstrap`` build module, you must have ``yum`` installed on your system. It may seem counter-intuitive to install YUM on a system
that uses a different package manager, but you can do so. For instance, on Ubuntu you can install it like so:

.. code-block:: none

    $ sudo apt-get update && sudo apt-get install yum


.. _build-debootstrap:

-----------------
build-debootstrap
-----------------

.. _sec:build-debootstrap:

This module allows you to build a Debian/Ubuntu style container from a mirror URI.

Overview
========

Use the ``debootstrap`` module to specify a base for a Debian-like container. You must also specify the OS version and a URI for the mirror you would like to use.


Keywords
========

.. code-block:: none

    Bootstrap: debootstrap

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

.. code-block:: none

    OSVersion: xenial

The OSVersion keyword is mandatory. It specifies the OS version you would like to use. For Ubuntu you can use code words like ``trusty`` (14.04), ``xenial`` (16.04),
and ``yakkety`` (17.04). For Debian you can use values like ``stable``, ``oldstable``, ``testing``, and ``unstable`` or code words like ``wheezy`` (7), ``jesse`` (8), and ``stretch`` (9).

 .. code-block:: none

     MirrorURL:  http://us.archive.ubuntu.com/ubuntu/

The MirrorURL keyword is mandatory. It specifies a URL to use as a mirror when downloading the OS.

.. code-block:: none

    Include: somepackage

The Include keyword is optional. It allows you to install additional packages into the core operating system. It is a best practice to supply only the bare essentials
such that the ``%post`` section has what it needs to properly complete the build.

Notes
=====

In order to use the ``debootstrap`` build module, you must have ``debootstrap`` installed on your system. On Ubuntu you can install it like so:

.. code-block:: none

    $ sudo apt-get update && sudo apt-get install debootstrap

On CentOS you can install it from the epel repos like so:

.. code-block:: none

    $ sudo yum update && sudo yum install epel-release && sudo yum install debootstrap.noarch

.. _build-arch:

----------
build-arch
----------

.. _sec:build-arch:

This module allows you to build a Arch Linux based container.

Overview
========

Use the ``arch`` module to specify a base for an Arch Linux based container. Arch Linux uses the aptly named the ``pacman`` package manager (all puns intended).


Keywords
========

.. code-block:: none

    Bootstrap: arch

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

The Arch Linux bootstrap module does not name any additional keywords at this time. By defining the ``arch`` module, you have essentially given all of the
information necessary for that particular bootstrap module to build a core operating system.

Notes
=====

Arch Linux is, by design, a very stripped down, light-weight OS. You may need to perform a fair amount of configuration to get a usable OS. Please refer
to this `README.md <https://github.com/singularityware/singularity/blob/master/examples/arch/README.md>`_ and
the `Arch Linux example <https://github.com/singularityware/singularity/blob/master/examples/arch/Singularity>`_ for more info.

.. _build-busybox:

-------------
build-busybox
-------------

.. _sec:build-busybox:

This module allows you to build a container based on BusyBox.

Overview
========

Use the ``busybox`` module to specify a BusyBox base for container. You must also specify a URI for the mirror you would like to use.

Keywords
========

.. code-block:: none

    Bootstrap: busybox

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

.. code-block:: none

    MirrorURL: https://www.busybox.net/downloads/binaries/1.26.1-defconfig-multiarch/busybox-x86_64

The MirrorURL keyword is mandatory. It specifies a URL to use as a mirror when downloading the OS.

Notes
=====

You can build a fully functional BusyBox container that only takes up ~600kB of disk space!

.. _build-zypper:

------------
build-zypper
------------

.. _sec:build-zypper:

This module allows you to build a Suse style container from a mirror URI.

Overview
========

Use the ``zypper`` module to specify a base for a Suse-like container. You must also specify a URI for
the mirror you would like to use.

Keywords
========

.. code-block:: none

    Bootstrap: zypper

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

.. code-block:: none

    OSVersion: 42.2

The OSVersion keyword is optional. It specifies the OS version you would like to use.
It is only required if you have specified a %{OSVERSION} variable in the ``MirrorURL`` keyword.

.. code-block:: none

    Include: somepackage

The Include keyword is optional. It allows you to install additional packages into the core operating system.
It is a best practice to supply only the bare essentials such that the ``%post`` section has what it needs to properly complete the build.
One common package you may want to install when using the zypper build module is ``zypper`` itself.

.. _singularity-action-flags:

------------------------
Singularity Action Flags
------------------------
.. _sec:action-flags:

For each of ``exec``, ``run``, and ``shell``, there are a few important flags that we want to note for new users that have substantial impact on using
your container. While we won’t include the complete list of run options (for this complete list see ``singularity run --help`` or more generally
``singularity <action> --help``) we will review some highly useful flags that you can add to these actions.

-  **--contain**: Contain suggests that we want to better isolate the container runtime from the host. Adding the ``--contain`` flag will use minimal
``/dev`` and empty other directories (e.g., ``/tmp``).

-  **--containall**: In addition to what is provided with ``--contain`` (filesystems) also contain PID, IPC, and environment.

-  **--cleanenv**: Clean the environment before running the container.

-  **--pwd**: Initial working directory for payload process inside the container.

This is **not** a complete list! Please see the ``singularity <action> help`` for an updated list.


Examples
========

Here we are cleaning the environment. In the first command, we see that the variable ``PEANUTBUTTER`` gets passed into the container.

.. code-block:: none

    PEANUTBUTTER=JELLY singularity exec Centos7.img env | grep PEANUT

    PEANUTBUTTER=JELLY

And now here we add ``--cleanenv`` to see that it doesn’t.

.. code-block:: none

    PEANUTBUTTER=JELLY singularity exec --cleanenv Centos7.img env | grep PEANUT

Here we will test contain. We can first confirm that there are a lot of files on our host in /tmp, and the same files are found in the container.

.. code-block:: none

    # On the host

    $ ls /tmp | wc -l

    17


    # And then /tmp is mounted to the container, by default

    $ singularity exec Centos7.img  ls /tmp | wc -l


    # ..but not if we use --contain

    $ singularity exec --contain Centos7.img  ls /tmp | wc -l

    0

--------
Commands
--------

.. _command-usage:

Command Usage
=============

.. _sec:commandlineinterface:

The Singularity command
-----------------------

Singularity uses a primary command wrapper called ``singularity``. When you run ``singularity``
without any options or arguments it will dump the high level usage
syntax.

The general usage form is:

.. code-block:: none

    $ singularity (opts1) [subcommand] (opts2) ...

If you type ``singularity`` without any arguments, you will see a high
level help for all arguments. The main options include:
**Container Actions**

-  :ref:`build <build-command>` : Build a container on your user endpoint or build environment

-  :ref:`exec <exec-command>` : Execute a command to your container

-  :ref:`inspect <inspect-command>` : See labels, run and test scripts, and environment variables

-  :ref:`pull <pull-command>` : pull an image from Docker or Singularity Hub

-  :ref:`run <run-command>` : Run your image as an executable

-  :ref:`shell <shell-command>` : Shell into your image

**Image Commands**

-  :ref:`image.import <image-import>` : import layers or other file content to your image

-  :ref:`image.export <image-export>` : export the contents of the image to tar or stream

-  :ref:`image.create <image-create>` : create a new image, using the old ext3 filesystem

-  :ref:`image.expand <image-expand>` : increase the size of your image (old ext3)

**Instance Commands**

Instances were added in 2.4. This list is brief, and likely to expand
with further development.

-  :ref:`instances <running-services>` : Start, stop, and list container instances

**Deprecated Commands**
The following commands are deprecated in 2.4 and will be removed in
future releases.

-  :ref:`bootstrap <bootstrap>` : Bootstrap a container recipe

For the full usage, :ref:`see the bottom of this page <command-usage>`

Options and argument processing
'''''''''''''''''''''''''''''''

Because of the nature of how Singularity cascades commands and
sub-commands, argument processing is done with a mandatory order.
**This means that where you place arguments is important!** In the
above usage example, ``opts1`` are the global Singularity run-time options.
These options are always applicable no matter what subcommand you
select (e.g. ``--verbose`` or ``--debug`` ). But subcommand specific options must be passed
after the relevant subcommand.

To further clarify this example, the ``exec`` Singularity subcommand will
execute a program within the container and pass the arguments passed
to the program. So to mitigate any argument clashes, Singularity must
not interpret or interfere with any of the command arguments or
options that are not relevant for that particular function.

Singularity Help
''''''''''''''''

Singularity comes with some internal documentation by using the ``help``
subcommand followed by the subcommand you want more information about.
For example:

    .. code-block:: none

        $ singularity help create

        CREATE OPTIONS:

            -s/--size   Specify a size for an operation in MiB, i.e. 1024*1024B

                        (default 768MiB)

            -F/--force  Overwrite an image file if it exists


        EXAMPLES:


            $ singularity create /tmp/Debian.img

            $ singularity create -s 4096 /tmp/Debian.img


        For additional help, please visit our public documentation pages which are

        found at:


            https://www.sylabs.io/docs/


Commands Usage
--------------

    .. _sec:commandsusage:

    .. code-block:: none

        USAGE: singularity [global options...] <command> [command options...] ...


        GLOBAL OPTIONS:

            -d|--debug    Print debugging information

            -h|--help     Display usage summary

            -s|--silent   Only print errors

            -q|--quiet    Suppress all normal output

               --version  Show application version

            -v|--verbose  Increase verbosity +1

            -x|--sh-debug Print shell wrapper debugging information


        GENERAL COMMANDS:

            help       Show additional help for a command or container

            selftest   Run some self tests for singularity install


        CONTAINER USAGE COMMANDS:

            exec       Execute a command within container

            run        Launch a runscript within container

            shell      Run a Bourne shell within container

            test       Launch a testscript within container


        CONTAINER MANAGEMENT COMMANDS:

            apps       List available apps within a container

            bootstrap  *Deprecated* use build instead

            build      Build a new Singularity container

            check      Perform container lint checks

            inspect    Display a container's metadata

            mount      Mount a Singularity container image

            pull       Pull a Singularity/Docker container to $PWD


        COMMAND GROUPS:

            image      Container image command group

            instance   Persistent instance command group



        CONTAINER USAGE OPTIONS:

            see singularity help <command>


        For any additional help or support visit the Singularity

        website: https://www.sylabs.io/contact/


Support
-------

Have a question, or need further information? `Reach out to us <https://www.sylabs.io/contact/>`_.


.. _build-command:

build
=====

Use ``build`` to download and assemble existing containers, convert containers
from one format to another, or build a container from a :ref:`Singularity recipe <container-recipes>`.

Overview
--------

The ``build`` command accepts a target as input and produces a container as
output. The target can be a Singularity Hub or Docker Hub URI, a path
to an existing container, or a path to a Singularity Recipe file. The
output container can be in squashfs, ext3, or directory format.

For a complete list of ``build`` options type ``singularity help build``. For more info on building
containers see :ref:`Build a Container <build-a-container>`.

Examples
--------

Download an existing container from Singularity Hub or Docker Hub
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity build lolcow.simg shub://GodloveD/lolcow

    $ singularity build lolcow.simg docker://godlovedc/lolcow

Create --writable images and --sandbox directories
''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ sudo singularity build --writable lolcow.img shub://GodloveD/lolcow

    $ sudo singularity build --sandbox lolcow/ shub://GodloveD/lolcow

Convert containers from one format to another
'''''''''''''''''''''''''''''''''''''''''''''

You can convert the three supported container formats using any
combination.

.. code-block:: none

    $ sudo singularity build --writable development.img production.simg

    $ singularity build --sandbox development/ production.simg

    $ singularity build production2 development/

Build a container from a Singularity recipe
'''''''''''''''''''''''''''''''''''''''''''

Given a Singularity Recipe called ``Singularity`` :

.. code-block:: none

    $ sudo singularity build lolcow.simg Singularity


.. _exec-command:

exec
====

The ``exec`` Singularity sub-command allows you to spawn an arbitrary command
within your container image as if it were running directly on the host
system. All standard IO, pipes, and file systems are accessible via the
command being exec’ed within the container. Note that this exec is
different from the Docker exec, as it does not require a container to be
“running” before using it.

Examples
--------

Printing the OS release inside the container
''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity exec container.img cat /etc/os-release

    PRETTY_NAME="Debian GNU/Linux 8 (jessie)"

    NAME="Debian GNU/Linux"

    VERSION_ID="8"

    VERSION="8 (jessie)"

    ID=debian

    HOME_URL="http://www.debian.org/"

    SUPPORT_URL="http://www.debian.org/support"

    BUG_REPORT_URL="https://bugs.debian.org/"

    $

Printing the OS release for a running instance
''''''''''''''''''''''''''''''''''''''''''''''

Use the ``instance://<instance name>`` syntax like so:

.. code-block:: none

    $ singularity exec instance://my-instance cat /etc/os-release

Runtime Flags
'''''''''''''

If you are interested in containing an environment or filesystem
locations, we highly recommend that you look at the ``singularity run help`` and our
documentation on :ref:`flags <singularity-action-flags>` to better customize this command.

Special Characters
''''''''''''''''''

And properly passing along special characters to the program within the
container.

.. code-block:: none

    $ singularity exec container.img echo -ne "hello\nworld\n\n"

    hello

    world

    $

And a demonstration using pipes:

.. code-block:: none

    $ cat debian.def | singularity exec container.img grep 'MirrorURL'

    MirrorURL "http://ftp.us.debian.org/debian/"

    $

A Python example
''''''''''''''''

Starting with the file ``hello.py`` in the current directory with the contents of:

.. code-block:: none

    #!/usr/bin/python


    import sys

    print("Hello World: The Python version is %s.%s.%s" % sys.version_info[:3])


Because our home directory is automatically bound into the container,
and we are running this from our home directory, we can easily execute
that script using the Python within the container:

.. code-block:: none

    $ singularity exec /tmp/Centos7-ompi.img /usr/bin/python hello.py

    Hello World: The Python version is 2.7.5


We can also pipe that script through the container and into the Python
binary which exists inside the container using the following command:

.. code-block:: none

    $ cat hello.py | singularity exec /tmp/Centos7-ompi.img /usr/bin/python

    Hello World: The Python version is 2.7.5


For demonstration purposes, let’s also try to use the latest Python
container which exists in DockerHub to run this script:

.. code-block:: none

    $ singularity exec docker://python:latest /usr/local/bin/python hello.py

    library/python:latest

    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4

    Downloading layer: sha256:fbd06356349dd9fb6af91f98c398c0c5d05730a9996bbf88ff2f2067d59c70c4

    Downloading layer: sha256:644eaeceac9ff6195008c1e20dd693346c35b0b65b9a90b3bcba18ea4bcef071

    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4

    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4

    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4

    Downloading layer: sha256:766692404ca72f4e31e248eb82f8eca6b2fcc15b22930ec50e3804cc3efe0aba

    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4

    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4

    Downloading layer: sha256:6a3d69edbe90ef916e1ecd8d197f056de873ed08bcfd55a1cd0b43588f3dbb9a

    Downloading layer: sha256:ff18e19c2db42055e6f34323700737bde3c819b413997cddace2c1b7180d7efd

    Downloading layer: sha256:7b9457ec39de00bc70af1c9631b9ae6ede5a3ab715e6492c0a2641868ec1deda

    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4

    Downloading layer: sha256:6a5a5368e0c2d3e5909184fa28ddfd56072e7ff3ee9a945876f7eee5896ef5bb

    Hello World: The Python version is 3.5.2


A GPU example
'''''''''''''

If your host system has an NVIDIA GPU card and a driver installed you
can leverage the card with the ``--nv`` option. (This example requires a fairly
recent version of the NVIDIA driver on the host system to run the latest
version of TensorFlow.

.. code-block:: none

    $ git clone https://github.com/tensorflow/models.git

    $ singularity exec --nv docker://tensorflow/tensorflow:latest-gpu \

        python ./models/tutorials/image/mnist/convolutional.py

    Docker image path: index.docker.io/tensorflow/tensorflow:latest-gpu

    Cache folder set to /home/david/.singularity/docker

    [19/19] |===================================| 100.0%

    Creating container runtime...

    Extracting data/train-images-idx3-ubyte.gz

    Extracting data/train-labels-idx1-ubyte.gz

    Extracting data/t10k-images-idx3-ubyte.gz

    Extracting data/t10k-labels-idx1-ubyte.gz

    2017-08-18 20:33:59.677580: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.1 instructions, but these are available on your machine and could speed up CPU computations.

    2017-08-18 20:33:59.677620: W tensorflow/core/platform/cpu_feature_guard.cc:45] The TensorFlow library wasn't compiled to use SSE4.2 instructions, but these are available on your machine and could speed up CPU computations.

    2017-08-18 20:34:00.148531: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:893] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero

    2017-08-18 20:34:00.148926: I tensorflow/core/common_runtime/gpu/gpu_device.cc:955] Found device 0 with properties:

    name: GeForce GTX 760 (192-bit)

    major: 3 minor: 0 memoryClockRate (GHz) 0.8885

    pciBusID 0000:03:00.0

    Total memory: 2.95GiB

    Free memory: 2.92GiB

    2017-08-18 20:34:00.148954: I tensorflow/core/common_runtime/gpu/gpu_device.cc:976] DMA: 0

    2017-08-18 20:34:00.148965: I tensorflow/core/common_runtime/gpu/gpu_device.cc:986] 0:   Y

    2017-08-18 20:34:00.148979: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1045] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce GTX 760 (192-bit), pci bus id: 0000:03:00.0)

    Initialized!

    Step 0 (epoch 0.00), 21.7 ms

    Minibatch loss: 8.334, learning rate: 0.010000

    Minibatch error: 85.9%

    Validation error: 84.6%

    Step 100 (epoch 0.12), 20.9 ms

    Minibatch loss: 3.235, learning rate: 0.010000

    Minibatch error: 4.7%

    Validation error: 7.8%

    Step 200 (epoch 0.23), 20.5 ms

    Minibatch loss: 3.363, learning rate: 0.010000

    Minibatch error: 9.4%

    Validation error: 4.2%

    [...snip...]

    Step 8500 (epoch 9.89), 20.5 ms

    Minibatch loss: 1.602, learning rate: 0.006302

    Minibatch error: 0.0%

    Validation error: 0.9%

    Test error: 0.8%

.. _inspect-command:

inspect
=======

How can you sniff an image? We have provided the inspect command for
you to easily see the runscript, test script, environment, help, and
metadata labels.

This command is essential for making containers understandable by
other tools and applications.

JSON Api Standard
-----------------

For any inspect command, by adding ``--json`` you can be assured to get a
JSON API standardized response, for example:

.. code-block:: none

    singularity inspect -l --json ubuntu.img

    {

        "data": {

            "attributes": {

                "labels": {

                    "SINGULARITY_DEFFILE_BOOTSTRAP": "docker",

                    "SINGULARITY_DEFFILE": "Singularity",

                    "SINGULARITY_BOOTSTRAP_VERSION": "2.2.99",

                    "SINGULARITY_DEFFILE_FROM": "ubuntu:latest"

                }

            },

            "type": "container"

        }

    }


Inspect Flags
-------------

The default, if run without any arguments, will show you the container
labels file

.. code-block:: none

    $ singularity inspect ubuntu.img

    {

        "SINGULARITY_DEFFILE_BOOTSTRAP": "docker",

        "SINGULARITY_DEFFILE": "Singularity",

        "SINGULARITY_BOOTSTRAP_VERSION": "2.2.99",

        "SINGULARITY_DEFFILE_FROM": "ubuntu:latest"

    }

and as outlined in the usage, you can specify to see any combination of ``--labels``
, ``--environment`` , ``--runscript`` , ``--test`` , and ``--deffile``. The quick command to see everything, in json format, would
be:

.. code-block:: none

    $ singularity inspect -l -r -d -t -e -j -hf ubuntu.img

    {

        "data": {

            "attributes": {

                "test": null,

                "help": "This is how you run the image!\n",

                "environment": "# Custom environment shell code should follow\n\n",

                "labels": {

                    "SINGULARITY_DEFFILE_BOOTSTRAP": "docker",

                    "SINGULARITY_DEFFILE": "Singularity",

                    "SINGULARITY_BOOTSTRAP_VERSION": "2.2.99",

                    "SINGULARITY_DEFFILE_FROM": "ubuntu:latest"

                },

                "deffile": "Bootstrap:docker\nFrom:ubuntu:latest\n",

                "runscript": "#!/bin/sh\n\nexec /bin/bash \"$@\""

            },

            "type": "container"

        }

    }

Labels
''''''

The default, if run without any arguments, will show you the container
labels file (located at ``/.singularity.d/labels.json`` in the container. These labels are the ones that
you define in the ``%labels`` section of your bootstrap file, along with any Docker ``LABEL``
that came with an image that you imported, and other metadata about the
bootstrap. For example, here we are inspecting labels for ``ubuntu.img``

.. code-block:: none

    $ singularity inspect ubuntu.img

    {

        "SINGULARITY_DEFFILE_BOOTSTRAP": "docker",

        "SINGULARITY_DEFFILE": "Singularity",

        "SINGULARITY_BOOTSTRAP_VERSION": "2.2.99",

        "SINGULARITY_DEFFILE_FROM": "ubuntu:latest"

    }

This is the equivalent of both of:

.. code-block:: none

    $ singularity inspect -l ubuntu.img

    $ singularity inspect --labels ubuntu.img

Runscript
'''''''''

The commands ``--runscript`` or ``--r`` will show you the runscript, which also can be shown in ``--json``:

.. code-block:: none

    $ singularity inspect -r -j ubuntu.img{

        "data": {

            "attributes": {

                "runscript": "#!/bin/sh\n\nexec /bin/bash \"$@\""

            },

            "type": "container"

        }

    }


or in a human friendly, readable print to the screen:

.. code-block:: none

    $ singularity inspect -r ubuntu.img


    ##runscript

    #!/bin/sh


    exec /bin/bash "$@"


Help
''''

The commands ``--helpfile`` or ``--hf`` will show you the runscript helpfile, if it exists.
With ``--json`` you can also see it as such:

.. code-block:: none

    singularity inspect -hf -j dino.img

    {

        "data": {

            "attributes": {

                "help": "\n\n\nHi there! This is my image help section.\n\nUsage:\n\nboobeep doo doo\n\n --arg/a arrrrg I'm a pirate!\n --boo/b eeeeeuzzz where is the honey?\n\n\n"

            },

            "type": "container"

        }

    }


or in a human friendly, readable print to the screen, don’t use ``-j`` or ``--json``:

.. code-block:: none

    $ singularity inspect -hf dino.img



    Hi there! This is my image help section.


    Usage:


    boobeep doo doo


     --arg/a arrrrg I'm a pirate!

     --boo/b eeeeeuzzz where is the honey?


Environment
'''''''''''

The commands ``--environment`` and ``-e`` will show you the container’s environment, again
specified by the ``%environment`` section of a bootstrap file, and other ENV labels that
might have come from a Docker import. You can again choose to see ``--json`` :

.. code-block:: none

    $ singularity inspect -e --json ubuntu.img

    {

        "data": {

            "attributes": {

                "environment": "# Custom environment shell code should follow\n\n"

            },

            "type": "container"

        }

    }


or human friendly:

.. code-block:: none

    $ singularity inspect -e ubuntu.img


    ##environment

    # Custom environment shell code should follow


The container in the example above did not have any custom environment

variables set.


Test
''''

The equivalent ``--test`` or ``-t`` commands will print any test defined for the
container, which comes from the  ``%test`` section of the bootstrap specification
Singularity file. Again, we can ask for ``--json`` or human friendly (default):

.. code-block:: none

    $ singularity --inspect -t --json ubuntu.img

    {

        "data": {

            "attributes": {

                "test": null

            },

            "type": "container"

        }

    }


    $ singularity inspect -t  ubuntu.img

    {

        "status": 404,

        "detail": "This container does not have any tests defined",

        "title": "Tests Undefined"

    }


Deffile
'''''''

Want to know where your container came from? You can see the entire
Singularity definition file, if the container was created with a
bootstrap, by using ``--deffile`` or ``-d``:

.. code-block:: none

    $ singularity inspect -d  ubuntu.img


    ##deffile

    Bootstrap:docker

    From:ubuntu:latest


or with ``--json`` output.

.. code-block:: none

    $ singularity inspect -d --json ubuntu.img

    {

        "data": {

            "attributes": {

                "deffile": "Bootstrap:docker\nFrom:ubuntu:latest\n"

            },

            "type": "container"

        }

    }

The goal of these commands is to bring more transparency to containers,
and to help better integrate them into common workflows by having them
expose their guts to the world! If you have feedback for how we can
improve or amend this, `please let us know <https://github.com/singularityware/singularity/issues>`_!

.. _pull-command:

pull
====

.. _sec:pull:

Singularity ``pull`` is the command that you would want to use to communicate
with a container registry. The command does exactly as it says - there
exists an image external to my host, and I want to pull it here. We
currently support pull for both `Docker <https://hub.docker.com/>`_ and `Singularity Hub
images <https://singularity-hub.org/>`_, and will review usage for both.

Singularity Hub
---------------

Singularity differs from Docker in that we serve entire images, as
opposed to layers. This means that pulling a Singularity Hub means
downloading the entire (compressed) container file, and then having it
extract on your local machine. The basic command is the following:

.. code-block:: none

    singularity pull shub://vsoch/hello-world

    Progress |===================================| 100.0%

    Done. Container is at: ./vsoch-hello-world-master.img


How do tags work?
'''''''''''''''''

On Singularity Hub, a ``tag`` coincide with a branch. So if you have a repo
called ``vsoch/hello-world`` , by default the file called ``Singularity`` (your build recipe file) will be
looked for in the base of the master branch. The command that we issued
above would be equivalent to doing:

.. code-block:: none

    singularity pull shub://vsoch/hello-world:master

To enable other branches to build, they must be turned on in your
collection. If you then put another Singularity file in a branch called development,
you would pull it as follows:

.. code-block:: none

    singularity pull shub://vsoch/hello-world:development

The term ``latest`` in Singularity Hub will pull, across all of your
branches, the most recent image. If ``development`` is more recent than
``master``, it would be pulled, for example.

Image Names
'''''''''''

As you can see, since we didn’t specify anything special, the default
naming convention is to use the username, reponame, and the branch
(tag). You have three options for changing this:

.. code-block:: none

    PULL OPTIONS:

        -n/--name   Specify a custom container name (first priority)

        -C/--commit Name container based on GitHub commit (second priority)

        -H/--hash   Name container based on file hash (second priority)


Custom Name
'''''''''''

.. code-block:: none

    singularity pull --name meatballs.img shub://vsoch/hello-world

    Progress |===================================| 100.0%

    Done. Container is at: ./meatballs.img


Name by commit
''''''''''''''

Each container build on Singularity Hub is associated with the GitHub
commit of the repo that was used to build it. You can specify to name
your container based on the commit with the ``--commit`` flag, if, for example, you
want to match containers to their build files:

.. code-block:: none

    singularity pull --commit shub://vsoch/hello-world

    Progress |===================================| 100.0%

    Done. Container is at: ./4187993b8b44cbfa51c7e38e6b527918fcdf0470.img


Name by hash
''''''''''''

If you prefer the hash of the file itself, you can do that too.

.. code-block:: none

    singularity pull --hash shub://vsoch/hello-world

    Progress |===================================| 100.0%

    Done. Container is at: ./4db5b0723cfd378e332fa4806dd79e31.img


Pull to different folder
''''''''''''''''''''''''

For any of the above, if you want to specify a different folder for
your image, you can define the variable ``SINGULARITY_PULLFOLDER``. By default, we will first
check if you have the ``SINGULARITY_CACHEDIR`` defined, and pull images there. If not, we look
for ``SINGULARITY_PULLFOLDER``. If neither of these are defined, the image is pulled to the
present working directory, as we showed above. Here is an example of
pulling to ``/tmp`` .

.. code-block:: none

    SINGULARITY_PULLFOLDER=/tmp

    singularity pull shub://vsoch/hello-world

    Progress |===================================| 100.0%

    Done. Container is at: /tmp/vsoch-hello-world-master.img


Pull by commit
''''''''''''''

You can also pull different versions of your container by using their
commit id ( ``version`` ).

.. code-block:: none

    singularity pull shub://vsoch/hello-world@42e1f04ed80217895f8c960bdde6bef4d34fab59

    Progress |===================================| 100.0%

    Done. Container is at: ./vsoch-hello-world-master.img


In this example, the first build of this container will be pulled.

Docker
------

Docker pull is similar (on the surface) to a Singularity Hub pull, and
we would do the following:

.. code-block:: none

    singularity pull docker://ubuntu

    Initializing Singularity image subsystem

    Opening image file: ubuntu.img

    Creating 223MiB image

    Binding image to loop

    Creating file system within image

    Image is done: ubuntu.img

    Docker image path: index.docker.io/library/ubuntu:latest

    Cache folder set to /home/vanessa/.singularity/docker

    Importing: base Singularity environment

    Importing: /home/vanessa/.singularity/docker/sha256:b6f892c0043b37bd1834a4a1b7d68fe6421c6acbc7e7e63a4527e1d379f92c1b.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:55010f332b047687e081a9639fac04918552c144bc2da4edb3422ce8efcc1fb1.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:2955fb827c947b782af190a759805d229cfebc75978dba2d01b4a59e6a333845.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:3deef3fcbd3072b45771bd0d192d4e5ff2b7310b99ea92bce062e01097953505.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:cf9722e506aada1109f5c00a9ba542a81c9e109606c01c81f5991b1f93de7b66.tar.gz

    Importing: /home/vanessa/.singularity/metadata/sha256:fe44851d529f465f9aa107b32351c8a0a722fc0619a2a7c22b058084fac068a4.tar.gz

    Done. Container is at: ubuntu.img

If you specify the tag, the image would be named accordingly (eg, ``ubuntu-latest.img``). Did
you notice that the output looks similar to if we did the following?

.. code-block:: none

    singularity create ubuntu.img

    singularity import ubuntu.img docker://ubuntu

this is because the same logic is happening on the back end. Thus, the
pull command with a docker uri also supports arguments ``--size`` and ``--name`` . Here is how I
would pull an ubuntu image, but make it bigger, and name it something
else.

.. code-block:: none

    singularity pull --size 2000 --name jellybelly.img docker://ubuntu

    Initializing Singularity image subsystem

    Opening image file: jellybelly.img

    Creating 2000MiB image

    Binding image to loop

    Creating file system within image

    Image is done: jellybelly.img

    Docker image path: index.docker.io/library/ubuntu:latest

    Cache folder set to /home/vanessa/.singularity/docker

    Importing: base Singularity environment

    Importing: /home/vanessa/.singularity/docker/sha256:b6f892c0043b37bd1834a4a1b7d68fe6421c6acbc7e7e63a4527e1d379f92c1b.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:55010f332b047687e081a9639fac04918552c144bc2da4edb3422ce8efcc1fb1.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:2955fb827c947b782af190a759805d229cfebc75978dba2d01b4a59e6a333845.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:3deef3fcbd3072b45771bd0d192d4e5ff2b7310b99ea92bce062e01097953505.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:cf9722e506aada1109f5c00a9ba542a81c9e109606c01c81f5991b1f93de7b66.tar.gz

    Importing: /home/vanessa/.singularity/metadata/sha256:fe44851d529f465f9aa107b32351c8a0a722fc0619a2a7c22b058084fac068a4.tar.gz

    Done. Container is at: jellybelly.img

.. _run-command:

run
===

It’s common to want your container to “do a thing.” Singularity ``run`` allows
you to define a custom action to be taken when a container is either ``run`` or
executed directly by file name. Specifically, you might want it to
execute a command, or run an executable that gives access to many
different functions for the user.

Overview
--------

First, how do we run a container? We can do that in one of two ways -
the commands below are identical:

.. code-block:: none

    $ singularity run centos7.img

    $ ./centos7.img


In both cases, we are executing the container’s “runscript” (the
executable ``/singularity`` at the root of the image) that is either an actual file
(version 2.2 and earlier) or a link to one (2.3 and later). For example,
looking at a 2.3 image, I can see the runscript via the path to the
link:

.. code-block:: none

    $ singularity exec centos7.img cat /singularity

    #!/bin/sh


    exec /bin/bash "$@"


or to the actual file in the container’s metadata folder, ``/.singularity.d``

.. code-block:: none

    $ singularity exec centos7.img cat /.singularity.d/runscript

    #!/bin/sh


    exec /bin/bash "$@"

Notice how the runscript has bash followed by ``\$@`` ? This is good practice
to include in a runscript, as any arguments passed by the user will be
given to the container.

Runtime Flags
-------------

If you are interested in containing an environment or filesystem
locations, we highly recommend that you look at the ``singularity run help`` and our
documentation on :ref:`flags <singularity-action-flags>`
to better customize this command.

Examples
--------

In this example the container has a very simple runscript defined.

.. code-block:: none

    $ singularity exec centos7.img cat /singularity

    #!/bin/sh


    echo motorbot


    $ singularity run centos7.img

    motorbot


Defining the Runscript
''''''''''''''''''''''

When you first create a container, the runscript is defined using the
following order of operations:

#. A user defined runscript in the ``%runscript`` section of a bootstrap takes
   preference over all

#. If the user has not defined a runscript and is importing a Docker
   container, the Docker ``ENTRYPOINT`` is used.

#. If a user has not defined a runscript and adds ``IncludeCmd: yes`` to the bootstrap file,
   the ``CMD`` is used over the ``ENTRYPOINT``

#. If the user has not defined a runscript and the Docker container
  doesn’t have an ``ENTRYPOINT``, we look for ``CMD``, even if the user hasn’t asked for it.

#. If the user has not defined a runscript, and there is no ``ENTRYPOINT`` or ``CMD`` (or we
   aren’t importing Docker at all) then we default to ``/bin/bash``

Here is how you would define the runscript section when you :ref:`build <build-a-container>` an image:

.. code-block:: none

    Bootstrap: docker

    From: ubuntu:latest


    %runscript

    exec /usr/bin/python "$@"


and of course python should be installed as /usr/bin/python. The
addition of ``$@`` ensures that arguments are passed along from the user. If
you want your container to run absolutely any command given to it, and
you want to use run instead of exec, you could also just do:

.. code-block:: none

    Bootstrap: docker

    From: ubuntu:latest


    %runscript

    exec "$@"`


If you want different entrypoints for your image, we recommend using the
%apprun syntax (see :ref:`apps <reproducible-sci-f-apps>`). Here we have two entrypoints for foo and bar:

.. code-block:: none

    %runscript

    exec echo "Try running with --app dog/cat"


    %apprun dog

    exec echo Hello "$@", this is Dog


    %apprun cat

    exec echo Meow "$@", this is Cat


and then running (after build of a complete recipe) would look like:

.. code-block:: none

    sudo singularity build catdog.simg Singularity


    $ singularity run catdog.simg

    Try running with --app dog/cat


    $ singularity run --app cat catdog.simg

    Meow , this is Cat

    $ singularity run --app dog catdog.simg

    Hello , this is Dog


Generally, it is advised to provide help for your container with ``%help`` or ``%apphelp``. If
you find it easier, you can also provide help by way of a runscript that
tells your user how to use the container, and gives access to the
important executables. Regardless of your strategy. a reproducible
container is one that tells the user how to interact with it.

.. _shell-command:

shell
=====

The ``shell`` Singularity sub-command will automatically spawn an interactive
shell within a container. As of v2.3 the default that is spawned via the
shell command is ``/bin/bash`` if it exists otherwise ``/bin/sh`` is called.

.. code-block:: none

    $ singularity shell

    USAGE: singularity (options) shell [container image] (options)

Here we can see the default shell in action:

.. code-block:: none

    $ singularity shell centos7.img

    Singularity: Invoking an interactive shell within container...


    Singularity centos7.img:~> echo $SHELL

    /bin/bash


Additionally any arguments passed to the Singularity command (after the
container name) will be passed to the called shell within the container,
and shell can be used across image types. Here is a quick example of
shelling into a container assembled from Docker layers. We highly
recommend that you look at the ``singularity shell help`` and our documentation on :ref:`flags <singularity-action-flags>` to
better customize this command.

Change your shell
-----------------

The ``shell`` sub-command allows you to set or change the default shell using the ``--shell``
argument. As of Singularity version 2.2, you can also use the
environment variable ``SINGULARITY_SHELL`` which will use that as your shell entry point into
the container.

Bash
''''

The correct way to do it:

.. code-block:: none

        export SINGULARITY_SHELL="/bin/bash --norc"

        singularity shell centos7.img Singularity: Invoking an interactive shell within container...

        Singularity centos7.img:~/Desktop> echo $SHELL

        /bin/bash --norc


Don’t do this, it can be confusing:

.. code-block:: none

    $ export SINGULARITY_SHELL=/bin/bash

    $ singularity shell centos7.img

    Singularity: Invoking an interactive shell within container...


    # What? We are still on my Desktop? Actually no, but the uri says we are!

    vanessa@vanessa-ThinkPad-T460s:~/Desktop$ echo $SHELL

    /bin/bash


Depending on your shell, you might also want the ``--noprofile`` flag. How can you learn
more about a shell? Ask it for help, of course!

Shell Help
----------

.. code-block:: none

    $ singularity shell centos7.img --help

    Singularity: Invoking an interactive shell within container...


    GNU bash, version 4.2.46(1)-release-(x86_64-redhat-linux-gnu)

    Usage:  /bin/bash [GNU long option] [option] ...

        /bin/bash [GNU long option] [option] script-file ...

    GNU long options:

        --debug

        --debugger

        --dump-po-strings

        --dump-strings

        --help

        --init-file

        --login

        --noediting

        --noprofile

        --norc

        --posix

        --protected

        --rcfile

        --rpm-requires

        --restricted

        --verbose

        --version

    Shell options:

        -irsD or -c command or -O shopt_option      (invocation only)

        -abefhkmnptuvxBCHP or -o option

    Type `/bin/bash -c "help set"' for more information about shell options.

    Type `/bin/bash -c help' for more information about shell builtin commands.


And thus we should be able to do:

.. code-block:: none

    $ singularity shell centos7.img -c "echo hello world"

    Singularity: Invoking an interactive shell within container...


    hello world

-------------------
Image Command Group
-------------------

.. _image-export:

image.export
============

.. _sec:imageexport:

Export is a way to dump the contents of your container into a ``.tar.gz``, or a
stream to put into some other place. For example, you could stream
this into an in memory tar in python. Importantly, this command was
originally intended for Singularity version less than 2.4 in the case
of exporting an ext3 filesystem. For Singularity greater than 2.4, the
resulting export file is likely to be larger than the original
squashfs counterpart. An example with an ext3 image is provided.

Here we export an image into a ``.tar`` file:

.. code-block:: none

    singularity image.export container.img > container.tar

We can also specify the file with ``--file``

.. code-block:: none

  singularity image.export --file container.tar container.img

And here is the recommended way to compress your image:

.. code-block:: none

    singularity image.export container.img | gzip -9 > container.img.tar.gz

.. _image-expand:

image.expand
============

.. _sec:imageexpand:

While the squashfs filesystem means that you typically don’t need to
worry about the size of your container being built, you might find that
if you are building an ext3 image (pre Singularity 2.4) you want to
expand it.

Increasing the size of an existing image
----------------------------------------

You can increase the size of an image after it has been instantiated
by using the image.expand Singularity sub-command. In the example
below, we:

#. create an empty image

#. inspect it’s size

#. expand it

#. confirm it’s larger

.. code-block:: none

    $ singularity image.create container.img

    Creating empty 768MiB image file: container.imglarity image.create container.im

    Formatting image with ext3 file system

    Image is done: container.img


    $ ls -lh container.img

    -rw-rw-r-- 1 vanessa vanessa 768M Oct  2 18:48 container.img


    $ singularity image.expand container.img

    Expanding image by 768MB

    Checking image's file system

    e2fsck 1.42.13 (17-May-2015)

    Pass 1: Checking inodes, blocks, and sizes

    Pass 2: Checking directory structure

    Pass 3: Checking directory connectivity

    Pass 4: Checking reference counts

    Pass 5: Checking group summary information

    container.img: 11/49152 files (0.0% non-contiguous), 7387/196608 blocks

    Resizing image's file system

    resize2fs 1.42.13 (17-May-2015)

    Resizing the filesystem on container.img to 393216 (4k) blocks.

    The filesystem on container.img is now 393216 (4k) blocks long.

    Image is done: container.img


    $ ls -lh container.img

    -rw-rw-r-- 1 vanessa vanessa 1.5G Oct  2 18:48 container.img


Similar to the create sub-command, you can override the default size
increase (which is 768MiB) by using the ``--size`` option.

.. _image-import:

image.import
============

.. _sec:imageimport:

Singularity import is essentially taking a dump of files and folders
and adding them to your image. This works for local compressed things
(e.g., tar.gz) but also for docker image layers that you don’t have on
your system. As of version 2.3, import of docker layers includes the
environment and metadata without needing sudo. It’s generally very
intuitive.

As an example, here is a common use case: wanting to import a Docker
image:

.. code-block:: none

    singularity image.import container.img docker://ubuntu:latest

.. _image-create:

image.create
============

.. _sec:imagecreate:

A Singularity image, which can be referred to as a “container,” is a
single file that contains a virtual file system. As of Singularity
2.4, we strongly recommend that you build (create and install) an
image using :ref:`build <build-a-container>`. If you have reason to create an empty image, or use
create for any other reason, the original ``create`` command is replaced with a
more specific ``image.create``. After creating an image you can install an operating
system, applications, and save meta-data with it.

Whereas Docker assembles images from layers that are stored on your
computer (viewed with the ``docker history`` command), a Singularity image is just one
file that can sit on your Desktop, in a folder on your cluster, or
anywhere. Having Singularity containers housed within a single image
file greatly simplifies management tasks such as sharing, copying, and
branching your containers. It also means that standard Linux file
system concepts like permissions, ownership, and ACLs apply to the
container (e.g. I can give read only access to a colleague, or block
access completely with a simple ``chmod`` command).

Creating a new blank Singularity container image
------------------------------------------------

    Singularity will create a default container image of 768MiB using the
    following command:

    .. code-block:: none

        singularity image.create container.img

        Creating empty 768MiB image file: container.img

        Formatting image with ext3 file system

        Image is done: container.img


    How big is it?

    .. code-block:: none

        $ du -sh container.img

        29M     container.img

    Create will make an ``ext3`` filesystem. Let’s create and import a docker base
    (the pre-2.4 way with two commands), and then compare to just building
    (one command) from the same base.

    .. code-block:: none

        singularity create container.img

        sudo singularity bootstrap container.img docker://ubuntu


        ...


        $ du -sh container.img

        769M

    Prior to 2.4, you would need to provide a ``--size`` to change from the default:

    .. code-block:: none

        $ singularity create --size 2048 container2.img

        Initializing Singularity image subsystem

        Opening image file: container2.img

        Creating 2048MiB image

        Binding image to loop

        Creating file system within image

        Image is done: container2.img


        $ ls -lh container*.img

        -rwxr-xr-x 1 user group 2.1G Apr 15 11:34 container2.img

        -rwxr-xr-x 1 user group 769M Apr 15 11:11 container.img


    Now let’s compare to if we just built, without needing to specify a
    size.

    .. code-block:: none

        sudo singularity build container.simg docker://ubuntu


        ...


        du -sh container.simg

        45M container.simg


Quite a difference! And one command instead of one.

Overwriting an image with a new one
'''''''''''''''''''''''''''''''''''

    For any commands that If you have already created an image and wish to
    overwrite it, you can do so with the ``--force`` option.

    .. code-block:: none

        $ singularity image.create container.img

        ERROR: Image file exists, not overwriting.



        $ singularity image.create --force container.img

        Creating empty 768MiB image file: container.img

        Formatting image with ext3 file system

        Image is done: container.img


    ``@GodLoveD`` has provided a nice interactive demonstration of creating an image (pre
    2.4).

.. _instance-command-group:

----------------------
Instance Command Group
----------------------

.. _sec:instances:


instance.start
==============

.. _sec:instancestart:

New in Singularity version 2.4 you can use the ``instance`` command group to run
instances of containers in the background. This is useful for running
services like databases and web servers. The ``instance.start`` command lets you initiate a
named instance in the background.

Overview
--------

To initiate a named instance of a container, you must call the ``instance.start`` command
with 2 arguments: the name of the container that you want to start and a
unique name for an instance of that container. Once the new instance is
running, you can join the container’s namespace using a URI style syntax
like so:

.. code-block:: none

    $ singularity shell instance://<instance_name>

You can specify options such as bind mounts, overlays, or custom
namespaces when you initiate a new instance of a container with
instance.start. These options will persist as long as the container
runs.

For a complete list of options see the output of:

.. code-block:: none

    singularity help instance.start

Examples
--------

These examples use a container from Singularity Hub, but you can use
local containers or containers from Docker Hub as well. For a more
detailed look at ``instance`` usage see :ref:`Running Instances <running-services>`.

Start an instance called cow1 from a container on Singularity Hub
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity instance.start shub://GodloveD/lolcow cow1

Start an interactive shell within the instance that you just started
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity shell instance://cow1

    Singularity GodloveD-lolcow-master.img:~> ps -ef

    UID        PID  PPID  C STIME TTY          TIME CMD

    ubuntu       1     0  0 20:03 ?        00:00:00 singularity-instance: ubuntu [cow1]

    ubuntu       3     0  0 20:04 pts/0    00:00:00 /bin/bash --norc

    ubuntu       4     3  0 20:04 pts/0    00:00:00 ps -ef

    Singularity GodloveD-lolcow-master.img:~> exit


Execute the runscript within the instance
'''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity run instance://cow1

     _________________________________________

    / Clothes make the man. Naked people have \

    | little or no influence on society.      |

    |                                         |

    \ -- Mark Twain                           /

     -----------------------------------------

            \   ^__^

             \  (oo)\_______

                (__)\       )\/\

                    ||----w |

                    ||     ||


Run a command within a running instance
'''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity exec instance://cow1 cowsay "I like blending into the background"

     _____________________________________

    < I like blending into the background >

     -------------------------------------

            \   ^__^

             \  (oo)\_______

                (__)\       )\/\

                    ||----w |

                    ||     ||



instance.list
=============

.. _sec:instancelist:

New in Singularity version 2.4 you can use the ``instance`` command group to run
instances of containers in the background. This is useful for running
services like databases and web servers. The ``instance.list`` command lets you keep track
of the named instances running in the background.

Overview
--------

After initiating one or more named instances to run in the background
with the ``instance.start`` command you can list them with the ``instance.list`` command.

Examples
--------

These examples use a container from Singularity Hub, but you can use
local containers or containers from Docker Hub as well. For a more
detailed look at ``instance`` usage see :ref:`Running Instances <running-services>`.

Start a few named instances from containers on Singularity Hub
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity instance.start shub://GodloveD/lolcow cow1

    $ singularity instance.start shub://GodloveD/lolcow cow2

    $ singularity instance.start shub://vsoch/hello-world hiya


List running instances
''''''''''''''''''''''

.. code-block:: none

    $ singularity instance.list

    DAEMON NAME      PID      CONTAINER IMAGE

    cow1             20522    /home/ubuntu/GodloveD-lolcow-master.img

    cow2             20558    /home/ubuntu/GodloveD-lolcow-master.img

    hiya             20595    /home/ubuntu/vsoch-hello-world-master.img



instance.stop
=============

.. _sec:instancestop:

New in Singularity version 2.4 you can use the ``instance`` command group to run
instances of containers in the background. This is useful for running
services like databases and web servers. The ``instance.stop`` command lets you stop
instances once you are finished using them

Overview
--------

After initiating one or more named instances to run in the background
with the ``instance.start`` command you can stop them with the ``instance.stop`` command.

Examples
--------

These examples use a container from Singularity Hub, but you can use
local containers or containers from Docker Hub as well. For a more
detailed look at ``instance`` usage see :ref:`Running Instances <running-services>`.

Start a few named instances from containers on Singularity Hub
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: none

    $ singularity instance.start shub://GodloveD/lolcow cow1

    $ singularity instance.start shub://GodloveD/lolcow cow2

    $ singularity instance.start shub://vsoch/hello-world hiya


Stop a single instance
''''''''''''''''''''''

.. code-block:: none

    $ singularity instance.stop cow1

    Stopping cow1 instance of /home/ubuntu/GodloveD-lolcow-master.img (PID=20522)


Stop all running instances
''''''''''''''''''''''''''

.. code-block:: none

    $ singularity instance.stop --all

    Stopping cow2 instance of /home/ubuntu/GodloveD-lolcow-master.img (PID=20558)

    Stopping hiya instance of /home/ubuntu/vsoch-hello-world-master.img (PID=20595)


----------
Deprecated
----------

.. note.. code-block:: none
    The bootstrap command is deprecated for Singularity Version
    2.4. You should use :ref:`build <build-command>` instead.

.. _bootstrap:

bootstrap
=========

.. _sec:bootstrap:

Bootstrapping was the original way (for Singularity versions prior to
2.4) to install an operating system and then configure it appropriately
for a specified need. Bootstrap is very similar to build, except that it
by default uses an `ext3 <https://en.wikipedia.org/wiki/Ext3>`_ filesystem and allows for writability. The
images unfortunately are not immutable in this way, and can degrade over
time. As of 2.4, bootstrap is still supported for Singularity, however
we encourage you to use :ref:`build <build-a-container>` instead.

Quick Start
-----------

A bootstrap is done based on a Singularity recipe file (a text file
called Singularity) that describes how to specifically build the
container. Here we will overview the sections, best practices, and a
quick example.

.. code-block:: none

    $ singularity bootstrap

    USAGE: singularity [...] bootstrap <container path> <definition file>

The ``<container path>`` is the path to the Singularity image file, and the ``<definition file>`` is the location
of the definition file (the recipe) we will use to create this
container. The process of building a container should always be done
by root so that the correct file ownership and permissions are
maintained. Also, so installation programs check to ensure they are
the root user before proceeding. The bootstrap process may take
anywhere from one minute to one hour depending on what needs to be
done and how fast your network connection is.

Let’s continue with our quick start example. Here is your spec file, ``Singularity`` ,

.. code-block:: none

    Bootstrap:docker

    From:ubuntu:latest


You next create an image:

.. code-block:: none

    $ singularity image.create ubuntu.img

    Initializing Singularity image subsystem

    Opening image file: ubuntu.img

    Creating 768MiB image

    Binding image to loop

    Creating file system within image

    Image is done: ubuntu.img


and finally run the bootstrap command, pointing to your image ( ``<container path>`` ) and
the file Singularity ( ``<definition file>`` ).

.. code-block:: none

    $ sudo singularity bootstrap ubuntu.img Singularity

    Sanitizing environment

    Building from bootstrap definition recipe

    Adding base Singularity environment to container

    Docker image path: index.docker.io/library/ubuntu:latest

    Cache folder set to /root/.singularity/docker

    [5/5] |===================================| 100.0%

    Exploding layer: sha256:b6f892c0043b37bd1834a4a1b7d68fe6421c6acbc7e7e63a4527e1d379f92c1b.tar.gz

    Exploding layer: sha256:55010f332b047687e081a9639fac04918552c144bc2da4edb3422ce8efcc1fb1.tar.gz

    Exploding layer: sha256:2955fb827c947b782af190a759805d229cfebc75978dba2d01b4a59e6a333845.tar.gz

    Exploding layer: sha256:3deef3fcbd3072b45771bd0d192d4e5ff2b7310b99ea92bce062e01097953505.tar.gz

    Exploding layer: sha256:cf9722e506aada1109f5c00a9ba542a81c9e109606c01c81f5991b1f93de7b66.tar.gz

    Exploding layer: sha256:fe44851d529f465f9aa107b32351c8a0a722fc0619a2a7c22b058084fac068a4.tar.gz

    Finalizing Singularity container


Notice that bootstrap does require sudo. If you do an import, with a
docker uri for example, you would see a similar flow, but the calling
user would be you, and the cache your ``$HOME``.

.. code-block:: none

    $ singularity image.create ubuntu.img

    singularity import ubuntu.img docker://ubuntu:latest

    Docker image path: index.docker.io/library/ubuntu:latest

    Cache folder set to /home/vanessa/.singularity/docker

    Importing: base Singularity environment

    Importing: /home/vanessa/.singularity/docker/sha256:b6f892c0043b37bd1834a4a1b7d68fe6421c6acbc7e7e63a4527e1d379f92c1b.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:55010f332b047687e081a9639fac04918552c144bc2da4edb3422ce8efcc1fb1.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:2955fb827c947b782af190a759805d229cfebc75978dba2d01b4a59e6a333845.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:3deef3fcbd3072b45771bd0d192d4e5ff2b7310b99ea92bce062e01097953505.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:cf9722e506aada1109f5c00a9ba542a81c9e109606c01c81f5991b1f93de7b66.tar.gz

    Importing: /home/vanessa/.singularity/metadata/sha256:fe44851d529f465f9aa107b32351c8a0a722fc0619a2a7c22b058084fac068a4.tar.gz


For details and best practices for creating your Singularity recipe, :ref:`read about them here <container-recipes>`.
