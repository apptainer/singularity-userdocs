.. _running_services:

================
Running Services
================

There are :ref:`different ways <runcontainer>`  in which you can run Singularity
containers. If you use commands like ``run``, ``exec`` and ``shell`` to
interact with processes in the container, you are running Singularity containers
in the foreground. Singularity, also lets you run containers in a "detached" or
"daemon" mode which can run different services in the background. A 'service' is
essentially a process running in the background that multiple different clients
can use. For example, a web server or a database. To run services in a
Singularity container one should use *instances*. A container instance is a
persistent and isolated version of the container image that runs in the
background.

------------------------
Overview
------------------------

.. _sec:instances:

Singularity v2.4 introduced the concept of *instances* allowing users to run
services in Singularity. This page will help you understand instances using an
elementary example followed by a more useful example running an NGINX web server
using instances. In the end, you will find a more detailed example of running an
instance of an API that converts URL to PDFs.

To begin with, suppose you want to run an NGINX web server outside of a
container. You can simply install NGINX and start the service by:

.. code-block:: singularity

    $ sudo apt-get update && sudo apt-get install -y nginx
    $ service nginx start

If you were to do something like this from within a container you would also see
the service start, and the web server running. But then if you were to exit the
container, the process would continue to run within an unreachable mount
namespace. The process would still be running, but you couldn't easily kill or
interface with it. This is a called an orphan process. Singularity instances
give you the ability to handle services properly.

----------------------------------
Container Instances in Singularity
----------------------------------

For demonstration, let's use an easy (though somewhat useless) example of
`alpine_latest.sif <https://cloud.sylabs.io/library/_container/5baba5e594feb900016ea41c>`_
image from the container library:

.. code-block:: singularity

    $ singularity pull library://alpine

To start an instance, you should follow this procedure :

.. code-block:: singularity

    [command]                      [image]              [name of instance]

    $ singularity instance start   alpine_latest.sif     instance1

This command causes Singularity to create an isolated environment for the
container services to live inside. One can confirm that an instance is running
by using the ``instance list`` command like so:

.. code-block:: singularity

    $ singularity instance list

    INSTANCE NAME    PID      IMAGE
    instance1        12715    /home/ysub/alpine_latest.sif

.. note::
    The instances are linked with your user. So make sure to run *all* the
    instance commands either with or without the ``sudo`` privilege. If you
    ``start`` an instance with sudo and then you must ``list`` it with sudo, as
    well or you will not be able to locate the instance.

If you want to run multiple instances from the same image, it’s as simple as
running the command multiple times with different instance names. The instance
name uniquely identify instances, so they cannot be repeated.

.. code-block:: singularity

      $ singularity instance start alpine_latest.sif instance2
      $ singularity instance start alpine_latest.sif instance3

And again to confirm that the instances are running as we expected:

.. code-block:: singularity

    $ singularity instance list

    INSTANCE NAME    PID      IMAGE
    instance1        12715    /home/ysub/alpine_latest.sif
    instance2        12795    /home/ysub/alpine_latest.sif
    instance3        12837    /home/ysub/alpine_latest.sif

You can use the ``singularity run/exec`` commands on instances:

.. code-block:: singularity

    $ singularity run instance://instance1
    $ singularity exec instance://instance2 cat /etc/os-release

When using ``run`` with an instance URI, the ``runscript`` will be executed
inside of the instance. Similarly with ``exec``, it will execute the given
command in the instance.

If you want to poke around inside of your instance, you can do a normal
``singularity shell`` command, but give it the instance URI:

.. code-block:: singularity

    $ singularity shell instance://instance3
    Singularity>

When you are finished with your instance you can clean it up with the
``instance stop`` command as follows:

.. code-block:: singularity

    $ singularity instance stop instance1

If you have multiple instances running and you want to stop all of them, you can
do so with a wildcard or the -a flag:

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

