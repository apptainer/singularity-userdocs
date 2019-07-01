.. _mpi

================================
Singularity and MPI applications
================================

.. _sec:mpi

The `Message Passing Interface (MPI) <https://mpi-forum.org>`_
is a standard extensively used by HPC applications to implement various communication
across compute nodes of a single system or across compute platforms.
There are two main open-source implementations of MPI at the
moment - `OpenMPI <https://www.open-mpi.org//>`_ and `MPICH <https://www.mpich.org/>`_,
both of which are supported by Singularity. The goal of this page is to
demonstrate the development and running of MPI programs using Singularity containers.

Although there are several ways of carrying this out, the most popular way of
executing MPI applications installed in a Sigularity container is to rely on the
MPI implementation available on the host. This is called the *Host MPI* or
the *Hybrid* model since both the MPI implementations provided by system
administrators (on the host) and in the containers will be used.

.. note::
  It is also possible to mount storage volumes into the container to use the host
  MPI from the containers but we will not cover this use case here since
  requiring file system sharing between the host and containers is usually
  not an option on high-performance computing platforms. This restriction on some
  HPC systems is due to the fact that mounting a storage volume would either
  require the execution of privileged operations or potentially compromise the
  access restrictions to other users' data.

The basic idea behind *Hybrid Approach* is when you execute a Singularity
container with MPI code, you will call ``mpiexec`` or a similar launcher on the
``singularity`` command itself. The MPI process outside of the container will
then work in tandem with MPI inside the container and the containerized MPI code
to instantiate the job.

The Open MPI/Singularity workflow in detail:

1. The MPI launcher (e.g., ``mpirun``, ``mpiexec``) is called by the resource manager or the user directly from a shell.
2. Open MPI then calls the process management daemon (ORTED).
3. The ORTED process launches the Singularity container requested by the launcher command, as such ``mpirun``.
4. Singularity builds the container and namespace environment.
5. Singularity then launches the MPI application within the container.
6. The MPI application launches and loads the Open MPI libraries.
7. The Open MPI libraries connect back to the ORTED process via the Process Management Interface (PMI).

At this point the processes within the container run as they would normally directly on the host.

The advantages of this approach are:
  - Integration with resource managers such as Slurm.
  - Simplicity since similar to natively running MPI applications.

The drawbacks are:
  - The MPI in the container must be compatible with the version of MPI
    available on the host.
  - The configuration of the MPI implementation in the container must be
    configured for optimal use of the hardware if performance is critical.

Since the MPI implementation in the container must be compliant with the version
available on the system, a standard approach is to build your own MPI container,
including the target MPI implementation.

To illustrate how Singularity can be used to execute MPI applications, we will
assume for a moment that the application is `mpitest.c`, a simple Hello World:

.. code-block:: none

	#include <mpi.h>
	#include <stdio.h>
	#include <stdlib.h>

	int main (int argc, char **argv) {
		int rc;
		int size;
		int myrank;

		rc = MPI_Init (&argc, &argv);
		if (rc != MPI_SUCCESS) {
			fprintf (stderr, "MPI_Init() failed");
			return EXIT_FAILURE;
		}

		rc = MPI_Comm_size (MPI_COMM_WORLD, &size);
		if (rc != MPI_SUCCESS) {
			fprintf (stderr, "MPI_Comm_size() failed");
			goto exit_with_error;
		}

		rc = MPI_Comm_rank (MPI_COMM_WORLD, &myrank);
		if (rc != MPI_SUCCESS) {
			fprintf (stderr, "MPI_Comm_rank() failed");
			goto exit_with_error;
		}

		fprintf (stdout, "Hello, I am rank %d/%d", myrank, size);

		MPI_Finalize();

		return EXIT_SUCCESS;

	 exit_with_error:
		MPI_Finalize();
		return EXIT_FAILURE;
	}

.. note::
     MPI is an interface to a library, so it consists of function calls and
     libraries that can be used my many programming languages. It comes with
     bindings for Fortran and C. However, it can support applications in many
     languages like Python, R, etc.

The next step is to build the definition file which will depend on the MPI
implementation available on the host.

If the host MPI is MPICH, a definition file such as the following example can be used:

