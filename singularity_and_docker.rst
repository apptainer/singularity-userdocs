.. _singularity-and-docker:

======================
Singularity and Docker
======================

Singularity is good friends with Docker. The reason is because the
developers use and really like using Docker, and scientists have already
put much resources into creating Docker images. Thus, one of our early goals was to support Docker. What can you do?

-  You don’t need Docker installed

-  You can shell into a Singularity-ized Docker image

-  You can run a Docker image instantly as a Singularity image

-  You can pull a Docker image (without sudo)

-  You can build images with bases from assembled Docker layers that
   include environment, guts, and labels

---------------------------
TLDR (Too Long Didn’t Read)
---------------------------

You can shell, import, run, and exec.

.. code-block:: none

    singularity shell docker://ubuntu:latest

    singularity run docker://ubuntu:latest

    singularity exec docker://ubuntu:latest echo "Hello Dinosaur!"


    singularity pull docker://ubuntu:latest

    singularity build ubuntu.img docker://ubuntu:latest


----------------------------------------------
Import a Docker image into a Singularity Image
----------------------------------------------

The core of a Docker image is basically a compressed set of files, a set
of ``.tar.gz`` that (if you look in your `Docker image folder <http://stackoverflow.com/questions/19234831/where-are-docker-images-stored-on-the-host-machine>`_ on your host
machine, you will see. The Docker Registry, which you probably interact
with via `Docker Hub <https://hub.docker.com/>`_, serves these layers. These are the layers that
you see downloading when you interact with the docker daemon. We are
going to use these same layers for Singularity!

--------------------------------
Quick Start: The Docker Registry
--------------------------------

The Docker engine communicates with the Docker Hub via the `Docker
Remote API <https://docs.docker.com/engine/reference/api/docker_remote_api/>`_, and guess what, we can too! The easiest thing to do is
create an image, and then pipe a Docker image directly into it from
the Docker Registry. You don’t need Docker installed on your machine,
but you will need a working internet connection. Let’s create an
ubuntu operating system, from Docker. We will pull, then build:

.. code-block:: none

    singularity pull docker://ubuntu

    WARNING: pull for Docker Hub is not guaranteed to produce the

    WARNING: same image on repeated pull. Use Singularity Registry

    WARNING: (shub://) to pull exactly equivalent images.

    Docker image path: index.docker.io/library/ubuntu:latest

    Cache folder set to /home/vanessa/.singularity/docker

    [5/5] |===================================| 100.0%

    Importing: base Singularity environment

    Importing: /home/vanessa/.singularity/docker/sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e.tar.gz

    Importing: /home/vanessa/.singularity/docker/sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9.tar.gz

    Importing: /home/vanessa/.singularity/metadata/sha256:77cece4ce6ef220f66747bb02205a00d9ca5ad0c0a6eea1760d34c744ef7b231.tar.gz

    WARNING: Building container as an unprivileged user. If you run this container as root

    WARNING: it may be missing some functionality.

    Building Singularity image...

    Cleaning up...

    Singularity container built: ./ubuntu.img


The warnings mean well - it is to tell you that you are creating the
image on the fly from layers, and if one of those layers changes, you
won’t produce the same image next time.

-----------------------------------------
The Build Specification file, Singularity
-----------------------------------------

Just like Docker has the Dockerfile, Singularity has a file called
Singularity that (currently) applications like Singularity Hub know to
sniff for. For reproducibility of your containers, our strong
recommendation is that you build from these files. Any command that you
issue to change a container sandbox (building with ``--sandbox`` ) or to a build with ``--writable``
is by default not recorded, and your container loses its
reproducibility. So let’s talk about how to make these files! First,
let’s look at the absolute minimum requirement:

.. code-block:: none

    Bootstrap: docker

    From: ubuntu


We would save this content to a file called Singularity and then issue
the following commands to bootstrap the image from the file

.. code-block:: none

    sudo singularity build ubuntu.img Singularity

Do you want to specify a particular tag? or version? You can just add
that to the docker uri:

.. code-block:: none

    Bootstrap: docker

    From: ubuntu:latest


.. note::

    Note that the default is ``latest`` . If you want to customize the Registry or
    Namespace, just add those to the header:

.. code-block:: none

    Bootstrap: docker

    From: ubuntu

    Registry: pancakes.registry.index.io

    Namespace: blue/berry/cream


The power of build comes with the other stuff that you can do! This
means running specific install commands, specifying your containers
runscript (what it does when you execute it), adding files, labels, and
customizing the environment. Here is a full Singularity file:

.. code-block:: none

    Bootstrap: docker

    From: tensorflow/tensorflow:latest


    %runscript

        exec /usr/bin/python "$@"


    %post

        echo "Post install stuffs!"


    %files

    /home/vanessa/Desktop/analysis.py /tmp/analysis.py

    relative_path.py /tmp/analysis2.py


    %environment

    TOPSECRET=pancakes

    HELLO=WORLD

    export HELLO TOPSECRET


    %labels

    AUTHOR Vanessasaur


In the example above, I am overriding any Dockerfile ``ENTRYPOINT`` or ``CMD`` because I have
defined a ``%runscript`` . If I want the Dockerfile ``ENTRYPOINT`` to take preference, I would remove
the ``%runscript`` section. If I want to use ``CMD`` instead of ``ENTRYPOINT`` , I would again remove the
runscript, and add IncludeCmd to the header:

.. code-block:: none

    Bootstrap: docker

    From: tensorflow/tensorflow:latest

    IncludeCmd: yes


    %post


        echo "Post install stuffs!"


Did you know that you can commit this Singularity file to a GitHub repo
and it will automatically build for you when you push to `Singularity
Hub <https://singularity-hub.org/>`_?. This will ensure maximum reproducibility of your work.

----------------------------
How does the runscript work?
----------------------------

Docker has two commands in the ``Dockerfile`` that have something to do with
execution, ``CMD`` and ``ENTRYPOINT``. The differences are subtle, but the best description
I’ve found is the following:

    A ``CMD`` is to provide defaults for an executing container.

and

    An ``ENTRYPOINT`` helps you to configure a container that you can run as an
    executable.

Given the definition, the ``ENTRYPOINT`` is most appropriate for the Singularity ``%runscript`` , and
so using the default bootstrap (whether from a ``docker://`` endpoint or a ``Singularity`` spec file)
will set the ``ENTRYPOINT`` variable as the runscript. You can change this behavior by
specifying ``IncludeCmd: yes`` in the Spec file (see below). If you provide any sort of ``%runscript`` in
your Spec file, this overrides anything provided in Docker. In summary,
the order of operations is as follows:

#. If a ``%runscript`` is specified in the Singularity spec file, this takes prevalence
   over all

#. If no ``%runscript`` is specified, or if the ``import`` command is used as in the example
   above, the ``ENTRYPOINT`` is used as runscript.

#. If no ``%runscript`` is specified, but the user has a ``Singularity`` spec with ``IncludeCmd`` , then the Docker ``CMD`` is
   used.

#. If no ``%runscript`` is specified, and there is no ``CMD`` or ``ENTRYPOINT`` , the image’s default
   execution action is to run the bash shell.

---------------------------------
How do I specify my Docker image?
---------------------------------

In the example above, you probably saw that we referenced the docker
image first with the uri ``docker://`` and that is important to tell Singularity that
it will be pulling Docker layers. To ask for ubuntu, we asked for ``docker://ubuntu`` . This
uri that we give to Singularity is going to be very important to choose
the following Docker metadata items:

-  registry (e.g., “index.docker.io”)

-  namespace (e.g., “library”)

-  repository (e.g., “ubuntu”)

-  tag (e.g., “latest”) OR version (e.g., "@sha256:1234…)

When we put those things together, it looks like this:

.. code-block:: none

    docker://<registry>/<namespace>/<repo_name>:<repo_tag>

By default, the minimum requirement is that you specify a repository
name (eg, ubuntu) and it will default to the following:

.. code-block:: none

    docker://index.docker.io/library/ubuntu:latest

If you provide a version instead of a tag, that will be used instead:

.. code-block:: none

    docker://index.docker.io/library/ubuntu@sha256:1235...

You can have one or the other, both are considered a “digest” in
Docker speak.

If you want to change any of those fields and are having trouble with
the uri, you can also just state them explicitly:

.. code-block:: none

    Bootstrap: docker

    From: ubuntu

    Registry: index.docker.io

    Namespace: library


---------------------
Custom Authentication
---------------------

For both import and build using a build spec file, by default we use
the Docker Registry ``index.docker.io`` . Singularity first tries the call without a
token, and then asks for one with pull permissions if the request is
defined. However, it may be the case that you want to provide a custom
token for a private registry. You have two options. You can either
provide a ``Username`` and ``Password`` in the build specification file (if stored locally and
there is no need to share), or (in the case of doing an import or
needing to secure the credentials) you can export these variables to
environmental variables. We provide instructions for each of these
cases:

Authentication in the Singularity Build File
============================================

You can simply specify your additional authentication parameters in the
header with the labels ``Username`` and ``Password`` :

.. code-block:: none

    Username: vanessa

    Password: [password]


Again, this can be in addition to specification of a custom registry
with the ``Registry`` parameter.

Authentication in the Environment
=================================

You can export your username, and password for Singularity as follows:

.. code-block:: none

    export SINGULARITY_DOCKER_USERNAME=vanessasaur

    export SINGULARITY_DOCKER_PASSWORD=rawwwwwr

Testing Authentication
======================

If you are having trouble, you can test your token by obtaining it on
the command line and putting it into an environmental variable, ``CREDENTIAL`` :

.. code-block:: none

    CREDENTIAL=$(echo -n vanessa:[password] | base64)

    TOKEN=$(http 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:vanessa/code-samples:pull' Authorization:"Basic $CREDENTIAL" | jq -r '.token')

This should place the token in the environmental variable ``TOKEN`` . To test that
your token is valid, you can do the following

.. code-block:: none

    http https://index.docker.io/v2/vanessa/code-samples/tags/list Authorization:"Bearer $TOKEN"

The above call should return the tags list as expected. And of course
you should change the repo name to be one that actually exists that you
have credentials for.

--------------
Best Practices
--------------

While most docker images can import and run without a hitch, there are
some special cases for which things can go wrong. Here is a general list
of suggested practices, and if you discover a new one in your building
ventures please `let us know <https://www.github.com/singularityware/singularityware.github.io/issues>`_.

1. Installation to Root
=======================

When using Docker, you typically run as root, meaning that root’s home
at ``/root`` is where things will install given a specification of home. This is
fine when you stay in Docker, or if the content at ``/root`` doesn’t need any
kind of write access, but generally can lead to a lot of bugs because
it is, after all, root’s home. This leads us to best practice #1.

Don’t install anything to root’s home, ``/root``.

2. Library Configurations
=========================

The command `ldconfig <https://codeyarns.com/2014/01/14/how-to-add-library-directory-to-ldconfig-cache/>`_ is used to update the shared library cache. If
you have software that requires symbolic linking of libraries and you
do the installation without updating the cache, then the Singularity
image (in read only) will likely give you an error that the library is
not found. If you look in the image, the library will exist but the
symbolic link will not. This leads us to best practice #2:

Update the library cache at the end of your Dockerfile with a call
to ldconfig.

3. Don't install to $HOME or $TMP
=================================

We can assume that the most common Singularity use case has the $USER
home being automatically mounted to ``$HOME``, and ``$TMP`` also mounted. Thus, given
the potential for some kind of conflict or missing files, for best
practice #3 we suggest the following:

Don’t put container valuables in ``$TMP`` or ``$HOME``

Have any more best practices? Please `let us know <https://www.github.com/singularityware/singularityware.github.io/issues>`_!

---------------
Troubleshooting
---------------

Why won’t my image build work? If you can’t find an answer on this site,
please `ping us an issue <https://www.github.com/singularityware/singularity/issues>`_. If you’ve found an answer and you’d like to
see it on the site for others to benefit from, then post to us
`here <https://www.github.com/singularityware/singularityware.github.io/issues>`__.
