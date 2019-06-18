================
Remote Endpoints
================

Sylabs introduced the `Singularity Container Services
<https://cloud.sylabs.io/home>`_ for enabling users to `Create
<https://cloud.sylabs.io/builder>`_,
`Secure <https://cloud.sylabs.io/keystore?sign=true>`_, and
`Share <https://cloud.sylabs.io/library/guide#create>`_ their container images
with others. With the development of the ``remote`` command, you can now
configure Singularity to point to a specific instance of the container services,
enabling access to a private Container Library, Remote Builder and Key Store.
The ``remote`` command group manages these endpoints. The configurations are
usually stored in ``~/.singularity/remote.yaml`` file.

--------
Overview
--------

The remote endpoints can be configured per-user or globally for all users.
Multiple endpoints can be defined allowing the greatest flexibility.
This page will describe the subcommands under the ``remote`` command group.

Once a remote point is ``added``, and logged in, commands like the following can
be used with the selected remote endpoint:

`pull <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_pull.html>`_,
`push <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_push.html>`_,
`build --remote <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_build.html#options>`_,
`key <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_key.html>`_,
`search <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_search.html>`_,
`verify <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_verify.html>`_,
`exec <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_exec.html>`_,
`shell <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_shell.html>`_,
`run <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_run.html>`_,
`instance <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_instance.html>`_

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

To ``add`` a global endpoint (available to all users on the system):

.. code-block:: none

    $ sudo singularity remote add --global <remote_name> <remote_uri>

.. note::
     Global remote configurations can only be modified by the root user and can
     be viewed in ``~/.singularity/remote.yaml`` file.

Conversely, to ``remove`` an endpoint:

.. code-block:: none

    $ sudo singularity remote remove <remote_name>

Setting a default endpoint:

.. code-block:: none

    $ singularity remote use <remote_name>

Before using an endpoint, you'll need to ``login`` to it. This will require
an access token to be obtained from your `cloud <http://cloud.sylabs.io/auth>`_
account.

.. code-block:: none

    $ singularity remote login <remote_name>

Instructions for creating and saving a token will then be displayed.

To check ``status`` of an endpoint and the various services:

.. code-block:: none

    $ singularity remote status <remote_name>


Once logged in to a remote endpoint, you can push & pull images to your
designated endpoint using the ``library://`` uri.

.. note::
    Since, the remote endpoints are linked with the user, make sure to use all
    the commands either with or without **sudo** privilege. If you ``add`` an
    endpoint using **sudo**, you must ``list`` it using **sudo** as well.