The above example, although not very useful, should serve as a fair introduction
to the concept of Singularity instances and running services in the background.
The following illustrates a more useful example of setting up a sample NGINX web
server using instances. First we will create a basic
:ref:`definition file <definition-files>` (let's call it nginx.def):

.. code-block:: singularity

    Bootstrap: docker
    From: nginx
    Includecmd: no

    %startscript
       nginx


This downloads the official NGINX Docker container, converts it to a Singularity
image, and tells it to run NGINX when you start the instance. Since we’re
running a web server, we’re going to run the following commands as root.

.. code-block:: singularity

    $ sudo singularity build nginx.sif nginx.def
    $ sudo singularity instance start --writable-tmpfs nginx.sif web

.. note::
    The above ``start`` command requires `sudo` because we are running a web
    server. Also, to let the instance write temporary files during execution,
    you should use `--writable-tmpfs` while starting the instance.

Just like that we’ve downloaded, built, and run an NGINX Singularity
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

In this section, we will demonstrate an example of packaging a service into a
container and running it. The service we will be packaging is an API server that
converts a web page into a PDF, and can be found `here
<https://github.com/alvarcarto/url-to-pdf-api>`__. You can build the image by
following the steps described below or you can just download the final image
directly from Container Library, simply run
``singularity pull library://sylabs/doc-examples/url-to-pdf:latest``.

Building the image
==================

This section will describe the requirements for creating the definition file
(url-to-pdf.def) that will be used to build the container image.
``url-to-pdf-api`` is based on a Node 8 server that uses a headless version of
Chromium called `Puppeteer <https://github.com/GoogleChrome/puppeteer>`_.
Let’s first choose a base from which to build our container, in this case the
docker image ``node:8`` which comes pre-installed with Node 8 has been used:

.. code-block:: singularity

    Bootstrap: docker
    From: node:8
    Includecmd: no


Puppeteer also requires a few dependencies to be manually installed in addition
to Node 8, so we can add those into the ``post`` section as well as the
installation script for the ``url-to-pdf``:

.. code-block:: singularity

    %post

        apt-get update && apt-get install -yq gconf-service libasound2 \
            libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 \
            libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 \
            libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 \
            libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
            libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
            libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates \
            fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils \
            wget curl && rm -r /var/lib/apt/lists/*
        git clone https://github.com/alvarcarto/url-to-pdf-api.git pdf_server
        cd pdf_server
        npm install
        chmod -R 0755 .

And now we need to define what happens when we start an instance of the
container. In this situation, we want to run the commands that starts up the
url-to-pdf service:

.. code-block:: singularity

    %startscript
        cd /pdf_server
        # Use nohup and /dev/null to completely detach server process from terminal
        nohup npm start > /dev/null 2>&1 < /dev/null &


Also, the ``url-to-pdf`` service requires some environment variables to be set,
which we can do in the environment section:

.. code-block:: singularity

    %environment
        NODE_ENV=development
        PORT=9000
        ALLOW_HTTP=true
        URL=localhost
        export NODE_ENV PORT ALLOW_HTTP URL

.. code-block:: singularity

    $ sudo singularity build url-to-pdf.sif url-to-pdf.def


Running the Service
==================

We can now start an instance and run the service:

.. code-block:: singularity

    $ sudo singularity instance start url-to-pdf.sif pdf

.. note::
    If there occurs an error related to port connection being refused while
    starting the instance or while using it later, you can try specifying
    different port numbers in the definition file above.

We can confirm it’s working by sending the server an http request using
curl:

.. code-block:: singularity

    $ curl -o sylabs.pdf localhost:9000/api/render?url=http://sylabs.io/docs

    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                             Dload  Upload   Total   Spent    Left  Speed

    100 73750  100 73750    0     0  14583      0  0:00:05  0:00:05 --:--:-- 19130

You should see a PDF file being generated like the one shown below:

.. image:: docpage.png
    :alt: Screenshot of the PDF generated!


If you shell into the instance, you can see the running processes:

.. code-block:: singularity

    $ sudo singularity shell instance://pdf
    Singularity: Invoking an interactive shell within container...

    Singularity final.sif:/home/ysub> ps auxf
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root       461  0.0  0.0  18204  3188 pts/1    S    17:58   0:00 /bin/bash --norc
    root       468  0.0  0.0  36640  2880 pts/1    R+   17:59   0:00  \_ ps auxf
    root         1  0.0  0.1 565392 12144 ?        Sl   15:10   0:00 sinit
    root        16  0.0  0.4 1113904 39492 ?       Sl   15:10   0:00 npm
    root        26  0.0  0.0   4296   752 ?        S    15:10   0:00  \_ sh -c nodemon --watch ./src -e js src/index.js
    root        27  0.0  0.5 1179476 40312 ?       Sl   15:10   0:00      \_ node /pdf_server/node_modules/.bin/nodemon --watch ./src -e js src/index.js
    root        39  0.0  0.7 936444 61220 ?        Sl   15:10   0:02          \_ /usr/local/bin/node src/index.js

    Singularity final.sif:/home/ysub> exit


Making it Pretty
================

Now that we have confirmation that the server is working, let’s make it a little
cleaner. It’s difficult to remember the exact ``curl`` command and URL syntax
each time you want to request a PDF, so let’s automate it. To do that, we can
use Standard Container Integration Format (SCIF) apps, that are integrated
directly into singularity. If you haven’t already, check out the `Scientific
Filesystem documentation <https://sci-f.github.io/>`_ to come up to speed.

First off, we’re going to move the installation of the url-to-pdf into an app,
so that there is a designated spot to place output files. To do that, we want to
add a section to our definition file to build the server:

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


Now we want to define the pdf_client app, which we will run to send the requests
to the server:

.. code-block:: singularity

    %apprun pdf_client
        if [ -z "${1:-}" ]; then
            echo "Usage: singularity run --app pdf <instance://name> <URL> [output file]"
            exit 1

        fi
        curl -o "${SINGULARITY_APPDATA}/output/${2:-output.pdf}" "${URL}:${PORT}/api/render?url=${1}"


As you can see, the ``pdf_client`` app checks to make sure that the user
provides at least one argument. Now that we have an output directory in the
container, we need to expose it to the host using a bind mount. Once we’ve
rebuilt the container, make a new directory called ``out`` for the generated
PDFs to go. After building the image from the edited definition file we simply
start the instance:

.. code-block:: singularity

    $ singularity instance start -B out/:/scif/data/pdf_client/output/ url-to-pdf.sif pdf

To request a pdf simply do:

.. code-block:: singularity

    $ singularity run --app pdf_client instance://pdf http://sylabs.io/docs sylabs.pdf

To confirm that it worked:

.. code-block:: singularity

    $ ls out/
    sylabs.pdf

When you are finished, use the instance stop command to close all running
instances.

.. code-block:: singularity

    $ singularity instance stop \*

.. note::
    If the service you want to run in your instance requires a bind mount,
    then you must pass the ``-B`` option when calling ``instance start``. For
    example, if you wish to capture the output of the ``web`` container instance
    which is placed at ``/output/`` inside the container you could do:

    .. code-block:: singularity

        $ singularity instance start -B output/dir/outside/:/output/ nginx.sif  web
