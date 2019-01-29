.. _cloud_library:

Cloud Library
=============

This page will cover how to use our cloud services with Singularity.

--------
Overview
--------

The Cloud Library is the place to push (upload) your containers to the cloud so other users can
download, :ref:`Verify <signNverify>` (optional), and use the containers.

We also provide a :ref:`Remote Builder <remote_builder>`, this is used for building your containers remotely,
this offers advantages:

 - Usually fast.

 - No root access needed.

 - Can build directly to the library without the need to :ref:`push <push>` your container after. (only through the web GUI)

content...

.. _make_a_account:

---------------
Make an Account
---------------

Making an account is easy, and straightforward:

 1. Go to: https://cloud.sylabs.io/library.
 2. Click "Sign in to Sylabs" (top right corner).
 3. Select you method to sign in, with Google, GitHub, GitLab, or Microsoft.
 4. Type your passwords, and that's it!

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

-------------------
Pushing a Container
-------------------

The ``singularity push`` will push a container to the container library with the given URL. Here's an example of a typical push command:

.. code-block:: console

    $ singularity push my-container.sif library://your-name/project-dir/my-container:latest

The ``:latest`` is the container tag. Tags are used to have different version of the same container. Here's an example:

Let's assume you have your container (v1.0.1), and you want to push that container without deleting your ``:latest`` container, then you can add a version tag to that container, like so:

.. code-block:: console

    $ singularity push my-container.sif library://your-name/project-dir/my-container:1.0.1

You can download the container with that tag by replacing the ``:latest``, with the tagged container you want to download.

.. _pull:

-------------------
Pulling a container
-------------------

The ``singularity pull`` will pull a container from the `Library <https://cloud.sylabs.io/library>`_ (``library://``), and also `Docker Hub <https://hub.docker.com/>`_ (``docker://``).

.. note::

    When pulling from Docker, the container will automatically be converted to a SIF (Singularity Image Format) container.

Here's a typical pull command:

.. code-block:: console

    $ singularity pull file-out.sif library://alpine:latest

.. note::

    If there's no tag after the container name, Singularity automatically will pull the container with the ``:latest`` tag.

Pulling your own container
--------------------------

The ``singularity pull`` can pull a container from the `Library <https://cloud.sylabs.io/library>`_ (``library://``),
and also `Docker Hub <https://hub.docker.com/>`_ (``docker://``).

.. note::

    When pulling from Docker, the container will automatically be converted to a SIF (Singularity Image Format) container.

Here's a typical pull command:

.. code-block:: console

    $ singularity pull file-out.sif library://alpine:latest

If there's no tag after the container name, Singularity will pull the container with the latest tag.

To pull a container with a specific tag, just add the tag to the library URL:

.. code-block:: console

    $ singularity pull file-out.sif library://alpine:3.8

Of course, you can pull your own containers. Here's what that will look like:

.. code-block:: console

    $ singularity pull library://your-name/project-dir/my-container:latest

    # or use a different tag:

    $ singularity pull library://your-name/project-dir/my-container:1.0.1

.. note::

    You don't have to specify a output file, one will be created automatically, but it's good practice to always
    specify your output file.

...more content...

--------------------------
Verify/Sign your Container
--------------------------

Verify containers that you pull from the library, ensuring they are bit-for-bit reproductions of the original image.

Check out :ref:`this page <signNverify>` on how to: :ref:`verify a container <verify_container_from_library>`,
:ref:`making PGP key, and sign your own containers <sign_your_own_containers>`.

.. _search_the_library:

------------------------------------
Searching the Library for Containers
------------------------------------

When it comes to searching the library, you could always go to: https://cloud.sylabs.io/library and search from there.
Or you can use ``singularity search <container/user>``, this will search the library for the ``<container/user>``.

Using the CLI Search
--------------------

Here is an example for searching the library for ``centos``:

.. code-block:: console

    $ singularity search centos
    No users found for 'centos'
    
    No collections found for 'centos'
    
    Found 6 containers for 'centos'
    	library://dtrudg/linux/centos
    		Tags: 6 7 centos6 centos7 latest
    	library://library/default/centos
    		Tags: 6 7 latest
    	library://gmk/demo/centos-vim
    		Tags: latest
    	library://mroche/baseline/centos
    		Tags: 7 7.5 7.5.1804 7.6 7.6.1810 latest
    	library://gmk/default/centos7-devel
    		Tags: latest
    	library://emmeff/default/centos7-python36
    		Tags: 1.0

Notice there are different tags for the same container.

.. _remote_builder:

--------------
Remote Builder
--------------

The remote builder service can build your container remotly, (you dont need root access
to use remote builder)

Building from a defition file:
------------------------------

This is are defition file, lets call it ``ubuntu.def``:

.. code-block:: singularity

    bootstrap: library
    from: ubuntu:18.04

    %runscript
    echo "hello world from ubuntu container!"

Now, to build the container, use the ``--remote`` flag, and without ``sudo``:

.. code-block:: console

    $ singularity build --remote ubuntu.sif ubuntu.def

.. note:

    Make sure you have a access token, otherwise the build will fail.

Then, you should wave your container; ``ubuntu.sif``, and you can test it by running it:

.. code-block:: console

    $ ./ubuntu.sif
    hello world from ubuntu container!

