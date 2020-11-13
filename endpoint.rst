================
Remote Endpoints
================

--------
Overview
--------

Sylabs introduced the online `Sylabs Cloud
<https://cloud.sylabs.io/home>`_ to enable users to `Create
<https://cloud.sylabs.io/builder>`_, `Secure
<https://cloud.sylabs.io/keystore?sign=true>`_, and `Share
<https://cloud.sylabs.io/library>`_ their container
images with others.

The ``remote`` command group in Singularity allows you to login to an
account on the public Sylabs Cloud, or configure Singularity to point
to a local installation of Singularity Enterprise, which provides an
on-premise private Container Library, Remote Builder and Key Store.

Users can setup and switch between multiple remote endpoints, which
are stored in their ``~/.singularity/remote.yaml``
file. Alternatively, remote endpoints can be set system-wide by an
administrator.

.. note::

   The ``remote`` command group configures Singularity to use
   and authenticate to the public Sylabs Cloud, a private installation
   of Singularity Enterprise, or community-developed services that are
   API compatible.

   The ``remote`` command group *cannot be used* to e.g. configure
   singularity to store credentials for access to a docker
   registry. See the :ref:`singularity-and-docker`
   guide for information about authenticating to various docker
   registries.

-------------------
Public Sylabs Cloud
-------------------

A fresh, default installation of Singularity is configured to connect
to the public `cloud.sylabs.io <https://cloud.sylabs.io>`__
services. If you only want to use the public services you just need to
obtain an authentication token, and then ``singularity remote login``:

  1) Go to: https://cloud.sylabs.io/
  2) Click "Sign In" and follow the sign in steps.
  3) Click on your login id (same and updated button as the Sign in one).
  4) Select "Access Tokens" from the drop down menu.
  5) Enter a name for your new access token, such as "test token"
  6) Click the "Create a New Access Token" button.
  7) Click "Copy token to Clipboard" from the "New API Token" page.
  8) Run ``singularity remote login`` and paste the access token at the prompt.

Once your token is stored, you can check that you are able to connect
to the services with the ``status`` subcommand:

.. code:: console

    $ singularity remote status
    INFO:    Checking status of default remote.
    SERVICE    STATUS  VERSION             URI
    Builder    OK      v1.1.14-0-gc7a68c1  https://build.sylabs.io
    Consent    OK      v1.0.2-0-g2a24b4a   https://auth.sylabs.io/consent
    Keyserver  OK      v1.13.0-0-g13c778b  https://keys.sylabs.io
    Library    OK      v1.0.16-0-gb7eeae4  https://library.sylabs.io
    Token      OK      v1.0.2-0-g2a24b4a   https://auth.sylabs.io/token
    INFO:    Access Token Verified!

    Valid authentication token set (logged in).

If you see any errors you may need to check if your system requires
proxy environment variables to be set, or if a firewall is blocking
access to ``*.sylabs.io``. Talk to your system administrator.

You can interact with the public Sylabs Cloud using various Singularity commands:

`pull <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_pull.html>`_,
`push <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_push.html>`_,
`build --remote <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_build.html#options>`_,
`key <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_key.html>`_,
`search <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_search.html>`_,
`verify <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_verify.html>`_,
`exec <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_exec.html>`_,
`shell <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_shell.html>`_,
`run <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_run.html>`_,
`instance <https://www.sylabs.io/guides/\{version\}/user-guide/cli/singularity_instance.html>`_

.. note::

   Using ``docker://``, ``oras://`` and ``shub://`` URIs with these commands
   does not interact with the Sylabs Cloud.

-------------------------
Managing Remote Endpoints
-------------------------

Generally, users and administrators should manage remote endpoints
using the ``singularity remote`` command, and avoid editing
``remote.yaml`` configuration files directly.

List and Login to Remotes
=========================

To ``list`` existing remote endpoints, run this:

