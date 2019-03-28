.. _oci_runtime:


===================
OCI Runtime Support 
===================

.. --------
.. Overview
.. --------

.. TODO Allude to connection with the OCI image spec and implementation in Singularity 

.. TODO All commands require root access ... 

.. TODO Intro OCI acronym
 OCI is an acronym for the `Open Containers Initiative <https://www.opencontainers.org/>`_ - an independent organization whose mandate is to develop open standards relating to containerization. To date, standardization efforts have focused on container formats and runtimes; it is the former that is emphasized here.  

.. TODO Need to account for the diff bootstrap agents that could produce a SIF file for OCI runtime support ... 

.. TODO Compliance testing/validation  - need to document ... https://github.com/opencontainers/runtime-tools

------------------------------
Mounted OCI Filesystem Bundles
------------------------------

Mounting an OCI Filesystem Bundle
=================================

Suppose the Singularity Image Format (SIF) file ``lolcow_latest.sif`` exists locally. (Recall that

.. code-block:: none

	vagrant@vagrant:~$ singularity pull docker://godlovedc/lolcow
	INFO:    Starting build...
	Getting image source signatures
	Copying blob sha256:9fb6c798fa41e509b58bccc5c29654c3ff4648b608f5daa67c1aab6a7d02c118
	 45.33 MiB / 45.33 MiB [====================================================] 2s
	Copying blob sha256:3b61febd4aefe982e0cb9c696d415137384d1a01052b50a85aae46439e15e49a
	 848 B / 848 B [============================================================] 0s
	Copying blob sha256:9d99b9777eb02b8943c0e72d7a7baec5c782f8fd976825c9d3fb48b3101aacc2
	 621 B / 621 B [============================================================] 0s
	Copying blob sha256:d010c8cf75d7eb5d2504d5ffa0d19696e8d745a457dd8d28ec6dd41d3763617e
	 853 B / 853 B [============================================================] 0s
	Copying blob sha256:7fac07fb303e0589b9c23e6f49d5dc1ff9d6f3c8c88cabe768b430bdb47f03a9
	 169 B / 169 B [============================================================] 0s
	Copying blob sha256:8e860504ff1ee5dc7953672d128ce1e4aa4d8e3716eb39fe710b849c64b20945
	 53.75 MiB / 53.75 MiB [====================================================] 2s
	Copying config sha256:73d5b1025fbfa138f2cacf45bbf3f61f7de891559fa25b28ab365c7d9c3cbd82
	 3.33 KiB / 3.33 KiB [======================================================] 0s
	Writing manifest to image destination
	Storing signatures
	INFO:    Creating SIF file...
	INFO:    Build complete: lolcow_latest.sif

is one way to bootstrap creation of this image in SIF that *retains* a local copy. Additional approaches and details can be found in the section :ref:`Support for Docker and OCI <singularity-and-docker>`). 

For the purpose of boostrapping the creation of an OCI compliant runtime, this SIF file can be mounted as follows: 

.. code-block:: none 

	$ sudo singularity oci mount ./lolcow_latest.sif /var/tmp/lolcow

Because ``mount`` is a command requiring privileged access, so does this OCI variant in Singularity. By issuing this command, the Singularity container runtime encapsulated in the SIF file ``lolcow_latest.sif`` is mounted on the mount point ``/var/tmp/lolcow`` as an ``overlay`` file system, 

.. code-block:: none

	$ sudo df -k 
	Filesystem                   1K-blocks      Used Available Use% Mounted on
	udev                            475192         0    475192   0% /dev
	tmpfs                           100916      1548     99368   2% /run
	/dev/mapper/vagrant--vg-root  19519312   2242944  16261792  13% /
	tmpfs                           504560         0    504560   0% /dev/shm
	tmpfs                             5120         0      5120   0% /run/lock
	tmpfs                           504560         0    504560   0% /sys/fs/cgroup
	vagrant                      243352964 143016400 100336564  59% /vagrant
	tmpfs                           100912         0    100912   0% /run/user/900
	overlay                       19519312   2242944  16261792  13% /var/tmp/lolcow/rootfs

with permissions as follows:

.. code-block:: none

	$ sudo ls -ld /var/tmp/lolcow
	drwx------ 4 root root 4096 Mar 20 15:45 /var/tmp/lolcow

.. note:: 

	All commands in the ``oci`` group *must* be executed as the ``root`` user. 



