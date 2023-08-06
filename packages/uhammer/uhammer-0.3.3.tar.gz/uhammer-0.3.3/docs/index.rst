Welcome to uhammers's documentation!
======================================

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

Contents
--------

.. toctree::
   :maxdepth: 1

   installation
   usage
   modules
   authors
   history


Example usage
-------------

To use `uhammer` you need:

- an instance of :py:class:`~uhammer.parameters.Parameters` for declaring the
  parameters you want to sample from.

- a function, e.g. named ``lnprob``, which takes a parameters object and possible
  extra arguments. This function returns the logarithic value of the computed
  posterior probability.

- finally you call :py:func:`~uhammer.sampler.sample` for running the sampler.
  Click at         :py:func:`~uhammer.sampler.sample` to see all options.

.. literalinclude:: ../examples/sample_line_fit.py

.. code-block:: shell-session

  $ python examples/sample_line_fit.py
  uhammer: capture (hide) output during sampling.
  uhammer: perform 25 steps of emcee sampler
  ✗ passed: 00:00:00.4 left: -1:59:60.0 - [∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣]

  [0.50197292 0.48450715 0.96744469]



Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
