tuftswebcenter
==============

Simplified interactions with Tufts' Webcenter.

What is it?
-----------

A quick and easy way to do things on Tufts' Webcenter portal (webcenter.studentservices.tufts.edu).

What can I do?
--------------

For now, you can get reports on housing lottery groups. Soon you'll be able to download past exams.

Why?
---

I want to check if our housing group is going to get into Hillsides!

With the web interface:
=> login
=> select housing from dropdown 
=> click view housing groups 
=> pick Apartments from dropdown
=> click Submit so the list loads

versus

.. code-block:: pycon

	>>> from webcenter.webcenter import *
	>>> wc = WebcenterSession(mystudentid, mypin)
	>>> print wc.get_housing_groups_reports("Apartment")

Installation
------------

Make a virtualenv (or not, but you should).

.. code-block:: bash

	$ pip install -r requirements.txt
	$ cd examples
	$ mv webcenter_credentials.py.example webcenter_credentials.py
	$ vim webcenter_credentials.py
	$ python list_apartments.py