====
FAQ
====

.. _sec:faq:


------------------------
General Singularity Info
------------------------

Why the name "Singularity"?
===========================

A “Singularity” is an astrophysics phenomenon in which a single point becomes infinitely dense.
This type of a singularity can thus contain massive quantities of universe within it and thus encapsulating an infinite amount of data within it.

Additionally, the name “Singularity” for me (Greg) also stems back from my past experience working at a company called `Linuxcare <https://en.wikipedia.org/wiki/Linuxcare>`_
where the Linux Bootable Business Card (LNX-BBC) was developed. The BBC, was a Linux rescue disk which paved the way for all live CD bootable
distributions using a compressed single image file system called the “singularity”.

The name has  **NOTHING**  to do with Kurzweil’s (among others) prediction that artificial intelligence will abruptly have the ability to reprogram itself,
surpass that of human intelligence and take control of the planet. If you are interested in this may I suggest the movie Terminator 2: Judgment Day.

What is so special about Singularity?
=====================================

While Singularity is a container solution (like many others), Singularity differs in it’s primary design goals and architecture:

#. **Reproducible software stacks:** These must be easily verifiable via checksum or cryptographic signature in such a manner that does not change formats (e.g. splatting a tarball out to disk). By default Singularity uses a container image file which can be checksummed, signed, and thus easily verified and/or validated.

#. **Mobility of compute:** Singularity must be able to transfer (and store) containers in a manner that works with standard data mobility tools (rsync, scp, gridftp, http, NFS, etc..) and maintain software and data controls compliancy (e.g. HIPPA, nuclear, export, classified, etc..)

#. **Compatibility with complicated architectures:** The runtime must be immediately compatible with existing HPC, scientific, compute farm and even enterprise architectures any of which maybe running legacy kernel versions (including RHEL6 vintage systems) which do not support advanced namespace features (e.g. the user namespace)

#. **Security model:** Unlike many other container systems designed to support trusted users running trusted containers we must support the opposite model of untrusted users running untrusted containers. This changes the security paradigm considerably and increases the breadth of use cases we can support.


Which namespaces are virtualized? Is that select-able?
======================================================


That is up to you!

While some namespaces, like newns (mount) and fs (file system) must be virtualized, all of the others are conditional depending on what you want to do.
For example, if you have a workflow that relies on communication between containers (e.g. MPI), it is best to not isolate any more than absolutely
necessary to avoid performance regressions. While other tasks are better suited for isolation (e.g. web and data base services).

Namespaces are selected via command line usage and system administration configuration.


What Linux distributions are you trying to get on-board?
========================================================

All of them! Help us out by letting them know you want Singularity to be included!

How do I request an installation on my resource?
================================================

It’s important that your administrator have all of the resources available to him or her to make a decision to install Singularity.
We’ve prepared a :ref:`helpful guide <installation-request>` that you can send to him or her to start a conversation. If there are any unanswered questions, we recommend
that you `reach out <https://www.sylabs.io/contact/>`_.

-----------------------
Basic Singularity usage
-----------------------

Do you need administrator privileges to use Singularity?
========================================================


You generally do not need admin/sudo to use Singularity containers but you do however need admin/root access to install Singularity and for some
container build functions (for example, building from a recipe, or a writable image).

This then defines the work-flow to some extent. If you have a container (whether Singularity or Docker) ready to go, you can run/shell/import
without root access. If you want to build a new Singularity container image from scratch it must be built and configured on a host where you have root
access (this can be a physical system or on a VM). And of course once the container image has been configured it can be used on a system where you do not have root access as long as Singularity has been installed there.

What if I don't want to install Singularity on my computer?
===========================================================

If you don’t want to build your own images, `Singularity Hub <https://singularity-hub.org/>`_ will connect to your GitHub repos with build specification files, and build the containers automatically for you.
You can then interact with them easily where Singularity is installed (e.g., on your cluster):


.. code-block:: none

    singularity shell shub://vsoch/hello-world

    singularity run shub://vsoch/hello-world

    singularity pull shub://vsoch/hello-world

    singularity build hello-world.simg shub://vsoch/hello-world # redundant, you would already get an image


Can you edit/modify a Singularity container once it has been instantiated?
==========================================================================

We strongly advocate for reproducibility, so if you build a squashfs container, it is immutable. However, if you build with
 ``--sandbox`` or ``--writable`` you can produce a writable sandbox folder or a writable ext3 image, respectively.
 From a sandbox you can develop, test, and make changes, and then build or convert it into a standard image.

We recommend to use the default compressed, immutable format for production containers.

Can multiple applications be packaged into one Singularity Container?
=====================================================================

Yes! You can even create entire pipe lines and work flows using many applications, binaries, scripts, etc..
The ``%runscript`` bootstrap section is where you can define what happens when a Singularity container is run,
and with the introduction of :ref:`modular apps <reproducible-scif-apps>`  you can now even define ``%apprun`` sections for different entrypoints to your container.

How are external file systems and paths handled in a Singularity Container?
===========================================================================

Because Singularity is based on container principals, when an application is run from within a Singularity container its default
view of the file system is different from how it is on the host system. This is what allows the environment to be portable.
This means that root (‘/’) inside the container is different from the host!

Singularity automatically tries to resolve directory mounts such that things will just work and be portable with whatever environment
you are running on. This means that ``/tmp`` and ``/var/tmp`` are automatically shared into the container as is ``/home``.
Additionally, if you are in a current directory that is not a system directory, Singularity will also try to bind that to your container.

There is a caveat in that a directory must already exist within your container to serve as a mount point. If that directory does not exist,
Singularity will not create it for you! You must do that. To create custom mounts at runtime, you should use the ``-B`` or ``--bind`` argument:

