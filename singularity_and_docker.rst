.. _singularity-and-docker:


=====================================
Singularity and Docker/OCI containers
=====================================


--------
Overview
--------

.. TODO Overview content ... 

.. Review the overview of the Sy interface ... 


--------------------------------------------
Running action commands on Docker Hub images
--------------------------------------------



.. code-block:: none

    $ singularity run docker://godlovedc/lolcow
    INFO:    Converting OCI blobs to SIF format
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
     45.33 MiB / 45.33 MiB [====================================================] 1s
    Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
     848 B / 848 B [============================================================] 0s
    Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
     621 B / 621 B [============================================================] 0s
    Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
     853 B / 853 B [============================================================] 0s
    Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
     169 B / 169 B [============================================================] 0s
    Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
     53.75 MiB / 53.75 MiB [====================================================] 2s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: /home/vagrant/.singularity/cache/oci-tmp/a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb/lolcow_latest.sif
    INFO:    Image cached as SIF at /home/vagrant/.singularity/cache/oci-tmp/a692b57abc43035b197b10390ea2c12855d21649f2ea2cc28094d18b93360eeb/lolcow_latest.sif
     ___________________________________
    / Repartee is something we think of \
    | twenty-four hours too late.       |
    |                                   |
    \ -- Mark Twain                     /
     -----------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||



.. TODO info about shell, run, and exec on Docker Hub images
.. TODO explanation that layers are downloaded and then "spatted out to disk" to 
    .. TODO create an ephemeral Singularity container in which commands are run

.. TODO add a note re: ./??.sif above 

.. _sec:use_prebuilt_public_docker_images:

---------------------------------------------------------
Making use of pre-built public images from the Docker Hub
---------------------------------------------------------

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

.. TODO Should explain here or in previous section that docker to Singularity is 
    .. a one-way operation because info is lost.
    .. Also some words on how this is considered less reproducible than pulling
    .. from the container library.  


.. note:: 

    The above authentication warning originates from a check for the existence of ``${HOME}/.singularity/sylabs-token``. It can be ignored when making use of the Docker Hub. 

.. note:: 

    ``singularity search [search options...] <search query>`` does *not* support Docker registries like `Docker Hub <https://hub.docker.com/>`_. Use the search box at Docker Hub to locate Docker images. Docker ``pull`` commands, e.g., ``docker pull godlovedc/lolcow``, can be easily translated into the corresponding command for Singularity. The Docker ``pull`` command is available under "DETAILS" for a given image on Docker Hub. 

.. _sec:use_prebuilt_public_docker_images_SUB_inspect:

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

The ``sign`` command allows a cryptographic signature to be added. Refer to 
:ref:`Signing and Verifying Containers <signNverify>` for details. But caution
should be exercised in signing images from Docker Hub because, unless you build
an image from scratch (OS mirrors) you are probably not really sure about the
complete contents of that image. 

.. note::

    ``pull`` actually builds a SIF file that corresponds to the image you retrieved from the Docker Hub. Updates to the image on the Docker Hub will *not* be reflected in your *local* copy. 

.. TODO explain the full Docker URI - add the line below to a larger discussion - the existing 
    explanation is pretty good, but probably needs style edits.  

In our example ``docker://godlovedc/lolcow``, ``godlovedc`` specifies a Docker Hub user, whereas ``lolcow`` is the name of the repository. Adding the option to specifiy an image tag, the generic version of the URI is ``docker://<hub-user>/<repo-name>[:<tag>]``. `Repositories on Docker Hub <https://docs.docker.com/docker-hub/repos/>`_ provides additional details.

.. TODO Docker layers = OCI blobs ??? need note re: repeat blob here??? 


----------------------------------------------------------
Making use of pre-built private images from the Docker Hub
----------------------------------------------------------

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
====================================

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
========================================

Environment variables offer an alternative means for authentication with the Docker Hub. The **required** exports are as follows:

.. code-block:: none

    export SINGULARITY_DOCKER_USERNAME=ilumb
    export SINGULARITY_DOCKER_PASSWORD=<redacted>

Of course, the ``<redacted>`` plain-text password needs to be replaced by a valid one to be of practical use. 

