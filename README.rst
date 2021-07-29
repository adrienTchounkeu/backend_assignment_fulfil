Backend API FULFIL.IO Assignment
================================

|Python-Versions| |pip-Version| |django-Version| |drf-Version|  |postgre-Version| |celery-Version| |redis-Version| |Pandas-Version| |Requests-Version| |socket-Version|

``Backend API FULFIL.IO Assignment`` is a Django Backend API that reads data from a csv file, delivers its computation
to a celery worker, and stores in PostgreSQL. Thereby, you can interact with those data : retrieve, add, delete, and update

--------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:

Technologies used and Why ?
---------------------------

To resolve this problem, we have used ``django``, ``djangorestframework``,
``celery & redis`` , ``django-signals`` , ``socketIO`` , ``PostgreSQL`` , and ``pandas``.

* ``django``: among the best python web framework.
* ``djangorestframework``: we are supposed to build a small REST API. Therefore, Django Rest Framework is suitable for the solution.
* ``celery & redis``: perform asynchronous tasks with the redis broker
* ``django-signals``: handle webhooks configurations.
* ``socketIO``: send socket messages to the client. It's an alternative of SSE, not correctly working with Django
* ``PostgreSQL``: Database used to store our data.
* ``pandas``: read the input Csv file and deduplicate the data.


Installation
------------

To run my Backend solution, you must have ``python``,  ``pip``, ``redis-server``, and ``PostGreSQL`` installed in your system and configure
the redis server and postgresql with django

Download the project from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To clone my code, you run the command below in the CLI

.. code:: sh

    git clone "https://github.com/adrienTchounkeu/backend_assignment_fulfil.git"

You can also download the project by clicking the link `Backend_assignment_fulfil <https://github.com/adrienTchounkeu/backend_assignment_fulfil.git>`_


Install Dependencies
~~~~~~~~~~~~~~~~~~~~~

After downloading the code, Open the CLI in the root directory and execute the command :

.. code:: sh

   pip install -r requirements.txt


NB: *"requirements.txt is a file which contains all the project dependencies"*

All the project dependencies installed, run the command

.. code:: sh

   python manage.py runserver # on Windows

or

.. code:: sh

   python3 manage.py runserver # on Linux

To run the Celery worker, run the command

.. code:: sh

    celery -A backend_assignment worker -l info --pool=solo # to launch celery

NB: *The server generally starts on the port 8000*



Heroku Deploy and Frontend app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Backend API is available through the link `https://backend-assignment-fulfil.herokuapp.com <https://backend-assignment-fulfil.herokuapp.com>`_

Assumptions & Issues
####################

* To deploy my application, two add-ons were needed : postgresql and redis. I, therefore, connected my visa card account to heroku because unable to add more than one add-on otherwise.

* Due to some dynos(processes on Heroku) limitations, my backend is not working properly. Some endpoints are neither returning the good response nor performing the request. Though, it is working perfectly in the local environment

*NB :* You will see in the commit history, many useless commits when is was tyring to figure out heroku deployment errors

Frontend App
############

* The Backend communicate with the Frontend app written in VueJs. You can access through the link `Frontend_assignment_fulfil <https://github.com/adrienTchounkeu/frontend_assignment_fulfil.git>`_




Analyzing The Solution
----------------------

Before starting coding, We have to understand the problem and think of the solution. We have structured our project as follow :

* Choose a great tool to read large csv files : Pandas for instance
* Create custom signals to dispatch when there's a manual create/update action.
* After loosing a lot of time on trying to integrate SSE with Django, I finally choose SocketIO to send live streams events to the Client
* To avoid high cost performance in our app, we use a worker to handle asynchronous tasks and a redis server to work along with Celery, and channels our socket events.

* A high in performance SQL Database : PostGreSQL for instance.


Solving ``Backend API FULFIL.IO Assignment``
-------------------------------------------

Assumptions
~~~~~~~~~~~

To solve the problem, we did some hypothesis:

* The file is stored in other for the worker to efficiently process it.

Solution
~~~~~~~~~~~

To solve the problem, we use ``DataFrames`` and ``pandas as pd`` functions, workers, brokers, sockets and signals

* read large CSV files with ``pd.read_csv`` in chunks(100000)
* drop duplicates on sku in DataFrames with ``pd.drop_duplicates``
* *bulk_create* django orm functions to store all the data at *once*
* celery workers to perform asynchronous tasks, along with brokers
* sockets to send data status event messages to the client
* signals to handle webhooks configurations

Tests
~~~~~

*No tests* have been done to test the endpoints and functions



Further perspectives
---------------------

Limitations & Optimizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Even though my code is solving the problem, I have some performance and resources used issues.
To optimize my solution, I think

* implement parallelization : optimization reading CSV files
* use SSE to establish a unidirectional connection with the client, for speed and security issues
* after lots of research, Flask along with SQLAlchemy best fits the solution because it functions smoothly with SSE
* Regarding deployment, we should implement the solution on a well-designed server (Linux for instance) rather than using an easy deploy service(huge limitation)

Real-life Adaptation
~~~~~~~~~~~~~~~~~~~~

Assuming that we have files coming from more multiple sources, we will encounter the following problems:

* performance issues while reading files
* storing huge amounts of data
* requesting on huge amount of data
* computing huge amounts of data

To solve this problem, we need, to begin, create indexes on our columns in our database to optimize queries,
use a server with great memory and processor, and finally use efficient tools to read and deduplicate, dask must be tested
because of his apparently proven performance.


.. |Python-Versions| image:: https://img.shields.io/pypi/pyversions/pip?logo=python&logoColor=white   :alt: Python Version
.. |pip-Version| image:: https://img.shields.io/pypi/v/pip?label=pip&logoColor=white   :alt: pip Version
.. |django-Version| image:: https://img.shields.io/pypi/v/django?label=django&logo=django   :alt: django Version
.. |drf-Version| image:: https://img.shields.io/pypi/v/djangorestframework?label=djangorestframework
.. |celery-Version| image:: https://img.shields.io/pypi/v/celery?label=celery&logo=celeryhttps://img.shields.io/pypi/v/celery?label=celery&logo=celery   :alt: Celery Version
.. |redis-Version| image:: https://img.shields.io/pypi/v/redis?label=redis&logo=redis   :alt: Redis Version
.. |Pandas-Version| image:: https://img.shields.io/pypi/v/pandas?label=pandas&logo=pandas&logoColor=white   :alt: pandas Version
.. |Requests-Version| image:: https://img.shields.io/pypi/v/requests?label=requests
.. |socket-Version| image:: https://img.shields.io/pypi/v/socketio?label=socketio&logo=socketio   :alt: socket Version
.. |postgre-Version| image:: https://img.shields.io/badge/postgresql-13-blue   :alt: postgre Version

