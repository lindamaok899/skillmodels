.. _basic_usage:

***********
Basic Usage
***********

Some Python Skills you will need
********************************

To use skillmodels you probably will have to create a pandas DataFrame from a file on your disk and a python dictionary from a json file. Both things are very easy:

To create the DataFrame:

.. code::

    # from a .dta file
    import pandas as pd
    dataset = pd.read_stata('some/path/to/data.dta')

.. code::

    # from a .csv file
    import pandas as pd
    dataset = pd.read_csv('some/path/to/data.csv')

For any other file formats or advanced options for loading .dta and .csv files, see the `pandas documentation`_.

To load the model dictionary:

.. code::

    import json

    with open('some/path/to/model_dict.json') as j:
        model_dict = json.load(j)

In case of any problem check the documentation of the `json module`_.


Usage of Skillmodels
********************

Fitting models is very similar to fitting models in `Statsmodels`_

The main object a user interacts with is ``SkillModel`` (see :ref:`estimation`) which is a subclass of Statsmodel's `GenericLikelihoodModel`_. To create an instance of this class just type:

.. code::

    from skillmodels import SkillModel
    mod = SkillModel(model_dict, dataset, estimator)

The mandatory arguments of SkillModel are:

* model_dict: dictionary that defines the model (usually loaded from a json file). See :ref:`model_specs` for details.
* dataset: a pandas dataframe in long format. It has to contain columns that identify the period and individual. The names of these columns are indicated as 'period_identifier' and 'person_identifier' in the general section of the model dictionary. The default values are 'period' and 'id'.
* estimator: a string that can take the values 'wa' (Wiswall Agostinelli Estimator) and 'chs' (Cunha, Heckman, Schennach estimator).

Optional arguments of SkillModel are:

* model_name: a string that gives a name to the model that will be used in error messages or warnings. If you estimate several models it will help you a lot to locate the problems.
* dataset_name: same as model_name
* save_path: a string that indicates where intermediate results are saved. Saving intermediate results is optional and can be controlled in the "general" section of the model_dict. If anything is saved, you must provide a save_path.
* bootstrap_samples: a list of lists. Each sublist contains a sample of elements from the 'person_identifier' column of the dataset. If you don't specify this argument, sampling for bootstrap is handled automatically. For this it is assumed that your data is iid.


Using the fit() method of ``SkillModel`` like so:

.. code::

    res = mod.fit()

will return an instance of ``SkillModelResults`` which is a subclass of ``GenericLikelihoodModelResults`` and has (or will have) most of the usual attributes and methods described `here`_. For example you can:

.. code::

    # access the estimated parameter vector (long form)
    estimated_parameters = res.params
    # access standard errors based on the method you specified in the general
    # section of the model dictionary.
    standard_errrors = res.bse
    # access the t-valuess of the parameters
    tvalues = res.tvalues
    # access the p-values of the parameters
    pvalues = res.pvalues
    # access the confidence intervals (5 %)
    confidence_intervals = res.conf_int
    # calculate marginal effects
    margeff = res.marginal_effects(of='fac2', on='fac1')

For the chs estimator you can also use the many other ways of calculating standard errors documented `here`_. It should already work to use the t-test, f-test and wald-test as described `here`_ but I haven't tested it yet.

Some methods are not yet implemented but are on my To-Do list:

    * save, load and remove_data
    * summary
    * predict

.. Note:: Some functions of the CHS estimator use numpy functions that call fast multithreaded
    routines from the Intel Math Kernel Library (MKL). This is usually what you want, but if you fit several models in parallel (e.g. if you have datasets from different countries or you calculate boostrap standard errors) you might get better results if reduce the number of threads used. To do so, see the `documentation`_ of Anaconda.


.. _Statsmodels:
    http://statsmodels.sourceforge.net/stable/

.. _GenericLikelihoodModel:
    http://statsmodels.sourceforge.net/devel/examples/notebooks/generated/generic_mle.html

.. _here:
    http://nipy.bic.berkeley.edu/nightly/statsmodels/doc/html/dev/generated/statsmodels.base.model.GenericLikelihoodModelResults.html#statsmodels.base.model.GenericLikelihoodModelResults

.. _documentation:
    https://docs.continuum.io/mkl-service/

.. _pandas documentation:
    http://pandas.pydata.org/pandas-docs/stable/io.html

.. _json module:
    https://docs.python.org/3.4/library/json.html
