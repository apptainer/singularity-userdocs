.. _environment-and-metadata:

========================
Environment and Metadata
========================

.. _sec:envandmetadata:

Singularity containers support environment variables and labels that you
can add to your container during the build process.
If you are looking for specific environment variables for build time,
see our :ref:`build environment section <build-environment>`.

--------
Overview
--------

Environment variables can be included in your container by adding them in the following sections:

- On your ``%environment`` section of your definition file.

  Like this:

.. code-block:: singularity

        Bootstrap: library
        From: library/alpine
        %environment
            VARIABLE_ONE = hello
            VARIABLE_TWO = world
            export VARIABLE_ONE VARIABLE_TWO

- Or on your ``%post`` section of your definition file.

    Like this:

.. code-block:: singularity

        Bootstrap: library
        From: library/alpine
        %post
            echo 'export VARIABLE_NAME=VARIABLE_VALUE' >>$SINGULARITY_ENVIRONMENT

To check the available labels on your container you can also run the following command:

.. code-block:: singularity

    $  singularity inspect mysifimage.sif

This will give you the following output:

.. code-block:: singularity

      {
          "OWNER": "Joana",
          "org.label-schema.build-date": "Monday_07_January_2019_0:01:50_CET",
          "org.label-schema.schema-version": "1.0",
          "org.label-schema.usage": "/.singularity.d/runscript.help",
          "org.label-schema.usage.singularity.deffile.bootstrap": "library",
          "org.label-schema.usage.singularity.deffile.from": "debian:9",
          "org.label-schema.usage.singularity.runscript.help": "/.singularity.d/runscript.help",
          "org.label-schema.usage.singularity.version": "3.0.1-236.g2453fdfe"
      }

Of course, all of these labels will be shown by default, so to add new custom labels you
should use the ``%labels`` section in your definition file.

Like this:

.. code-block:: singularity

          Bootstrap: library
          From: library/alpine
          %labels
            MASTER = yoda

So after building this container with the label inside the ``%labels`` section, the inspect command
will return the list with the ``MASTER`` label inside.

Notice that you can use any type of combination that suits your needs, you can consider the sections that
you consider are important for building your container. To know more about the inspect command you can see the
:ref:`inspect command section <inspect-command>`.

-----------
Environment
-----------

If you build a container from Container Library or Docker Hub, the
environment will be included with the container at build time. You can
also define custom environment variables in your definition file as follows:

.. code-block:: singularity

    Bootstrap: library
    From: library/alpine
    %environment
        #First define the variables
        VARIABLE_PATH=/usr/local/bootstrap
        VARIABLE_VERSION=3.0
        #Then export them
        export VARIABLE_PATH VARIABLE_VERSION

You may need to add environment variables to your container during the
``%post`` section. For instance, maybe you will not know the appropriate
value of a variable until you have installed some software.
To add variables to the environment during ``%post`` you can use the
``$SINGULARITY_ENVIRONMENT`` variable with the following syntax:

.. code-block:: singularity

    %post
        echo 'export VARIABLE_NAME=VARIABLE_VALUE' >>$SINGULARITY_ENVIRONMENT

Text in the ``%environment`` section will be appended to the file ``/.singularity.d/env/90-environment.sh`` while text redirected
to ``$SINGULARITY_ENVIRONMENT`` will end up in the file ``/.singularity.d/env/91-environment.sh``.
Of course if nothing is redirected to ``$SINGULARITY_ENVIRONMENT`` in the ``%post`` section, the file ``/.singularity.d/env/91-environment.sh`` will not exist.

Because files in ``/.singularity.d/env`` are sourced in alpha-numerical order, this means that
variables added using ``$SINGULARITY_ENVIRONMENT`` take precedence over those added via the ``%environment``
section.

If you need to define a variable in the container at runtime, when you execute
Singularity pass a variable prefixed with ``SINGULARITYENV_``. They will be
transposed automatically and the prefix will be stripped. For example,
let’s say we want to set the variable ``HELLO`` to have value ``WORLD``. We can do that
as follows:

.. code-block:: singularity

    $ SINGULARITYENV_HELLO=WORLD singularity exec --cleanenv centos7.img env
    HELLO=WORLD
    LD_LIBRARY_PATH=:/usr/local/lib:/usr/local/lib64
    SINGULARITY_NAME=test.img
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    PWD=/home/gmk/git/singularity
    LANG=en_US.UTF-8
    SHLVL=0
    SINGULARITY_INIT=1
    SINGULARITY_CONTAINER=test.img

Notice the ``--cleanenv`` in the example above? That argument specifies that we want
to remove the host environment from the container. If we remove the ``--cleanenv``,
we will still pass forward ``HELLO=WORLD``, and the list shown above, but we will
also pass forward all the other environment variables from the host.

If you need to change the ``$PATH`` of your container at runtime there are
a few environmental variables you can use:

-  ``SINGULARITYENV_PREPEND_PATH=/good/stuff/at/beginning`` to prepend directories to the beginning of the ``$PATH``