.. code-block:: none

    $ singularity remote list

    Cloud Services Endpoints
    ========================

    NAME         URI              ACTIVE  GLOBAL  EXCLUSIVE
    SylabsCloud  cloud.sylabs.io  YES     YES     NO

    Keyservers
    ==========

    URI                     GLOBAL  INSECURE  ORDER
    https://keys.sylabs.io  YES     NO        1*


The ``YES`` in the ``ACTIVE`` column for ``SylabsCloud`` shows that
this is the current default remote endpoint.
   
To ``login`` to a remote, for the first time or if your token expires
or was revoked:

.. code-block:: console

    # Login to the default remote endpoint
    $ singularity remote login
                
    # Login to another remote endpoint                
    $ singularity remote login <remote_name>

    # example...
    $ singularity remote login SylabsCloud
    singularity remote login SylabsCloud
    INFO:    Authenticating with remote: SylabsCloud
    Generate an API Key at https://cloud.sylabs.io/auth/tokens, and paste here:
    API Key: 
    INFO:    API Key Verified!

    
If you ``login`` to a remote that you already have a valid token for,
you will be prompted, and the new token will be verified, before it
replaces your existing credential. If you enter an incorrect token
your existing token will not be replaced:

.. code-block:: console
   
    $ singularity remote login
    An access token is already set for this remote. Replace it? [N/y]y
    Generate an access token at https://cloud.sylabs.io/auth/tokens, and paste it here.
    Token entered will be hidden for security.
    Access Token: 
    FATAL:   while verifying token: error response from server: Invalid Credentials

    # Previous token is still in place
    
    
Add & Remove Remotes
====================

To ``add`` a remote endpoint (for the current user only):

.. code-block:: none

    $ singularity remote add <remote_name> <remote_uri>

For example, if you have an installation of Singularity enterprise
hosted at enterprise.example.com:

.. code-block:: none

    $ singularity remote add myremote https://enterprise.example.com
   
    INFO:    Remote "myremote" added.
    INFO:    Authenticating with remote: myremote
    Generate an API Key at https://enterprise.example.com/auth/tokens, and paste here:
    API Key:

You will be prompted to setup an API key as the remote is added. The
web address needed to do this will always be given.

To ``add`` a global remote endpoint (available to all users on the
system) an administrative user should run:

.. code-block:: none

    $ sudo singularity remote add --global <remote_name> <remote_uri>

    # example..

    $ sudo singularity remote add --global company-remote https://enterprise.example.com
    [sudo] password for dave: 
    INFO:    Remote "company-remote" added.
    INFO:    Global option detected. Will not automatically log into remote.
   
.. note:: Global remote configurations can only be modified by the
     root user and are stored in the ``etc/singularity/remote.yaml``
     file, at the Singularity installation location.

Conversely, to ``remove`` an endpoint:

.. code-block:: none

    $ singularity remote remove <remote_name>

Use the ``--global`` option as the root user to remove a global
endpoint:

.. code-block:: none

    $ sudo singularity remote remove --global <remote_name>


Set the Default Remote
======================
    
A remote endpoint can be set as the default to use with commands such
as ``push``, ``pull`` etc. via ``remote use``:

.. code-block:: none

    $ singularity remote use <remote_name>

The default remote shows up in ``[...]`` square brackets in the output of ``remote list``:

.. code-block:: none

    $ singularity remote list
    NAME            URI                     GLOBAL
    [SylabsCloud]   cloud.sylabs.io         YES
    company-remote  enterprise.example.com  YES
    myremote        enterprise.example.com  NO

    $ singularity remote use myremote
    INFO:    Remote "myremote" now in use.

    $ singularity remote list
    NAME            URI                     GLOBAL
    SylabsCloud     cloud.sylabs.io         YES
    company-remote  enterprise.example.com  YES
    [myremote]      enterprise.example.com  NO

    
If you do not want to switch remote with ``remote use`` you can:

* Make ``push`` and ``pull`` use an alternative library server with
  the ``--library`` option.
* Make ``build --remote`` use an alternative remote builder with the
  ``--builder`` option.
* Make ``keys`` use an alternative keyserver with the ``-url`` option.
