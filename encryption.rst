.. _encrypted_containers:

====================
Encrypted Containers
====================

--------
Overview
--------

Encryption feature allows the user to build a secure container environment by encrypting the root filesystem of the container. 


.. note:: 
        This feature utilizes Linux's dm-crypt library and cryptsetup utility under the covers and requires cryptsetup version of >= 2.2.0

Internally, the root filesystem of the container is encrypted using dm-crypt libraries by utilizing cryptsetup utility using a secret. The secret can be either supplied, in case of plaintext password encryption, or randomly generated, in the case of asymmetric encryption.


-----
Usage
-----

----------
Encryption
----------

A container can be encrypted either by supplying a key-file containing asymmetric RSA public key or by using a passphrase in plaintext format.

Key-file or passphrase is supplied either by an environment variable or a command line option

+-------------------+------------------------------------+-----------------------+
| Encryption Method | Environment Variable               | Commandline Option    |
+-------------------+====================================+=======================+
| Plaintext         | SINGULARITY_ENCRYPTION_PASSPHRASE  | --passphrase          |
+-------------------+------------------------------------+-----------------------+
| Asymmentric (PEM) | SINGULARITY_ENCRYPTION_PEMPATH     | --pempath             | 
+-------------------+------------------------------------+-----------------------+

-e|--encrypt build flag is used to indicate that container needs to be encrypted.


--------------------
Plaintext Encryption
--------------------
In case of plaintext encryption, passphrase is supplied either by either one of the ways mentioned in the table above.

Example 1: 
        env SINGULARITY_ENCRYPTION_PASSPHRASE="secret" sudo singularity build -e encrypted.sif encrypted.recipe

Example 2:
        sudo singularity build -e --passphrase="secret" encrypted.sif encrypted.recipe
        Enter passphrase for encrypted container: <secret>
        Starting build...

---------------------
Asymmetric Encryption
---------------------
Singularity currently supports RSA encryption using public/private key-pair. Keys are supplied in Privacy Enhanced Mail (PEM) format.

Example 1:
        sudo singularity build -e --pempath=<path-to-public-key> encrypted.sif encrypted.recipe

Example 2:
        sudo env SINGULARITY_ENCRYPTION_PEM_PATH=<path-to-public-key> singularity build -e encrypted.sif encrypted.recipe


----------
Decryption
----------

To decrypt an encrypted image, the same credentials used to encrypt the image need to be supplied, either in a key-file supplying the asymmetric private key or a plaintext passphrase

--------------------
Plaintext Decryption
--------------------
In case of plaintext decryption, passphrase can be supplied by either one of th ways listed in the Encryption section above.

Example 1:
        env SINGULARITY_ENCRYPTION_PASSPHRASE="secret" singularity run encrypted.sif ls
Example 2:
        singularity run --passphrase="secret" encrypted.sif ls

---------------------
Asymmetric Decryption
---------------------

In case of asymmetric decryption, private key is supplied in Privacy Enhanced Mail (PEM) format using either one of the methods listed in the Encryption section above.

Example 1:
        env SINGULARITY_ENCRYPTION_PEM_PATH=<path-to-private-key> singularity run encrypted.sif ls

Example 2:
        singularity run --pem-path=<path-to-private-key> singularity run encrypted.sif ls

.. note:: 
        If both environment variable and commandline option are supplied, commandline option will be given priorityboth in encryption and decryption cases

Eg: sudo env SINGULARITY_ENCRYPTION_PEM_PATH=<path-to-public-key1> singularity build -e --pempath=<path-to-public-key2> encrypted.sif encrypted.recipe

In the above example, encrypted.sif will be encrypted using the public key found in the file path-to-public-key2.


---------------
Generating Keys
---------------

`ssh-keygen` can be used to generate public and private keys in PEM format.

$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/vagrant/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/vagrant/.ssh/id_rsa.
Your public key has been saved in /home/vagrant/.ssh/id_rsa.pub.

Public key can be converted into PEM format using

$ ssh-keygen -f ~/.ssh/id_rsa.pub -e -m pem

Private key in PEM format can be found at ~/.ssh/id_rsa
