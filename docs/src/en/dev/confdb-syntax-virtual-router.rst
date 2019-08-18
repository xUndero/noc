.. _dev-confdb-syntax-virtual-router:

virtual-router
^^^^^^^^^^^^^^

========  ==
Parent    -
Required  No
Multiple  No
Default:  -
========  ==


Contains:

+-------------------------------------------------+------------+---------+
| Node                                            | Required   | Multi   |
+=================================================+============+=========+
| :ref: `vr<dev-confdb-syntax-virtual-router-vr>` | Yes        | No      |
+-------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr:

virtual-router \*<vr>
^^^^^^^^^^^^^^^^^^^^^

========  ========================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router>`
Required  Yes
Multiple  Yes
Default:  default
Name      vr
========  ========================================================


Contains:

+--------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                 | Required   | Multi   |
+======================================================================================+============+=========+
| :ref: `forwarding-instance<dev-confdb-syntax-virtual-router-vr-forwarding-instance>` | Yes        | Yes     |
+--------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance:

virtual-router \*<vr> forwarding-instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===========================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr>`
Required  Yes
Multiple  No
Default:  -
========  ===========================================================


Contains:

+------------------------------------------------------------------------------------+------------+---------+
| Node                                                                               | Required   | Multi   |
+====================================================================================+============+=========+
| :ref: `instance<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>` | Yes        | No      |
+------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance:

virtual-router \*<vr> forwarding-instance \*<instance>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===============================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance>`
Required  Yes
Multiple  Yes
Default:  default
Name      instance
========  ===============================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                              | Required   | Multi   |
+===================================================================================================================+============+=========+
| :ref: `type<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-type>`                               | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `description<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-description>`                 | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `route-distinguisher<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-distinguisher>` | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `vrf-target<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target>`                   | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `vpn-id<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vpn-id>`                           | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `vlans<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans>`                             | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `interfaces<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces>`                   | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `route<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route>`                             | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `protocols<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`                     | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-type:

virtual-router \*<vr> forwarding-instance \*<instance> type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                     | Required   | Multi   |
+==========================================================================================+============+=========+
| :ref: `type<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-type-type>` | Yes        | No      |
+------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-type-type:

virtual-router \*<vr> forwarding-instance \*<instance> type <type>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =============================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-type>`
Required  Yes
Multiple  No
Default:  -
Name      type
========  =============================================================================================


.. py:function:: make_forwarding_instance_type(type)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> type \<type\>` node

    :param type: virtual-router \*\<vr\> forwarding-instance \*\<instance\> type

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-description:

virtual-router \*<vr> forwarding-instance \*<instance> description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                          | Required   | Multi   |
+===============================================================================================================+============+=========+
| :ref: `description<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-description-description>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-description-description:

virtual-router \*<vr> forwarding-instance \*<instance> description <description>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ====================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-description>`
Required  No
Multiple  No
Default:  -
Name      description
========  ====================================================================================================


.. py:function:: make_forwarding_instance_description(description)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> description \<description\>` node

    :param description: virtual-router \*\<vr\> forwarding-instance \*\<instance\> description

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-distinguisher:

virtual-router \*<vr> forwarding-instance \*<instance> route-distinguisher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                | Required   | Multi   |
+=====================================================================================================+============+=========+
| :ref: `rd<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-distinguisher-rd>` | Yes        | No      |
+-----------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-distinguisher-rd:

virtual-router \*<vr> forwarding-instance \*<instance> route-distinguisher <rd>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ============================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-distinguisher>`
Required  Yes
Multiple  No
Default:  -
Name      rd
========  ============================================================================================================


.. py:function:: make_forwarding_instance_rd(rd)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> route-distinguisher \<rd\>` node

    :param rd: virtual-router \*\<vr\> forwarding-instance \*\<instance\> route-distinguisher

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target:

virtual-router \*<vr> forwarding-instance \*<instance> vrf-target
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+----------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                               | Required   | Multi   |
+====================================================================================================+============+=========+
| :ref: `import<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-import>` | No         | No      |
+----------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `export<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-export>` | No         | No      |
+----------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-import:

virtual-router \*<vr> forwarding-instance \*<instance> vrf-target import
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target>`
Required  No
Multiple  No
Default:  -
========  ===================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                      | Required   | Multi   |
+===========================================================================================================+============+=========+
| :ref: `target<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-import-target>` | No         | No      |
+-----------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-import-target:

virtual-router \*<vr> forwarding-instance \*<instance> vrf-target import \*<target>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-import>`
Required  No
Multiple  Yes
Default:  -
Name      target
========  ==========================================================================================================