Content of an OCI Compliant Filesystem Bundle
=============================================

The *expected* contents of the mounted filesystem are as follows:

.. code-block:: none 

	$ sudo ls -la /var/tmp/lolcow
	total 28
	drwx------ 4 root root 4096 Mar 20 15:45 .
	drwxrwxrwt 4 root root 4096 Mar 20 15:45 ..
	-rw-rw-rw- 1 root root 9878 Mar 20 15:45 config.json
	drwx------ 4 root root 4096 Mar 20 15:45 overlay
	drwx------ 1 root root 4096 Mar 20 15:45 rootfs

From the perspective of the `OCI runtime specification <https://github.com/opencontainers/runtime-spec/blob/master/bundle.md>`_, this content is expected because it prescribes a 

	"... a format for encoding a container as a **filesystem bundle** - a set of files organized in a certain way, and containing all the necessary data and metadata for any compliant runtime to perform all standard operations against it." 

Critical to compliance with the specification is the presence of the following *mandatory* artifacts residing locally in a single directory:

	1. The ``config.json`` file - a file of configuration data that must reside in the root of the bundle directory under this name 

	2. The container's root filesystem - a referenced directory

.. note::

	Because the directory itself, i.e., ``/var/tmp/lolcow`` is *not* part of the bundle, the mount point can be chosen arbitrarily. 

The `filtered <https://github.com/stedolan/jq>`_ ``config.json`` file corresponding to the OCI mounted ``lolcow_latest.sif`` container can be detailed as follows via ``$ sudo cat /var/tmp/lolcow/config.json | jq``: 

