.. _singularity-and-docker:


=====================================
Singularity and Docker/OCI containers
=====================================

.. TODO Singularity Hub ? <-- I would not worry about either Singularity Hub or
    .. the contaienr library on this page.  Both of those host containers that are 
    .. in native Singularity formats.  I think this page is more for interacting 
    .. with things in Docker or OCI format.  (feel free to delete comment.)

--------
Overview
--------

.. TODO Overview content ... 

.. TODO relocate below ??? 

.. Review the overview of the Sy interface ... 


.. ------------------------------------------
.. Making use of pre-built Singularity images
.. ------------------------------------------

.. SHUB and NVIDIA ... 


----------------------------
Interoperability with Docker
----------------------------

Running action commands on Docker Hub images
============================================

.. info about shell, run, and exec on Docker Hub images
.. explanation that layers are downloaded and then "spatted out to disk" to 
    .. create an ephemeral Singularity container in which commands are run


.. _sec:use_prebuilt_public_docker_images:

Making use of pre-built public images from the Docker Hub
=========================================================

Singularity can make use of pre-built public images available from the `Docker Hub <https://hub.docker.com/>`_. By specifying the ``docker://`` URI for an image you have already located, Singularity can ``pull``  it - e.g.: 

.. code-block:: none

    $ singularity pull docker://godlovedc/lolcow
    WARNING: Authentication token file not found : Only pulls of public images will succeed
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
     45.33 MiB / 45.33 MiB [====================================================] 2s
    Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
     848 B / 848 B [============================================================] 0s
    Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
     621 B / 621 B [============================================================] 0s
    Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
     853 B / 853 B [============================================================] 0s
    Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
     169 B / 169 B [============================================================] 0s
    Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
     53.75 MiB / 53.75 MiB [====================================================] 3s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_latest.sif

This ``pull`` results in a *local* copy of the Docker image in SIF, the Singularity Image Format:

.. code-block:: none

    $ file lolcow_latest.sif 
    lolcow_latest.sif: a /usr/bin/env run-singularity script executable (binary data)

In translating to SIF, individual layers of the Docker image have been *combined* into a single, native file for use via Singularity; there is no need to subsequently ``build`` the image for Singularity. For example, you can now ``exec``, ``run`` or ``shell`` into the SIF version via Singularity. See :ref:`Interact with images <quick-start>`. 

.. TODO improve ref above to quick start ... interact 
    .. Should explain here or in previous section that docker to Singularity is 
    .. a one-way operation because info is lost.
    .. Also some workds on how this is considered less reproducible than pulling
    .. from the container library.  
    .. Also should talk about how a build and a pull are really the same thing
    .. under the hood.  Both are really "builds" in the sense that the layers 
    .. are built into a Singularity image.

.. note:: 

    The above authentication warning originates from a check for the existence of ``${HOME}/.singularity/sylabs-token``. It can be ignored when making use of the Docker Hub. 

.. note:: 

    ``singularity search [search options...] <search query>`` does *not* support Docker registries like `Docker Hub <https://hub.docker.com/>`_. Use the search box at Docker Hub to locate Docker images. Docker ``pull`` commands, e.g., ``docker pull godlovedc/lolcow``, can be easily translated into the corresponding command for Singularity. The Docker ``pull`` command is available under "DETAILS" for a given image on Docker Hub. 

``inspect`` reveals metadata for the container encapsulated via SIF:

.. code-block:: none

        $ singularity inspect lolcow_latest.sif 

        {
            "org.label-schema.build-date": "Thursday_6_December_2018_17:29:48_UTC",
            "org.label-schema.schema-version": "1.0",
            "org.label-schema.usage.singularity.deffile.bootstrap": "docker",
            "org.label-schema.usage.singularity.deffile.from": "godlovedc/lolcow",
            "org.label-schema.usage.singularity.version": "3.0.1-40.g84083b4f"
        }

SIF files built from Docker images are *not* crytographically signed:

.. code-block:: none

    $ singularity verify lolcow_latest.sif 
    Verifying image: lolcow_latest.sif
    ERROR:   verification failed: error while searching for signature blocks: no signatures found for system partition

.. TODO Need to fix ref below ... 

The ``sign`` command allows a cryptographic signature to be added. Refer to 
:ref:`Signing and Verifying Containers <signNverify>` for details. But caution
should be exercised in signing images from Docker Hub because, unless you build
an image from scratch (OS mirrors) you are probably not really sure about the
complete contents of that image. 

.. note::

    ``pull`` actually builds a SIF file that corresponds to the image you retrieved from the Docker Hub. Updates to the image on the Docker Hub will *not* be reflected in your *local* copy. 

.. the line below should probaby be added to a larger discussion in which the 
.. entire URI is explained.  I think the existing explanation is pretty good,
.. but probably needs style edits. 

