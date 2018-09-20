.. _reproducible-scif-apps:

=======================
Reproducible SCI-F Apps
=======================

.. _sec:scifapps:

---------------------
Why do we need SCI-F?
---------------------

The Scientific Filesystem (SCIF) provides a consistent and modular method to create containers.
The SCI-F makes some assumptions about how the container will be created. By adhering to with the SCI-F format containers can become more reproducible.
For example, installing a set of libraries, defining environment variables, or adding labels that
belong to application ``foo`` makes a strong assertion that those dependencies belong
to ``foo``. When I run ``foo``, I can be confident that the container is running
in this context, meaning with ``foo's`` custom environment, and with ``foo's`` libraries
and executables on the path. This approach is different from
serving many executables in a single container, that may have no way to know which application is associated with the container’s
intended functions. This documentation will walk through some
rationale, background, and examples of the SCI-F integration for
Singularity containers. For other examples (and a client that works
across container technologies) see the the `scientific filesystem <https://sci-f.github.io/>`_.

To start, let’s take a look at this series of steps to install
dependencies for software foo and bar.

.. code-block:: none

    %post


    # install dependencies 1

    # install software A (foo)

    # install software B (bar)

    # install software C (foo)

    # install software D (bar)


The creator may know that A and C were installed for ``foo`` and B and D for ``bar`` ,
but down the road, when someone discovers the container, if they can
find the software at all, the intention of the container creator would
be lost. As many are now, containers without any form of internal
organization and predictability are black boxes. We don’t know if some
software installed to ``/opt`` , or to  ``/usr/local/bin`` , or to their custom favorite folder ``/code`` . We
could assume that the creator added important software to the path and
look in these locations, but that approach is still akin to fishing in a
swamp. We might only hope that the container’s main function, the
Singularity runscript, is enough to make the container perform as
intended.

Mixed up Modules
================

| If your container truly runs one script, the traditional model of a
  runscript fits well. Even in the case of having two functions like ``foo`` and ``bar``
  you probably have something like this.

.. code-block:: none

    %runscript

    if some logic to choose foo:

       check arguments for foo

       run foo

    else if some logic to choose bar:

       run bar


and maybe your environment looks like this:

.. code-block:: none

    %environment

        BEST_GUY=foo

        export BEST_GUY


| but what if you run into this issue, with foo and bar?

.. code-block:: none

    %environment

        BEST_GUY=foo

        BEST_GUY=bar

        export BEST_GUY


You obviously can’t have them at separate times. You’d have to source
some custom environment file (that you make on your own) and it gets
confusing with issues of using shell and sourcing the container. We don’t know who
the best guy is! You probably get the general idea. Without consistent internal
organization and modularity the following may result:

-  You have to do a lot of manual work to expose the different software
   to the user via a custom runscript (and be a generally decent
   programmer).

-  All software must share the same metadata, environment, and labels.

Under these conditions, containers are at best black boxes with unclear
delineation between software provided, and only one context of running
anything. The container creator shouldn’t need to spend inordinate
amounts of time writing custom runscripts to support multiple functions
and inputs. Each of ``foo`` and ``bar`` should be easy to define, and have its own
runscript, environment, labels, tests and help section.

Container Transparency
======================

Applications that use the SCI-F make ``foo`` and ``bar`` transparent, and solve the problem of mixed up
modules. Our simple issue of mixed up modules could be solved if we
could do this:

.. code-block:: none

    Bootstrap:docker

    From: ubuntu:16.04


    %appenv foo

        BEST_GUY=foo

        export BEST_GUY


    %appenv bar

        BEST_GUY=bar

        export BEST_GUY


    %apprun foo

        echo The best guy is $BEST_GUY


    %apprun bar

        echo The best guy is $BEST_GUY


and generate the container as follows:

.. code-block:: none

    $ sudo singularity build foobar.simg Singularity

and finally, run the container with the context of ``foo`` and then ``bar``

.. code-block:: none

    $ singularity run --app bar foobar.simg

    The best guy is bar

    $ singularity run --app foo foobar.simg

    The best guy is foo


