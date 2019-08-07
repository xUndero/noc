.. _dev-confdb-syntax:

=============
ConfDB Syntax
=============

.. contents:: On this page
    :local:
    :backlinks: none
    :depth: 1
    :class: singlecol

*Normalized Config* is the device-independent configuration representation.
Raw device config processed by *Config Tokenizer* and converted to
the list of *Tokens*. *Tokens* processed by *Config Normalizer*
and became *Normalized Config*.

Syntax
------

* :ref:`system<dev-confdb-syntax-system>`

  * :ref:`hostname<dev-confdb-syntax-system-hostname>`

    * :ref:`<hostname><dev-confdb-syntax-system-hostname-hostname>`

  * :ref:`domain-name<dev-confdb-syntax-domain-name>`

    * :ref:`<domain name><dev-confdb-syntax-domain-name-domain_name>`

  * **prompt**

    * ``<prompt>``

  * **clock**

    * **timezone**

      * ``<tz name>``

    * **source**

      * ``<source>``

* virtual-router

  * ``<vr name>``

    * **forwarding-instance**

      * ``<fi name>``

        * **interfaces**

          * ``<interface name>``

            * **decscription**

              * ``<interface description>``

            * **unit**

              * ``<unit name>``

                * **description**

                  * ``<unit description>``

                * **inet**

                  * **address**

                    * ``<IPv4 address>``

                * **inet6**

                  * **address**

                    * ``<IPv6 address>``

                * **iso**

                  * **address**

                    * ``<ISO address>``

                * **bridge**

                  * **port-security**

                    * **max-mac-count**

                      * ``<max mac count>``

        * **route**

          * **inet**

            * **static**

              * ``<prefix>``

                * **next-hop**

                  * ``<address>``

          * **inet6**

            * **static**

              * ``<prefix>``

                * **next-hop**

                  * ``<address>``

        * **protocols**

          * **spanning-tree**

            * **interface**

              * ``<interface name>``

                * **cost**

                  * ``<interface cost>``

          * **ntp**

            * ``<server name>``

              * **version**

                * ``<version>``

              * **address**

                * ``<address>``

              * **mode**

                * ``<mode>``

              * **authentication**

                * **type**

                  * ``<type>``

                * **key**

                  * ``<key>``

              * **prefer**

              * **broadcast**

                * **version**

                  * ``<version>``

                * **address**

                  * ``<address>``

                * **authentication**

                  * **type**

                    * ``<type>``

                  * **key**

                    * ``<key>``

.. _dev-confdb-syntax-system:

system
^^^^^^
Grouping node for system-wide settings

========= ==
Parent    -
Required  No
Multiple  No
Default   -
========= ==

Contains:

+-------------------------------------------------------+----------+-------+
| Node                                                  | Required | Multi |
+=======================================================+==========+=======+
| :ref:`hostname<dev-confdb-syntax-system-hostname>`    | No       | No    |
+-------------------------------------------------------+----------+-------+
| :ref:`hostname<dev-confdb-syntax-system-domain-name>` | No       | No    |
+-------------------------------------------------------+----------+-------+
| :ref:`hostname<dev-confdb-syntax-system-prompt>`      | No       | No    |
+-------------------------------------------------------+----------+-------+
| :ref:`hostname<dev-confdb-syntax-system-clock>`       | No       | No    |
+-------------------------------------------------------+----------+-------+

.. _dev-confdb-syntax-system-hostname:

system hostname
^^^^^^^^^^^^^^^
Grouping node for system hostname settings

========= =======================================
Parent    :ref:`system<dev-confdb-syntax-system>`
Required  No
Multiple  No
Default   -
========= =======================================

Contains:

+-------------------------------------------------------------+----------+-------+
| Node                                                        | Required | Multi |
+=============================================================+==========+=======+
| :ref:`hostname<dev-confdb-syntax-system-hostname-hostname>` | Yes      | No    |
+-------------------------------------------------------------+----------+-------+

.. _dev-confdb-syntax-system-hostname-hostname:

system hostname <hostname>
^^^^^^^^^^^^^^^^^^^^^^^^^^
System hostname

========= ================================================
Parent    :ref:`system<dev-confdb-syntax-system-hostname>`
Required  Yes
Multiple  No
Default   -
Name      hostname
========= ================================================

.. py:function:: make_hostname(hostname)

    Generate `system hostname <hostname>` node

    :param hostname: System Hostname

.. _dev-confdb-syntax-system-hostname:

system domain-name
^^^^^^^^^^^^^^^^^^
Grouping node for system domain name settings

========= =======================================
Parent    :ref:`system<dev-confdb-syntax-system>`
Required  No
Multiple  No
Default   -
========= =======================================

Contains:

+-------------------------------------------------------------------+----------+-------+
| Node                                                              | Required | Multi |
+===================================================================+==========+=======+
| :ref:`hostname<dev-confdb-syntax-system-domain-name-domain_name>` | Yes      | No    |
+-------------------------------------------------------------------+----------+-------+

.. _dev-confdb-syntax-system-domain-name-domain_name:

system domain-name <domain_name>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
System domain name

========= ===================================================
Parent    :ref:`system<dev-confdb-syntax-system-domain-name>`
Required  Yes
Multiple  No
Default   -
Name      domain_name
========= ===================================================

.. py:function:: make_domain_name(domain_name)

    Generate `system domain-name <domain_name>` node

    :param hostname: System domain name
