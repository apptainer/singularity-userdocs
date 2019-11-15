.. _cloud_library:

Cloud Library
=============

This page will cover how to use the Singularity Cloud Services (SCS) with Singularity.

--------
Overview
--------

The Cloud Library is the place to :ref:`push <push>` your containers to the cloud so other users can
download, :ref:`verify <signNverify>`, and use the containers.

Sylabs also provides a :ref:`Remote Builder <remote_builder>`, used to build your containers 
containers without root access within the cloud.

.. _make_a_account:

---------------
Make an Account
---------------

Making an account is easy, and straightforward:

 1. Go to: https://cloud.sylabs.io/library.
 2. Click "Sign in to Sylabs" (top right corner).
 3. Select your method to sign in, with Google, GitHub, GitLab, or Microsoft.
 4. Type your passwords, and that's it!

.. _creating_a_access_token:

-----------------------
Creating a Access token
-----------------------

Access tokens for pushing a container, and remote builder.

To generate a access token, do the following steps:

 1. Go to: https://cloud.sylabs.io/library.
 2. Click the top right button with your username.
 3. From the dropdown menu, click "Access Tokens".
 4. Enter a token name, like ``my token for linux ws``, then click "Create a new token".
 5. Copy the token to the clipboard.
 6. Run ``singularity remote login`` and past the token at the prompt.

Now that you have your token, you are ready to push your container!

.. _push:

-------------------
Pushing a Container
-------------------

The ``singularity push`` command will push a container to the container library with the given URL. Here's an example
of a typical push command:

.. code-block:: none

    $ singularity push my-container.sif library://your-name/project-dir/my-container:latest

The ``:latest`` is the container tag. Tags are used to have different version of the same container.

.. note::
    When pushing your container, theres no need to add a ``.sif`` (Singularity Image Format) to the end of the container name, (like
    on your local machine), because all containers on the library are SIF containers.

Let's assume you have your container (v1.0.1), and you want to push that container without deleting
your ``:latest`` container, then you can add a version tag to that container, like so:

.. code-block:: none

    $ singularity push my-container.sif library://your-name/project-dir/my-container:1.0.1

You can download the container with that tag by replacing the ``:latest``, with the tagged container you want to download.

.. _pull:

-------------------
Pulling a container
-------------------

The ``singularity pull`` command will download a container from the `Library <https://cloud.sylabs.io/library>`_
(``library://``), `Docker Hub <https://hub.docker.com/>`_ (``docker://``), and also
`Shub <https://singularity-hub.org/collections>`_ (``shub://``).

.. note::
    When pulling from Docker, the container will automatically be converted to a SIF (Singularity Image Format) container.

Here's a typical pull command:

.. code-block:: none

    $ singularity pull file-out.sif library://alpine:latest

    # or pull from docker:

    $ singularity pull file-out.sif docker://alpine:latest

.. note::
    If there's no tag after the container name, Singularity automatically will pull the container with the ``:latest`` tag.

To pull a container with a specific tag, just add the tag to the library URL:

.. code-block:: none

    $ singularity pull file-out.sif library://alpine:3.8

Of course, you can pull your own containers. Here's what that will look like:

Pulling your own container
--------------------------

Pulling your own container is just like pulling from Github, Docker, etc...

.. code-block:: none

    $ singularity pull out-file.sif library://your-name/project-dir/my-container:latest

    # or use a different tag:

    $ singularity pull out-file.sif library://your-name/project-dir/my-container:1.0.1

.. note::
    You *don't* have to specify a output file, one will be created automatically, but it's good practice to always
    specify your output file.

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

When it comes to searching the library, you could always go to: https://cloud.sylabs.io/library and search from there
through the web GUI. Or you can use ``singularity search <container/user>``, this will search the library for
the ``<container/user>``.

Using the CLI Search
--------------------

Here is an example for searching the library for ``centos``:

.. code-block:: none

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

The remote builder service can build your container in the cloud removing the requirement for root access.

Here's a typical remote build command:

.. code-block:: none

    $ singularity build --remote file-out.sif docker://ubuntu:18.04


Building from a definition file:
--------------------------------

This is our definition file. Let's call it ``ubuntu.def``:

.. code-block:: singularity

    bootstrap: library
    from: ubuntu:18.04

    %runscript
        echo "hello world from ubuntu container!"

Now, to build the container, use the ``--remote`` flag, and without ``sudo``:

.. code-block:: none

    $ singularity build --remote ubuntu.sif ubuntu.def

.. note::
    Make sure you have a :ref:`access token <creating_a_access_token>`, otherwise the build will fail.

After building, you can test your container like so:

.. code-block:: none

    $ ./ubuntu.sif
    hello world from ubuntu container!

You can also use the web GUI to build containers remotely. First, go to https://cloud.sylabs.io/builder (make sure you are signed in).
Then you can copy and paste, upload, or type your definition file. When you are finished, click build. Then you can download the container
with the URL.