Using SCI-F apps, a user can easily discover both ``foo`` and ``bar`` without knowing
anything about the container:

.. code-block:: none

    singularity apps foobar.simg

    bar

    foo

Each applications can be inspected individually:

.. code-block:: none

    singularity inspect --app foo  foobar.simg

    {

        "SCIF_APP_NAME": "foo",

        "SCIF_APP_SIZE": "1MB"

    }

Container Modularity
====================

This behavior is made possible by a simple, clean organization that
is tied to a set of sections in the build recipe relevant to each app.
For example, I can specify custom install procedures (and they are
relevant to each app’s specific base defined under ``/scif/apps``), labels, tests, and
help sections. Before we examine the sections, consider what the organization looks like, for each app:

.. code-block:: none

    /scif/apps/


         foo/

            bin/

            lib/

            scif/

                runscript.help

                runscript

                env/

                    01-base.sh

                    90-environment.sh


         bar/

         ....

If you are familiar with Singularity, the above should look similar to other environments.
It mirrors the Singularity (main container) metadata folder, except
instead of ``.singularity.d`` we have ``scif``. The name and base ``scif`` is chosen intentionally to be
something short, and likely to be unique. On the level of organization
and metadata, these internal apps are like little containers.

You need to remember all the path details because you can environment variables in your runscripts,
etc. Here we are looking at the environment active for lolcat:

.. code-block:: none

    singularity exec --app foo foobar.simg env | grep foo

Consider the output of the above in sections, you will notice
some interesting things. First, notice that the app’s ``bin`` has been added to
the path, and its ``lib`` folder is added to the ``LD_LIBRARY_PATH`` . This means that anything you drop in
either will automatically be added. You don’t need to make these folders
either, they are created for you.

.. code-block:: none

    LD_LIBRARY_PATH=/scif/apps/foo/lib::/.singularity.d/libs

    PATH=/scif/apps/foo/bin:/scif/apps/foo:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

Next, notice the environment variables relevant to the active
app’s (foo) data and metadata. They will look like the following:

.. code-block:: none

    SCIF_APPOUTPUT=/scif/data/foo/output

    SCIF_APPDATA=/scif/data/foo

    SCIF_APPINPUT=/scif/data/foo/input

    SCIF_APPMETA=/scif/apps/foo/scif

    SCIF_APPROOT=/scif/apps/foo

    SCIF_APPNAME=foo

We also have foo’s environment variables defined under ``%appenv foo`` , and
importantly, we don’t see bar’s.

.. code-block:: none

    BEST_GUY=foo

Also provided are more global paths for data and apps:

.. code-block:: none

    SCIF_APPS=/scif/apps

    SCIF_DATA=/scif/data

Note, each application has its own modular location. When you do an ``%appinstall foo``,
the commands are all done in context of that base. The bin and lib are
also automatically generated. Consider a simple application:

Just add a script and name it:

.. code-block:: none

    %appfiles foo

        runfoo.sh   bin/runfoo.sh

and then maybe for install I’d make it executable

.. code-block:: none

    %appinstall foo

        chmod u+x bin/runfoo.sh

You don’t even need files! You could just do this.

.. code-block:: none

    %appinstall foo

        echo 'echo "Hello Foo."' >> bin/runfoo.sh

        chmod u+x bin/runfoo.sh

We can summarize these observations about using apps:

-  the specific environment (``%appenv_foo``) is active because ``BEST_APP`` is foo

-  the lib folder in foo’s base is added to the LD\_LIBRARY\_PATH

-  the bin folder is added to the path

-  locations for input, output, and general data are exposed. It’s up to
   you how you use these, but you can predictably know that a well made
   application will look for inputs and outputs in its specific folder.

-  environment variables are provided for the app’s root, its data, and
   its name

Sections
========

Finding the section ``%appinstall`` , ``%apphelp`` , or ``%apprun`` is indication of an application command.
The following string is parsed as the name of the application, and
this folder is created, in lowercase, under ``/scif/apps`` if it doesn’t exist. A
singularity metadata folder, .singularity.d, equivalent to the
container’s main folder, is generated inside the application. An
application thus is like a smaller image inside of its parent.
Specifically, SCI-F defines the following new sections for the build
recipe, where each is optional for zero or more apps:

