.. _contributing:

============
Contributing
============

-------------------
Support Singularity
-------------------

Singularity is an open source project, meaning we have the challenge of limited resources.
We are grateful for any support that you might offer to other users in the way of helping with issues, documentation,
or code! If you haven’t already, check out some of the ways to contribute to code and docs:

.. _contribute-to-the-code:

-  `Contribute code <#contribute-to-the-code>`_

.. _contributing-to-documentation:

-  `Contribute docs <#contributing-to-documentation>`_

Singularity Google Group
========================

This is a huge endeavor, and it is greatly appreciated! If you have been using Singularity and having good luck with it,
join our `Google Group <https://groups.google.com/a/lbl.gov/forum/#!forum/singularity>`_  and help out other users! Post to online communities about Singularity, and request that your distribution vendor,
service provider, and system administrators include Singularity for you!

Singularity on Slack
====================

Many of our users come to Slack for quick help with an issue. You can find us at `singularity-container <https://singularity-container.slack.com/>`_.

----------------------
Contribute to the code
----------------------

To contribute to the development of Singularity, you must:

-  Own the code and/or have the right to contribute it.

-  Be able to submit software under the ``3 clause BSD`` (or equivalent) license (while other licenses are allowed to be submitted by the license, acceptance of any contribution is up to the project lead).

-  Read, understand, and agree to the license.

-  Have a GitHub account (this just makes it easier for me).

We use the traditional `GitHub Flow <https://guides.github.com/introduction/flow/>`_ to develop. This means that you fork the repo and checkout a branch to make changes, you submit a pull request (PR) to the development branch with your changes, and the development branch gets merged with master for official releases.
We also have an official `CONTRIBUTING <https://github.com/sylabs/singularity/blob/master/CONTRIBUTING.md>`_ document, which also includes a `code of conduct <https://github.com/sylabs/singularity/blob/master/CONTRIBUTING.md#code-of-conduct>`_.


Step 1. Fork the repo
=====================

To contribute to Singularity, you should obtain a GitHub account and fork the `Singularity <https://github.com/sylabs/singularity>`_ repository.
Once forked, you will want to clone the fork of the repo to your computer. Let’s say my GitHub username is vsoch, and I am using ssh:

.. code-block:: none

    git clone git@github.com:vsoch/singularity.git

    cd singularity/


Step 2. Set up your config
==========================

The GitHub config file, located at .git/config, is the best way to keep track of many different forks of a repository.
I usually open it up right after cloning my fork to add the repository that I forked as a `remote <https://help.github.com/articles/adding-a-remote/>`_, so I can easily get updated from it.
Let’s say my ``.git/config`` first looks like this, after I clone my own branch:

