.. _contributing:

============
Contributing
============

-------------------
Support Singularity
-------------------

Singularity is an open source project, meaning we have the challenge of limited resources.
We are grateful for any support that you might offer to other users in the way of helping with issues, documentation,
or code! If you haven’t already, check out some of the ways to contribute: to docs, code, and issue reporting:

-  `Contribute docs <#contributing-to-documentation>`_

-  `Contribute code <#contribute-to-the-code>`_

-  `Report a Issue <#reporting-a-issue>`_


Singularity Google Group
========================

This is a huge endeavor, and it is greatly appreciated! If you have been using Singularity and having good luck with it,
join our `Google Group <https://groups.google.com/a/lbl.gov/forum/#!forum/singularity>`_  and help out other users! Post to online communities about Singularity, and request that your distribution vendor,
service provider, and system administrators include Singularity for you!

Singularity on Slack
====================

Many of our users come to Slack for quick help with an issue. You can find us at `singularity-container <https://singularity-container.slack.com/>`_.

.. _contributing-to-documentation:

-----------------------------
Contributing to Documentation
-----------------------------

We (like almost all open source software providers) have a documentation dilemma… We tend to focus on the code features and functionality before working on documentation. And there is very good reason for this: we want to share the love so nobody feels left out!

You can contribute to the documentation by sending a `pull request <https://help.github.com/articles/about-pull-requests/>`_ on our repository for documentation.

The current documentation is generated with:

- `reStructured Text (RST) <http://docutils.sourceforge.net/rst.html>`_ and `ReadTheDocs <https://readthedocs.org/>`_.

Other dependencies include:

- `Python 2.7 <https://www.python.org/download/releases/2.7/>`_.

- `Sphinx <https://pypi.org/project/Sphinx/>`_.

More information about contributing to the documentation, and the instructions on how to install the dependencies, and how to generate the files can be obtained `here <https://github.com/sylabs/singularity-userdocs/blob/master/README.md#singularity-user-docs>`_.

.. _contribute-to-the-code:

----------------------
Contribute to the code
----------------------

We use the traditional `GitHub Flow <https://guides.github.com/introduction/flow/>`_ to develop. This means that you fork the repo and checkout a branch to make changes, you submit a pull request (PR) to the development branch with your changes, and the development branch gets merged with master for official releases.

Check out our official `CONTRIBUTING <https://github.com/sylabs/singularity/blob/master/CONTRIBUTING.md>`_ document, which also includes a `code of conduct <https://github.com/sylabs/singularity/blob/master/CONTRIBUTING.md#code-of-conduct>`_.


Step 1. Fork the repo
=====================

To contribute to Singularity, you should obtain a GitHub account and fork the `Singularity <https://github.com/sylabs/singularity>`_ repository. Once forked, you will want to clone the fork of the repo to your computer: (obviously, you should replace ``your-username`` with your GitHub username)

.. code-block:: none

    git clone https://github.com/your-username/singularity.git

    cd singularity/


Now, we need to checkout are branch, more-content...

.. code-block:: none

    git checkout master
    
    git pull upstream master
    
    git push origin master


Step 3. Checkout a new branch
=============================

`Branches <https://guides.github.com/introduction/flow//>`_ are a way of isolating your features from the main branch. Given that we’ve just cloned the repo, we probably want to work off of the current development branch, which has the most up to date “next version” of the software. So we can start by checking-out that branch:

.. code-block:: none

    git checkout -b development
    
    git pull origin development


At this point, you can either choose to work on this branch, push to your origin development and pull request to Sylabs development, or you can checkout another branch specific to your feature. We recommend always working from, and staying, in sync with development. The command below would checkout a branch called ``my-awesome-new-feature`` from development.

.. code-block:: none

    # Checkout a new branch called my-awesome-feature
    
    git checkout -b my-awesome-feature development

Note that you should commit changes to the branch you are working on before changing branches, otherwise they would be lost. GitHub will give you a warning and prevent you from changing branches if this is the case, so don’t worry too much about it.


Step 4. Make your changes
=========================

On your new branch, go nuts! Make changes, test them, and when you are happy with a bit of progress, commit the changes to
the branch:

.. code-block:: none

    git add file-changed1 files-chenged2
    
    git commit -m "what changed?"

This commit message is important - it should describe exactly the changes that you have made. Good commit messages are like:

- ``changed function get_config in functions.py to output csv to fix #2``

- ``updated docs about shell to close #10``

The tags ``close #10`` and ``fix #2`` are referencing issues that are posted on the main repo you are going to do a pull request to. Given that your fix is merged into the master branch, these messages will automatically close the issues, and further, it will link your commits directly to the issues they intended to fix. This is very important down the line if someone wants to understand your contribution, or (hopefully not) revert the code back to a previous version.

Step 5. Push your branch to your fork
=====================================

When you are done with your commits, you should push your branch to your fork (and you can also continuously push commits here as you work):

.. code-block:: none

    git push origin my-awesome-feature


Note that you should always check the status of your branches to see what has been pushed (or not):

.. code-block:: none

    git status


Step 6. Submit a Pull Request
=============================

Once you have pushed your branch, then you can go to either fork and (in the GUI) `submit a Pull Request
<https://help.github.com/articles/creating-a-pull-request/>`_. Regardless of the name of your branch, your PR should be
submitted to the Sylabs development branch. This will open up a nice conversation interface / forum for the developers of
Singularity to discuss your contribution, likely after testing. At this time, any continuous integration that is linked with
the code base will also be run. If there is an issue, you can continue to push commits to your branch and it will update the
Pull Request.

Support, helping, and spreading the word!
=========================================

This is a huge endeavor, and it is greatly appreciated! If you have been using Singularity and having good luck with it, join our `Google Group <https://groups.google.com/a/lbl.gov/forum/#!forum/singularity>`_ and help out other users! Post to online communities about Singularity, and request that your distribution vendor, service provider, and system administrators include Singularity for you!

.. _report-a-issue:

-----------------
Reporting a Issue
-----------------


For general bugs/issues, you can open a issue `at our GitHub repo <https://github.com/sylabs/singularity>`_. However, if you find a security related issue/problem, please email us instead at `security@sylabs.io <mailto:security@sylabs.io>`_.