In our example ``docker://godlovedc/lolcow``, ``godlovedc`` specifies a Docker Hub user, whereas ``lolcow`` is the name of the repository. Adding the option to specifiy an image tag, the generic version of the URI is ``docker://<hub-user>/<repo-name>[:<tag>]``. `Repositories on Docker Hub <https://docs.docker.com/docker-hub/repos/>`_ provides additional details.

.. TODO Docker layers = OCI blobs ??? need note re: repeat blob here??? 


Making use of pre-built private images from the Docker Hub
==========================================================

After successful authentication, Singularity can also make use of pre-built *private* images available from the `Docker Hub <https://hub.docker.com/>`_. The three means available for authentication follow here. Before describing these means, it is instructive to illustate the error generated when attempting access a private image *without* credentials:

.. code-block:: none

    $ singularity pull docker://ilumb/mylolcow
    INFO:    Starting build...
    FATAL:   Unable to pull docker://ilumb/mylolcow: conveyor failed to get: Error reading manifest latest in docker.io/ilumb/mylolcow: errors:
    denied: requested access to the resource is denied
    unauthorized: authentication required

In this case, the ``mylolcow`` repository of user ``ilumb`` **requires** authentication through specification of a valid username and password. 


.. _sec:authentication_via_docker_login: 

Authentication via Interactive Login
------------------------------------

Interactive login is the first of three means provided for authentication with the Docker Hub. It is enabled through use of the ``--docker-login`` option of Singularity's ``pull`` command; for example:

.. code-block:: none 

    $ singularity pull --docker-login docker://ilumb/mylolcow
    Enter Docker Username: ilumb
    Enter Docker Password: 
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:7b8b6451c85f072fd0d7961c97be3fe6e2f772657d471254f6d52ad9f158a580
    Skipping fetch of repeat blob sha256:ab4d1096d9ba178819a3f71f17add95285b393e96d08c8a6bfc3446355bcdc49
    Skipping fetch of repeat blob sha256:e6797d1788acd741d33f4530106586ffee568be513d47e6e20a4c9bc3858822e
    Skipping fetch of repeat blob sha256:e25c5c290bded5267364aa9f59a18dd22a8b776d7658a41ffabbf691d8104e36
    Skipping fetch of repeat blob sha256:258e068bc5e36969d3ba4b47fd3ca0d392c6de465726994f7432b14b0414d23b
    Copying config sha256:8a8f815257182b770d32dffff7f185013b4041d076e065893f9dd1e89ad8a671
     3.12 KiB / 3.12 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: mylolcow_latest.sif

After successful authentication, the private Docker image is pulled and converted to SIF as described above. 

.. note::

    For interactive sessions, ``--docker-login`` is recommended as use of plain-text passwords in your environment is *avoided*. Encoded authentication data is communicated with the Docker Hub via secure HTTP. 


.. _sec:authentication_via_environment_variables: 

Authentication via Environment Variables
----------------------------------------

Environment variables offer an alternative means for authentication with the Docker Hub. The **required** exports are as follows:

.. code-block:: none

    export SINGULARITY_DOCKER_USERNAME=ilumb
    export SINGULARITY_DOCKER_PASSWORD=<redacted>

Of course, the ``<redacted>`` plain-text password needs to be replaced by a valid one to be of practical use. 

.. note:: 

    This approach for authentication supports both interactive and non-interactive sessions. However, the requirement for a plain-text password assigned to an envrionment variable, is a security compromise for this flexibility. 

