============
Installation
============

.. _sec:installation:

This document will guide you through the process of installing
Singularity from source with the version and location of your choice.

----------------
Before you begin
----------------

If you have an earlier version of Singularity installed, you should
remove it before executing the installation commands.

These instructions will build Singularity from source on your system.
So you will need to have some development tools installed. If you run
into missing dependencies, try installing them like so:

.. code-block:: none

    $ sudo apt-get update && \

        sudo apt-get install \

        python \

        dh-autoreconf \

        build-essential \

        libarchive-dev


.. code-block:: none

    $ sudo yum update && \

        sudo yum groupinstall 'Development Tools' && \

        sudo yum install libarchive-devel


-------------------------
Install the master branch
-------------------------

The following commands will install the latest version of the `GitHub
repo <https://github.com/singularityware/singularity>`_ master branch to ``/usr/local``.

.. code-block:: none

    $ git clone https://github.com/singularityware/singularity.git

    $ cd singularity

    $ ./autogen.sh

    $ ./configure --prefix=/usr/local --sysconfdir=/etc

    $ make

    $ sudo make install


.. note.. code-block:: none
    Note that the installation prefix is ``/usr/local`` but the configuration directory
    is ``/etc``. This ensures that the configuration file ``singularity.conf`` is placed in the
    standard location.

If you omit the ``--sysconfdir`` option , the configuration file will be installed in ``/usr/local/etc``.
If you omit the ``--prefix`` option, Singularity will be installed in the ``/usr/local`` directory
hierarchy by default. And if you specify a custom directory with the ``--prefix``
option, all of Singularity’s binaries and the configuration file will
be installed within that directory. This last option can be useful if
you want to install multiple versions of Singularity, install
Singularity on a shared system, or if you want to remove Singularity
easily after installing it.

--------------------------
Install a specific release
--------------------------

The following commands will install a specific release from `GitHub
releases <https://github.com/singularityware/singularity/releases>`_ page to ``/usr/local``.

.. code-block:: none

    $ VER=2.5.1

    $ wget https://github.com/singularityware/singularity/releases/download/$VER/singularity-$VER.tar.gz

    $ tar xvf singularity-$VER.tar.gz

    $ cd singularity-$VER

    $ ./configure --prefix=/usr/local --sysconfdir=/etc

    $ make

    $ sudo make install


------------------------------
Install the development branch
------------------------------

If you want to test a development branch the routine above should be
tweaked slightly:

.. code-block:: none

    $ git clone https://github.com/singularityware/singularity.git

    $ cd singularity

    $ git fetch

    $ git checkout development

    $ ./autogen.sh

    $ ./configure --prefix=/usr/local --sysconfdir=/etc

    $ make

    $ sudo make install


---------------------
Remove an old version
---------------------

Let’s say that we installed Singularity to ``/usr/local``. To remove it completely,
you need to hit all of the following:

.. code-block:: none

    $ sudo rm -rf /usr/local/libexec/singularity

    $ sudo rm -rf /usr/local/etc/singularity

    $ sudo rm -rf /usr/local/include/singularity

    $ sudo rm -rf /usr/local/lib/singularity

    $ sudo rm -rf /usr/local/var/lib/singularity/

    $ sudo rm /usr/local/bin/singularity

    $ sudo rm /usr/local/bin/run-singularity

    $ sudo rm /usr/local/etc/bash_completion.d/singularity

    $ sudo rm /usr/local/man/man1/singularity.1


If you modified the system configuration directory, remove the ``singularity.conf`` file
there as well.
If you installed Singularity in a custom directory, you need only
remove that directory to uninstall Singularity. For instance if you
installed singularity with the ``--prefix=/some/temp/dir`` option argument pair, you can remove
Singularity like so:

.. code-block:: none

    $ sudo rm -rf /some/temp/dir

What should you do next? You can check out the :ref:`quickstart <quick-start>` guide, or learn how to
interact with your container via the :ref:`shell <shell>` , :ref:`exec <exec>` , or :ref:`run <run>` commands. Or click **next**
below to continue reading.

------------------------------------------
Running Singularity with Vagrant (Windows)
------------------------------------------

Setup
=====

First, install the following software:

- install `Git for Windows <https://git-for-windows.github.io/>`_

- install `VirtualBox for Windows <https://www.virtualbox.org/wiki/Downloads>`_

- install `Vagrant for Windows <https://www.vagrantup.com/downloads.html>`_

- install `Vagrant Manager for Windows <http://vagrantmanager.com/downloads/>`_

Singularityware Vagrant Box
===========================

We are maintaining a set of Vagrant Boxes via `Vagrant Cloud <https://www.vagrantup.com/>`_, one of `Hashicorp <https://www.hashicorp.com/#open-source-tools>`_ many tools that likely you’ve used and haven’t known it. The current stable version of Singularity is available here:

- `singularityware/singularity-2.4 <https://app.vagrantup.com/singularityware/boxes/singularity-2.4/versions/2.4>`_

For other versions of Singularity see `our Vagrant Cloud repository <https://app.vagrantup.com/singularityware>`_