.. py:function:: make_forwarding_instance_import_target(target)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> vrf-target import \*\<target\>` node

    :param target: virtual-router \*\<vr\> forwarding-instance \*\<instance\> vrf-target import

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-export:

virtual-router \*<vr> forwarding-instance \*<instance> vrf-target export
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target>`
Required  No
Multiple  No
Default:  -
========  ===================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                      | Required   | Multi   |
+===========================================================================================================+============+=========+
| :ref: `target<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-export-target>` | No         | No      |
+-----------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-export-target:

virtual-router \*<vr> forwarding-instance \*<instance> vrf-target export \*<target>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vrf-target-export>`
Required  No
Multiple  Yes
Default:  -
Name      target
========  ==========================================================================================================


.. py:function:: make_forwarding_instance_export_target(target)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> vrf-target export \*\<target\>` node

    :param target: virtual-router \*\<vr\> forwarding-instance \*\<instance\> vrf-target export

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vpn-id:

virtual-router \*<vr> forwarding-instance \*<instance> vpn-id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                           | Required   | Multi   |
+================================================================================================+============+=========+
| :ref: `vpn_id<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vpn-id-vpn_id>` | Yes        | No      |
+------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vpn-id-vpn_id:

virtual-router \*<vr> forwarding-instance \*<instance> vpn-id <vpn_id>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===============================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vpn-id>`
Required  Yes
Multiple  No
Default:  -
Name      vpn_id
========  ===============================================================================================


.. py:function:: make_forwarding_instance_vpn_id(vpn_id)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> vpn-id \<vpn_id\>` node

    :param vpn_id: virtual-router \*\<vr\> forwarding-instance \*\<instance\> vpn-id

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans:

virtual-router \*<vr> forwarding-instance \*<instance> vlans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+-------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                            | Required   | Multi   |
+=================================================================================================+============+=========+
| :ref: `vlan_id<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id>` | No         | No      |
+-------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id:

virtual-router \*<vr> forwarding-instance \*<instance> vlans \*<vlan_id>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans>`
Required  No
Multiple  Yes
Default:  -
Name      vlan_id
========  ==============================================================================================


.. py:function:: make_vlan_id(vlan_id)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> vlans \*\<vlan_id\>` node

    :param vlan_id: virtual-router \*\<vr\> forwarding-instance \*\<instance\> vlans


Contains:

+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                            | Required   | Multi   |
+=================================================================================================================+============+=========+
| :ref: `name<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-name>`               | No         | Yes     |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `description<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-description>` | No         | Yes     |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-name:

virtual-router \*<vr> forwarding-instance \*<instance> vlans \*<vlan_id> name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id>`
Required  No
Multiple  No
Default:  -
========  ======================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                   | Required   | Multi   |
+========================================================================================================+============+=========+
| :ref: `name<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-name-name>` | Yes        | No      |
+--------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-name-name:

virtual-router \*<vr> forwarding-instance \*<instance> vlans \*<vlan_id> name <name>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===========================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-name>`
Required  Yes
Multiple  No
Default:  -
Name      name
========  ===========================================================================================================


.. py:function:: make_vlan_name(name)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> vlans \*\<vlan_id\> name \<name\>` node

    :param name: virtual-router \*\<vr\> forwarding-instance \*\<instance\> vlans \*\<vlan_id\> name

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-description:

virtual-router \*<vr> forwarding-instance \*<instance> vlans \*<vlan_id> description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id>`
Required  No
Multiple  No
Default:  -
========  ======================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                        | Required   | Multi   |
+=============================================================================================================================+============+=========+
| :ref: `description<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-description-description>` | Yes        | No      |
+-----------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-description-description:

virtual-router \*<vr> forwarding-instance \*<instance> vlans \*<vlan_id> description <description>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-vlans-vlan_id-description>`
Required  Yes
Multiple  No
Default:  -
Name      description
========  ==================================================================================================================


.. py:function:: make_vlan_description(description)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> vlans \*\<vlan_id\> description \<description\>` node

    :param description: virtual-router \*\<vr\> forwarding-instance \*\<instance\> vlans \*\<vlan_id\> description

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                     | Required   | Multi   |
+==========================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface>` | Yes        | No      |
+----------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces>`
Required  Yes
Multiple  Yes
Default:  -
Name      interface
========  ===================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                     | Required   | Multi   |
+==========================================================================================================+============+=========+
| :ref: `unit<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit>` | No         | Yes     |
+----------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =============================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface>`
Required  No
Multiple  No
Default:  -
========  =============================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                          | Required   | Multi   |
+===============================================================================================================+============+=========+
| :ref: `unit<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit>`
Required  No
Multiple  Yes
Default:  0
Name      unit
========  ==================================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                             | Required   | Multi   |
+==================================================================================================================================+============+=========+
| :ref: `description<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-description>` | No         | Yes     |
+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `inet<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet>`               | No         | Yes     |
+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `inet6<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6>`             | No         | Yes     |
+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `iso<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-iso>`                 | No         | Yes     |
+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `mpls<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-mpls>`               | No         | Yes     |
+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `bridge<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge>`           | No         | Yes     |
+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-description:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                         | Required   | Multi   |
+==============================================================================================================================================+============+=========+
| :ref: `description<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-description-description>` | Yes        | No      |
+----------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-description-description:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> description <description>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-description>`
Required  Yes
Multiple  No
Default:  -
Name      description
========  ===================================================================================================================================


