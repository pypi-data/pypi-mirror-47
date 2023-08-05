***********
CARTOframes
***********

.. image:: https://travis-ci.org/CartoDB/cartoframes.svg?branch=master
    :target: https://travis-ci.org/CartoDB/cartoframes
.. image:: https://coveralls.io/repos/github/CartoDB/cartoframes/badge.svg?branch=master
    :target: https://coveralls.io/github/CartoDB/cartoframes?branch=master
.. image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/cartodb/cartoframes/v0.9.2?filepath=examples

A Python package for integrating `CARTO <https://carto.com/>`__ maps, analysis, and data services into data science workflows.

Python data analysis workflows often rely on the de facto standards `pandas <http://pandas.pydata.org/>`__ and `Jupyter notebooks <http://jupyter.org/>`__. Integrating CARTO into this workflow saves data scientists time and energy by not having to export datasets as files or retain multiple copies of the data. Instead, CARTOframes give the ability to communicate reproducible analysis while providing the ability to gain from CARTO's services like hosted, dynamic or static maps and `Data Observatory <https://carto.com/data-observatory/>`__ augmentation.

Features
========

- Write pandas DataFrames to CARTO tables
- Read CARTO tables and queries into pandas DataFrames
- Create customizable, interactive CARTO maps in a Jupyter notebook
- Interact with CARTO's Data Observatory
- Use CARTO's spatially-enabled database for analysis
- Try it out without needing a CARTO account by using the `Examples functionality <https://cartoframes.readthedocs.io/en/latest/#module-cartoframes.examples>`__

Common Uses
===========

- Visualize spatial data programmatically as matplotlib images or embedded interactive maps
- Perform cloud-based spatial data processing using CARTO's analysis tools
- Extract, transform, and Load (ETL) data using the Python ecosystem for getting data into and out of CARTO
- Data Services integrations using CARTO's `Data Observatory <https://carto.com/data-observatory/>`__ and other `Data Services APIs <https://carto.com/location-data-services/>`__

Try it out
==========

The easiest way to try out cartoframes is to use the cartoframes example notebooks running in binder: https://mybinder.org/v2/gh/CartoDB/cartoframes/master?filepath=examples If you already have an API key, you can follow along and complete all of the example notebooks.

If you do not have an API key, you can use the `Example Context <https://cartoframes.readthedocs.io/en/latest/#module-cartoframes.examples>`__ to read the example data, make maps, and run arbitrary queries from the datasets there. The best place to get started is in the "Example Datasets" notebook found when running binder or downloading from the `examples <https://github.com/CartoDB/cartoframes/blob/master/examples/Example%20Datasets.ipynb>`__ directory in the cartoframes GitHub repository.

.. note::
    The example context only provides read access, so not all cartoframes features are available. For full access, `Start a free 30 day trial <https://carto.com/signup>`__ or get free access with a `GitHub Student Developer Pack <https://education.github.com/pack>`__.

More info
=========

- Complete documentation: http://cartoframes.readthedocs.io/en/latest/
- Source code: https://github.com/CartoDB/cartoframes
- bug tracker / feature requests: https://github.com/CartoDB/cartoframes/issues

.. note::
    `cartoframes` users must have a CARTO API key for most `cartoframes` functionality. For example, writing DataFrames to an account, reading from private tables, and visualizing data on maps all require an API key. CARTO provides API keys for education and nonprofit uses, among others. Request access at support@carto.com. API key access is also given through `GitHub's Student Developer Pack <https://carto.com/blog/carto-is-part-of-the-github-student-pack>`__.

Install Instructions
====================

To install `cartoframes` on your machine, do the following to install the
latest version:

.. code:: bash

    $ pip install cartoframes

`cartoframes` is continuously tested on Python versions 2.7, 3.5, and 3.6. It is recommended to use `cartoframes` in Jupyter Notebooks (`pip install jupyter`). See the example usage section below or notebooks in the `examples directory <https://github.com/CartoDB/cartoframes/tree/master/examples>`__ for using `cartoframes` in that environment.

Virtual Environment
-------------------

Using `virtualenv`
^^^^^^^^^^^^^^^^^^


Make sure your `virtualenv` package is installed and up-to-date. See the `official Python packaging page <https://packaging.python.org/guides/installing-using-pip-and-virtualenv/>`__ for more information.

To setup `cartoframes` and `Jupyter` in a `virtual environment <http://python-guide.readthedocs.io/en/latest/dev/virtualenvs/>`__:

.. code:: bash

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install cartoframes jupyter
    (venv) $ jupyter notebook

Then create a new notebook and try the example code snippets below with tables that are in your CARTO account.

Using `pipenv`
^^^^^^^^^^^^^^

Alternatively, `pipenv <https://pipenv.readthedocs.io/en/latest/>`__ provides an easy way to manage virtual environments. The steps below are: 

1. Create a virtual environment with Python 3.4+ (recommended instead of Python 2.7)
2. Install cartoframes and Jupyter (optional) into the virtual environment
3. Enter the virtual environment
4. Launch a Jupyter notebook server

.. code:: bash

    $ pipenv --three
    $ pipenv install cartoframes jupyter
    $ pipenv shell

