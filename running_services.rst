.. _running_services:

================
Running Services
================

There are :ref:`different ways <runcontainer>`  in which you can run Singularity containers. If you used commands like `run`,
`exec` and `shell` to interact with processes in the container, that's running  Singularity containers in the
foreground. Singularity, also lets you run containers in a "detached" or "deamon" mode which can run different services
in the background. A 'service' is essentially a software functionality with a purpose that different clients can reuse for
different purposes. For example, if you wanted to run services like a web server or a database in a Singularity container in the background,
container instances are used in such cases. A container instance, simply put, is a persistent and isolated version of the container image that runs
in the background.

------------------------
Overview
------------------------

.. _sec:instances:

Singularity 2.4v introduced the ability to run "Container instances" allowing users to run services using Singularity.
This page will help you understand `instances` with the help of an elementary example followed by running Nginx web server using instances.
In the end, you will find a very useful example of running an instance of API that converts URL to PDFs.

Let's understand the importance of Singularity instances before we start operating on them.
Suppose you want to run an nginx web server, you can simply install nginx and start the service by:

.. code-block:: singularity

    $ apt-get update && apt-get install -y nginx
    $ service nginx start

With older versions of Singularity, if you were to do something like
this, from inside the container you would happily see the service
start, and the web server running! But then if you were to log out of
the container what would happen?
Orphan process within unreachable namespaces!
You would lose control of the process. It would still be running, but
you couldn’t easily kill or interface with it. This is a called an
orphan process. Singularity versions 2.4 and later can handle running services
properly.

----------------------------------
Container Instances in Singularity
----------------------------------

For demonstration, let's use an easy example of :ref:`lolcow_latest.sif<cowimage>` image that we
previously built.

To start an instance, you should follow this structure:

.. code-block:: singularity

          [command]                 [image]             [name of instance]

    $ singularity instance start   lolcow_latest.sif     cow1

When you run that command, Singularity creates an isolated environment
for the container instances’ processes/services to live inside. We can
confirm that this command started an instance by running the
``instance list`` command like so:

.. code-block:: singularity

    $ singularity instance list

    INSTANCE NAME    PID      IMAGE
    cow1             7388     /home/sushma/lolcow_latest.sif

.. note::
    The instances are linked with your user. So make sure to run ALL the instance
    commands either with or without the ``sudo`` privilege.
    If you ``start`` an instance with sudo and then ``list`` it without sudo, it
    might not be able to locate the instance.

If you want to run multiple instances from the same image, it’s as simple
as running the command multiple times with different instance names.
The instance names uniquely identifies an instance, so they cannot be
repeated.

.. code-block:: singularity

      $ singularity instance start   lolcow_latest.sif  cow2
      $ singularity instance start   lolcow_latest.sif  cow3

And again to confirm that the instances are running as we expected:

.. code-block:: singularity

    $ singularity instance list

    INSTANCE NAME    PID      IMAGE
    cow1             16519    /home/sushma/lolcow_latest.sif
    cow2             16576    /home/sushma/lolcow_latest.sif
    cow3             16618    /home/sushma/lolcow_latest.sif

You can use the ``singularity run/exec`` commands on instances:

.. code-block:: singularity

    $ singularity run instance://cow1
    $ singularity exec instance://cow1 cowsay moo

When using ``run`` with an instance URI, the ``runscript`` will be executed
inside of the instance. Similarly with ``exec``, it will execute the given
command in the instance.

If you want to poke around inside of your instance, you can do a normal
``singularity shell`` command, but give it the instance URI:

.. code-block:: singularity

    $ singularity shell instance://cow1
    Singularity lolcow_latest.sif:~>

When you are finished with your instance you can clean it up with the
``instance stop`` command as follows:

.. code-block:: singularity

    $ singularity instance stop cow1

If you have multiple instances running and you want to stop all of
them, you can do so with a wildcard or the -a flag:

.. code-block:: singularity

    $ singularity instance stop \*
    or
    $ singularity instance stop -a
    or
    $ singularity instance stop --all

.. note::
    Note that you must escape the wildcard with a backslash like this ``\*`` to
    pass it properly.