.. py:function:: make_unit_description(description)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> description \<description\>` node

    :param description: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> description

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> inet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                          | Required   | Multi   |
+===============================================================================================================================+============+=========+
| :ref: `address<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet-address>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet-address:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> inet address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ============================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet>`
Required  No
Multiple  No
Default:  -
========  ============================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                  | Required   | Multi   |
+=======================================================================================================================================+============+=========+
| :ref: `address<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet-address-address>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet-address-address:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> inet address \*<address>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ====================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet-address>`
Required  No
Multiple  Yes
Default:  -
Name      address
========  ====================================================================================================================================


.. py:function:: make_unit_inet_address(address)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> inet address \*\<address\>` node

    :param address: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> inet address

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> inet6
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                           | Required   | Multi   |
+================================================================================================================================+============+=========+
| :ref: `address<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6-address>` | No         | No      |
+--------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6-address:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> inet6 address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =============================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6>`
Required  No
Multiple  No
Default:  -
========  =============================================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                   | Required   | Multi   |
+========================================================================================================================================+============+=========+
| :ref: `address<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6-address-address>` | No         | No      |
+----------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6-address-address:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> inet6 address \*<address>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =====================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-inet6-address>`
Required  No
Multiple  Yes
Default:  -
Name      address
========  =====================================================================================================================================


.. py:function:: make_unit_inet6_address(address)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> inet6 address \*\<address\>` node

    :param address: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> inet6 address

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-iso:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> iso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================================


.. py:function:: make_unit_iso(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> iso` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\>

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-mpls:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> mpls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================================


