.. _security:

***********************************
Security in Singularity Containers
***********************************

Containers are all the rage today for many good reasons. They are light weight, easy to spin-up and require reduced IT management resources as compared to hardware VM environments. More importantly, container technology facilitates advanced research computing by granting the ability to package software in highly portable and reproducible environments encapsulating all dependencies, including the operating system. But there are still some challenges to container security. 

Singularity, which is a container paradigm created by necessity for scientific and application driven workloads, addresses some 
core missions of containers : Mobility of Compute, Reproducibility, HPC support, and **Security**. This document intends to inform
users of different security features supported by Singularity.

Singularity Runtime
###################

Singularity Runtime enforces a unique security model that makes it appropriate for *untrusted users* to run *untrusted containers* 
safely on multi-tenant resources. Since Singularity Runtime dynamically writes UID and GID information to the appropriate files 
within the container at runtime, the user remains the same *inside* and *outside* the container, i.e., if you're an unprivileged 
user while entering the container you'll remain an unprivileged user inside the container. A privilege separation model is in place
to prevent users from escalating privileges once they are inside of a container. The container file system is mounted using the 
``nosuid`` option, and processes are spawned with the ``PR_NO_NEW_PRIVS`` flag. Taken together, this approach provides a secure way 
for users to run containers and greatly simplifies things like reading and writing data to the host system with appropriate 
ownership.

It is also important to note that the philosophy of Singularity is *Integration* over *Isolation*. Most container run times strive 
to isolate your container from the host system and other containers as much as possible. Singularity, on the 
other hand, assumes that the user’s primary goals are portability, reproducibility, and ease of use and that isolation is often a 
tertiary concern. Therefore, Singularity only isolates the mount namespace by default, and will also bind mount several host 
directories such as ``$HOME`` and ``/tmp`` into the container at runtime. If needed, additional levels of isolation can be achieved
by passing options causing Singularity to enter any or all of the other kernel namespaces and to prevent automatic bind mounting.
These measures allow users to interact with the host system from within the container in sensible ways.

Singularity Image Format (SIF)
##############################

Sylabs addresses Container Security as a continuous process. It attempts to provide container integrity throughout the distribution
pipeline.. i.e., at rest, in transit and while running. Hence, the SIF has been designed to achieve these goals. 

A SIF file is an immutable container runtime image. It is a physical representation of the container environment itself. An 
important component of SIF that elicits security feature is the ability to cryptographically sign a container, creating a signature
block within the SIF file which can guarantee immutability and provide accountability as to who signed it. Singularity follows the 
`OpenPGP <https://www.openpgp.org/>`_ standard to create and manage these keys. After building an image within Singularity, user can
``singularity sign`` the container and push it to the Library along with its public PGP key(Stored in :ref:`Keystore <keystore>`) which 
later can be verified (``singularity verify``) while pulling or downloading the image. :ref:`This feature <signNverify>` in particular 
protects collaboration within and between systems and teams. 

With a new development to SIF, the root file system that resides in the squashFS partition of SIF will be encrypted as a result of 
which everything inside the container becomes inaccessible without a key. This feature will make it necessary for the users to 
have a password in order to run the containers. It also ensures that no other user on the system will be able to look at your
container files. Since it is all encrypted, it can defend from intruders manipulating the image while in transit.

Unlike other container platforms where the build step requires a number of layers to be read and written into another layer 
involving the creation of intermediate containers, Singularity executes it in a single step resulting in a ``.sif`` file thereby
reducing the attack surface and eliminating any chances of creeping in malicious content during building and running of containers.


Admin Configurable Files
#########################

Singularity Administrators will have the ability to access various configuration files, that will let them set security 
restrictions, grant or revoke a user’s capabilities, manage resources and authorize containers etc. One such file interesting in this context is `ecl.toml <https://sylabs.io/guides/\{adminversion\}/admin-guide/configfiles.html#ecl-toml>`_ 
which allows blacklisting and whitelisting of containers. However, you should find all the configuration files and their parameters
documented `here <https://sylabs.io/guides/\{adminversion\}/admin-guide/configfiles.html>`_. 