.. code-block:: none

    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
    [remote "origin"]
        url = git@github.com:vsoch/singularity
        fetch = +refs/heads/*:refs/remotes/origin/*
    [branch "master"]
        remote = origin
        merge = refs/heads/master

I would want to add the upstream repository, which is where I forked from.

.. code-block:: none

    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
    [remote "origin"]
        url = git@github.com:vsoch/singularity
        fetch = +refs/heads/*:refs/remotes/origin/*
    [remote "upstream"]
        url = https://github.com/sylabs/singularity
        fetch = +refs/heads/*:refs/remotes/origin/*
    [branch "master"]
        remote = origin
        merge = refs/heads/master

I can also add some of my colleagues, if I want to pull from their branches:

.. code-block:: none

    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
    [remote "origin"]
        url = git@github.com:vsoch/singularity
        fetch = +refs/heads/*:refs/remotes/origin/*
    [remote "upstream"]
        url = https://github.com/sylabs/singularity
        fetch = +refs/heads/*:refs/remotes/origin/*
    [remote "greg"]
        url = https://github.com/gmkurtzer/singularity
        fetch = +refs/heads/*:refs/remotes/origin/*
    [branch "master"]
        remote = origin
        merge = refs/heads/master

In the GitHub flow, the master branch is the frozen, current version of the software.
Your master branch is always in sync with the upstream (our Sylabs master), and the Sylabs master is always the latest release of Singularity.

This would mean that I can update my master branch as follows:

.. code-block:: none

    git checkout master
    
    git pull upstream master
    
    git push origin master


and then I would return to working on the branch for my feature. How to do that exactly? Read on!

Step 3. Checkout a new branch
=============================

`Branches <https://guides.github.com/introduction/flow//>`_ are a way of isolating your features from the main branch. Given that we’ve just cloned the repo, we probably want to work off of the current development branch, which has the most up to date “next version” of the software. So we can start by checking out that branch:



.. code-block:: none

    git checkout -b development
    
    git pull origin development


At this point, you can either choose to work on this branch, push to your origin development and pull request to Sylabs development, or you can checkout another branch specific to your feature. We recommend always working from, and staying, in sync with development. The command below would checkout a branch called ``add/my-awesome-new-feature`` from development.

.. code-block:: none

    # Checkout a new branch called add/my-awesome-feature
    git checkout -b add/my-awesome-feature development


The addition of the ``-b`` argument tells git that we want to make a new branch. If I want to just change branches (for example back to master) I can do the same command without ``-b``:

.. code-block:: none

    # Change back to master

    git checkout master


Note that you should commit changes to the branch you are working on before changing branches, otherwise they would be lost. GitHub will give you a warning and prevent you from changing branches if this is the case, so don’t worry too much about it.


Step 4. Make your changes
=========================

On your new branch, go nuts! Make changes, test them, and when you are happy with a bit of progress, commit the changes to the branch:

.. code-block:: none

    git add file-changed1 files-chenged2
    
    git commit -m "what changed?"

This commit message is important - it should describe exactly the changes that you have made. Bad commit messages are like:

- changed code

- updated files

Good commit messages are like:

- changed function “get_config” in functions.py to output csv to fix #2

- updated docs about shell to close #10

The tags “close #10” and “fix #2” are referencing issues that are posted on the main repo you are going to do a pull request to. Given that your fix is merged into the master branch, these messages will automatically close the issues, and further, it will link your commits directly to the issues they intended to fix. This is very important down the line if someone wants to understand your contribution, or (hopefully not) revert the code back to a previous version.

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

Once you have pushed your branch, then you can go to either fork and (in the GUI) `submit a Pull Request <https://help.github.com/articles/creating-a-pull-request/>`_. Regardless of the name of your branch, your PR should be submitted to the Sylabs development branch. This will open up a nice conversation interface / forum for the developers of Singularity to discuss your contribution, likely after testing. At this time, any continuous integration that is linked with the code base will also be run. If there is an issue, you can continue to push commits to your branch and it will update the Pull Request.

Support, helping, and spreading the word!
========================================

This is a huge endeavor, and it is greatly appreciated! If you have been using Singularity and having good luck with it, join our `Google Group <https://groups.google.com/a/lbl.gov/forum/#!forum/singularity>`_ and help out other users! Post to online communities about Singularity, and request that your distribution vendor, service provider, and system administrators include Singularity for you!

-----------------------------
Contributing to Documentation
-----------------------------

We (like almost all open source software providers) have a documentation dilemma… We tend to focus on the code features and functionality before working on documentation. And there is very good reason for this: we want to share the love so nobody feels left out!

You can contribute to the documentation by sending a `pull request <https://help.github.com/articles/about-pull-requests/>`_ on our repository for documentation.

The current documentation is generated with:

- `reStructured Text (RST) <http://docutils.sourceforge.net/rst.html>`_ and `ReadTheDocs <https://readthedocs.org/>`_

Other dependencies include:

- `Python 2.7 <https://www.python.org/download/releases/2.7/>`_

- `Sphinx <https://pypi.org/project/Sphinx/>`_

More information about contributing to the documentation, and the instructions on how to install the dependencies, and how to generate the files can be obtained `here <https://github.com/sylabs/singularity-userdocs#singularity-user-docs>`_.