.. code-block:: json

	{
	  "ociVersion": "1.0.1-dev",
	  "process": {
	    "user": {
	      "uid": 0,
	      "gid": 0
	    },
	    "args": [
	      "/.singularity.d/actions/run"
	    ],
	    "env": [
	      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
	      "TERM=xterm"
	    ],
	    "cwd": "/",
	    "capabilities": {
	      "bounding": [
	        "CAP_CHOWN",
	        "CAP_DAC_OVERRIDE",
	        "CAP_FSETID",
	        "CAP_FOWNER",
	        "CAP_MKNOD",
	        "CAP_NET_RAW",
	        "CAP_SETGID",
	        "CAP_SETUID",
	        "CAP_SETFCAP",
	        "CAP_SETPCAP",
	        "CAP_NET_BIND_SERVICE",
	        "CAP_SYS_CHROOT",
	        "CAP_KILL",
	        "CAP_AUDIT_WRITE"
	      ],
	      "effective": [
	        "CAP_CHOWN",
	        "CAP_DAC_OVERRIDE",
	        "CAP_FSETID",
	        "CAP_FOWNER",
	        "CAP_MKNOD",
	        "CAP_NET_RAW",
	        "CAP_SETGID",
	        "CAP_SETUID",
	        "CAP_SETFCAP",
	        "CAP_SETPCAP",
	        "CAP_NET_BIND_SERVICE",
	        "CAP_SYS_CHROOT",
	        "CAP_KILL",
	        "CAP_AUDIT_WRITE"
	      ],
	      "inheritable": [
	        "CAP_CHOWN",
	        "CAP_DAC_OVERRIDE",
	        "CAP_FSETID",
	        "CAP_FOWNER",
	        "CAP_MKNOD",
	        "CAP_NET_RAW",
	        "CAP_SETGID",
	        "CAP_SETUID",
	        "CAP_SETFCAP",
	        "CAP_SETPCAP",
	        "CAP_NET_BIND_SERVICE",
	        "CAP_SYS_CHROOT",
	        "CAP_KILL",
	        "CAP_AUDIT_WRITE"
	      ],
	      "permitted": [
	        "CAP_CHOWN",
	        "CAP_DAC_OVERRIDE",
	        "CAP_FSETID",
	        "CAP_FOWNER",
	        "CAP_MKNOD",
	        "CAP_NET_RAW",
	        "CAP_SETGID",
	        "CAP_SETUID",
	        "CAP_SETFCAP",
	        "CAP_SETPCAP",
	        "CAP_NET_BIND_SERVICE",
	        "CAP_SYS_CHROOT",
	        "CAP_KILL",
	        "CAP_AUDIT_WRITE"
	      ],
	      "ambient": [
	        "CAP_CHOWN",
	        "CAP_DAC_OVERRIDE",
	        "CAP_FSETID",
	        "CAP_FOWNER",
	        "CAP_MKNOD",
	        "CAP_NET_RAW",
	        "CAP_SETGID",
	        "CAP_SETUID",
	        "CAP_SETFCAP",
	        "CAP_SETPCAP",
	        "CAP_NET_BIND_SERVICE",
	        "CAP_SYS_CHROOT",
	        "CAP_KILL",
	        "CAP_AUDIT_WRITE"
	      ]
	    },
	    "rlimits": [
	      {
	        "type": "RLIMIT_NOFILE",
	        "hard": 1024,
	        "soft": 1024
	      }
	    ]
	  },
	  "root": {
	    "path": "/var/tmp/lolcow/rootfs"
	  },
	  "hostname": "mrsdalloway",
	  "mounts": [
	    {
	      "destination": "/proc",
	      "type": "proc",
	      "source": "proc"
	    },
	    {
	      "destination": "/dev",
	      "type": "tmpfs",
	      "source": "tmpfs",
	      "options": [
	        "nosuid",
	        "strictatime",
	        "mode=755",
	        "size=65536k"
	      ]
	    },
	    {
	      "destination": "/dev/pts",
	      "type": "devpts",
	      "source": "devpts",
	      "options": [
	        "nosuid",
	        "noexec",
	        "newinstance",
	        "ptmxmode=0666",
	        "mode=0620",
	        "gid=5"
	      ]
	    },
	    {
	      "destination": "/dev/shm",
	      "type": "tmpfs",
	      "source": "shm",
	      "options": [
	        "nosuid",
	        "noexec",
	        "nodev",
	        "mode=1777",
	        "size=65536k"
	      ]
	    },
	    {
	      "destination": "/dev/mqueue",
	      "type": "mqueue",
	      "source": "mqueue",
	      "options": [
	        "nosuid",
	        "noexec",
	        "nodev"
	      ]
	    },
	    {
	      "destination": "/sys",
	      "type": "sysfs",
	      "source": "sysfs",
	      "options": [
	        "nosuid",
	        "noexec",
	        "nodev",
	        "ro"
	      ]
	    }
	  ],
	  "linux": {
	    "resources": {
	      "devices": [
	        {
	          "allow": false,
	          "access": "rwm"
	        }
	      ]
	    },
	    "namespaces": [
	      {
	        "type": "pid"
	      },
	      {
	        "type": "network"
	      },
	      {
	        "type": "ipc"
	      },
	      {
	        "type": "uts"
	      },
	      {
	        "type": "mount"
	      }
	    ],
	    "seccomp": {
	      "defaultAction": "SCMP_ACT_ERRNO",
	      "architectures": [
	        "SCMP_ARCH_X86_64",
	        "SCMP_ARCH_X86",
	        "SCMP_ARCH_X32"
	      ],
	      "syscalls": [
	        {
	          "names": [
	            "accept",
	            "accept4",
	            "access",
	            "alarm",
	            "bind",
	            "brk",
	            "capget",
	            "capset",
	            "chdir",
	            "chmod",
	            "chown",
	            "chown32",
	            "clock_getres",
	            "clock_gettime",
	            "clock_nanosleep",
	            "close",
	            "connect",
	            "copy_file_range",
	            "creat",
	            "dup",
	            "dup2",
	            "dup3",
	            "epoll_create",
	            "epoll_create1",
	            "epoll_ctl",
	            "epoll_ctl_old",
	            "epoll_pwait",
	            "epoll_wait",
	            "epoll_wait_old",
	            "eventfd",
	            "eventfd2",
	            "execve",
	            "execveat",
	            "exit",
	            "exit_group",
	            "faccessat",
	            "fadvise64",
	            "fadvise64_64",
	            "fallocate",
	            "fanotify_mark",
	            "fchdir",
	            "fchmod",
	            "fchmodat",
	            "fchown",
	            "fchown32",
	            "fchownat",
	            "fcntl",
	            "fcntl64",
	            "fdatasync",
	            "fgetxattr",
	            "flistxattr",
	            "flock",
	            "fork",
	            "fremovexattr",
	            "fsetxattr",
	            "fstat",
	            "fstat64",
	            "fstatat64",
	            "fstatfs",
	            "fstatfs64",
	            "fsync",
	            "ftruncate",
	            "ftruncate64",
	            "futex",
	            "futimesat",
	            "getcpu",
	            "getcwd",
	            "getdents",
	            "getdents64",
	            "getegid",
	            "getegid32",
	            "geteuid",
	            "geteuid32",
	            "getgid",
	            "getgid32",
	            "getgroups",
	            "getgroups32",
	            "getitimer",
	            "getpeername",
	            "getpgid",
	            "getpgrp",
	            "getpid",
	            "getppid",
	            "getpriority",
	            "getrandom",
	            "getresgid",
	            "getresgid32",
	            "getresuid",
	            "getresuid32",
	            "getrlimit",
	            "get_robust_list",
	            "getrusage",
	            "getsid",
	            "getsockname",
	            "getsockopt",
	            "get_thread_area",
	            "gettid",
	            "gettimeofday",
	            "getuid",
	            "getuid32",
	            "getxattr",
	            "inotify_add_watch",
	            "inotify_init",
	            "inotify_init1",
	            "inotify_rm_watch",
	            "io_cancel",
	            "ioctl",
	            "io_destroy",
	            "io_getevents",
	            "ioprio_get",
	            "ioprio_set",
	            "io_setup",
	            "io_submit",
	            "ipc",
	            "kill",
	            "lchown",
	            "lchown32",
	            "lgetxattr",
	            "link",
	            "linkat",
	            "listen",
	            "listxattr",
	            "llistxattr",
	            "_llseek",
	            "lremovexattr",
	            "lseek",
	            "lsetxattr",
	            "lstat",
	            "lstat64",
	            "madvise",
	            "memfd_create",
	            "mincore",
	            "mkdir",
	            "mkdirat",
	            "mknod",
	            "mknodat",
	            "mlock",
	            "mlock2",
	            "mlockall",
	            "mmap",
	            "mmap2",
	            "mprotect",
	            "mq_getsetattr",
	            "mq_notify",
	            "mq_open",
	            "mq_timedreceive",
	            "mq_timedsend",
	            "mq_unlink",
	            "mremap",
	            "msgctl",
	            "msgget",
	            "msgrcv",
	            "msgsnd",
	            "msync",
	            "munlock",
	            "munlockall",
	            "munmap",
	            "nanosleep",
	            "newfstatat",
	            "_newselect",
	            "open",
	            "openat",
	            "pause",
	            "pipe",
	            "pipe2",
	            "poll",
	            "ppoll",
	            "prctl",
	            "pread64",
	            "preadv",
	            "prlimit64",
	            "pselect6",
	            "pwrite64",
	            "pwritev",
	            "read",
	            "readahead",
	            "readlink",
	            "readlinkat",
	            "readv",
	            "recv",
	            "recvfrom",
	            "recvmmsg",
	            "recvmsg",
	            "remap_file_pages",
	            "removexattr",
	            "rename",
	            "renameat",
	            "renameat2",
	            "restart_syscall",
	            "rmdir",
	            "rt_sigaction",
	            "rt_sigpending",
	            "rt_sigprocmask",
	            "rt_sigqueueinfo",
	            "rt_sigreturn",
	            "rt_sigsuspend",
	            "rt_sigtimedwait",
	            "rt_tgsigqueueinfo",
	            "sched_getaffinity",
	            "sched_getattr",
	            "sched_getparam",
	            "sched_get_priority_max",
	            "sched_get_priority_min",
	            "sched_getscheduler",
	            "sched_rr_get_interval",
	            "sched_setaffinity",
	            "sched_setattr",
	            "sched_setparam",
	            "sched_setscheduler",
	            "sched_yield",
	            "seccomp",
	            "select",
	            "semctl",
	            "semget",
	            "semop",
	            "semtimedop",
	            "send",
	            "sendfile",
	            "sendfile64",
	            "sendmmsg",
	            "sendmsg",
	            "sendto",
	            "setfsgid",
	            "setfsgid32",
	            "setfsuid",
	            "setfsuid32",
	            "setgid",
	            "setgid32",
	            "setgroups",
	            "setgroups32",
	            "setitimer",
	            "setpgid",
	            "setpriority",
	            "setregid",
	            "setregid32",
	            "setresgid",
	            "setresgid32",
	            "setresuid",
	            "setresuid32",
	            "setreuid",
	            "setreuid32",
	            "setrlimit",
	            "set_robust_list",
	            "setsid",
	            "setsockopt",
	            "set_thread_area",
	            "set_tid_address",
	            "setuid",
	            "setuid32",
	            "setxattr",
	            "shmat",
	            "shmctl",
	            "shmdt",
	            "shmget",
	            "shutdown",
	            "sigaltstack",
	            "signalfd",
	            "signalfd4",
	            "sigreturn",
	            "socket",
	            "socketcall",
	            "socketpair",
	            "splice",
	            "stat",
	            "stat64",
	            "statfs",
	            "statfs64",
	            "symlink",
	            "symlinkat",
	            "sync",
	            "sync_file_range",
	            "syncfs",
	            "sysinfo",
	            "syslog",
	            "tee",
	            "tgkill",
	            "time",
	            "timer_create",
	            "timer_delete",
	            "timerfd_create",
	            "timerfd_gettime",
	            "timerfd_settime",
	            "timer_getoverrun",
	            "timer_gettime",
	            "timer_settime",
	            "times",
	            "tkill",
	            "truncate",
	            "truncate64",
	            "ugetrlimit",
	            "umask",
	            "uname",
	            "unlink",
	            "unlinkat",
	            "utime",
	            "utimensat",
	            "utimes",
	            "vfork",
	            "vmsplice",
	            "wait4",
	            "waitid",
	            "waitpid",
	            "write",
	            "writev"
	          ],
	          "action": "SCMP_ACT_ALLOW"
	        },
	        {
	          "names": [
	            "personality"
	          ],
	          "action": "SCMP_ACT_ALLOW",
	          "args": [
	            {
	              "index": 0,
	              "value": 0,
	              "op": "SCMP_CMP_EQ"
	            },
	            {
	              "index": 0,
	              "value": 8,
	              "op": "SCMP_CMP_EQ"
	            },
	            {
	              "index": 0,
	              "value": 4294967295,
	              "op": "SCMP_CMP_EQ"
	            }
	          ]
	        },
	        {
	          "names": [
	            "chroot"
	          ],
	          "action": "SCMP_ACT_ALLOW"
	        },
	        {
	          "names": [
	            "clone"
	          ],
	          "action": "SCMP_ACT_ALLOW",
	          "args": [
	            {
	              "index": 0,
	              "value": 2080505856,
	              "op": "SCMP_CMP_MASKED_EQ"
	            }
	          ]
	        },
	        {
	          "names": [
	            "arch_prctl"
	          ],
	          "action": "SCMP_ACT_ALLOW"
	        },
	        {
	          "names": [
	            "modify_ldt"
	          ],
	          "action": "SCMP_ACT_ALLOW"
	        }
	      ]
	    }
	  }
	}