cgroups support
****************

Starting v3.0, Singularity added native support for ``cgroups``, allowing users to limit the resources their containers consume 
without the help of a separate program like a batch scheduling system. This feature helps in preventing  DoS attacks where one 
container seizes control of all available system resources in order to stop other containers from operating properly. 
To utilize this feature, a user first creates a configuration file. An example configuration file is installed by default with 
Singularity to provide a guide. At runtime, the ``--apply-cgroups`` option is used to specify the location of the configuration 
file and cgroups are configured accordingly. More about cgroups support `here <https://sylabs.io/guides/\{adminversion\}/admin-guide/configfiles.html#cgroups-toml>`_.

``--security`` options
***********************

Singularity supports a number of methods for specifying the security scope and context when running Singularity containers. 
Additionally, it supports new flags that can be passed to the action commands; ``shell``, ``exec``, and ``run`` allowing fine 
grained control of security. Details about them are documented `here <https://sylabs.io/guides/\{version\}/user-guide/security_options.html>`_.

Security in SCS
################

`Singularity Container Services (SCS) <https://cloud.sylabs.io/home>`_ consist of a Remote Builder, a Container Library, and a 
Keystore. Taken together, the Singularity Container Services provide an end-to-end solution for packaging and distributing 
applications in secure and trusted containers.

Remote Builder
**************

As mentioned earlier, singularity runtime prevents executing code with root-level permissions on the host system. But building a 
container requires elevated privileges that most of the commercial environments do not grant its users. `Build Service <https://cloud.sylabs.io/builder>`_ 
aims to help this challenge by allowing unprivileged users a service that can be used to build containers targeting one or more CPU 
architectures. System administrators can use the system to monitor which users are building containers, and the contents of those 
containers. Starting with Singularity 3.0, the CLI has native integration with the Build Service from version 3.0 onwards. In 
addition, a browser interface to the Build Service also exists, which allows users to build containers using only a web browser.

.. note::

    Please see the :ref:`Fakeroot feature <fakeroot>` which is a secure option for admins in multi-tenant HPC environments and 
    similar use cases where they might want to grant a user special privileges inside a container.

Container Library
*****************

The `Container Library <https://cloud.sylabs.io/library>`_ enables users to store and share Singularity container images based on 
the Singularity Image Format (SIF). A web front-end allows users to create new projects within the Container Library, edit 
documentation associated with container images, and discover container images published by their peers.

.. _keystore:

Key Store
*********

The `Key Store <https://cloud.sylabs.io/keystore>`_ is a key management system offered by Sylabs that utilizes `OpenPGP implementation <https://gnupg.org/>`_ to facilitate sharing and maintaining of PGP public keys used to sign and verify Singularity container images. This service is based on the OpenPGP HTTP Keyserver Protocol (HKP), with several enhancements:

- The Service requires connections to be secured with Transport Layer Security (TLS).
- The Service implements token-based authentication, allowing only authenticated users to add or modify PGP keys.
- A web front-end allows users to view and search for PGP keys using a web browser.


Security Considerations of Cloud Services:
******************************************

1. Communications between users, the auth service and the above-mentioned services are secured via TLS.

2. The services support authentication of users via authentication tokens.

3. There is no implicit trust relationship between Auth and each of these services. Rather, each request between the services is authenticated using the authentication token supplied by the user in the associated request.

4. The services support MongoDB authentication as well as TLS/SSL. 

.. note::

   SingularityPRO is a professionally curated and licensed version of Singularity that provides added security, stability, and 
   support beyond that offered by the open source project. Subscribers receive advanced access to security patches through regular 
   updates so, when a CVE is announced publicly PRO subscribers are already using patched software.


Security is not a check box that one can tick and forget.  It’s an ongoing process that begins with software architecture, and 
continues all the way through to ongoing security practices.  In addition to ensuring that containers are run without elevated 
privileges where appropriate, and that containers are produced by trusted sources, users must monitor their containers for newly 
discovered vulnerabilities and update when necessary just as they would with any other software. Sylabs is constantly probing to 
find and patch vulnerabilities within Singularity, and will continue to do so.