.. code-block:: none

    singularity run --bind /home/vanessa/Desktop:/data container.img


How does Singularity handle networking?
=======================================

As of 2.4, Singularity can support the network namespace to a limited degree. At present, we just use it for isolation,
but it will soon be more featurefull.

Can Singularity support daemon processes?
=========================================

Singularity has container “instance” support which allows one to start a container process, within its own namespaces, and use that instance
like it was a stand alone, isolated system.

At the moment (as above describes), the network (and UTS) namespace is not well supported, so if you spin up a process daemon, it will exist on
your host’s network. This means you can run a web server, or any other daemon, from within a container and access it directly from your host.

Can a Singularity container be multi-threaded?
==============================================

Yes. Singularity imposes no limitations on forks, threads or processes in general.

Can a Singularity container be suspended or check-pointed?
==========================================================

Yes and maybe respectively. Any Singularity application can be suspended using standard Linux/Unix signals. Check-pointing requires some preloaded
libraries to be automatically loaded with the application but because Singularity escapes the hosts library stack, the checkpoint libraries would not
be loaded. If however you wanted to make a Singularity container that can be check-pointed, you would need to install the checkpoint libraries into the Singularity container via the specfile.

On our roadmap is the ability to checkpoint the entire container process thread, and restart it. Keep an eye out for that feature!

Are there any special requirements to use Singularity through an HPC job scheduler?
===================================================================================

Singularity containers can be run via any job scheduler without any modifications to the scheduler configuration or architecture.
This is because Singularity containers are designed to be run like any application on the system, so within your job script just call Singularity as you would any other application!

Does Singularity work in multi-tenant HPC cluster environments?
===============================================================

Yes! HPC was one of the primary use cases in mind when Singularity was created.

Most people that are currently integrating containers on HPC resources do it by creating virtual clusters within the physical host cluster.
This precludes the virtual cluster from having access to the host cluster’s high performance fabric, file systems and other investments which make an HPC system high performance.

Singularity on the other hand allows one to keep the high performance in High Performance Computing by containerizing applications and supporting
a runtime which seamlessly interfaces with the host system and existing environments.

Can I run X11 apps through Singularity?
=======================================

Yes. This works exactly as you would expect it to.

Can I containerize my MPI application with Singularity and run it properly on an HPC system?
============================================================================================

Yes! HPC was one of the primary use cases in mind when Singularity was created.

While we know for a fact that Singularity can support multiple MPI implementations, we have spent a considerable effort working with Open MPI
as well as adding a Singularity module into Open MPI (v2) such that running at extreme scale will be as efficient as possible.

note: We have seen no major performance impact from running a job in a Singularity container.

Why do we call 'mpirun' from outside the container (rather than inside)?
========================================================================

With Singularity, the MPI usage model is to call ‘mpirun’ from outside the container, and reference the container from your ‘mpirun’ command. Usage would look like this:

.. code-block:: none

    $ mpirun -np 20 singularity exec container.img /path/to/contained_mpi_prog


By calling ‘mpirun’ outside the container, we solve several very complicated work-flow aspects. For example, if ‘mpirun’ is called from within the container it must have a method for spawning processes on remote nodes. Historically ssh is used for this which means that there must be an sshd running within the container on the remote nodes, and this sshd process must not conflict with the sshd running on that host! It is also possible for the resource manager to launch the job and (in Open MPI’s case) the Orted processes on the remote system, but that then requires resource manager modification and container awareness.

In the end, we do not gain anything by calling ‘mpirun’ from within the container except for increasing the complexity levels and possibly losing out on some added performance benefits (e.g. if a container wasn’t built with the proper OFED as the host).

See the Singularity on HPC page for more details.

Does Singularity support containers that require GPUs?
======================================================

Yes. Many users run GPU-dependent code within Singularity containers. The experimental ``--nv`` option allows you to leverage host GPUs without installing system level drivers into your container. See the :ref:`exec <exec-command>` command for an example.

---------------------
Container portability
---------------------


Are Singularity containers kernel-dependent?
============================================

No, never. But sometimes yes.

Singularity is using standard container principals and methods so if you are leveraging any kernel version specific or external patches/module functionality (e.g. OFED), then yes there maybe kernel dependencies you will need to consider.

Luckily most people that would hit this are people that are using Singularity to inter-operate with an HPC (High Performance Computing) system where there are highly tuned interconnects and file systems you wish to make efficient use of. In this case, See the documentation of MPI with Singularity.

There is also some level of glibc forward compatibility that must be taken into consideration for any container system. For example, I can take a Centos-5 container and run it on Centos-7, but I can not take a Centos-7 container and run it on Centos-5.

note: If you require kernel-dependent features, a container platform is probably not the right solution for you.

Can a Singularity container resolve GLIBC version mismatches?
=============================================================

Yes. Singularity containers contain their own library stack (including the Glibc version that they require to run).

What is the performance trade off when running an application native or through Singularity?
============================================================================================

So far we have not identified any appreciable regressions of performance (even in parallel applications running across nodes with InfiniBand).
There is a small start-up cost to create and tear-down the container, which has been measured to be anywhere from 10 - 20 thousandths of a second.

----
Misc
----

The following are miscellaneous questions.

Are there any special security concerns that Singularity introduces?
====================================================================

No and yes.

While Singularity containers always run as the user launching them, there are some aspects of the container execution which requires escalation of privileges. This escalation is achieved via a SUID portion of code. Once the container environment has been instantiated, all escalated privileges are dropped completely, before running any programs within the container.

Additionally, there are precautions within the container context to mitigate any escalation of privileges. This limits a user’s ability to gain root control once inside the container.

You can read more about the Singularity :ref:`security overview here <security-and-privilege-escalation>`.
