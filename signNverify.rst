.. _signNverify:

================================
Signing and Verifying Containers
================================

.. _sec:signNverify:

Singularity 3.0 introduces the abilities to create and manage PGP keys and use
them to sign and verify containers. This provides a trusted method for
Singularity users to share containers. It ensures a bit-for-bit reproduction
of the original container as the author intended it.

-----------------------------------------------
Verifying containers from the Container Library
-----------------------------------------------

The ``verify`` command will allow you to verify that a container has been
signed using a PGP key. To use this feature with images that you pull from the
container library, you must first generate an access token to the Sylabs Cloud.
If you don't already have a valid access token, follow these steps:

  1) Go to : https://cloud.sylabs.io/
  2) Click "Sign in to Sylabs" and follow the sign in steps.
  3) Click on your login id (same and updated button as the Sign in one).
  4) Select "Access Tokens" from the drop down menu.
  5) Click the "Manage my API tokens" button from the "Account Management" page.
  6) Click "Create".
  7) Click "Copy token to Clipboard" from the "New API Token" page.
  8) Paste the token string into your ``~/.singularity/sylabs-token`` file.

Now you can verify containers that you pull from the library, ensuring they are
bit-for-bit reproductions of the original image.

.. code-block:: none

    $ singularity pull library://alpine

    $ singularity verify alpine_latest.sif
    Verifying image: alpine_latest.sif
    Data integrity checked, authentic and signed by:
    	Sylabs Admin <support@sylabs.io>, KeyID 51BE5020C508C7E9

In this example you can see that **Sylabs Admin** has signed the container.

---------------------------
Signing your own containers
---------------------------

Generating and managing PGP keys
================================

To sign your own containers you first need to generate one or more keys.

If you attempt to sign a container before you have generated any keys,
Singularity will guide you through the interactive process of creating a new
key. Or you can use the ``newpair`` subcommand in the ``key`` command group
like so:.

.. code-block:: none

    $ singularity keys newpair
    Enter your name (e.g., John Doe) : Dave Godlove
    Enter your email address (e.g., john.doe@example.com) : d@sylabs.io
    Enter optional comment (e.g., development keys) : demo
    Generating Entity and OpenPGP Key Pair... Done
    Enter encryption passphrase :

The ``list`` subcommand will show you all of the keys you have created or saved
locally.`

.. code-block:: none

    $ singularity keys list
    Public key listing (/home/david/.singularity/sypgp/pgp-public):

    0) U: Dave Godlove (demo) <d@sylabs.io>
       C: 2018-10-08 15:25:30 -0400 EDT
       F: 135E426D67D8416DE1D6AC7FFED5BBA38EE0DC4A
       L: 4096
       --------

In the output above, the letters stand for the following:

       - U: User
       - C: Creation date and time
       - F: Fingerprint
       - L: Key length

After generating your key you can optionally push it to the `Keystore <https://cloud.sylabs.io/keystore>`_
using the fingerprint like so:

.. code-block:: none

    $ singularity keys push 135E426D67D8416DE1D6AC7FFED5BBA38EE0DC4A
    public key `135E426D67D8416DE1D6AC7FFED5BBA38EE0DC4A` pushed to server successfully

This will allow others to verify images that you have signed.

If you delete your local public PGP key, you can always locate and download it
again like so.

.. code-block:: none

    $ singularity keys search Godlove
    Search results for 'Godlove'

    Type bits/keyID     Date       User ID
    --------------------------------------------------------------------------------
    pub  4096R/8EE0DC4A 2018-10-08 Dave Godlove (demo) <d@sylabs.io>
    --------------------------------------------------------------------------------

    $ singularity keys pull 8EE0DC4A
    1 key(s) fetched and stored in local cache /home/david/.singularity/sypgp/pgp-public

But note that this only restores the *public* key (used for verifying) to your
local machine and does not restore the *private* key (used for signing).

Signing and validating your own containers
==========================================

Now that you have a key generated, you can use it to sign images like so:

.. code-block:: none

    $ singularity sign my_container.sif
    Signing image: my_container.sif
    Enter key passphrase:
    Signature created and applied to my_container.sif

Because your public PGP key is saved locally you can verify the image without
needing to contact the Keystore.

.. code-block:: none

    $ singularity verify my_container.sif
    Verifying image: my_container.sif
    Data integrity checked, authentic and signed by:
	Dave Godlove (demo) <d@sylabs.io>, KeyID FED5BBA38EE0DC4A


If you've pushed your key to the Keystore you can also verify this image in the
absence of a local key.  To demonstrate this, first delete your local keys, and
then try to use the ``verify`` command again.

.. code-block:: none

    $ rm ~/.singularity/sypgp/*

    $ singularity verify my_container.sif
    Verifying image: my_container.sif
    INFO:    key missing, searching key server for KeyID: FED5BBA38EE0DC4A...
    INFO:    key retreived successfully!
    Store new public key 135E426D67D8416DE1D6AC7FFED5BBA38EE0DC4A? [Y/n] y
    Data integrity checked, authentic and signed by:
    	Dave Godlove (demo) <d@sylabs.io>, KeyID FED5BBA38EE0DC4A


Answering yes at the interactive prompt will store the Public key locally so
you will not have to contact the Keystore again the next time you verify your
container.
