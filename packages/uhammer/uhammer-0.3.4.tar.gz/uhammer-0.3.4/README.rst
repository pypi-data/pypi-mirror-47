About uhammer
==============

``uhammer`` offers a convenience layer for ``emcee``.

Features: ``uhammer``

- offers a simplified API.
- requires no code changes between running on multiple cores or with MPI.
- fixes some issues with the MPI Pool from emcee / schwimmbad.
- prints diagnostic messages when allocated nodes / cores do not fit well to specified
  number of walkers or other parallelization related settings.
- can capture worker specific output to separate files.
- implements persisting of sampler state and supports continuation of sampling at a later time.
- can show an animated progress bar.


Example usage
-------------

To use ``uhammer`` you need:

- an instance of ``Parameters`` for declaring the
  parameters you want to sample from.

- a function, e.g. named ``lnprob``, which takes a parameters object and possible
  extra arguments. This function returns the logarithic value of the computed
  posterior probability.

- finally you call ``sample`` for running the sampler.

.. code-block:: python

   import time

   import numpy as np

   from uhammer import Parameters, sample

   sigma = .5


   def gen_data():
      a0 = .5
      b0 = .5
      c0 = 1

      x = np.linspace(-2, 2, 100)
      y_measured = a0 + b0 * x + c0 * x ** 2 + sigma * np.random.randn(*x.shape)
      return x, y_measured


   p = Parameters()
   p.add("a", (0, 1))
   p.add("b", (0, 1))
   p.add("c", (0, 2))


   def lnprob(p, x, y_measured):
      time.sleep(.0002)
      y = p.a + p.b * x + p.c * x ** 2
      diff = (y - y_measured) / sigma
      return -np.dot(diff.T, diff) / 2


   n_samples = 15000
   n_walkers_per_param = 200


   samples, lnprobs = sample(
      lnprob,
      p,
      args=gen_data(),
      n_walkers_per_param=n_walkers_per_param,
      n_samples=n_samples,
      show_progress=True,
      show_output=False,
   )

   print()
   print(samples[5000:].mean(axis=0))

.. code-block:: shell-session

  $ python examples/sample_line_fit.py
  uhammer: perform 25 steps of emcee sampler
  ✗ passed: 00:00:11.2 left: 00:00:00.0 - [∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣∣]

  [0.52389808 0.53415134 1.01585175]




Credits
-------

This package was created with Cookiecutter_ and the `uweschmitt/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`uweschmitt/cookiecutter-pypackage`: https://github.com/uweschmitt/cookiecutter-pypackage