.. code-block:: none

  Bootstrap: docker
  From: ubuntu:latest

  %files
      mpitest.c /opt

  %environment
      MPICH_DIR=/opt/mpich-3.3
      export MPICH_DIR
      export SINGULARITY_MPICH_DIR=$MPICH_DIR
      export SINGULARITYENV_APPEND_PATH=$MPICH_DIR/bin
      export SINGULAIRTYENV_APPEND_LD_LIBRARY_PATH=$MPICH_DIR/lib

  %post
      echo "Installing required packages..."
      apt-get update && apt-get install -y wget git bash gcc gfortran g++ make

      # Information about the version of MPICH to use
      export MPICH_VERSION=3.3
      export MPICH_URL="http://www.mpich.org/static/downloads/$MPICH_VERSION/mpich-$MPICH_VERSION.tar.gz"
      export MPICH_DIR=/opt/mpich

      echo "Installing MPICH..."
      mkdir -p /tmp/mpich
      mkdir -p /opt
      # Download
      cd /tmp/mpich && wget -O mpich-$MPICH_VERSION.tar.gz $MPICH_URL && tar xzf mpich-$MPICH_VERSION.tar.gz
      # Compile and install
      cd /tmp/mpich/mpich-$MPICH_VERSION && ./configure --prefix=$MPICH_DIR && make install
      # Set env variables so we can compile our application
      export PATH=$MPICH_DIR/bin:$PATH
      export LD_LIBRARY_PATH=$MPICH_DIR/lib:$LD_LIBRARY_PATH
      export MANPATH=$MPICH_DIR/share/man:$MANPATH

      echo "Compiling the MPI application..."
      cd /opt && mpicc -o mpitest mpitest.c


If the host MPI is Open MPI, the definition file looks like:

.. code-block:: none

  Bootstrap: docker
  From: ubuntu:latest

  %files
      mpitest.c /opt

  %environment
      OMPI_DIR=/opt/ompi
      export OMPI_DIR
      export SINGULARITY_OMPI_DIR=$OMPI_DIR
      export SINGULARITYENV_APPEND_PATH=$OMPI_DIR/bin
      export SINGULAIRTYENV_APPEND_LD_LIBRARY_PATH=$OMPI_DIR/lib

  %post
      echo "Installing required packages..."
      apt-get update && apt-get install -y wget git bash gcc gfortran g++ make file

      echo "Installing Open MPI"
      export OMPI_DIR=/opt/ompi
      export OMPI_VERSION=4.0.1
      export OMPI_URL="https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-$OMPI_VERSION.tar.bz2"
      mkdir -p /tmp/ompi
      mkdir -p /opt
      # Download
      cd /tmp/ompi && wget -O openmpi-$OMPI_VERSION.tar.bz2 $OMPI_URL && tar -xjf openmpi-$OMPI_VERSION.tar.bz2
      # Compile and install
      cd /tmp/ompi/openmpi-$OMPI_VERSION && ./configure --prefix=$OMPI_DIR && make install
      # Set env variables so we can compile our application
      export PATH=$OMPI_DIR/bin:$PATH
      export LD_LIBRARY_PATH=$OMPI_DIR/lib:$LD_LIBRARY_PATH
      export MANPATH=$OMPI_DIR/share/man:$MANPATH

      echo "Compiling the MPI application..."
      cd /opt && mpicc -o mpitest mpitest.c

The standard way to execute MPI applications with Singularity containers is to
run the native ``mpirun`` command from the host, which will start Singularity
containers and ultimately MPI ranks within the containers.

Assuming your container with MPI and your application is already build,
the ``mpirun`` command to start your application looks like:

.. code-block:: none

    $ mpirun -n <NUMBER_OF_RANKS> singularity exec <PATH/TO/MY/IMAGE> </PATH/TO/BINARY/WITHIN/CONTAINER>

Practically, this command will first start a process instantiating ``mpirun``
and then Singularity containers on compute nodes. Finally, when the containers
start, the MPI binary is executed.

If your target system is setup with a batch system such as SLURM, a standard
way to execute MPI applications is through a batch script. The following
example illustrates the context of a batch script for Slurm that aims at
starting a Singularity container on each node allocated to the execution of
the job. It can easily be adapted for all major batch systems available.

.. code-block:: none

    $ cat my_job.sh
    #!/bin/bash
    #SBATCH --job-name singularity-mpi
    #SBATCH -N $NNODES # total number of nodes
    #SBATCH --time=00:05:00 # Max execution time

    mpirun -n $NP singularity exec /var/nfsshare/gvallee/mpich.sif /opt/mpitest

In fact, the example describes a job that requests the number of nodes specified
by the ``NNODES`` environment variable and a total number of MPI processes specified
by the ``NP`` environment variable.

A user can then submit a job by executing the following SLURM command:

.. code-block:: none

    $ sbatch my_job.sh