-  ``SINGULARITYENV_APPEND_PATH=/good/stuff/at/end`` to append directories to the end of the ``$PATH``

-  ``SINGULARITYENV_PATH=/a/new/path`` to override the ``$PATH`` within the container

------
Labels
------

Your container stores metadata about its build, along with Docker
labels, and custom labels that you define during build in a ``%labels`` section.

For containers that are generated with Singularity version 3.0 and
later, labels are represented using the `rc1 Label Schema <http://label-schema.org/rc1/>`_. For
example:

.. code-block:: singularity

    $ singularity inspect jupyter.sif
        {
            "OWNER": "Joana",
            "org.label-schema.build-date": "Friday_21_December_2018_0:49:50_CET",
            "org.label-schema.schema-version": "1.0",
            "org.label-schema.usage": "/.singularity.d/runscript.help",
            "org.label-schema.usage.singularity.deffile.bootstrap": "library",
            "org.label-schema.usage.singularity.deffile.from": "debian:9",
            "org.label-schema.usage.singularity.runscript.help": "/.singularity.d/runscript.help",
            "org.label-schema.usage.singularity.version": "3.0.1-236.g2453fdfe"
        }

You will notice that the one label doesn’t belong to the label schema, ``OWNER`` .
This was a user provided label during bootstrap.

You can add custom labels to your container in a bootstrap file:

.. code-block:: singularity

    Bootstrap: docker
    From: ubuntu: latest
    %labels
      AUTHOR Joana

The ``inspect`` command is useful for viewing labels and other container meta-data,
we will see more in detail the different options that this command offers in the next section.

-----------------------
The ``inspect`` command
-----------------------

.. _sec:inspect-command:

The ``inspect`` command gives you the possibility to print out the environment variables and/or metadata that was added in your definition file and that were then added into your container.

Of course the simple execution of inspect command will give you an output in JSON format, but if you are looking to know some parts of the definition file and do not want to print them all,
you might be interested in the following options:

^^^^^^^^^^^^
``--labels``
^^^^^^^^^^^^

This flag corresponds to the default behavior of the ``inspect`` command. When you run a ``singularity inspect <your-container.sif>`` you will get this same output.

.. code-block:: singularity

    $ singularity inspect --labels jupyter.sif

And the output would look like:

.. code-block:: singularity

    {
        "org.label-schema.build-date": "Friday_21_December_2018_0:49:50_CET",
        "org.label-schema.schema-version": "1.0",
        "org.label-schema.usage": "/.singularity.d/runscript.help",
        "org.label-schema.usage.singularity.deffile.bootstrap": "library",
        "org.label-schema.usage.singularity.deffile.from": "debian:9",
        "org.label-schema.usage.singularity.runscript.help": "/.singularity.d/runscript.help",
        "org.label-schema.usage.singularity.version": "3.0.1-236.g2453fdfe"
    }

Which of course is the same output as running ``singularity inspect jupyter.sif``.

^^^^^^^^^^^^^
``--deffile``
^^^^^^^^^^^^^

This flag will give you as an output the def file as you would ``cat`` your definition file on the command line.

.. code-block:: singularity

    $ singularity inspect --deffile jupyter.sif

And the output would look like:

