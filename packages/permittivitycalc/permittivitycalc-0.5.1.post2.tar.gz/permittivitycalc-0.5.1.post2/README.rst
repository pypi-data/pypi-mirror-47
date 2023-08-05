permittivitycalc 
================

+-------------------------+---------------+-----------------+---------------+
| Continuous Integration  | Code Coverage | PyPI Package    | Citation      |
+=========================+===============+=================+===============+
|  |TravisCI| |Appveyor|  |   |Codecov|   |   |PyPiBadge|   |   |DOIBadge|  |
+-------------------------+---------------+-----------------+---------------+

.. |TravisCI| image:: https://travis-ci.org/boivinalex/permittivitycalc.svg?branch=master
    :target: https://travis-ci.org/boivinalex/permittivitycalc

.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/xh0t09l9hnnpn0po/branch/master?svg=true
	:target: https://ci.appveyor.com/project/boivinalex/permittivitycalc

.. |Codecov| image:: https://codecov.io/gh/boivinalex/permittivitycalc/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/boivinalex/permittivitycalc

.. |PyPiBadge| image:: https://badge.fury.io/py/permittivitycalc.svg
    :target: https://badge.fury.io/py/permittivitycalc

.. |DOIBadge| image:: https://zenodo.org/badge/98680301.svg
   :target: https://zenodo.org/badge/latestdoi/98680301

Scripts to calculate and plot the complex permittivity from S-parameter data acquired with transmission-line measurements

Overview
--------
permittivitycalc is a Python package made to take S-parameter data output from METAS VNA Tools II (https://www.metas.ch/vnatools) and process it to calculate and plot the complex permittivity of a material measured in a coaxial transmission line.

Currently, permittivitycalc uses the New Non-iterative Method for permittivity calculation from S-parameters from [Boughriet1997]_ which assumes that the material is non-magnetic (i.e. \mu = 1).

permittivitycalc can also use the Nicholson-Ross-Weir method to calculate the complex permittivity and permeability of a sample. This method, however, is unstable at multiples of one-half wavelength in the sample [NicolsonRoss1970]_ [Weir1974]_.

You can use permittivitycalc to:

- Input and plot raw S-parameter data in tabular form with or without uncertainties.
- Calculate and plot the complex permittivity with full propagation of uncertainties.
- Perform connector de-embedding on the raw S-parameters to extract the sample S-parameters, if necessary. Example: de-embedding washers used to cap the transmission line when measuring powdered samples.
- Correct for the boundary effect in the transmission line when measuring powdered samples after [Hickson2017]_.
- Correct for the air gap when measuring solid samples after [Baker-Jarvis1993]_.
- Plot data from multiple measurements together for comparison.

Usage
-----
For usage examples and a walkthrough on how to use permittivitycalc, see the `Tutorial <https://gist.github.com/boivinalex/175313bf8fdfa0dfd6a7501cf8a28087>`_

Installation
------------

Requirements
^^^^^^^^^^^^

permittivitycalc was written for Python 3 and tested on the following versions of Python:

- 3.6

permittivitycalc uses the following packages:

- tkinter
- numpy 
- uncertainties
- scipy
- matplotlib
- seaborn
- cycler

Installing Anaconda
^^^^^^^^^^^^^^^^^^^

We recommend using `Anaconda`_ to manage your Python environments.

.. _`Anaconda`: https://www.anaconda.com/distribution/

1. `Install Anaconda <https://www.anaconda.com/download/>`_.

2. Open a terminal window and create a `conda virtual environment`_ (name it anything you like, and set the python version to a compatible version in `Requirements`_)::

    conda create --name your_env_name python=3.6

3. Activate the environment (on Windows, omit "source")::

    source activate your_env_name

.. _`conda virtual environment`: https://conda.io/docs/using/envs

Quick Install
^^^^^^^^^^^^^

Install permittivitycalc with pip::

	pip install permittivitycalc

Manual Install
^^^^^^^^^^^^^^

1. (Optional) Fork `permittivitycalc on Github <https://github.com/boivinalex/permittivitycalc>`_

2. Clone or download the repository.

3. Navigate to the permittivitycalc root directory and install with::

	python setup.py install

Contributors
------------
permittivitycalc was developed with the aid of these `contributors <https://github.com/boivinalex/permittivitycalc/graphs/contributors>`_.

References
----------
.. [Baker-Jarvis1993] Baker-Jarvis, J., Janezic, M. D., Grosvenor Jr, J. H., & Geyer, R. G. (1993). Transmission/reflection and short-circuit line methods for measuring permittivity and permeability. NIST Technical Note 1355-R. Boulder, CO. http://doi.org/10.6028/NIST.TN.1355r
.. [Boughriet1997] Boughriet, A. H., Legrand, C., & Chapoton, A. (1997). Noniterative stable transmission/reflection method for low-loss material complex permittivity determination. IEEE Transactions on Microwave Theory and Techniques, 45(1), 52–57. http://doi.org/10.1109/22.552032
.. [Hickson2017] Hickson, D., Sotodeh, S., Daly, M. G., Ghent, R., & Nolan, M. C. (2017). Improvements on effective permittivity measurements of powdered alumina: Implications for bulk permittivity properties of asteroid regoliths. Advances in Space Research, 59(1), 472–482. http://doi.org/10.1016/j.asr.2016.08.011
.. [NicolsonRoss1970] Nicolson, A. M., & Ross, G. F. (1970). Measurement of the Intrinsic Properties of Materials by Time-Domain Techniques. IEEE Transactions on Instrumentation and Measurement, 19(4), 377–382. http://doi.org/10.1109/TIM.1970.4313932
.. [Weir1974] Weir, W. B. (1974). Automatic Measurement of Complex Dielectric Constant and Permeability at Microwave Frequencies. Proceedings of the IEEE, 62(1), 33–36. http://doi.org/10.1109/PROC.1974.9382
