.. _cloud_library:

Cloud Library
=============

This page will cover how to use our cloud services with Singularity.

--------
Overview
--------

The Cloud Library is the place to push your containers to the cloud so other users can
download, :ref:`Verify <signNverify>` (optional), and use the containers.

We also pervide a :ref:`Remote Builder <remote_builder>`, this is used for building your containers remotly,
this offers advantags:

 - Usally fast.

 - No root access needed.

 - Can build directly to the library without the need to :ref:`push <push>` your container after.

content...

.. _make_a_account:

-------------
Make a Acount
-------------

Makeing a acount is easy, and straightforward:

 1. Go to: https://cloud.sylabs.io/library.
 2. Click ``Sign in to Sylabs`` (top right corner).
 3. Select you method to sign in, with Google, GitHub, GitLab, or MicroSoft.
 4. Type your passwords, and thats it!


.. _creating_a_access_token:

-----------------------
Creating a Access token
-----------------------

Access tokens are used to... more content...

To generate a access token, do the following steps:

 1. Go to: https://cloud.sylabs.io/library.
 2. Click the top right button with your username.
 3. From the dropdown menu, click "Access Tokens".
 4. From there, click "Manage my API tokens"
 5. Enter a token name, like ``my token for linux ws``, then click "Create a new token".
 6. Copy the token and paste it to ``~/.singularity/sylabs-token``.

Now that you have your token, you are ready to push your container!

.. _push:

Pushing a Container
-------------------

The ``singularity push`` will push a container to the container library with the givin URL.
Heres an example of a typical push command:

.. code-block:: bash

    $ singularity push my-container.sif library://your-name/project-dir/my-container:latest

The ``:latest`` is the contianer tag, this is used to have difrent version of that container.
Heres an example:

.. code-block:: bash

    $ singularity push my-container.sif library://your-name/project-dir/my-container:1.0.0

Now you can download (pull) that container from the ``singularity pull`` command.

.. _pull:

Pulling a container
-------------------


The ``singularity pull`` will pull a container from the library (``library://``), or docker hub (``docker://``).

...more content...

