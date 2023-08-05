owattr
######

.. image:: https://travis-ci.org/narusemotoki/owattr.svg?branch=master
   :target: https://travis-ci.org/narusemotoki/owattr

owattr overwrites attributes.

Example
=======

config.py:
----------

.. code-block:: python

   import sys

   import owattr


   REDIS_URL = "redis://localhost:6379/0"
   IS_DEV_ENV = True


   owattr.from_dict(sys.modules[__name__], dict(os.environ))


The :code:`config` module has :code:`REDIS_URL` as attribute. You might want to change the value for your production environment. In this example, if you have defined :code:`REDIS_URL` in environment variables, when you load :code:`config` module, it is overwritten. If you don't define :code:`REDIS_URL`, you can use the original value.
When owattr read the dict, it casts dict value to type of the original value. So in environment variable, everything is str type. In this example, if you have defined :code:`IS_DEV_ENV=False` in environment variable, :code:`IS_DEV_ENV` of :code:`config` has :code:`False` as bool type.
Booleans are cast as follows:

- :code:`'false'`, :code:`'False'` and :code:`''` are cast to False
- :code:`'true'` and :code:`'True'` are cast to True
- anything else raises a :code:`'ValueError'`

If your object has :code:`__all__`, owattr overwrites only variables which written in :code:`__all__`.