**%appinstall** corresponds to executing commands within the folder to
install the application. These commands would previously belong in
%post, but are now attributable to the application.

**%apphelp** is written as a file called runscript.help in the
application’s metadata folder, where the Singularity software knows
where to find it. If no help section is provided, the software simply
will alert the user and show the files provided for inspection.

**%apprun** is also written as a file called runscript.exec in the
application’s metadata folder, and again looked for when the user asks
to run the software. If not found, the container should default to
shelling into that location.

**%applabels** will write a labels.json in the application’s metadata
folder, allowing for application specific labels.

**%appenv** will write an environment file in the application’s base
folder, allowing for definition of application specific environment
variables.

**%apptest** will run tests specific to the application, with present
working directory assumed to be the software module’s folder

**%appfiles** will add files to the app’s base at ``/scif/apps/<app>``

Interaction
===========

The complete output of a ``grep`` to the environment when
running foo in the first example was not shown because the remainder of variables
are more germane to a discussion about app interaction. Essentially, when
any application is active, we also have named variable that can explicitly
reference the environment file, labels file, runscript, ``lib`` and ``bin`` folders for
all app’s in the container. For our above Singularity Recipe, we would
also find:

.. code-block:: none

    SCIF_APPDATA_bar=/scif/data/bar

    SCIF_APPRUN_bar=/scif/apps/bar/scif/runscript

    SCIF_APPROOT_bar=/scif/apps/bar

    SCIF_APPLIB_bar=/scif/apps/bar/lib

    SCIF_APPMETA_bar=/scif/apps/bar/scif

    SCIF_APPBIN_bar=/scif/apps/bar/bin

    SCIF_APPENV_bar=/scif/apps/bar/scif/env/90-environment.sh

    SCIF_APPLABELS_bar=/scif/apps/bar/scif/labels.json


    SCIF_APPENV_foo=/scif/apps/foo/scif/env/90-environment.sh

    SCIF_APPLABELS_foo=/scif/apps/foo/scif/labels.json

    SCIF_APPDATA_foo=/scif/data/foo

    SCIF_APPRUN_foo=/scif/apps/foo/scif/runscript

    SCIF_APPROOT_foo=/scif/apps/foo

    SCIF_APPLIB_foo=/scif/apps/foo/lib

    SCIF_APPMETA_foo=/scif/apps/foo/scif

    SCIF_APPBIN_foo=/scif/apps/foo/bin


This design means that we can have apps interact with one another internally. For example, let’s modify the recipe a bit:

.. code-block:: none

    Bootstrap:docker

    From: ubuntu:16.04


    %appenv cow

        ANIMAL=COW

        NOISE=moo

        export ANIMAL NOISE


    %appenv bird

        NOISE=tweet

        ANIMAL=BIRD

        export ANIMAL


    %apprun moo

        echo The ${ANIMAL} goes ${NOISE}


    %appenv moo

        . ${APPENV_cow}


In the above example, we have three apps. One for a cow, one for a bird,
and a third that depends on the cow. We can’t define global functions or
environment variables (in ``%post`` or  ``/environment`` , respectively) because they would
interfere with the third app, bird, that has equivalently named
variables. What we do then, is source the environment for “cow” in the
environment for “moo” and the result is what we would want:

.. code-block:: none

    $ singularity run --app moo /tmp/one.simg

    The COW goes moo

The same is true for each of the labels, environment, runscript, bin,
and lib. The following variables are available to you, for each application in
the container, whenever any application is run:

-  **SCIF\_APPBIN\_**: the path to the bin folder, if you want to add
   an application that isn’t active to your ``PATH``

-  **SCIF\_APPLIB\_**: the path to the lib folder, if you want to add
   an application that isn’t active to your ``LD\_LIBRARY\_PATH``

-  **SCIF\_APPRUN\_**: the application’s runscript (so you can call it from
   elsewhere)

-  **SCIF\_APPMETA\_**: the path to the metadata folder for the application

-  **SCIF\_APPENV\_**: the path to the primary environment file (for
   sourcing) if it exists