Furthermore, and through use of ``$ sudo cat /var/tmp/lolcow/config.json | jq [.root.path]``, the property

.. code-block:: json

	[
	  "/var/tmp/lolcow/rootfs"
	]

identifies ``/var/tmp/lolcow/rootfs`` as the container's root filesystem, as required by the standard; this filesystem has contents:

.. code-block:: none

	$ sudo ls /var/tmp/lolcow/rootfs
	bin   core  environment  home  lib64  mnt  proc  run   singularity  sys  usr
	boot  dev   etc		 lib   media  opt  root  sbin  srv	    tmp  var

.. note::

	``environment`` and ``singularity`` above are symbolic links to the ``.singularity.d`` directory. 

.. TODO Is the ``.singularity.d`` ignored in this case? Relates to the other quote I lifted ... 

	"The definition of a bundle is only concerned with how a container, and its configuration data, are stored on a local filesystem so that it can be consumed by a compliant runtime."

Beyond ``root.path``, the ``config.json`` file includes a multitude of additional properties - for example:

	- ``ociVersion`` - a mandatory property that identifies the version of the OCI runtime specification that the bundle is compliant with 

	- ``process`` - an optional property that specifies the container process. When invoked via Singularity, subproperties such as ``args`` are populated by making use of the contents of the ``.singularity.d`` directory, e.g. via ``$ sudo cat /var/tmp/lolcow/config.json | jq [.process.args]``:

	.. code-block:: json

		[
		  [
		    "/.singularity.d/actions/run"
		  ]
		]

	where ``run`` equates to the :ref:`familiar runscript <sec:inspect_container_metadata>` for this container. 

For a comprehensive discussion of all the ``config.json`` file properties, refer to the `implementation guide <https://github.com/opencontainers/runtime-spec/blob/master/config.md>`_. 

Technically, the ``overlay`` directory was *not* content expected of an OCI compliant filesystem bundle. As detailed in the section dedicated to `Persistent Overlays <https://www.sylabs.io/guides/3.0/user-guide/persistent_overlays.html>`_, these directories allow for the introduction of 
a writable file system on an otherwise immutable read-only container; thus they permit the illusion of read-write access.

.. TODO Need to ensure that what's written above is correct 

.. note::

	SIF is stated to be an extensible format capable of encasulating the entire container runtime in a single file. By encapsulating a filesystem bundle that conforms with the OCI runtime specification, the extensibility of SIF is demonstrably evident.


------------------------------------------
Creating OCI Compliant Container Instances 
------------------------------------------

SIF files encapsulate filesystem bundles that conform with the OCI runtime specification. By 'OCI mounting' a SIF file (see above), this encapsulated filesystem bundle is exposed. Once exposed, the filesystem bundle can be used to bootstrap the creation of an OCI compliant container instance as follows: 

.. code-block:: none

	$ sudo singularity oci create -b /var/tmp/lolcow lolcow 

In this example, the filesystem bundle is located in the directory ``/var/tmp/lolcow`` - i.e., the mount point identified above with respect to 'OCI mounting'. The ``config.json`` file, along with the ``rootfs`` and ``overlay`` filesystems, are all employed in the bootstrap process. The instance is named ``lolcow`` in this example. 

