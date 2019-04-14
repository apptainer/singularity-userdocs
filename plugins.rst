.. _plugins:

=======
Plugins
=======

--------
Overview
--------

A Singularity plugin is a package that can be dynamically loaded by the
Singularity runtime, augmenting Singularity with experimental, non-standard
and/or vendor-specific functionality. Currently, plugins are able to add
commands and flags to Singularity. In the future, plugins will also be able to
interface with more complex subsystems of the Singularity runtime.

-------------
Using Plugins
-------------

The ``list`` command prints the currently installed plugins.

.. code-block:: none

    $ singularity plugin list
    There are no plugins installed.

Plugins are packaged and distributed as binaries encoded with the versatile
Singularity Image Format (SIF). However, plugin authors may also distribute the
source code of their plugins. A plugin can be compiled from its source code
with the ``compile`` command. A sample plugin ``test-plugin`` is included with
the Singularity source code.

.. code-block:: none

    $ singularity plugin compile examples/plugins/test-plugin/

Upon successful compilation, a SIF file will appear in the directory of the
plugin's source code.

.. code-block:: none

    $ ls examples/plugins/test-plugin/ | grep sif
    test-plugin.sif

.. note::

    Currently, **all** plugins must be compiled from the Singularity source
    code tree.

Every plugin encapsulates various information such as the plugin's author, the
plugin's version, etc. To view this information about a plugin, use the
``inspect`` command.

.. code-block:: none

    $ singularity plugin inspect examples/plugins/test-plugin/test-plugin.sif
    Name: sylabs.io/test-plugin
    Description: This is a short test plugin for Singularity
    Author: Michael Bauer
    Version: 0.0.1

To install a plugin, use the ``install`` command. This operation requires root
privilege.

.. code-block:: none

    $ sudo singularity plugin install examples/plugins/test-plugin/test-plugin.sif
    $ singularity plugin list
    ENABLED  NAME
        yes  sylabs.io/test-plugin

After successful installation, the plugin will automatically be enabled. Any
plugin can be disabled with the ``disable`` command and re-enabled with the
``enable`` command. Both of these operations require root privilege.

.. code-block:: none

    $ sudo singularity plugin disable sylabs.io/test-plugin
    $ singularity plugin list
    ENABLED  NAME
         no  sylabs.io/test-plugin
    $ sudo singularity plugin enable sylabs.io/test-plugin
    $ singularity plugin list
    ENABLED  NAME
        yes  sylabs.io/test-plugin

Finally, to uninstall a plugin, use the ``uninstall`` command. This operation
requires root privilege.

.. code-block:: none

    $ sudo singularity plugin uninstall sylabs.io/test-plugin
    Uninstalled plugin "sylabs.io/test-plugin".
    $ singularity plugin list
    There are no plugins installed.
