XIST provides an extensible HTML and XML generator. XIST is also a XML parser
with a very simple and pythonesque tree API. Every XML element type corresponds
to a Python class and these Python classes provide a conversion method to
transform the XML tree (e.g. into HTML). XIST can be considered
'object oriented XSLT'.

XIST also includes the following modules and packages:

* ``ll.ul4c`` is compiler for a cross-platform templating language with
  similar capabilities to `Django's templating language`__. ``UL4`` templates
  are compiled to an internal format, which makes it possible to implement
  template renderers in other languages and makes the template code "secure"
  (i.e. template code can't open or delete files).

  __ https://docs.djangoproject.com/en/1.5/topics/templates/

  There are implementations for Python, Java and Javascript.

* ``ll.ul4on`` provides functions for encoding and decoding a lightweight
  machine-readable text-based format for serializing the object types supported
  by UL4. It is extensible to allow encoding/decoding arbitrary instances
  (i.e. it is basically a reimplementation of ``pickle``, but with string
  input/output instead of bytes and with an eye towards cross-plattform
  support).

  There are implementations for Python, Java and Javascript.

* ``ll.orasql`` provides utilities for working with cx_Oracle_:

  - It allows calling functions and procedures with keyword arguments.

  - Query results will be put into Record objects, where database fields
    are accessible as object attributes.

  - The ``Connection`` class provides methods for iterating through the
    database metadata.

  - Importing the modules adds support for URLs with the scheme ``oracle`` to
    ``ll.url``.

  .. _cx_Oracle: https://oracle.github.io/python-cx_Oracle/

* ``ll.make`` is an object oriented make replacement. Like make it allows
  you to specify dependencies between files and actions to be executed
  when files don't exist or are out of date with respect to one
  of their sources. But unlike make you can do this in a object oriented
  way and targets are not only limited to files.

* ``ll.color`` provides classes and functions for handling RGB color values.
  This includes the ability to convert between different color models
  (RGB, HSV, HLS) as well as to and from CSS format, and several functions
  for modifying and mixing colors.

* ``ll.sisyphus`` provides classes for running Python scripts as cron jobs.

* ``ll.url`` provides classes for parsing and constructing RFC 2396
  compliant URLs.

* ``ll.nightshade`` can be used to serve the output of PL/SQL
  functions/procedures with CherryPy__.

* ``ll.misc`` provides several small utility functions and classes.

* ``ll.astyle`` can be used for colored terminal output (via ANSI escape
  sequences).

* ``ll.daemon`` can be used on UNIX to fork a daemon process.

* ``ll.xml_codec`` contains a complete codec for encoding and decoding XML.

__ http://www.cherrypy.org/


Changes in 5.44 (released 06/07/2019)
-------------------------------------

* ``ll.orasql.Connection.objects`` now outputs ``Job`` objects too.
  Since Oracle provides no dependency information about jobs, ``Job``
  objects will always be output last (in "create" mode; in "drop" mode they
  will be output first).

* ``ll.orasql.Job.references`` will now yield the appropriate
  ``ll.orasql.JobClass`` object (if the job class isn't a system job class).

* ``ll.orasql.JobClass.referencedby`` will now yield all
  ``ll.orasql.Job`` objects that use this job class.

* The ``owner`` argument for various ``ll.orasql`` methods now supports
  passing a set or tuple of owner names.

* PySQL scripts now can contains PySQL commands in "function call form", i.e.
  ``checkerrors()`` instead of ``{'type': 'checkerrors'}``.

* PySQL scripts can now contains literal Python source code (between lines
  with ``#>>>`` and ``#<<<``, e.g.::

    #>>>
    cursor = connection.cursor()
    cursor.execute("drop user foo cascade")
    #<<<

* Comments in PySQL scripts are supported now (via lines starting with
  ``#``).

* Since PySQL scripts can open their own database connections the
  ``connectstring`` argument for the ``pysql`` script is now optional.

* The PySQL command ``compileall`` has been removed. This same effect can
  simply be achieved by calling ``utl_recomp.recomp_parallel()`` or
  ``dbms_utility.compile_schema()``.

* Added several new PySQL commands: ``ll.pysql.commit`` and
  ``ll.pysql.rollback``, ``ll.pysql.drop_types``,
  ``ll.pysql.user_exists``, ``ll.pysql.object_exists`` and
  ``ll.pysql.env``.

* The ``--commit`` argument for the pysql script (with the options ``record``,
  ``once`` and ``never``) has been replaced with a flag option ``--rollback``.
  Automatically committing after every record is no longer available.

* The PySQL terminator comment (``-- @@@``) can now no longer be specified
  via a command line option.

* The ``-v``/``--verbose`` option for ``ll.pysql`` now supports new output
  modes (``file`` and ``log``) and full mode now outputs much more information.

* The ``ll.url.URL`` methods ``ll.url.URL.owner`` and
  ``ll.url.URL.group`` now will return the ``uid`` or ``gid``
  respectively when the user or group name can't be determined instead of
  raising a ``KeyError``.

* Fixed SQL statement for dropping ``ll.orasql.Job`` objects.




