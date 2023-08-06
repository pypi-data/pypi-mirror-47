=========
uhammer
=========

`uhammer` offers a convenience layer for `emcee`.

Features: `uhammer`

- offers a simplified API.
- requires no code changes between running on multiple cores or with MPI.
- fixes some issues with the MPI Pool from emcee / schwimmbad.
- prints diagnostic messages when allocated nodes / cores do not fit well to specified
  number of walkers or other parallelization related settings.
- can capture worker specific output to separate files.
- implements persisting of sampler state and supports continuation of sampling at a later time.
- can show an animated progress bar.


Credits
-------

This package was created with Cookiecutter_ and the `uweschmitt/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`uweschmitt/cookiecutter-pypackage`: https://github.com/uweschmitt/cookiecutter-pypackage