-  **SCIF\_APPROOT\_**: the application’s install folder

-  **SCIF\_APPDATA\_**: the application’s data folder

-  **SCIF\_APPLABELS\_**: The path to the label.json in the metadata
   folder, if it exists

Singularity containers are already reproducible in that they package
dependencies. The basic format of SCI-F adds to that by making the software
inside of containers modular, predictable, and programmatically accessible.

By pre-setting some set of steps, labels, or variables in the
runscript is associated with a particular action of the container, users can better encapsulate how dependencies relate to each step in a scientific
work-flow.

Making containers can be challenging. When a scientist starts to
write a recipe for his set of tools, she probably doesn’t know where to
put various tags and data. The SCI-F file system makes it easy to build consistent maintainable containers.

-------------------------------
SCI-F Example: Cowsay Container
-------------------------------

As an example, we will use the `cowsay container`_. ``cowsay`` is a program that generates ASCII pictures of a cow with a message.
It also uses the ``fortune```program to produce random "fortunes" and the ``lolcat`` applications that add rainbow color to an ASCII string.

.. warning::
    **Important!** This example has been developed for Singularity 2.4.

Download the recipe, and save it to your
present working directory.

.. code-block:: none

    wget https://raw.githubusercontent.com/sylabs/singularity/master/examples/apps/Singularity.cowsay

    sudo singularity build moo.simg Singularity.cowsay

Determine what applications are installed using the following command:

.. code-block:: none

    singularity apps moo.simg

    cowsay

    fortune

    lolcat


Ask for help for a specific application as follows:

.. code-block:: none

    singularity help --app fortune moo.simg

    fortune is the best app


A simple loop can be used to ask for help from all apps (without asking in advance what they are):

.. code-block:: none

    for app in $(singularity apps moo.simg)

       do

         singularity help --app $app moo.simg

    done

    cowsay is the best app

    fortune is the best app

    lolcat is the best app


To run the ``fortune`` application, enter the following (the actual fortune is random, so your display may differ):

.. code-block:: none

    singularity run --app fortune moo.simg

        My dear People.

        My dear Bagginses and Boffins, and my dear Tooks and Brandybucks,

    and Grubbs, and Chubbs, and Burrowses, and Hornblowers, and Bolgers,

    Bracegirdles, Goodbodies, Brockhouses and Proudfoots.  Also my good

    Sackville Bagginses that I welcome back at last to Bag End.  Today is my

    one hundred and eleventh birthday: I am eleventy-one today!"

            -- J. R. R. Tolkien


Next, pipe the output of ``fortune`` into ``lolcat`` to add color to the fortune.

.. code-block:: none

    singularity run --app fortune moo.simg | singularity run --app lolcat moo.simg

    You will be surrounded by luxury.


Send the output of ``fortune```to the ``cowsay`` application.

.. code-block:: none

    singularity run --app fortune moo.simg | singularity run --app cowsay moo.simg

     ________________________________________

    / Executive ability is prominent in your \

    \ make-up.                               /

     ----------------------------------------

            \   ^__^

             \  (oo)\_______

                (__)\       )\/\

                    ||----w |

                    ||     ||


Finally use all three applications and demonstrate how to use an environment variable for the command:

.. code-block:: none

    CMD="singularity run --app"

    $CMD fortune moo.simg | $CMD cowsay moo.simg | $CMD lolcat moo.simg

     _________________________________________

    / Ships are safe in harbor, but they were \

    \ never meant to stay there.              /

     -----------------------------------------

            \   ^__^

             \  (oo)\_______

                (__)\       )\/\

                    ||----w |

                    ||     ||


The application can be inspected with the following command:

.. code-block:: none

    singularity inspect --app fortune moo.simg

    {

        "SCIF_APP_NAME": "fortune",

        "SCIF_APP_SIZE": "1MB"

    }


If you want to see the full specification or create your own
Scientific Filesystem integration (doesn’t have to be Singularity, or
Docker, or containers!) see the `full documentation <https://sci-f.github.io/>`_.

Also, you can follow along with this example by going to: `take a look at these examples <https://asciinema.org/a/139153?speed=3>`_
