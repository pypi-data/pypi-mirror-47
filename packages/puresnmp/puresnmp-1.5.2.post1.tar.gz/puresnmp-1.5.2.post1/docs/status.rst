Status of the Project
=====================

Implemented Features
--------------------

* SNMP v2c GET
* SNMP v2c WALK (and, implicitly GETNEXT as well)
* SNMP v2c SET
* SNMP Bulk GET support
* SNMP Bulk WALK support

Tests executed on
-----------------

* A docker maching running ``snmpd`` (the Dockerfile can be found in the
  ``docker`` folder).
* An Alcatel 7750SR12 box.

Missing Features
----------------

These features are planned but not yet implemented. In order of priority:

* SNMPv3.

If you want to help move the project forward, please see :ref:`contributing`.