.. note::

	The outcome of this creation request is truly a container **instance**. Multiple instances of the same container can easily be created by simply changing the name of the instance upon subsequent invocation requests. 

The ``state`` of the container instance can be determined via ``$ sudo singularity oci state lolcow``:

.. code-block:: json

	{
		"ociVersion": "1.0.1-dev",
		"id": "lolcow",
		"status": "created",
		"pid": 3759,
		"bundle": "/var/tmp/lolcow",
		"createdAt": 1553794727524020213,
		"attachSocket": "/var/run/singularity/instances/root/lolcow/attach.sock",
		"controlSocket": "/var/run/singularity/instances/root/lolcow/control.sock"
	}

.. TODO Confirmm the above is OCI stnadrads compliant ^^^ 

Whereas the above is provided via the OCI command group, container instances created in this fashion are still known to Singularity - for example: 

.. code-block:: none

	$ sudo singularity instance list
	INSTANCE NAME    PID      IMAGE
	lolcow           3759     /var/tmp/lolcow/var/tmp/lolcow/rootfs
	lolcow2          4014     /var/tmp/lolcow/var/tmp/lolcow/rootfs
	lolcow3          3938     /var/tmp/lolcow/var/tmp/lolcow/rootfs

Because these three instances are owned by ``root``, use of ``sudo`` is *required* here. 

.. TODO - illustrate use of cgroups 


.. ------------------------------------------
.. Starting OCI Compliant Container Instances 
.. ------------------------------------------


.. $ sudo singularity oci start lolcow
.. vagrant@vagrant:~$  _______________________________________
.. / So so is good, very good, very        \
.. | excellent good: and yet it is not; it |
.. | is but so so.                         |
.. |                                       |
.. | -- William Shakespeare, "As You Like  |
.. \ It"                                   /
..  ---------------------------------------
..         \   ^__^
..          \  (oo)\_______
..             (__)\       )\/\
..                 ||----w |
..                 ||     ||

.. ~$ sudo singularity oci state lolcow
.. {
.. 	"ociVersion": "1.0.1-dev",
.. 	"id": "lolcow",
.. 	"status": "stopped",
.. 	"pid": 3759,
.. 	"bundle": "/var/tmp/lolcow",
.. 	"createdAt": 1553794727524020213,
.. 	"startedAt": 1553799071388238359,
.. 	"finishedAt": 1553799071604837173,
.. 	"exitCode": 0,
.. 	"exitDesc": "exited with code 0",
.. 	"attachSocket": "/var/run/singularity/instances/root/lolcow/attach.sock",
.. 	"controlSocket": "/var/run/singularity/instances/root/lolcow/control.sock"
.. }

.. TODO Review CC's responses again ... see GDocs note on March 20, 2019

.. TODO Highlight UID & GID ??? 

.. TODO What is an overlay fs?  ^^^ https://www.datalight.com/blog/2016/01/27/explaining-overlayfs-%E2%80%93-what-it-does-and-how-it-works/ 
.. Check again after I create a bundle and container ... 

.. sandbox???