Run GitBash. The default home directory will be C:\Users\your_username

.. code-block:: none

    mkdir singularity-2.4
    cd singularity-2.4

Note that if you had installed a previous version of the vm (and are using the same folder), you must destroy it first. In our example we create a new folder. To destroy a previous vm:

.. code-block:: none

    vagrant destroy

Then issue the following commands to bring up the Virtual Machine:

.. code-block:: none

    vagrant init singularityware/singularity-2.4
    vagrant up
    vagrant ssh

You are then ready to go with Singularity 2.4!

.. code-block:: none

    vagrant@vagrant:~$ which singularity
    /usr/local/bin/singularity
    vagrant@vagrant:~$ singularity --version
    2.4-dist

    vagrant@vagrant:~$ sudo singularity build growl-llo-world.simg shub://vsoch/hello-world
    Cache folder set to /root/.singularity/shub
    Progress |===================================| 100.0%
    Building from local image: /root/.singularity/shub/vsoch-hello-world-master.simg
    Building Singularity image...
    Singularity container built: growl-llo-world.simg
    Cleaning up...
    vagrant@vagrant:~$ ./growl-llo-world.simg
    RaawwWWWWWRRRR!!

Note that when you do ``vagrant up`` you can also select the provider, if you use vagrant for multiple providers. For example:

.. code-block:: none

    vagrant up --provider virtualbox

although this isn’t entirely necessary if you only have it configured for virtualbox.


----------------
Install on Linux
----------------

You can try the following two options:

Option 1: Download latest stable release
========================================

You can always download the latest tarball release from `GitHub <https://github.com/singularityware/singularity/releases>`_

For example, here is how to download version ``2.5.2`` and install:

.. code-block:: none

    VERSION=2.5.2
    wget https://github.com/singularityware/singularity/releases/download/$VERSION/singularity-$VERSION.tar.gz
    tar xvf singularity-$VERSION.tar.gz
    cd singularity-$VERSION
    ./configure --prefix=/usr/local
    make
    sudo make install

Note that when you configure, ``squashfs-tools`` is **not** required, however it is required for full functionality. You will see this message after the configuration:

.. code-block:: none

    mksquashfs from squash-tools is required for full functionality

If you choose not to install ``squashfs-tools``, you will hit an error when you try a pull from Docker Hub, for example.

Option 2: Download the latest development code
==============================================

To download the most recent development code, you should use Git and do the following:

.. code-block:: none

    git clone https://github.com/singularityware/singularity.git
    cd singularity
    ./autogen.sh
    ./configure --prefix=/usr/local
    make
    sudo make install


.. note::
    The ‘make install’ is required to be run as root to get a properly installed Singularity implementation. If you do not run it as root, you will only be able to launch Singularity as root due to permission limitations.

Prefix in special characters
----------------------------

If you build Singularity with a non-standard ``--prefix`` argument, please be sure to review the `admin guide <https://www.sylabs.io/guides/2.5.2/admin-guide/>`_ for details regarding the ``--localstatedir`` variable. This is especially important in environments utilizing shared filesystems.

Updating
--------

To update your Singularity version, you might want to first delete the executables for the old version:

.. code-block:: none

    sudo rm -rf /usr/local/libexec/singularity

And then install using one of the methods above.

---------------------
Debian Ubuntu Package
---------------------

Singularity is available on Debian (and Ubuntu) systems starting with Debian stretch and the Ubuntu 16.10 yakkety releases.
The package is called ``singularity-container``. For recent releases of singularity and backports for older Debian and Ubuntu releases,
we recommend that you use the `NeuroDebian repository <http://neuro.debian.net/pkgs/singularity-container.html>`_.

Testing first with Docker
=========================

If you want a quick preview of the NeuroDebian mirror, you can do this most easily with the NeuroDebian Docker image (and if you don’t, skip to the next section). Obviously you should have `Docker installed <https://docs.docker.com/engine/installation/linux/ubuntu/>`_ before you do this.

First we run the ``neurodebian`` Docker image:

.. code-block:: none

    $ docker run -it --rm neurodebian

Then we update the cache (very quietly), and look at the ``singularity-container`` policy provided:

.. code-block:: none

    $ apt-get update -qqq
    $ apt-cache policy singularity-container
    singularity-container:
      Installed: (none)
      Candidate: 2.3-1~nd80+1
      Version table:
        2.3-1~nd80+1 0
          500 http://neuro.debian.net/debian/ jessie/main amd64 Packages


You can continue working in Docker, or go back to your host and install Singularity.

Adding the Mirror and installing
================================

You should first enable the NeuroDebian repository following instructions on the `NeuroDebian <http://neuro.debian.net/>`_ site. This means using the dropdown menus to find the correct mirror for your operating system and location. For example, after selecting Ubuntu 16.04 and selecting a mirror in CA, I am instructed to add these lists:

.. code-block:: none

    sudo wget -O- http://neuro.debian.net/lists/xenial.us-ca.full | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
    sudo apt-key adv --recv-keys --keyserver hkp://pool.sks-keyservers.net:80 0xA5D32F012649A5A9
