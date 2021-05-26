ckanext-scheming_dcat
=====================================

|
|

**ckanext-scheming_dcat** makes it possible for you to publish dcat(https://github.com/ckan/ckanext-dcat) **packages** and **resources**.

|
|

**Image below**: A **DCAT add button** will be added to your theme.

|

.. image:: docs/img/add_dcat_dataset.png
    :alt: DCAT add button

|

**Image below**: Creating a **DCAT** package.

|

.. image:: docs/img/create_dcat_package.png
    :alt: Creating a DCAT package

|

**Image below**: Creating a **DCAT** resource.
|

.. image:: docs/img/dcat_resource_create.png
    :alt: Creating a DCAT resource

|

**Image below**: Viewing a **DCAT** package and resource.

|

.. image:: docs/img/dcat_view.png
    :alt: Viewing a DCAT package and resource

|

Requirements
------------

Before installing ckanext-scheming_dcat, make sure that you have installed the following:

* CKAN 2.8 and above
* DCAT (https://github.com/ckan/ckanext-dcat)
* ckanext-scheming (https://github.com/ckan/ckanext-scheming.git)


Installation
------------

To install ckanext-scheming_dcat:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-scheming_dcat Python package into your virtual environment::

     pip install ckanext-scheming_dcat



3. Add ``dcat dcat_json_interface structured_data scheming_datasets scheming_organizations scheming_dcat`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload



Configuration
-------------

You must make sure that the following is set in your CKAN config::

    ckan.plugins = dcat dcat_json_interface structured_data scheming_datasets scheming_organizations scheming_dcat

    # OPTIONALLY CONFIGURE DCAT # DCAT ckanext.dcat.rdf.profiles = euro_dcat_ap ckanext.dcat.enable_rdf_endpoints = True

    # Scheming # module-path:file to schemas being used scheming.dataset_schemas = ckanext.scheming_dcat:scheming/dcat.yaml scheming.organization_schemas = ckanext.scheming_dcat:scheming/dcat_org.json scheming.presets = ckanext.scheming_dcat:scheming/presets.json


Development
-----------

To install ckanext-scheming_dcat for development, activate your CKAN virtualenv and do::

    git clone https://bitbucket.org/cioapps/ckanext-scheming_dcat.git
    cd ckanext-scheming_dcat
    python setup.py develop

Tests
-----

To run the tests:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate


2. From the CKAN root directory (not the extension root) do::

    pytest --ckan-ini=test.ini ckanext/scheming_dcat/tests