.. py:function:: make_unit_mpls(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> mpls` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\>

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                        | Required   | Multi   |
+=============================================================================================================================================+============+=========+
| :ref: `switchport<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport>`       | No         | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `port-security<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `num<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num>`                     | Yes        | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `num<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num>`                     | Yes        | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `dynamic_vlans<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge switchport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge>`
Required  No
Multiple  No
Default:  -
========  ==============================================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                         | Required   | Multi   |
+==============================================================================================================================================+============+=========+
| :ref: `untagged<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-untagged>` | No         | No      |
+----------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `native<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-native>`     | No         | No      |
+----------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `tagged<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-tagged>`     | No         | No      |
+----------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-untagged:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge switchport untagged
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =========================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport>`
Required  No
Multiple  No
Default:  -
========  =========================================================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                        | Required   | Multi   |
+=============================================================================================================================================================+============+=========+
| :ref: `vlan_filter<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-untagged-vlan_filter>` | Yes        | No      |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-untagged-vlan_filter:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge switchport untagged \*<vlan_filter>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-untagged>`
Required  Yes
Multiple  Yes
Default:  -
Name      vlan_filter
========  ==================================================================================================================================================


.. py:function:: make_switchport_untagged(vlan_filter)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge switchport untagged \*\<vlan_filter\>` node

    :param vlan_filter: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge switchport untagged

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-native:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge switchport native
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =========================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport>`
Required  No
Multiple  No
Default:  -
========  =========================================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                              | Required   | Multi   |
+===================================================================================================================================================+============+=========+
| :ref: `vlan_id<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-native-vlan_id>` | Yes        | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-native-vlan_id:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge switchport native <vlan_id>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-native>`
Required  Yes
Multiple  No
Default:  -
Name      vlan_id
========  ================================================================================================================================================


.. py:function:: make_switchport_native(vlan_id)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge switchport native \<vlan_id\>` node

    :param vlan_id: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge switchport native

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-tagged:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge switchport tagged
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =========================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport>`
Required  No
Multiple  No
Default:  -
========  =========================================================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                      | Required   | Multi   |
+===========================================================================================================================================================+============+=========+
| :ref: `vlan_filter<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-tagged-vlan_filter>` | Yes        | No      |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-tagged-vlan_filter:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge switchport tagged \*<vlan_filter>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-switchport-tagged>`
Required  Yes
Multiple  Yes
Default:  -
Name      vlan_filter
========  ================================================================================================================================================


.. py:function:: make_switchport_tagged(vlan_filter)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge switchport tagged \*\<vlan_filter\>` node

    :param vlan_filter: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge switchport tagged

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge port-security
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge>`
Required  No
Multiple  No
Default:  -
========  ==============================================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                      | Required   | Multi   |
+===========================================================================================================================================================+============+=========+
| :ref: `max-mac-count<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security-max-mac-count>` | No         | No      |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security-max-mac-count:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge port-security max-mac-count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ============================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security>`
Required  No
Multiple  No
Default:  -
========  ============================================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                    | Required   | Multi   |
+=========================================================================================================================================================+============+=========+
| :ref: `limit<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security-max-mac-count-limit>` | Yes        | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security-max-mac-count-limit:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge port-security max-mac-count <limit>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-port-security-max-mac-count>`
Required  Yes
Multiple  No
Default:  -
Name      limit
========  ==========================================================================================================================================================


.. py:function:: make_unit_port_security_max_mac(limit)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge port-security max-mac-count \<limit\>` node

    :param limit: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge port-security max-mac-count

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge>`
Required  Yes
Multiple  Yes
Default:  -
Name      num
========  ==============================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                        | Required   | Multi   |
+=============================================================================================================================================+============+=========+
| :ref: `stack<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-stack>`             | No         | Yes     |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `outer_vlans<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-outer_vlans>` | No         | Yes     |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `inner_vlans<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-inner_vlans>` | No         | Yes     |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `op_num<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num>`           | No         | Yes     |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-stack:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                  | Required   | Multi   |
+=======================================================================================================================================+============+=========+
| :ref: `stack<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-stack-stack>` | Yes        | No      |
+---------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-stack-stack:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> stack <stack>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-stack>`
Required  Yes
Multiple  No
Default:  0
Name      stack
========  ========================================================================================================================================


.. py:function:: make_input_vlan_map_stack(stack)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> stack \<stack\>` node

    :param stack: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> stack

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-outer_vlans:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> outer_vlans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                    | Required   | Multi   |
+=========================================================================================================================================================+============+=========+
| :ref: `vlan_filter<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-outer_vlans-vlan_filter>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-outer_vlans-vlan_filter:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> outer_vlans \*<vlan_filter>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-outer_vlans>`
Required  No
Multiple  Yes
Default:  -
Name      vlan_filter
========  ==============================================================================================================================================


.. py:function:: make_input_vlan_map_outer_vlans(vlan_filter)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> outer_vlans \*\<vlan_filter\>` node

    :param vlan_filter: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> outer_vlans

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-inner_vlans:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> inner_vlans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                    | Required   | Multi   |
+=========================================================================================================================================================+============+=========+
| :ref: `vlan_filter<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-inner_vlans-vlan_filter>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-inner_vlans-vlan_filter:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> inner_vlans \*<vlan_filter>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-inner_vlans>`
Required  No
Multiple  Yes
Default:  -
Name      vlan_filter
========  ==============================================================================================================================================


.. py:function:: make_input_vlan_map_inner_vlans(vlan_filter)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> inner_vlans \*\<vlan_filter\>` node

    :param vlan_filter: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> inner_vlans

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> \*<op_num>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num>`
Required  No
Multiple  Yes
Default:  -
Name      op_num
========  ==================================================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                             | Required   | Multi   |
+==================================================================================================================================+============+=========+
| :ref: `op<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num-op>` | Yes        | Yes     |
+----------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num-op:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> \*<op_num> <op>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =========================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num>`
Required  Yes
Multiple  No
Default:  -
Name      op
========  =========================================================================================================================================


.. py:function:: make_input_vlan_map_rewrite_operation(op)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> \*\<op_num\> \<op\>` node

    :param op: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> \*\<op_num\>


Contains:

+-----------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                    | Required   | Multi   |
+=========================================================================================================================================+============+=========+
| :ref: `vlan<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num-op-vlan>` | No         | No      |
+-----------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num-op-vlan:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge \*<num> \*<op_num> <op> <vlan>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ============================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-num-op_num-op>`
Required  No
Multiple  No
Default:  -
Name      vlan
========  ============================================================================================================================================


.. py:function:: make_input_vlan_map_rewrite_vlan(vlan)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> \*\<op_num\> \<op\> \<vlan\>` node

    :param vlan: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge \*\<num\> \*\<op_num\> \<op\>

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge dynamic_vlans
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge>`
Required  No
Multiple  No
Default:  -
========  ==============================================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                  | Required   | Multi   |
+=======================================================================================================================================================+============+=========+
| :ref: `vlan_filter<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge dynamic_vlans \*<vlan_filter>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ============================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans>`
Required  No
Multiple  Yes
Default:  -
Name      vlan_filter
========  ============================================================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                      | Required   | Multi   |
+===========================================================================================================================================================+============+=========+
| :ref: `service<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter-service>` | No         | Yes     |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter-service:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge dynamic_vlans \*<vlan_filter> service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                              | Required   | Multi   |
+===================================================================================================================================================================+============+=========+
| :ref: `service<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter-service-service>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter-service-service:

virtual-router \*<vr> forwarding-instance \*<instance> interfaces \*<interface> unit \*<unit> bridge dynamic_vlans \*<vlan_filter> service <service>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-interfaces-interface-unit-unit-bridge-dynamic_vlans-vlan_filter-service>`
Required  No
Multiple  No
Default:  -
Name      service
========  ================================================================================================================================================================


.. py:function:: make_interface_serivce_vlan(service)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge dynamic_vlans \*\<vlan_filter\> service \<service\>` node

    :param service: virtual-router \*\<vr\> forwarding-instance \*\<instance\> interfaces \*\<interface\> unit \*\<unit\> bridge dynamic_vlans \*\<vlan_filter\> service

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route:

virtual-router \*<vr> forwarding-instance \*<instance> route
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+---------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                        | Required   | Multi   |
+=============================================================================================+============+=========+
| :ref: `inet<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet>`   | No         | No      |
+---------------------------------------------------------------------------------------------+------------+---------+
| :ref: `inet6<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6>` | No         | No      |
+---------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet:

virtual-router \*<vr> forwarding-instance \*<instance> route inet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route>`
Required  No
Multiple  No
Default:  -
========  ==============================================================================================


Contains:

+----------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                               | Required   | Multi   |
+====================================================================================================+============+=========+
| :ref: `static<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static>` | No         | No      |
+----------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static:

virtual-router \*<vr> forwarding-instance \*<instance> route inet static
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet>`
Required  No
Multiple  No
Default:  -
========  ===================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                    | Required   | Multi   |
+=========================================================================================================+============+=========+
| :ref: `route<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route>` | No         | No      |
+---------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route:

virtual-router \*<vr> forwarding-instance \*<instance> route inet static <route>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static>`
Required  No
Multiple  No
Default:  -
Name      route
========  ==========================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                | Required   | Multi   |
+=====================================================================================================================+============+=========+
| :ref: `next-hop<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route-next-hop>` | No         | No      |
+---------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `discard<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route-discard>`   | No         | No      |
+---------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route-next-hop:

virtual-router \*<vr> forwarding-instance \*<instance> route inet static <route> next-hop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route>`
Required  No
Multiple  No
Default:  -
========  ================================================================================================================


Contains:

+------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                         | Required   | Multi   |
+==============================================================================================================================+============+=========+
| :ref: `next_hop<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route-next-hop-next_hop>` | No         | No      |
+------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route-next-hop-next_hop:

virtual-router \*<vr> forwarding-instance \*<instance> route inet static <route> next-hop \*<next_hop>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =========================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route-next-hop>`
Required  No
Multiple  Yes
Default:  -
Name      next_hop
========  =========================================================================================================================


.. py:function:: make_inet_static_route_next_hop(next_hop)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> route inet static \<route\> next-hop \*\<next_hop\>` node

    :param next_hop: virtual-router \*\<vr\> forwarding-instance \*\<instance\> route inet static \<route\> next-hop

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route-discard:

virtual-router \*<vr> forwarding-instance \*<instance> route inet static <route> discard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet-static-route>`
Required  No
Multiple  No
Default:  -
========  ================================================================================================================


.. py:function:: make_inet_static_route_discard(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> route inet static \<route\> discard` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> route inet static \<route\>

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6:

virtual-router \*<vr> forwarding-instance \*<instance> route inet6
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route>`
Required  No
Multiple  No
Default:  -
========  ==============================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                | Required   | Multi   |
+=====================================================================================================+============+=========+
| :ref: `static<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static>` | No         | No      |
+-----------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static:

virtual-router \*<vr> forwarding-instance \*<instance> route inet6 static
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ====================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6>`
Required  No
Multiple  No
Default:  -
========  ====================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                     | Required   | Multi   |
+==========================================================================================================+============+=========+
| :ref: `route<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route>` | No         | No      |
+----------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route:

virtual-router \*<vr> forwarding-instance \*<instance> route inet6 static <route>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===========================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static>`
Required  No
Multiple  No
Default:  -
Name      route
========  ===========================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                 | Required   | Multi   |
+======================================================================================================================+============+=========+
| :ref: `next-hop<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route-next-hop>` | No         | No      |
+----------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route-next-hop:

virtual-router \*<vr> forwarding-instance \*<instance> route inet6 static <route> next-hop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route>`
Required  No
Multiple  No
Default:  -
========  =================================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                          | Required   | Multi   |
+===============================================================================================================================+============+=========+
| :ref: `next_hop<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route-next-hop-next_hop>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route-next-hop-next_hop:

virtual-router \*<vr> forwarding-instance \*<instance> route inet6 static <route> next-hop \*<next_hop>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-route-inet6-static-route-next-hop>`
Required  No
Multiple  Yes
Default:  -
Name      next_hop
========  ==========================================================================================================================


.. py:function:: make_inet6_static_route_next_hop(next_hop)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> route inet6 static \<route\> next-hop \*\<next_hop\>` node

    :param next_hop: virtual-router \*\<vr\> forwarding-instance \*\<instance\> route inet6 static \<route\> next-hop

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols:

virtual-router \*<vr> forwarding-instance \*<instance> protocols
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ========================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance>`
Required  No
Multiple  No
Default:  -
========  ========================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                            | Required   | Multi   |
+=================================================================================================================+============+=========+
| :ref: `telnet<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-telnet>`               | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `ssh<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ssh>`                     | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `http<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-http>`                   | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `https<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-https>`                 | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `snmp<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp>`                   | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `isis<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis>`                   | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `ospf<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf>`                   | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `ldp<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp>`                     | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `rsvp<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp>`                   | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `pim<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim>`                     | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `igmp-snooping<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping>` | No         | No      |
+-----------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-telnet:

virtual-router \*<vr> forwarding-instance \*<instance> protocols telnet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


.. py:function:: make_protocols_telnet(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols telnet` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ssh:

virtual-router \*<vr> forwarding-instance \*<instance> protocols ssh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


.. py:function:: make_protocols_ssh(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols ssh` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-http:

virtual-router \*<vr> forwarding-instance \*<instance> protocols http
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


.. py:function:: make_protocols_http(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols http` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-https:

virtual-router \*<vr> forwarding-instance \*<instance> protocols https
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


.. py:function:: make_protocols_https(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols https` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                         | Required   | Multi   |
+==============================================================================================================+============+=========+
| :ref: `community<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community>` | No         | No      |
+--------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `trap<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap>`           | No         | No      |
+--------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp community
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================


Contains:

+------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                   | Required   | Multi   |
+========================================================================================================================+============+=========+
| :ref: `community<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community>` | Yes        | No      |
+------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp community \*<community>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community>`
Required  Yes
Multiple  Yes
Default:  -
Name      community
========  =================================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                     | Required   | Multi   |
+==========================================================================================================================+============+=========+
| :ref: `level<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community-level>` | Yes        | Yes     |
+--------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community-level:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp community \*<community> level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===========================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community>`
Required  Yes
Multiple  No
Default:  -
========  ===========================================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                           | Required   | Multi   |
+================================================================================================================================+============+=========+
| :ref: `level<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community-level-level>` | Yes        | No      |
+--------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community-level-level:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp community \*<community> level <level>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-community-community-level>`
Required  Yes
Multiple  No
Default:  -
Name      level
========  =================================================================================================================================


.. py:function:: make_snmp_community_level(level)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols snmp community \*\<community\> level \<level\>` node

    :param level: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols snmp community \*\<community\> level

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp trap
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                              | Required   | Multi   |
+===================================================================================================================+============+=========+
| :ref: `community<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community>` | Yes        | No      |
+-------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp trap community
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ============================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap>`
Required  Yes
Multiple  No
Default:  -
========  ============================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                        | Required   | Multi   |
+=============================================================================================================================+============+=========+
| :ref: `community<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community>` | Yes        | No      |
+-----------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp trap community \*<community>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ======================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community>`
Required  Yes
Multiple  Yes
Default:  -
Name      community
========  ======================================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                        | Required   | Multi   |
+=============================================================================================================================+============+=========+
| :ref: `host<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community-host>` | Yes        | Yes     |
+-----------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community-host:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp trap community \*<community> host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community>`
Required  Yes
Multiple  No
Default:  -
========  ================================================================================================================================


Contains:

+----------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                   | Required   | Multi   |
+========================================================================================================================================+============+=========+
| :ref: `address<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community-host-address>` | Yes        | No      |
+----------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community-host-address:

virtual-router \*<vr> forwarding-instance \*<instance> protocols snmp trap community \*<community> host \*<address>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =====================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-snmp-trap-community-community-host>`
Required  Yes
Multiple  Yes
Default:  -
Name      address
========  =====================================================================================================================================

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis:

virtual-router \*<vr> forwarding-instance \*<instance> protocols isis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                         | Required   | Multi   |
+==============================================================================================================+============+=========+
| :ref: `area<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-area>`           | No         | No      |
+--------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface>` | No         | No      |
+--------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-area:

virtual-router \*<vr> forwarding-instance \*<instance> protocols isis area
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                    | Required   | Multi   |
+=========================================================================================================+============+=========+
| :ref: `area<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-area-area>` | Yes        | No      |
+---------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-area-area:

virtual-router \*<vr> forwarding-instance \*<instance> protocols isis area \*<area>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ============================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-area>`
Required  Yes
Multiple  Yes
Default:  -
Name      area
========  ============================================================================================================


.. py:function:: make_isis_area(area)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols isis area \*\<area\>` node

    :param area: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols isis area

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols isis interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================


Contains:

+------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                   | Required   | Multi   |
+========================================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface>` | Yes        | No      |
+------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols isis interface \*<interface>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface>`
Required  Yes
Multiple  Yes
Default:  -
Name      interface
========  =================================================================================================================


.. py:function:: make_isis_interface(interface)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols isis interface \*\<interface\>` node

    :param interface: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols isis interface


Contains:

+--------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                     | Required   | Multi   |
+==========================================================================================================================+============+=========+
| :ref: `level<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface-level>` | No         | Yes     |
+--------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface-level:

virtual-router \*<vr> forwarding-instance \*<instance> protocols isis interface \*<interface> level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===========================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface>`
Required  No
Multiple  No
Default:  -
========  ===========================================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                           | Required   | Multi   |
+================================================================================================================================+============+=========+
| :ref: `level<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface-level-level>` | Yes        | No      |
+--------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface-level-level:

virtual-router \*<vr> forwarding-instance \*<instance> protocols isis interface \*<interface> level \*<level>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-isis-interface-interface-level>`
Required  Yes
Multiple  Yes
Default:  -
Name      level
========  =================================================================================================================================


.. py:function:: make_isis_level(level)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols isis interface \*\<interface\> level \*\<level\>` node

    :param level: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols isis interface \*\<interface\> level

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf:

virtual-router \*<vr> forwarding-instance \*<instance> protocols ospf
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                         | Required   | Multi   |
+==============================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf-interface>` | No         | No      |
+--------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols ospf interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================


Contains:

+------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                   | Required   | Multi   |
+========================================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf-interface-interface>` | Yes        | No      |
+------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf-interface-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols ospf interface \*<interface>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ospf-interface>`
Required  Yes
Multiple  Yes
Default:  -
Name      interface
========  =================================================================================================================


.. py:function:: make_ospf_interface(interface)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols ospf interface \*\<interface\>` node

    :param interface: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols ospf interface

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp:

virtual-router \*<vr> forwarding-instance \*<instance> protocols ldp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                        | Required   | Multi   |
+=============================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp-interface>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols ldp interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp>`
Required  No
Multiple  No
Default:  -
========  ======================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                  | Required   | Multi   |
+=======================================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp-interface-interface>` | Yes        | No      |
+-----------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp-interface-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols ldp interface \*<interface>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-ldp-interface>`
Required  Yes
Multiple  Yes
Default:  -
Name      interface
========  ================================================================================================================


.. py:function:: make_ldp_interface(interface)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols ldp interface \*\<interface\>` node

    :param interface: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols ldp interface

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp:

virtual-router \*<vr> forwarding-instance \*<instance> protocols rsvp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                         | Required   | Multi   |
+==============================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp-interface>` | No         | No      |
+--------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols rsvp interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp>`
Required  No
Multiple  No
Default:  -
========  =======================================================================================================


Contains:

+------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                   | Required   | Multi   |
+========================================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp-interface-interface>` | Yes        | No      |
+------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp-interface-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols rsvp interface \*<interface>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-rsvp-interface>`
Required  Yes
Multiple  Yes
Default:  -
Name      interface
========  =================================================================================================================


.. py:function:: make_rsvp_interface(interface)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols rsvp interface \*\<interface\>` node

    :param interface: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols rsvp interface

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim:

virtual-router \*<vr> forwarding-instance \*<instance> protocols pim
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                        | Required   | Multi   |
+=============================================================================================================+============+=========+
| :ref: `mode<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-mode>`           | Yes        | No      |
+-------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-interface>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-mode:

virtual-router \*<vr> forwarding-instance \*<instance> protocols pim mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim>`
Required  Yes
Multiple  No
Default:  -
========  ======================================================================================================


Contains:

+--------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                   | Required   | Multi   |
+========================================================================================================+============+=========+
| :ref: `mode<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-mode-mode>` | Yes        | No      |
+--------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-mode-mode:

virtual-router \*<vr> forwarding-instance \*<instance> protocols pim mode <mode>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ===========================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-mode>`
Required  Yes
Multiple  No
Default:  -
Name      mode
========  ===========================================================================================================


.. py:function:: make_pim_mode(mode)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols pim mode \<mode\>` node

    :param mode: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols pim mode

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols pim interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ======================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim>`
Required  No
Multiple  No
Default:  -
========  ======================================================================================================


Contains:

+-----------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                  | Required   | Multi   |
+=======================================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-interface-interface>` | Yes        | No      |
+-----------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-interface-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols pim interface \*<interface>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-pim-interface>`
Required  Yes
Multiple  Yes
Default:  -
Name      interface
========  ================================================================================================================


.. py:function:: make_pim_interface(interface)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols pim interface \*\<interface\>` node

    :param interface: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols pim interface

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols>`
Required  No
Multiple  No
Default:  -
========  ==================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                        | Required   | Multi   |
+=============================================================================================================+============+=========+
| :ref: `vlan<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping>`
Required  No
Multiple  No
Default:  -
========  ================================================================================================================


Contains:

+------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                             | Required   | Multi   |
+==================================================================================================================+============+=========+
| :ref: `vlan<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan>` | No         | No      |
+------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan \*<vlan>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  =====================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan>`
Required  No
Multiple  Yes
Default:  -
Name      vlan
========  =====================================================================================================================


Contains:

+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                        | Required   | Multi   |
+=============================================================================================================================================+============+=========+
| :ref: `version<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-version>`                 | No         | Yes     |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `immediate-leave<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-immediate-leave>` | No         | Yes     |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface>`             | No         | Yes     |
+---------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-version:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan \*<vlan> version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan>`
Required  No
Multiple  No
Default:  -
========  ==========================================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                | Required   | Multi   |
+=====================================================================================================================================+============+=========+
| :ref: `version<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-version-version>` | Yes        | No      |
+-------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-version-version:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan \*<vlan> version <version>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-version>`
Required  Yes
Multiple  No
Default:  -
Name      version
========  ==================================================================================================================================

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-immediate-leave:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan \*<vlan> immediate-leave
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan>`
Required  No
Multiple  No
Default:  -
========  ==========================================================================================================================

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan \*<vlan> interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==========================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan>`
Required  No
Multiple  No
Default:  -
========  ==========================================================================================================================


Contains:

+-------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                      | Required   | Multi   |
+===========================================================================================================================================+============+=========+
| :ref: `interface<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface-interface>` | No         | No      |
+-------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface-interface:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan \*<vlan> interface \*<interface>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ====================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface>`
Required  No
Multiple  Yes
Default:  -
Name      interface
========  ====================================================================================================================================


.. py:function:: make_igmp_snooping_interface(interface)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols igmp-snooping vlan \*\<vlan\> interface \*\<interface\>` node

    :param interface: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols igmp-snooping vlan \*\<vlan\> interface


Contains:

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+
| Node                                                                                                                                                              | Required   | Multi   |
+===================================================================================================================================================================+============+=========+
| :ref: `multicast-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface-interface-multicast-router>` | No         | Yes     |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+---------+

.. _dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface-interface-multicast-router:

virtual-router \*<vr> forwarding-instance \*<instance> protocols igmp-snooping vlan \*<vlan> interface \*<interface> multicast-router
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========  ==============================================================================================================================================
Parent    :ref: `virtual-router<dev-confdb-syntax-virtual-router-vr-forwarding-instance-instance-protocols-igmp-snooping-vlan-vlan-interface-interface>`
Required  No
Multiple  No
Default:  -
========  ==============================================================================================================================================


.. py:function:: make_igmp_snooping_multicast_router(None)

    Generate `virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols igmp-snooping vlan \*\<vlan\> interface \*\<interface\> multicast-router` node

    :param None: virtual-router \*\<vr\> forwarding-instance \*\<instance\> protocols igmp-snooping vlan \*\<vlan\> interface \*\<interface\>

