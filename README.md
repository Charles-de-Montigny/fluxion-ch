ds-coach-nhl
==============================

Anlytic for NHL Teams and Players

## Requirements to use the cookiecutter template:

 - Python 3.5+
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:

``` bash
$ pip install cookiecutter
```
or
``` bash
$ conda config --add channels conda-forge
$ conda install cookiecutter
```

## Getting started

**Clone the repository**
``` bash
$ git clone https://gitlab.com/flux1on/ds-coach-nhl.git
```

**Create virtual environnement**

``` bash
$ python3 -m virtualenv venv
```

**Activate environnement**

``` bash
$ source venv/bin/activate
```

**Install packages**

``` bash
$ pip install -r requirements.txt
```

**Start the application**

``` bash
$ python3 app.py
```

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── assets             <- Include images, CSS and JavaScript files in that folder.
    │
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks for exploration and experimentation.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── dataset.py     <- Script to download or generate data.
        │
        ├── utils.py       <- A collection of usage utility functions in python.
        │
        ├── layout.py      <- The layout of the app and it describes what the application looks like.
        │
        └── viz.py         <- Script to create plots, tables and maps oriented for data visualizations.
    

--------

<p><small>Project created by <a target="_blank" href="https://www.fluxion.ca">cookiecutter dashdev project template</a>. #cookiecutterdashdev</small></p>