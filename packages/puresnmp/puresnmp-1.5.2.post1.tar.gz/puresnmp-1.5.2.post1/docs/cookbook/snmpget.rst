SNMP Get
--------

See :py:func:`puresnmp.get`

Python Code
~~~~~~~~~~~

.. code-block:: python

    from puresnmp import get

    IP = "127.0.0.1"
    COMMUNITY = 'private'

    OID = '1.3.6.1.2.1.1.2.0'
    result = get(IP, COMMUNITY, OID)
    print('''Get Result:
        Type: %s
        repr: %s
        str: %s
        ''' % (type(result), repr(result), result))

    OID = '1.3.6.1.2.1.1.3.0'
    result = get(IP, COMMUNITY, OID)
    print('''Get Result:
        Type: %s
        repr: %s
        str: %s
        ''' % (type(result), repr(result), result))

Output
~~~~~~


.. code-block:: text

    Get Result:
        Type: <class 'str'>
        repr: '1.3.6.1.4.1.8072.3.2.10'
        str: 1.3.6.1.4.1.8072.3.2.10

    Get Result:
        Type: <class 'datetime.timedelta'>
        repr: datetime.timedelta(2, 20199, 680000)
        str: 2 days, 5:36:39.680000