----------------------------------
Nginx “Hello-world” in Singularity
----------------------------------

The above example, although ineffectual, should have fairly introduced the concept of Singularity instances and
running services in the background. The following illustrates a more
functional example of setting up a sample nginx web server using instances in
Singularity. First we will just create a basic :ref:`definition file <definition-files>` (let's call it nginx.def):

.. code-block:: singularity

    Bootstrap: docker
    From: nginx
    Includecmd: no

    %startscript
       nginx


All this does is, download the official nginx Docker container, convert
it to a Singularity image, and tell it to run nginx when you start the
instance. Since we’re running a web server, we’re going to run the
following commands as root.

.. code-block:: singularity

    $ singularity build nginx.sif nginx.def
    $ sudo singularity instance start --writable-tmpfs ng.sif web

.. note::
    The above ``start`` command requires `sudo` because the "user" directive runs processes only
    with super user privileges. Also, to let the instance write temporary files during execution, you should use
    `--writable-tmpfs` while starting the instance.

Just like that we’ve downloaded, built, and run an nginx Singularity
image. And to confirm that it’s correctly running:

.. code-block:: singularity

    $ curl localhost

    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
     body {
         width: 35em;
         margin: 0 auto;
         font-family: Tahoma, Verdana, Arial, sans-serif;
     }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support please refer to
    <a href="http://nginx.org/">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="http://nginx.com/">nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>


Visit localhost on your browser, you should see a Welcome message!

--------------------
Putting all together
--------------------

In this section, we will demonstrate an example of packaging a service
into a container and running it. The service we will be packaging is an
API server that converts a web page into a PDF, and can be found
`here <https://github.com/alvarcarto/url-to-pdf-api>`__.
You can build the image by following below described steps or if you wish to
just download the final image directly from Container Library, simply run
``singularity pull library://sylabs/doc-examples/url-to-pdf:latest``.

Building the image
==================

This section will describe the requirements for creating definition file(url-pdf.def)
which will be used to the conatiner image. To begin, when looking at the GitHub
page of the ``url-to-pdf-api``, we can see that it is a Node 8 server that uses
headless Chromium called `Puppeteer <https://github.com/GoogleChrome/puppeteer>`_.
Let’s first choose a base from which to build our container, in this case I used
the docker image ``node:8`` which comes pre-installed with Node 8:

.. code-block:: singularity

    Bootstrap: docker
    From: node:8
    Includecmd: no


| Puppeteer also requires a few dependencies to be manually installed in
  addition to Node 8, so we can add those into the ``post`` section as well as
  the installation script for the ``url-to-pdf``:

.. code-block:: singularity

    %post

        apt-get update && apt-get install -yq gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3
        libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0
        libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6     libxfixes3
        libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release
        xdg-utils wget curl && rm -r /var/lib/apt/lists/*
        git clone https://github.com/alvarcarto/url-to-pdf-api.git pdf_server
        cd pdf_server
        npm install
        chmod -R 0755 .

And now we need to define what happens when we start an instance of the
container. In this situation, we want to run the commands that starts up
the url-to-pdf server:

.. code-block:: singularity

    %startscript
        cd /pdf_server
        # Use nohup and /dev/null to completely detach server process from terminal
        nohup npm start > /dev/null 2>&1 < /dev/null &


Also, the ``url-to-pdf`` server requires ``environment`` some variables be set, which we can do in the
environment section:

.. code-block:: singularity

    %environment
        NODE_ENV=development
        PORT=9000
        ALLOW_HTTP=true
        URL=localhost
        export NODE_ENV PORT ALLOW_HTTP URL

.. code-block:: singularity

    $ sudo singularity build url-pdf.sif url-pdf.def


Running the Server
==================

Now that we have an image, we are ready to start an instance and run the
server:

.. code-block:: singularity

    $ sudo singularity instance start url-pdf.sif pdf

.. note::
    If there occurs an error related to port connection being refused while starting
    the instance or while using it later, you can try mentioning different port
    numbers in the definition file above.

We can confirm it’s working by sending the server an http request using
curl:

.. code-block:: singularity

    $ curl -o sylabs.pdf localhost:9000/api/render?url=http://sylabs.io/docs

    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                             Dload  Upload   Total   Spent    Left  Speed

    100 73750  100 73750    0     0  14583      0  0:00:05  0:00:05 --:--:-- 19130
    
You should see a PDDF file file being generated like the one below:

.. image:: /home/sushma/Pictures/docpage.png
   :alt: Screenshot of the PDF generated


If you shell into the instance, you can see the running processes:

.. code-block:: singularity

    $ sudo singularity shell instance://pdf
    Singularity: Invoking an interactive shell within container...

    Singularity final.sif:/home/sushma> ps auxf
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root       461  0.0  0.0  18204  3188 pts/1    S    17:58   0:00 /bin/bash --norc
    root       468  0.0  0.0  36640  2880 pts/1    R+   17:59   0:00  \_ ps auxf
    root         1  0.0  0.1 565392 12144 ?        Sl   15:10   0:00 sinit
    root        16  0.0  0.4 1113904 39492 ?       Sl   15:10   0:00 npm
    root        26  0.0  0.0   4296   752 ?        S    15:10   0:00  \_ sh -c nodemon --watch ./src -e js src/index.js
    root        27  0.0  0.5 1179476 40312 ?       Sl   15:10   0:00      \_ node /pdf_server/node_modules/.bin/nodemon --watch ./src -e js src/index.js
    root        39  0.0  0.7 936444 61220 ?        Sl   15:10   0:02          \_ /usr/local/bin/node src/index.js

    Singularity final.sif:/home/sushma> exit


Making it Pretty
================

Now that we have confirmation that the server is working, let’s make
it a little cleaner. It’s difficult to remember the exact curl command
and URL syntax each time you want to request a PDF, so let’s automate
that. To do that, we’re going to be using Standard Container
Integration Format (SCIF) apps, which are integrated directly into
singularity. If you haven’t already, check out the `Singularity app documentation <https://sci-f.github.io/>`_
to come up to speed.

First off, we’re going to move the installation of the url-pdf
into an app, so that there is a designated spot to place output files.
To do that, we want to add a section to our definition file to build
the server:

.. code-block:: singularity

    %appinstall pdf_server
        git clone https://github.com/alvarcarto/url-to-pdf-api.git pdf_server
        cd pdf_server
        npm install
        chmod -R 0755 .


And update our ``startscript`` to point to the app location:

.. code-block:: singularity

    %startscript
        cd "${APPROOT_pdf_server}/pdf_server"
        # Use nohup and /dev/null to completely detach server process from terminal
        nohup npm start > /dev/null 2>&1 < /dev/null &


Now we want to define the pdf_client app, which we will run to send the
requests to the server:

.. code-block:: singularity

    %apprun pdf_client
        if [ -z "${1:-}" ]; then
            echo "Usage: singularity run --app pdf <instance://name> <URL> [output file]"
            exit 1

        fi
        curl -o "${SINGULARITY_APPDATA}/output/${2:-output.pdf}" "${URL}:${PORT}/api/render?url=${1}"


As you can see, the ``pdf_client`` app checks to make sure that the user provides at
least one argument. Now that we have an output directory in the
container, we need to expose it to the host using a bind mount. Once
we’ve rebuilt the container, make a new directory called ``out`` for the
generated PDF’s to go. Now we simply start the instance like so:

.. code-block:: singularity

    $ singularity instance start -B out/:/scif/data/pdf_client/output/ url-to-pdf-api.img pdf

And to request a pdf simply do:

.. code-block:: singularity

    $ singularity run --app pdf_client instance://pdf http://google.com google.pdf

And to confirm that it worked:

.. code-block:: singularity

    $ ls out/
    google.pdf

When you are finished, use the instance stop command to close all
running instances.

.. code-block:: singularity

    $ singularity instance stop \*

---------------
Important Notes
---------------

.. note::
    If the service you want to run in your instance requires a bind mount,
    then you must pass the ``-B`` option when calling ``instance start``. For example, if you wish to
    capture the output of the ``web`` container instance which is placed at ``/output/`` inside
    the container you could do:

    .. code-block:: singularity

        $ singularity instance start -B output/dir/outside/:/output/ nginx.sif  web
