.. _encryption:

====================
Encrypted Containers
====================

Users can build a secure container environment by encrypting the root file
system.

--------
Overview
--------

In Singularity >= v3.4.0 a new feature to build and run encrypted containers has
been added to allow users to encrypt the file system image within a SIF.  This 
encryption can be performed using either a passphrase or asymmetrically via a 
Privacy Enhanced Mail (PEM) file and a matching private RSA key.  The container 
is encrypted in transit, at rest, and even while running.  In other words, there 
is no intermediate, decrypted version of the container on disk or in memory.  
Container decryption occurs at runtime completely within kernel space.  

.. note:: 
        This feature utilizes the Linux ``dm-crypt`` library and ``cryptsetup`` 
        utility and requires cryptsetup version of >= 2.0.0.  This version 
        should be standard with recent Linux versions such as Ubuntu 18 and 
        Centos/RHEL 7, but users of older Linux versions may have to update. 

----------------------
Encrypting a container
----------------------

A container can be encrypted either by supplying a plaintext passphrase or a 
PEM file containing an asymmetric RSA public key.  Of these two methods the PEM
file is more secure and is therefore recommended for production use. 

A passphrase or a key-file is supplied at build time via an environment variable 
or a command line option. 

+------------------------+-------------------------------------------+--------------------------+
| **Encryption Method**  | **Environment Variable**                  | **Commandline Option**   |
+------------------------+-------------------------------------------+--------------------------+
| Passphrase             | ``SINGULARITY_ENCRYPTION_PASSPHRASE``     | ``--passphrase``         |
+------------------------+-------------------------------------------+--------------------------+
| Asymmentric (PEM)      | ``SINGULARITY_ENCRYPTION_PEM_PATH``       | ``--pem-path``           | 
+------------------------+-------------------------------------------+--------------------------+

An ``-e|--encrypt`` build flag is used to indicate that the container needs to 
be encrypted.  This flag must be used to encrypt via the 
``SINGULARITY_ENCRYPTION_*`` environment variables.  The ``-e|--encrypt`` flag
is implicitly set when the ``--passphrase`` or ``--pem-path`` flags are passed
with the build command.  If multiple encryption related flags and/or environment 
variables are set, the following precedence is respected.  

#. ``--pem-path``
#. ``--passphrase``
#. ``SINGULARITY_ENCRYPTION_PEM_PATH``
#. ``SINGULARITY_ENCRYPTION_PASSPHRASE``

Passphrase Encryption
=====================

.. note::

        Passphrase encryption is less secure the encrypting containers using a 
        PEM file and private RSA key (detailed below).  Passphrase encryption is
        provided as a convenience, and as a way for users to familiarize 
        themselves with the encrypted container workflow, but users running 
        encrypted containers in production are encouraged to use a PEM key.   

In case of plaintext passphrase encryption, a passphrase is supplied by one of 
the following methods.

Encrypting with a passphrase interactively
------------------------------------------

.. code-block:: none

        $ sudo singularity build --passphrase encrypted.sif encrypted.def
        Enter encryption passphrase: <secret>
        INFO:    Starting build...

Using an environment variable
-----------------------------

.. code-block:: none

        $ sudo SINGULARITY_ENCRYPTION_PASSPHRASE=<secret> singularity build --encrypt encrypted.sif encrypted.def
        Starting build...

In this case it is necessary to use the ``--encrypted`` flag since the presence
of an environment variable alone will not trigger the encrypted build workflow.

While this example shows how an environment variable can be used to set a
passphrase, you should set the environment variable in a way that will not 
record your passphrase on the command line.  For instance, you could save a 
plain text passphrase in a file (e.g. ``secret.txt``) and use it like so.

.. code-block:: none

        $ export SINGULARITY_ENCRYPTION_PASSPHRASE=$(cat secret.txt)

        $ sudo -E singularity build --encrypt encrypted.sif encrypted.def
        Starting build...

PEM File Encryption
===================

Singularity currently supports RSA encryption using public/private key-pair. 
Keys are supplied in PEM format.  

You can create a pair of RSA keys suitable for encrypting your container with 
the ``ssh-keygen`` command, and then create a PEM file with a few specific flags 
like so:

.. code-block:: none

        $ ssh-keygen
        Generating public/private rsa key pair.
        Enter file in which to save the key (/home/vagrant/.ssh/id_rsa): rsa
        Enter passphrase (empty for no passphrase):
        Enter same passphrase again:
        [snip...]

        $ ssh-keygen -f ./rsa.pub -e -m pem >rsa.pem

        $ ls
        rsa  rsa.pem  rsa.pub

You would use the ``rsa.pem`` file to encrypt your container and the ``rsa`` 
file to run it.  

Using a command line option
---------------------------

.. code-block:: none

        $ sudo singularity build --pem-path=rsa.pem encrypted.sif encrypted.def
        Starting build...

Using an environment variable
-----------------------------

.. code-block:: none

        $ sudo SINGULARITY_ENCRYPTION_PEM_PATH=rsa.pem singularity build --encrypt encrypted.sif encrypted.def
        Starting build...

In this case it is necessary to use the ``--encrypted`` flag since the presence
of an environment variable alone will not trigger the encrypted build workflow.

------------------------------
Running an encrypted container
------------------------------

To ``run``, ``shell``, or ``exec`` an encrypted image, the same credentials used 
to encrypt the image need to be supplied at runtime, either in a key-file 
supplying the private key or a plaintext passphrase.

Running a container encrypted with a passphrase
===============================================

A passphrase can be supplied at runtime by either of the ways listed in the 
sections above.

Running with a passphrase interactively
---------------------------------------

.. code-block:: none

        $ singularity run --passphrase encrypted.sif
        Enter passphrase for encrypted container: <secret>

Using an environment variable
-----------------------------

.. code-block:: none

        $ SINGULARITY_ENCRYPTION_PASSPHRASE="secret" singularity run encrypted.sif

While this example shows how an environment variable can be used to set a
passphrase, you should set the environment variable in a way that will not 
record your passphrase on the command line.  For instance, you could save a 
plain text passphrase in a file (e.g. ``secret.txt``) and use it like so.

.. code-block:: none

        $ export SINGULARITY_ENCRYPTION_PASSPHRASE=$(cat secret.txt)

        $ singularity run encrypted.sif

Running a container encrypted with a PEM file
=============================================

A private key is supplied using either of the methods listed in the Encryption 
section above.

Using a command line option
---------------------------

.. code-block:: none

        $ singularity run --pem-path=rsa encrypted.sif

Using an environment variable
-----------------------------

.. code-block:: none

        $ SINGULARITY_ENCRYPTION_PEM_PATH=rsa singularity run encrypted.sif