.. note:: 

    This approach for authentication supports both interactive and non-interactive sessions. However, the requirement for a plain-text password assigned to an envrionment variable, is a security compromise for this flexibility. 

.. note:: 

    When specifying passwords, 'special characters' (e.g., ``$``, ``#``, ``.``) need to be escaped to avoid interpretation by the shell. 
 
.. TODO testing auth - updated from the 2.6 docs - needed?


--------------------------------------------------------------
Making use of pre-built private images from Private Registries
--------------------------------------------------------------

Authentication is required to access *private* images that reside in the Docker Hub. Of course, private images can also reside in **private registries**. Accounting for locations *other* than the Docker Hub is easily achieved. 

In the complete command line specification

.. code-block:: none

    docker://<registry>/<hub-user>/<repo-name>[:<tag>]

``registry`` defaults to ``index.docker.io``. In other words,

.. code-block:: none

    $ singularity pull docker://godlovedc/lolcow

is functionally equivalent to 

.. code-block:: none

    $ singularity pull docker://index.docker.io/godlovedc/lolcow

From the above example, it is evident that 

.. code-block:: none

    $ singularity pull docker://nvcr.io/nvidia/pytorch:18.11-py3
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:18d680d616571900d78ee1c8fff0310f2a2afe39c6ed0ba2651ff667af406c3e
    <blob fetching details deleted>
    Skipping fetch of repeat blob sha256:c71aeebc266c779eb4e769c98c935356a930b16d881d7dde4db510a09cfa4222
    Copying config sha256:b77551af8073c85588088ab2a39007d04bc830831ba1eef4127b2d39aaf3a6b1
     21.28 KiB / 21.28 KiB [====================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: pytorch_18.11-py3.sif

will retrieve a specific version of the `PyTorch platform <https://pytorch.org/>`_ for Deep Learning from the NVIDIA GPU Cloud (NGC). Because NGC is a private registry, the above ``pull`` assumes :ref:`authentication via environment variables <sec:authentication_via_environment_variables>` when the blobs that collectively comprise the Docker image have not already been cached locally. In the NGC case, the required environment variable are set as follows:

.. code-block:: none 

    export SINGULARITY_DOCKER_USERNAME=$oauthtoken
    export SINGULARITY_DOCKER_PASSWORD=<redacted>

Upon use, these environment-variable settings allow for authentication with NGC.

.. note::

    The password provided via these means is actually an API token. This token is generated via your NGC account, and is **required** for use of the service. For additional details regarding authentication with NGC, and much more, please consult their `Getting Started <https://docs.nvidia.com/ngc/ngc-getting-started-guide/index.html>`_ documentation. 

Alternatively, for purely interactive use, ``--docker-login`` is recommended:

.. code-block:: none

    $ singularity pull --docker-login docker://nvcr.io/nvidia/pytorch:18.11-py3
    Enter Docker Username: $oauthtoken
    Enter Docker Password: 
    INFO:    Starting build...
    Getting image source signatures
    Skipping fetch of repeat blob sha256:18d680d616571900d78ee1c8fff0310f2a2afe39c6ed0ba2651ff667af406c3e
    <blob fetching details deleted>
    Skipping fetch of repeat blob sha256:c71aeebc266c779eb4e769c98c935356a930b16d881d7dde4db510a09cfa4222
    Copying config sha256:b77551af8073c85588088ab2a39007d04bc830831ba1eef4127b2d39aaf3a6b1
    21.28 KiB / 21.28 KiB [====================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: pytorch_18.11-py3.sif

Authentication aside, the outcome of the ``pull`` is the Singularity container ``pytorch_18.11-py3.sif`` in SIF. 


------------------------------------------------------
Building images for Singularity from Docker Registries
------------------------------------------------------

The ``build`` command is used to **create** Singularity containers. Because it is documented extensively :ref:`elsewhere in this manual <build-a-container>`, only specifics relevant to Docker are provided here - namely, working with the Docker Hub via the Singularity command line and through Singularity definition files. 


Working from the Singularity Command Line
=========================================

Remotely Hosted Images
----------------------

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


Locally Cached Images
---------------------

Singularity containers can be built at the command line from images cached locally by Docker. Suppose, for example: 

.. code-block:: none

    $ sudo docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    godlovedc/lolcow    latest              577c1fe8e6d8        16 months ago       241MB

This indicates that ``godlovedc/lolcow:latest`` has been cached locally by Docker. Then 

.. code-block:: none

    $ sudo singularity build lolcow_from_docker_cache.sif docker-daemon://godlovedc/lolcow:latest
    WARNING: Authentication token file not found : Only pulls of public images will succeed
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:a2022691bf950a72f9d2d84d557183cb9eee07c065a76485f1695784855c5193
     119.83 MiB / 119.83 MiB [==================================================] 6s
    Copying blob sha256:ae620432889d2553535199dbdd8ba5a264ce85fcdcd5a430974d81fc27c02b45
     15.50 KiB / 15.50 KiB [====================================================] 0s
    Copying blob sha256:c561538251751e3685c7c6e7479d488745455ad7f84e842019dcb452c7b6fecc
     14.50 KiB / 14.50 KiB [====================================================] 0s
    Copying blob sha256:f96e6b25195f1b36ad02598b5d4381e41997c93ce6170cab1b81d9c68c514db0
     5.50 KiB / 5.50 KiB [======================================================] 0s
    Copying blob sha256:7f7a065d245a6501a782bf674f4d7e9d0a62fa6bd212edbf1f17bad0d5cd0bfc
     3.00 KiB / 3.00 KiB [======================================================] 0s
    Copying blob sha256:70ca7d49f8e9c44705431e3dade0636a2156300ae646ff4f09c904c138728839
     116.56 MiB / 116.56 MiB [==================================================] 6s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_from_docker_cache.sif

results in ``lolcow_from_docker_cache.sif`` for native use by Singularity. There are two important differences in syntax evident in the above ``build`` command:

    1. The ``docker`` part of the URI has been appended by ``daemon``. This ensures Singularity seek an image locally cached by Docker to boostrap the conversion process to SIF, as opposed to attempting to retrieve an image remnotely hosted via the Docker Hub. 

    2. ``sudo`` is prepended to the ``build`` command for Singularity. This is required as the Docker daemon executes as ``root``.  

.. note:: 

    The tag ``latest`` is **required** when bootstraping creation of a container for Singularity from an image locally cached by Docker. 


Working with Definition Files
=============================

Mandatory Headers: Remotely Boostrapped
---------------------------------------

Akin to a set of blueprints that explain how to build a custom container, Singularity definition files (or "def files") are considered in detail :ref:`elsewhere in this manual <definition-files>`. Therefore, only def file nuances specific to interoperability with Docker receive consideration here. 

Singularity definition files are comprised of two parts - a **header** plus **sections**. 

When working with repositories such as the Docker Hub, ``Bootstrap`` and ``From`` are **mandatory** keywords within the header; for example, if the file ``lolcow.def`` has contents 

.. code-block:: singularity 

    Bootstrap: docker
    From: godlovedc/lolcow

then 

.. code-block:: none 

    sudo singularity build lolcow.sif lolcow.def

creates a Singularity container in SIF by bootstrapping from the public ``godlovedc/lolcow`` image from the Docker Hub. 

In the above definition file, ``docker`` is one of numerous, possible bootstrap agents; this, and other bootstrap agents receive attention :ref:`in the appendix <build-docker-module>`.     

Through the means for authentication described above, definition files permit use of private images hosted via the Docker Hub. For example, if the file ``mylolcow.def`` has contents

.. code-block:: singularity 

    Bootstrap: docker
    From: ilumb/mylolcow

then 

.. code-block:: none 

    sudo singularity build --docker-login mylolcow.sif mylolcow.def 

creates a Singularity container in SIF by bootstrapping from the *private* ``ilumb/mylolcow`` image from the Docker Hub after successful :ref:`interactive authentication <sec:authentication_via_docker_login>`. 

Alternatively, if :ref:`environment variables have been set as above <sec:authentication_via_environment_variables>`, then 

.. code-block:: none 

    sudo -E singularity build mylolcow.sif mylolcow.def

enables authenticated use of the private image. 

.. note:: 

    The ``-E`` option is required to preserve the user's existing environment variables upon ``sudo`` invocation - a priviledge escalation *required* to create Singularity containers via the ``build`` command. 

Mandatory Headers: Locally Boostrapped
---------------------------------------

If def file is 

.. code-block:: singularity 

    Bootstrap: docker-daemon
    From: godlovedc/lolcow:latest

then 

.. code-block:: none 

    $ sudo singularity build lolcow_from_docker_cache.sif lolcow-d.def 
    WARNING: Authentication token file not found : Only pulls of public images will succeed
    Build target already exists. Do you want to overwrite? [N/y] y
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:a2022691bf950a72f9d2d84d557183cb9eee07c065a76485f1695784855c5193
     119.83 MiB / 119.83 MiB [==================================================] 6s
    Copying blob sha256:ae620432889d2553535199dbdd8ba5a264ce85fcdcd5a430974d81fc27c02b45
     15.50 KiB / 15.50 KiB [====================================================] 0s
    Copying blob sha256:c561538251751e3685c7c6e7479d488745455ad7f84e842019dcb452c7b6fecc
     14.50 KiB / 14.50 KiB [====================================================] 0s
    Copying blob sha256:f96e6b25195f1b36ad02598b5d4381e41997c93ce6170cab1b81d9c68c514db0
     5.50 KiB / 5.50 KiB [======================================================] 0s
    Copying blob sha256:7f7a065d245a6501a782bf674f4d7e9d0a62fa6bd212edbf1f17bad0d5cd0bfc
     3.00 KiB / 3.00 KiB [======================================================] 0s
    Copying blob sha256:70ca7d49f8e9c44705431e3dade0636a2156300ae646ff4f09c904c138728839
     116.56 MiB / 116.56 MiB [==================================================] 6s
    Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
     3.33 KiB / 3.33 KiB [======================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: lolcow_from_docker_cache.sif


Optional Headers
----------------

In the two-previous examples, the ``From`` keyword specifies *both* the ``hub-user`` and ``repo-name`` in making use of the Docker Hub. *Optional* use of ``Namespace`` permits the more-granular split across two keywords:

.. code-block:: singularity

    Bootstrap: docker
    Namespace: godlovedc
    From: lolcow

.. note:: 

    In `their documentation <https://docs.docker.com/docker-hub/repos/>`_, "Docker ID namespace" and ``hub-user`` are employed as synonyms in the text and examples, respectively. 

.. note::

    The default value for the optional keyword ``Namespace`` is ``library``. 


Private Images and Registries 
-----------------------------

Thus far, use of Docker Hub has been assumed. To make use of a different repository of Docker images the **optional** ``Registry`` keyword can be added to the Singularity definition file. For example, to make use of a Docker image from the NVIDIA GPU Cloud (NGC) corresponding definition file is:

.. code-block:: singularity

    Bootstrap: docker
    From: nvidia/pytorch:18.11-py3
    Registry: nvcr.io

This def file ``ngc_pytorch.def`` can be passed as a specification to ``build`` as follows:

.. code-block:: none 

    $ sudo singularity build --docker-login mypytorch.sif ngc_pytorch.def 
    Enter Docker Username: $oauthtoken
    Enter Docker Password: <obscured>
    INFO:    Starting build...
    Getting image source signatures
    Copying blob sha256:18d680d616571900d78ee1c8fff0310f2a2afe39c6ed0ba2651ff667af406c3e
     41.34 MiB / 41.34 MiB [====================================================] 2s
    <blob copying details deleted>
    Copying config sha256:b77551af8073c85588088ab2a39007d04bc830831ba1eef4127b2d39aaf3a6b1
    21.28 KiB / 21.28 KiB [====================================================] 0s
    Writing manifest to image destination
    Storing signatures
    INFO:    Creating SIF file...
    INFO:    Build complete: mypytorch.sif

After successful authentication via interactive use of the ``--docker-login`` option, output as the SIF container ``mypytorch.sif`` is (ultimately) produced. As above, use of environment variables is another option available for authenticating private Docker type repositories such as NGC; once set, the ``build`` command is as above save for the absence of the ``--docker-login`` option. 


.. _sec:def_files_execution:

Directing Execution 
-------------------

The ``Dockerfile`` corresponding to ``godlovedc/lolcow`` (and `available here <https://hub.docker.com/r/godlovedc/lolcow/dockerfile>`_) is as follows:

.. code-block:: none

    FROM ubuntu:16.04

    RUN apt-get update && apt-get install -y fortune cowsay lolcat

    ENV PATH /usr/games:${PATH}
    ENV LC_ALL=C

    ENTRYPOINT fortune | cowsay | lolcat

The execution-specific part of this ``Dockerfile`` is the ``ENTRYPOINT`` - "... an optional definition for the first part of the command to be run ..." according to `the available documentation <https://docs.docker.com/search/?q=ENTRYPOINT>`_. After conversion to SIF, execution of ``fortune | cowsay | lolcat`` *within* the container produces the output:

.. code-block:: none 

    $ ./mylolcow.sif 
     ______________________________________
    / Q: How did you get into artificial   \
    | intelligence? A: Seemed logical -- I |
    \ didn't have any real intelligence.   /
     --------------------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||



In addition, ``CMD`` allows an arbitrary string to be *appended* to the ``ENTRYPOINT``. Thus, multiple commands or flags can be passed together through combined use.

Suppose now that a Singularity `%runscript` **section** is added to the definition file as follows:

.. code-block:: singularity

    Bootstrap: docker
    Namespace: godlovedc
    From: lolcow

    %runscript

        fortune

After conversion to SIF via the Singularity ``build`` command, exection of the resulting container produces the output:

.. code-block:: none 

    $ ./lolcow.sif 
    This was the most unkindest cut of all.
            -- William Shakespeare, "Julius Caesar"

In other words, introduction of a ``%runscript`` section into the Singularity definition file causes the ``ENTRYPOINT`` of the ``Dockerfile`` to be *bypassed*. The presence of the ``%runscript`` section would also bypass a ``CMD`` entry in the ``Dockerfile``. 

To *preserve* use of ``ENTRYPOINT`` and/or ``CMD`` as defined in the ``Dockerfile``, the ``%runscript`` section must be *absent* from the Singularity definition. In this case, and to favor execution of ``CMD`` *over* ``ENTRYPOINT``, a non-empty assignment of the *optional* ``IncludeCmd`` should be included in the header section of the Singularity definition file as follows:

.. code-block:: singularity

    Bootstrap: docker
    Namespace: godlovedc
    From: lolcow
    IncludeCmd: yes

.. note:: 

    Because only a non-empty ``IncludeCmd`` is required, *either* ``yes`` (as above) or ``no`` results in execution of ``CMD`` *over* ``ENTRYPOINT``. 

.. _sec:def_files_execution_SUB_execution_precedence:

To summarize execution precedence:  

    1. If present, the %runscript section of the Singularity definition file is executed 

    2. If ``IncludeCmd`` is a non-empty entry in the header of the Singularity definition file, then ``CMD`` from the ``Dockerfile`` is executed 

    3. If present in the ``Dockerfile``, ``ENTRYPOINT`` appended by ``CMD`` (if present) are executed in sequence 

    4. Execution of the ``bash`` shell is defaulted to

.. TODO Test CMD vs ENTRYPOINT via a documented example 


Container Metadata 
------------------

Singularity's ``inspect`` command displays container metadata - data about data that is encapsulated within a SIF file. Default output (assumed via the ``--labels`` option) from the command was :ref:`illustrated above <sec:use_prebuilt_public_docker_images_SUB_inspect>`. ``inspect``, however, provides a number of options that are alluded to here. 

Emphasis in this section has been on Singularity definition files. The definition file that created a SIF file can be determined from the container's metadata as follows:

.. code-block:: none

    $ singularity inspect --deffile lolcow.sif 

    namespace: godlovedc
    from: lolcow
    bootstrap: docker

    %runscript

        fortune

Of particular relevance to :ref:`execution precedence <sec:def_files_execution_SUB_execution_precedence>` is the ``--runscript`` option for ``inspect``. For example, using the definition file above, the runscript is unsurprisingly:

.. code-block:: none

    $ singularity inspect --runscript lolcow.sif 

    #!/bin/sh


        fortune

As stated above (i.e., :ref:`the first case of execution precedence <sec:def_files_execution_SUB_execution_precedence>`), the very existence of a ``%runscript`` section in a Singularity definition file *takes precedence* over commands that might exist in the ``Dockerfile``. 

When the ``%runscript`` section is *removed* from the Singularity definition file, the result is (once again):

.. code-block:: none

    $ singularity inspect --deffile lolcow.sif 

    from: lolcow
    bootstrap: docker
    namespace: godlovedc

.. TODO below ... Need to add a CMD to lolcow ... 

.. Note, however, that ``IncludeCmd: yes`` was *added* to the def file to allow for illustration of the :ref:`the second case of execution precedence <sec:def_files_execution_SUB_execution_precedence>`); the resulting runscript for the container is:

The runscript 'inherited' from the ``Dockerfile`` is:

.. code-block:: none

    $ singularity inspect --runscript lolcow.sif 

    #!/bin/sh
    OCI_ENTRYPOINT='"/bin/sh" "-c" "fortune | cowsay | lolcat"'
    OCI_CMD=''
    # ENTRYPOINT only - run entrypoint plus args
    if [ -z "$OCI_CMD" ] && [ -n "$OCI_ENTRYPOINT" ]; then
        SINGULARITY_OCI_RUN="${OCI_ENTRYPOINT} $@"
    fi

    # CMD only - run CMD or override with args
    if [ -n "$OCI_CMD" ] && [ -z "$OCI_ENTRYPOINT" ]; then
        if [ $# -gt 0 ]; then
            SINGULARITY_OCI_RUN="$@"
        else
            SINGULARITY_OCI_RUN="${OCI_CMD}"
        fi
    fi

    # ENTRYPOINT and CMD - run ENTRYPOINT with CMD as default args
    # override with user provided args
    if [ $# -gt 0 ]; then
        SINGULARITY_OCI_RUN="${OCI_ENTRYPOINT} $@"
    else
        SINGULARITY_OCI_RUN="${OCI_ENTRYPOINT} ${OCI_CMD}"
    fi

    eval ${SINGULARITY_OCI_RUN}

From this Bourne shell script, it is evident that only an ``ENTRYPOINT`` is detailed in the ``Dockerfile``; thus the ``ENTRYPOINT only - run entrypoint plus args`` conditional block is executed. In this case then, :ref:`the third case of execution precedence <sec:def_files_execution_SUB_execution_precedence>` has been illustrated. 

The above Bourne shell script also illustrates how the following scenarios will be handled:

    - A ``CMD`` only entry in the ``Dockerfile`` 

    - **Both** ``ENTRYPOINT`` *and* ``CMD`` entries in the ``Dockerfile`` 

From this level of detail, use of ``ENTRYPOINT`` *and/or* ``CMD`` in a Dockerfile has been made **explicit**. These remain examples within :ref:`the third case of execution precedence <sec:def_files_execution_SUB_execution_precedence>`. 

The ``--environment`` option for ``inspect`` is worth noting; for example:

.. code-block:: none

    $ singularity inspect --environment lolcow.sif

    #!/bin/sh
    #Custom environment shell code should follow

Other ``inspect`` options are detailed :ref:`elsewhere in this manual <environment-and-metadata>` and available online via ``singularity inspect --help``. 

.. TODO (optional) siftool ??? 


.. --------------
.. Best Practices
.. --------------

.. TODO Existing text 
.. TODO Maintaining images 

.. ---------------
.. Troubleshooting
.. ---------------

.. TODO Existing pgh + testing auth'n 





.. TODO Account for locally cached Docker images - further research required ...  

.. I suggest the following additional topics to round the page out.  Maybe we can 
.. carve off topics and work on the page together.
.. 

.. TODO The breakdown of the URI is useful and should be retained (but edited)
..     https://www.sylabs.io/guides/2.6/user-guide/singularity_and_docker.html#how-do-i-specify-my-docker-image

.. TODO build a singularity container from local docker images (ask Ian and/or Michael)
..     running in daemon
..     sitting on host 
.. build from an OCI bundle (ask Ian and/or Michael.)