Next, run a Python kernel by typing `$ python`, `$ jupyter notebook`, or however you typically run Python.

Native pip
----------

If you install packages at a system level, you can install `cartoframes` with:

.. code:: bash

    $ pip install cartoframes

Example usage
=============

Data workflow
-------------

Get table from CARTO, make changes in pandas, sync updates with CARTO:

.. code:: python

    import cartoframes
    # `base_url`s are of the form `https://{username}.carto.com/` for most users
    cc = cartoframes.CartoContext(base_url='https://eschbacher.carto.com/',
                                  api_key=APIKEY)

    # read a table from your CARTO account to a DataFrame
    df = cc.read('brooklyn_poverty_census_tracts')

    # do fancy pandas operations (add/drop columns, change values, etc.)
    df['poverty_per_pop'] = df['poverty_count'] / df['total_population']

    # updates CARTO table with all changes from this session
    cc.write(df, 'brooklyn_poverty_census_tracts', overwrite=True)


.. image:: https://raw.githubusercontent.com/CartoDB/cartoframes/master/docs/img/read_demo.gif

Write an existing pandas DataFrame to CARTO.

.. code:: python

    import pandas as pd
    import cartoframes
    df = pd.read_csv('acadia_biodiversity.csv')
    cc = cartoframes.CartoContext(base_url=BASEURL,
                                  api_key=APIKEY)
    cc.write(df, 'acadia_biodiversity')


Map workflow
------------

The following will embed a CARTO map in a Jupyter notebook, allowing for custom styling of the maps driven by `TurboCARTO <https://github.com/CartoDB/turbo-carto>`__ and `CARTOColors <https://carto.com/blog/introducing-cartocolors>`__. See the `CARTOColors wiki <https://github.com/CartoDB/CartoColor/wiki/CARTOColor-Scheme-Names>`__ for a full list of available color schemes.

.. code:: python

    from cartoframes import Layer, BaseMap, styling
    cc = cartoframes.CartoContext(base_url=BASEURL,
                                  api_key=APIKEY)
    cc.map(layers=[BaseMap('light'),
                   Layer('acadia_biodiversity',
                         color={'column': 'simpson_index',
                                'scheme': styling.tealRose(5)}),
                   Layer('peregrine_falcon_nest_sites',
                         size='num_eggs',
                         color={'column': 'bird_id',
                                'scheme': styling.vivid(10)})],
           interactive=True)

.. image:: https://raw.githubusercontent.com/CartoDB/cartoframes/master/docs/img/map_demo.gif

.. note::
    Legends are under active development. See
    https://github.com/CartoDB/cartoframes/pull/184 for more information. To
    try out that code, install `cartoframes` as:

        `pip install git+https://github.com/cartodb/cartoframes.git@add-legends-v1#egg=cartoframes`

Data Observatory
----------------

Interact with CARTO's `Data Observatory <https://carto.com/docs/carto-engine/data>`__:

.. code:: python

    import cartoframes
    cc = cartoframes.CartoContext(BASEURL, APIKEY)

    # total pop, high school diploma (normalized), median income, poverty status (normalized)
    # See Data Observatory catalog for codes: https://cartodb.github.io/bigmetadata/index.html
    data_obs_measures = [{'numer_id': 'us.census.acs.B01003001'},
                         {'numer_id': 'us.census.acs.B15003017',
                          'normalization': 'predenominated'},
                         {'numer_id': 'us.census.acs.B19013001'},
                         {'numer_id': 'us.census.acs.B17001002',
                          'normalization': 'predenominated'},]
    df = cc.data('transactions', data_obs_measures)


CARTO Credential Management
---------------------------

Typical usage
^^^^^^^^^^^^^

The most common way to input credentials into cartoframes is through the `CartoContext`, as below. Replace `{your_user_name}` with your CARTO username and `{your_api_key}` with your API key, which you can find at ``https://{your_user_name}.carto.com/your_apps``.

.. code:: python

    from cartoframes import CartoContext
    cc = CartoContext(
        base_url='https://{your_user_name}.carto.com',
        api_key='{your_api_key}'
    )


You can also set your credentials using the `Credentials` class:

.. code:: python

    from cartoframes import Credentials, CartoContext
    cc = CartoContext(
        creds=Credentials(key='{your_api_key}', username='{your_user_name}')
    )


Save/update credentials for later use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from cartoframes import Credentials, CartoContext
    creds = Credentials(username='eschbacher', key='abcdefg')
    creds.save()  # save credentials for later use (not dependent on Python session)

Once you save your credentials, you can get started in future sessions more quickly:

.. code:: python

    from cartoframes import CartoContext
    cc = CartoContext()  # automatically loads credentials if previously saved

Experimental features
---------------------

CARTOframes includes experimental features that we are testing for future releases into cartoframes core. These features exist as separate modules in `vis`. These features are stand-alone other than sometimes relying on some cartoframes utilities, etc. Vis features will also change often and without notice, so they should never be used in a production environment.

To import an experimental feature, like new vector maps, do the following:

.. code:: python

    from cartoframes.auth import Context
    from cartoframes.viz import Map, Layer

    context = Context()
    Map(Layer('<table name>', '<carto vl style>', context=context))
