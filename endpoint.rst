================
Remote Endpoints
================

Remote endpoints allow Singularity to use a separate container library, remote build server and keystore service other than the Sylabs Cloud.  

--------
Overview
--------

Each of the services that comprise Sylabs Cloud can be installed locally, allowing a private repository of images, local remote builder and a keystore service. Remote endpoints can be configured per-user or globally for all users.  Multiple endpoints can be defined allowing the greatest flexibility.  

The following commands will be directed to the select remote endpoint.  
- ``pull``
- ``push``
- ``build -remote``
- ``key`` NEED VERIFICATION
- ``search`` 

* docker:// and shub:// prefixes are unaffected by these commands

-----
Usage
-----

To ``list`` existing remote endpoints, run this:

.. code-block:: none

    $ singularity remote list

To ``add`` an endpoint (local to current user):

.. code-block:: none

    $ singularity remote add <i>name</i> <i>uri</i>

To ``add`` an global endpoint (available to all users on the system):

.. code-block:: none

    $ sudo singularity remote add -g <i>name</i> <i>uri</i>

Conversely, to ``remove`` an endpoint:

.. code-block:: none

    $ sudo singularity remote remove <i>name</i>

Setting a default endpoint:

.. code-block:: none

    $ singularity remote use <i>name</i>

Before using an endpoint, you'll need to ``login`` to it.  This will require an access token obtained from your keystore.  See `http://cloud.sylabs.io/auth` for an example.

.. code-block:: none

    $ singularity remote login <i>name</i>

To check ``status`` of an endpoint and the various services:

.. code-block:: none

    $ singularity remote status <i>name</i>

