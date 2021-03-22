=====
Usage
=====

To use FastABM in a project::

    import fastabm

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all tests run successfully (using tox) and then all your changes are committed.
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags