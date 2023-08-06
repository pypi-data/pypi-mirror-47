Injector - Python dependency injection framework, inspired by Guice
===================================================================

[![image](https://secure.travis-ci.org/alecthomas/injector.svg?branch=master)](https://travis-ci.org/alecthomas/injector)
[![Coverage Status](https://coveralls.io/repos/github/alecthomas/injector/badge.svg?branch=master)](https://coveralls.io/github/alecthomas/injector?branch=master)

Introduction
------------

Dependency injection as a formal pattern is less useful in Python than in other languages, primarily due to its support for keyword arguments, the ease with which objects can be mocked, and its dynamic nature.

That said, a framework for assisting in this process can remove a lot of boiler-plate from larger applications. That's where Injector can help. It automatically and transitively provides keyword arguments with their values. As an added benefit, Injector encourages nicely compartmentalised code through the use of `Module` s.

While being inspired by Guice, it does not slavishly replicate its API. Providing a Pythonic API trumps faithfulness.

### How to get Injector?

* GitHub (code repository, issues): https://github.com/alecthomas/injector

* PyPI (installable, stable distributions): https://pypi.python.org/pypi/injector. You can install it using pip:

  ```bash
  pip install injector
  ```

* Documentation: http://injector.readthedocs.org
* Change log: http://injector.readthedocs.io/en/latest/changelog.html

Injector works with CPython 3.5+ and PyPy 3 implementing Python 3.5+.

A Quick Example
---------------


```python
>>> from injector import Injector, inject
>>> class Inner:
...     def __init__(self):
...         self.forty_two = 42
...
>>> class Outer:
...     @inject
...     def __init__(self, inner: Inner):
...         self.inner = inner
...
>>> injector = Injector()
>>> outer = injector.get(Outer)
>>> outer.inner.forty_two
42

```

Or with `dataclasses` if you like:

```python
from dataclasses import dataclass
from injector import Injector, inject
class Inner:
    def __init__(self):
        self.forty_two = 42

@inject
@dataclass
class Outer:
    inner: Inner

injector = Injector()
outer = injector.get(Outer)
print(outer.inner.forty_two)  # Prints 42
```


A Full Example
--------------

Here's a full example to give you a taste of how Injector works:


```python
>>> from injector import Module, Key, provider, Injector, inject, singleton

```

We'll use an in-memory SQLite database for our example:


```python
>>> import sqlite3

```

And make up an imaginary `RequestHandler` class that uses the SQLite connection:


```python
>>> class RequestHandler:
...   @inject
...   def __init__(self, db: sqlite3.Connection):
...     self._db = db
...
...   def get(self):
...     cursor = self._db.cursor()
...     cursor.execute('SELECT key, value FROM data ORDER by key')
...     return cursor.fetchall()

```

Next, for the sake of the example, we'll create a configuration type:


```python
>>> class Configuration:
...     def __init__(self, connection_string):
...         self.connection_string = connection_string

```

Next, we bind the configuration to the injector, using a module:


```python
>>> def configure_for_testing(binder):
...     configuration = Configuration(':memory:')
...     binder.bind(Configuration, to=configuration, scope=singleton)

```

Next we create a module that initialises the DB. It depends on the configuration provided by the above module to create a new DB connection, then populates it with some dummy data, and provides a `Connection` object:


```python
>>> class DatabaseModule(Module):
...   @singleton
...   @provider
...   def provide_sqlite_connection(self, configuration: Configuration) -> sqlite3.Connection:
...     conn = sqlite3.connect(configuration.connection_string)
...     cursor = conn.cursor()
...     cursor.execute('CREATE TABLE IF NOT EXISTS data (key PRIMARY KEY, value)')
...     cursor.execute('INSERT OR REPLACE INTO data VALUES ("hello", "world")')
...     return conn

```

(Note how we have decoupled configuration from our database initialisation code.)

Finally, we initialise an `Injector` and use it to instantiate a `RequestHandler` instance. This first transitively constructs a `sqlite3.Connection` object, and the Configuration dictionary that it in turn requires, then instantiates our `RequestHandler`:


```python
>>> injector = Injector([configure_for_testing, DatabaseModule()])
>>> handler = injector.get(RequestHandler)
>>> tuple(map(str, handler.get()[0]))  # py3/py2 compatibility hack
('hello', 'world')

```

We can also verify that our `Configuration` and `SQLite` connections are indeed singletons within the Injector:


```python
>>> injector.get(Configuration) is injector.get(Configuration)
True
>>> injector.get(sqlite3.Connection) is injector.get(sqlite3.Connection)
True

```

You're probably thinking something like: "this is a large amount of work just to give me a database connection", and you are correct; dependency injection is typically not that useful for smaller projects. It comes into its own on large projects where the up-front effort pays for itself in two ways:

1.  Forces decoupling. In our example, this is illustrated by decoupling our configuration and database configuration.
2.  After a type is configured, it can be injected anywhere with no additional effort. Simply `@inject` and it appears. We don't really illustrate that here, but you can imagine adding an arbitrary number of `RequestHandler` subclasses, all of which will automatically have a DB connection provided.

Footnote
--------

This framework is similar to snake-guice, but aims for simplification.

&copy; Copyright 2010-2013 to Alec Thomas, under the BSD license