.. code-block:: singularity

    bootstrap: library
    from: debian:9
    %help
      Container with Anaconda 2 (Conda 4.5.11 Canary) and Jupyter Notebook 5.6.0 for Debian 9.x (Stretch).
      This installation is based on Python 2.7.15
    %environment
      JUP_PORT=8888
      JUP_IPNAME=localhost
      export JUP_PORT JUP_IPNAME
    %startscript
      PORT=""
      if [ -n "$JUP_PORT" ]; then
      PORT="--port=${JUP_PORT}"
      fi

      IPNAME=""
      if [ -n "$JUP_IPNAME" ]; then
      IPNAME="--ip=${JUP_IPNAME}"
      fi

      exec jupyter notebook --allow-root ${PORT} ${IPNAME}

    %setup
      #Create the .condarc file where the environments/channels from conda are specified, these are pulled with preference to root
      cd /
      touch .condarc

    %post
      echo 'export RANDOM=123456' >>$SINGULARITY_ENVIRONMENT
      #Installing all dependencies
      apt-get update && apt-get -y upgrade
      apt-get -y install \
      build-essential \
      wget \
      bzip2 \
      ca-certificates \
      libglib2.0-0 \
      libxext6 \
      libsm6 \
      libxrender1 \
      git
      rm -rf /var/lib/apt/lists/*
      apt-get clean
      #Installing Anaconda 2 and Conda 4.5.11
      wget -c https://repo.continuum.io/archive/Anaconda2-5.3.0-Linux-x86_64.sh
      /bin/bash Anaconda2-5.3.0-Linux-x86_64.sh -bfp /usr/local
      #Conda configuration of channels from .condarc file
      conda config --file /.condarc --add channels defaults
      conda config --file /.condarc --add channels conda-forge
      conda update conda
      #List installed environments
      conda list

Which is the definition file for the ``jupyter.sif`` container.

^^^^^^^^^^^^^^^
``--runscript``
^^^^^^^^^^^^^^^

This flag shows the runscript for the image.

.. code-block:: singularity

    $ singularity inspect --runscript jupyter.sif

And the output would look like:

.. code-block:: singularity

    #!/bin/sh
    OCI_ENTRYPOINT=""
    OCI_CMD="bash"
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

    exec $SINGULARITY_OCI_RUN

^^^^^^^^^^
``--test``
^^^^^^^^^^

This flag shows the test script for the image.

.. code-block:: singularity

    $ singularity inspect --test jupyter.sif

This will output the corresponding ``%test`` section from the definition file.

- ``--environment``

This flag shows the environment settings for the image. The respective environment variables set in ``%environment`` section ( So the ones in ``90-environment.sh`` ) and ``SINGULARITY_ENV`` variables set at runtime (that are located in``91-environment.sh``) will be printed out.

.. code-block:: singularity

    $ singularity inspect --environment jupyter.sif

And the output would look like:

.. code-block:: singularity

    ==90-environment.sh==
    #!/bin/sh

    JUP_PORT=8888
    JUP_IPNAME=localhost
    export JUP_PORT JUP_IPNAME

    ==91-environment.sh==
    export RANDOM=123456

As you can see, the ``JUP_PORT`` and ``JUP_IPNAME`` were previously defined in the ``%environment`` section of the defintion file,
while the RANDOM variable shown regards to the use of ``SINGULARITYENV_`` variables, so in this case ``SINGULARITYENV_RANDOM`` variable was set and exported at runtime.

^^^^^^^^^^^^^^
``--helpfile``
^^^^^^^^^^^^^^

This flag will show the container's description in the ``%help`` section of its definition file.

You can call it this way:

.. code-block:: singularity

    $ singularity inspect --helpfile jupyter.sif

And the output would look like:

.. code-block:: singularity

    Container with Anaconda 2 (Conda 4.5.11 Canary) and Jupyter Notebook 5.6.0 for Debian 9.x (Stretch).
    This installation is based on Python 2.7.15

- ``--json``

This flag gives you the possibility to output your labels in a JSON format.

You can call it this way:

.. code-block:: singularity

    $ singularity inspect --json jupyter.sif

And the output would look like:

.. code-block:: singularity

    {
	     "attributes": {
		     "labels": "{\n\t\"org.label-schema.build-date\": \"Friday_21_December_2018_0:49:50_CET\",\n\t\"org.label-schema.schema-version\": \"1.0\",\n\t\"org.label-schema.usage\": \"/.singularity.d/runscript.help\",\n\t\"org.label-schema.usage.singularity.deffile.bootstrap\": \"library\",\n\t\"org.label-schema.usage.singularity.deffile.from\": \"debian:9\",\n\t\"org.label-schema.usage.singularity.runscript.help\": \"/.singularity.d/runscript.help\",\n\t\"org.label-schema.usage.singularity.version\": \"3.0.1-236.g2453fdfe\"\n}"
	     },
	     "type": "container"
    }

------------------
Container Metadata
------------------

Inside of the container, metadata is stored in the ``/.singularity.d`` directory. You
probably shouldn’t edit any of these files directly but it may be
helpful to know where they are and what they do:

.. code-block:: singularity

    /.singularity.d/

    ├── actions
    │   ├── exec
    │   ├── run
    │   ├── shell
    │   ├── start
    │   └── test
    ├── env
    │   ├── 01-base.sh
    |   ├── 10-docker2singularity.sh
    │   ├── 90-environment.sh
    │   ├── 91-environment.sh
    |   ├── 94-appsbase.sh
    │   ├── 95-apps.sh
    │   └── 99-base.sh
    ├── labels.json
    ├── libs
    ├── runscript
    ├── runscript.help
    ├── Singularity
    └── startscript

-  **actions**: This directory contains helper scripts to allow the
   container to carry out the action commands. (e.g. ``exec`` , ``run`` or ``shell``)
   In later versions of Singularity, these files may be dynamically written at runtime.

-  **env**: All *.sh files in this directory are sourced in
   alpha-numeric order when the container is initiated. For legacy
   purposes there is a symbolic link called ``/environment`` that points to ``/.singularity.d/env/90-environment.sh``.

-  **labels.json**: The json file that stores a containers labels
   described above.

-  **libs**: At runtime the user may request some host-system libraries
   to be mapped into the container (with the ``--nv`` option for example). If so,
   this is their destination.

-  **runscript**: The commands in this file will be executed when the
   container is invoked with the ``run`` command or called as an executable. For
   legacy purposes there is a symbolic link called ``/singularity`` that points to this
   file.

-  **runscript.help**: Contains the description that was added in the ``%help`` section.

-  **Singularity**: This is the definition file that was used to generate
   the container. If more than 1 definition file was used to generate the
   container additional Singularity files will appear in numeric order
   in a sub-directory called ``bootstrap_history``.

-  **startscript**: The commands in this file will be executed when the
   container is invoked with the ``instance start`` command.
