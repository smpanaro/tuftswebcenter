tuftswebcenter
==============

Simplified interactions with Tufts' Webcenter.

What is it?
-----------

A quick and easy way to do things on Tufts' Webcenter portal (webcenter.studentservices.tufts.edu).

What can I do?
--------------

For now, you can do two things: get reports on housing groups and download past exams.

Why?
----

Checking housing groups is slow. I just want to see where my group ranks!

With the web interface:
::
	=> login
	=> select housing from dropdown 
	=> click view housing groups link
	=> pick Apartments from dropdown
	=> click Submit so the list loads

But now you can run a little script whenever you want to know.

.. code-block:: pycon

	>>> from webcenter.webcenter import *
	>>> wc = WebcenterSession(mystudentid, mypin)
	>>> print wc.get_housing_groups_reports("Apartment")


If you want to bulk download the past exams for a course you can do that too.(See if examples/download_exams.py fits your needs.)

Installation
------------

Make a virtualenv (or not, but you should).

.. code-block:: bash

	$ pip install -r requirements.txt
	$ cd examples
	$ mv webcenter_credentials.py.example webcenter_credentials.py
	$ vim webcenter_credentials.py
	$ python list_apartments.py