.. note:: 

    When specifying passwords, 'special characters' (e.g., ``$``, ``#``, ``.``) need to be escaped to avoid interpretation by the shell. 


.. TODO + NGC specifics 



Building images for Singularity from the Docker Hub
===================================================

The ``build`` command is used to **create** Singularity containers. Because it is documented extensively :ref:`elsewhere in this manual <build-a-container>`, only specifics relevant to Docker are provided here - namely, working with the Docker Hub via the Singularity command line and through Singularity definition files. 


Working from the Singularity Command Line
-----------------------------------------

In the simplest case, ``build`` is functionally equivalent to ``pull``: 

.. code-block:: none

    $ singularity build mylolcow_latest.sif docker://godlovedc/lolcow
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: mylolcow_latest.sif

This ``build`` results in a *local* copy of the Docker image in SIF, as did ``pull`` :ref:`above <sec:use_prebuilt_public_docker_images>`. Of course, ``build`` allows the name of the Singularity container to be specified as ``mylolcow_latest.sif``, whereas ``pull`` does not support this capability. 

.. note::

     ``docker://godlovedc/lolcow`` is the target provided as input for ``build``. Armed with this target, ``build`` applies the appropriate method to create the container - in this case, one appropriate for the Docker Hub. 

In addition to a read-only container image in SIF (**default**), ``build`` allows for the creation of a writable (ch)root directory called a sandbox for interactive development via the ``--sandbox`` option: 

.. code-block:: none

    $ singularity build --sandbox mylolcow_latest_sandbox.sif docker://godlovedc/lolcow
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
    Skipping fetch of repeat blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
    Skipping fetch of repeat blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
    Skipping fetch of repeat blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
    Skipping fetch of repeat blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
    Skipping fetch of repeat blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating sandbox directory...
    INFO:    Build complete: mylolcow_latest_sandbox.sif

After successful execution, the above command results in creation of the ``mylolcow_latest_sandbox.sif`` directory with contents:

.. code-block:: none

    bin  boot  core  dev  environment  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  singularity  srv  sys  tmp  usr  var

The ``build`` command of Singularity allows (e.g., development) sandbox containers to be converted into (e.g., production) read-only SIF containers, and vice-versa. Consult the :ref:`Build a container <build-a-container>` documentation for the details. 

Implicit in the above command-line interactions is use of pre-built public images from the Docker Hub. To make use of pre-built **private** images from the Docker Hub, authentication is required. Available means for authentication were described above. Use of environment variables is functionally equivalent for Singularity ``build`` as it is for ``pull``; see :ref:`Authentication via Environment Variables <sec:authentication_via_environment_variables>` above. For purely interactive use, authentication can be added to the ``build`` command as follows:

.. code-block:: none

    singularity build --docker-login mylolcow_latest_il.sif docker://ilumb/mylolcow

(Recall that ``docker://ilumb/mylolcow`` is a private image available via the Docker Hub.) See :ref:`Authentication via Interactive Login <sec:authentication_via_docker_login>` above regarding use of ``--docker-login``.


Working with Definition Files: Docker-Specific Headers
------------------------------------------------------

Akin to a set of blueprints that explain how to build a custom container, Singularity definition files (or "def files") are considered in detail :ref:`elsewhere in this manual <definition-files>`. Therefore, only def file nuances specific to interoperability with Docker receive consideration here. 

Singularity definition files are comprised of two parts - a **header** plus **sections**. 

When working with repositories such as the Docker Hub, ``Bootstrap`` and ``From`` are mandatory keywords within the header; for example, if the file ``lolcow.def`` has contents 

.. code-block:: singularity 

    Bootstrap: docker
    From: godlovedc/lolcow

then 

.. code-block:: none 

    sudo singularity build lolcow.sif lolcow.def

creates a Singularity container in SIF by bootstrapping from the public ``godlovedc/lolcow`` image from the Docker Hub. 

In the above definition file, ``docker`` is one of numerous, possible bootstrap agents; again, the section dedicated to definition files provides additional context. 

Through the means for authentication described above, definition files permit use of private images hosted via the Docker Hub. For example, if the file ``mylolcow.def`` has contents

.. code-block:: singularity 

    Bootstrap: docker
    From: ilumb/mylolcow

then 

.. code-block:: none 

    sudo singularity build --docker-login mylolcow.sif mylolcow.def 

creates a Singularity container in SIF by bootstrapping from the *private* ``ilumb/mylolcow`` image from the Docker Hub after successful :ref:`interactive authenticcation <sec:authentication_via_docker_login>`. 

Alternatively, if :ref:`environment variables have been set as above <sec:authentication_via_environment_variables>`, then 

.. code-block:: none 

    sudo -E singularity build mylolcow.sif mylolcow.def

enables authenticated use of the private image. 

.. note:: 

    The ``-E`` option is required to preserve the user's existing environment variables upon ``sudo`` invocation - a priviledge escalation *required* to create Singularity containers via the ``build`` command. 


Working with Definition Files: Docker-Specific Sections
-------------------------------------------------------

.. TODO https://www.sylabs.io/guides/3.0/user-guide/appendix.html#docker-bootstrap-agent 



.. --------------
.. Best Practices
.. --------------

.. TODO Existing text 
.. TODO Maintaining images 

.. ---------------
.. Troubleshooting
.. ---------------

.. TODO Existing pgh + testing auth'n 



.. TODO Othjer commands that can do this >>>>?? 


.. TODO What about private Docker registries? How does signing/verification work in that case? 



.. TODO Account for locally cached Docker images - further research required ...  

.. I suggest the following additional topics to round the page out.  Maybe we can 
.. carve off topics and work on the page together.
.. 
.. Using docker bootstrap agent in a def file (link to appendix)
..     Must figure out all of the CMD and ENTRYPOINT stuff.  afaik it has changed?
.. The breakdown of the URI is useful and should be retained (but edited)
..     https://www.sylabs.io/guides/2.6/user-guide/singularity_and_docker.html#how-do-i-specify-my-docker-image
.. Using custom authentication for a private Docker Hub repo (may need to set one
..     up for testing)
.. Using a different registry.  quay.io would provide a good example
.. How to use nvidia's cloud
.. build a singularity container from local docker images (ask Ian and/or Michael)
..     running in daemon
..     sitting on host 
.. build from an OCI bundle (ask Ian and/or Michael.)
.. The best practices section is also useful and should likely be retained


