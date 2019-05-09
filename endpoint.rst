================
Remote Endpoints
================

Singularity introduced the `Cloud Services <https://cloud.sylabs.io/home>`_ for
enabling its users to `Create <https://cloud.sylabs.io/builder>`_,
`Secure <https://cloud.sylabs.io/keystore?sign=true>`_, and
`Share <https://cloud.sylabs.io/library/guide#create>`_ their container images
with others.With the latest development of the ``remote`` command, you can now
configure Singularity to point to a specific instance of the Cloud services,
enabling access to a private Container Library, Remote Builder and Key Store.
The remote command group manages these endpoints. The configurations are usually
stored in ``singularity/etc/remote.yaml`` file.

--------
Overview
--------

The remote endpoints can be configured per-user or globally for all users.
Multiple endpoints can be defined allowing the greatest flexibility.
This page will describe the <subcommands> under  ``Remote`` command group.

Once a remote point is ``added``, and logged in, the following commands can be
used with the selected remote endpoint.

- ``pull``

- ``push``

- ``build -remote`` - To build SIF via Remote Builder

- ``key`` - To manage OpenPGP keys (Needs Verification)

- ``search`` - Allows you to search for images within a container library of your choice

.. note::
    ``docker://`` and ``shub://`` prefixes are unaffected by these commands

-----
Usage
-----

To ``list`` existing remote endpoints, run this:

.. code-block:: none

    $ singularity remote list

To ``add`` an endpoint (local to current user):

.. code-block:: none

    $ singularity remote add <remote_name> <remote_uri>

To ``add`` an global endpoint (available to all users on the system):

.. code-block:: none

    $ sudo singularity remote add -g <remote_name> <remote_uri>

Conversely, to ``remove`` an endpoint:

.. code-block:: none

    $ sudo singularity remote remove <remote_name>

Setting a default endpoint:

.. code-block:: none

    $ singularity remote use <remote_name>

Before using an endpoint, you'll need to ``login`` to it.  This will require
an access token to be obtained from your `cloud <http://cloud.sylabs.io/auth>`_
account.

.. code-block:: none

    $ singularity remote login <remote_name>

To check ``status`` of an endpoint and the various services:

.. code-block:: none

    $ singularity remote status name
