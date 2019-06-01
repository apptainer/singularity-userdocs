.. _mpi

========================
Running MPI applications
========================

.. _sec:mpi

-------------------------
Host MPI
-------------------------

Using the MPI implementation that is already available of the host, i.e., the
MPI implementation provided by system administrators, is the easier way to run
container and MPI applications. This configuration is called `host MPI` or
`hybrid approache` since both MPI on the host and containers will be used.
It is also possible to mount storage volumes into the container to use the host
MPI from the containers but we will not cover this use case here since
requiring file system sharing between the host and containers, which is usually
not an option on high-performance computing platforms.

The advantages of this approach are:
  - integration with resource managers such as Slurm,
  - simplicity since similar to natively running MPI applications.
The drawbacks are:
  - the MPI in the container MUST be compatible with the version of MPI
    available on the host,
  - the configuration of the MPI implementation in the container MUST be
    configured for optimal use of the hardware if performance is critical.

Since the MPI implementation in the container must be compliant with the version
available on the system, a standard approach is to build your own MPI container,
including the target MPI implementation.

Assuming the application is `mpitest.c`, and the host MPI is MPICH, a definition
file such as the following example can be used:

.. code-block: none

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
        export MPICH_URL="http://www.mpich.org/static/downloads/3.3/mpich-3.3.tar.gz"
        export MPICH_DIR=/opt/mpich

    	echo "Installing MPICH..."
	    mkdir -p /tmp/mpich
    	mkdir -p /opt
	    # Download
    	cd /tmp/mpich && wget -O mpich-$MPICH_VERSION.tar.gz $MPICH_URL && tar xzf mpich-$MPICH_VERSION.tar.gz
    	# Compile and install
	    cd /tmp/mpich/mpich-$MPICH_VERSION && ./configure --prefix=$MPICH_DIR && make -j8 install
    	# Set env variables so we can compile our application
    	export PATH=$MPICH_DIR/bin:$PATH
	    export LD_LIBRARY_PAtH=$MPICH_DIR/lib:$LD_LIBRARY_PATH
    	export MANPATH=$MPICH_DIR/share/man:$MANPATH

    	echo "Compiling the MPI application..."
	    cd /opt && mpicc -o mpitest mpitest.c

If the host MPI is Open MPI, the definition file looks like:

.. code-block: none

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
        OMPI_DIR=/opt/ompi
        export OMPI_VERSION=4.0.0
        export OMPI_URL="https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.1.tar.bz2"

        echo "Installing Open MPI"
        mkdir -p /tmp/ompi
        mkdir -p /opt
        # Download
        cd /tmp/ompi && wget -O openmpi-$OMPI_VERSION.tar.bz2 $OMPI_URL && tar -xjf openmpi-$OMPI_VERSION.tar.bz2
        # Compile and install
        cd /tmp/ompi/openmpi-$OMPI_VERSION && ./configure --prefix=$OMPI_DIR && make -j8 install
        # Set env variables so we can compile our application
        export PATH=$OMPI_DIR/bin:$OMPI_DIR
        export LD_LIBRARY_PATH=$OMPI_DIR/lib:$LD_LIBRARY_PATH
        export MANPATH=$OMPI_DIR/share/man:$MANPATH

        echo "Compiling the MPI application..."
        cd /opt && mpicc -o mpitest mpitest.c


The standard way to execute MPI applications with Singularity containers is to
run the native `mpirun` command from the host, which will start Singularity
containers and ultimately MPI ranks within the containers.

Assuming your container with MPI and your application is already build,
the `mpirun` command to start your application looks like:

.. code-block: none

    $ mpirun -n <NUMBER_OF_RANKS> singularity exec <PATH/TO/MY/IMAGE> </PATH/TO/BINARY/WITHIN/CONTAINER>

Practically, this command will start first a process instantiating `mpirun`
and then Singularity containers on compute nodes. Finally,
when the containers start, the MPI binary is executed.

If your target system is setup with a batch system such as SLURM, a standard
way to execute MPI applications is through a batch script. The following
example illustrates how to do so with Slurm but can easily be adapted for all
majour batch systems available.
The first step is to create a batch script. The following example describes a
job that requests the number of nodes specified by the `NNODES` environment
variable and a total number of MPI processes specified by the `NP` environment
variable.

.. code-block: non

    $ cat my_job.sh
    #!/bin/bash
    #SBATCH --job-name singularity-mpi
    #SBATCH -N $NNODES # total number of nodes
    #SBATCH --time=00:05:00 # Max execution time

    mpirun -n $NP singularity exec /var/nfsshare/gvallee/mpich.sif /opt/mpitest
