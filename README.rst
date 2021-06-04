ckanext-scheming_dcat
=====================================

|
|

**ckanext-scheming_dcat** provides the DCAT interface to create DCAT **metadata** and **resources**.

The plugin utilizes the exposed features of DCAT by extending the official DCAT plugin from CKAN https://github.com/ckan/ckanext-dcat.

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

|

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

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


|

Configuration
-------------

You must make sure that the following is set in your CKAN config::

    ckan.plugins = dcat dcat_json_interface structured_data scheming_datasets scheming_organizations scheming_dcat

    # OPTIONALLY CONFIGURE DCAT
    ckanext.dcat.rdf.profiles = euro_dcat_ap ckanext.dcat.enable_rdf_endpoints = True

    # Scheming # module-path:file to schemas being used
    scheming.dataset_schemas = ckanext.scheming_dcat:scheming/dcat.yaml
    scheming.organization_schemas = ckanext.scheming_dcat:scheming/dcat_org.json
    scheming.presets = ckanext.scheming_dcat:scheming/presets.json

|

Development
-----------

To install ckanext-scheming_dcat for development, activate your CKAN virtualenv and do::

    git clone https://bitbucket.org/cioapps/ckanext-scheming_dcat.git
    cd ckanext-scheming_dcat
    python setup.py develop

|

Tags
----

|

The plugin comes with Agrovoc support but you can easily configure the plugin to support vocabulary of your choice.

**Loading agrovoc tags**



.. code::

    cd ckanext-scheming_dcat/setup

    nano vocabulary.py

    # Configurations

    base_url= "http://localhost:5000"

    api_key = "XXXXX-XXXXX-XXXXX"

    filename = "agrovoc_en.csv"

    vocabulary_name="agrovoc_en"

    # Run the python script to load the tags

    create_and_load_vocabulary(url, api_key, file_name, vocabulary_name)




Tests
-----

To run the tests:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate


2. From the CKAN root directory (not the extension root) do::

    pytest --ckan-ini=test.ini ckanext/scheming_dcat/tests

|
|

Creating a DCAT package
-----------------------
    
.. list-table:: The table below shows required and type of values to pass to the fields
   :header-rows: 1

   * - Field Name
     - Type
     - Validation
     - Description
     - Required
   * - publisher_url
     - string
     - url
     - (foaf:homepage) A 'homepage' in this sense is a public Web document
     - false
   * - publisher_email
     - string
     - email
     - Internet mailbox associated with exactly one owner
     - false
   * - provenance
     - string
     - url
     - A link from a metadata description to the project that generated the metadata
     - false
   * - owner_org
     - string
     - string
     - The id of the dataset�s owning organization
     - true
   * - notes
     - string
     - string
     - A description of the dataset
     - true
   * - name
     - string
     - string
     - The name of the new dataset, must be between 2 and 100 characters long and contain only lowercase alphanumeric characters, - and _, e.g. 'warandpeace'
     - true
   * - contact_email
     - string
     - email
     - The maintainer or the author's email
     - false
     
**ckanext-scheming_dcat** also provides a field called language which takes a string

.. list-table:: Supported Languages
   :header-rows: 1

   * - Language
     - Value
   * - Arabic
     - ARA
   * - Chinese
     - ZHO
   * - English
     - ENG
   * - French
     - FRA
   * - Russian
     - RUS
   * - Spanish
     - SPA
     

Creating, updating, deleting a **DCAT** Metadata with **curl**

.. code::

    base_url=http://localhost:5000


**APIKEY**

.. code::

    APIKEY=xxxxx-xxxxx-xxxx-xxxxx


.. code::

    curl -H "Content-Type: application/json"
          -X POST $base_url/api/3/action/package_create
          -H "Authorization: $APIKEY" -d '{
                "frequency": "previous version released in 1981",
                "title": "The population",
                "name": "the-population",
                "notes": "This metadata was released and funded by the member countries"
                "owner_org": "africa",
                "private": True,
                "theme": "Africa",
                "language": ["ENG","SPA"],
                "provenance": "http://www.afrostats.com/provenance",
                "type": "dcat",
                "tags": [
                {
                "name": "population"
                }
                ],
                "temporal_start": "2006-01-01",
                "temporal_end": "2007-09-21",
                "publisher_name": "Ahmed Zulu",
                "publisher_email": "ahmed@gov.za",
                "publisher_url": "http://www.publisher.com",
                "contact_name": "Central Afro Stats",
                "contact_email": "info@gov.za",
                "state": "active",
                "version": "africa Rev.4"
                }'


**Updating**  a DCAT package

.. code::

    curl -X PATCH $base_url/api/3/action/package_update
          -H "Authorization: $APIKEY"
          -F "id=the-population" -F "description= The metadata also includes data from Asia and Europe"


**Deleting** a DCAT package

.. code::

    curl -H "Content-Type: application/json"
          -X POST $base_url/api/3/action/package_delete
          -H "Authorization: $APIKEY" -d '{
            "id": "the-population"
            }'


**Creating** a DCAT resource

.. code::

    curl  -H "Content-Type: application/json"
          -X POST $base_url/api/3/action/resource_create
          -H "Authorization: $APIKEY" -d '{
            "package_id": "the-population",
            "url": "data.gov.com/transport",
            "name": "Bus numbers",
            "description": "The number of buses per city in Africa",
            "format": "HTML",
            "license": "http://www.opendefinition.org/licenses/odc-pddl",
            "status": "Operational",
            "language":["ENG","RUS"],
            "download_url": "http://www.data.com/download",
            "issued": "2006-05-01"
            }'

**Creating** a DCAT resource with a file upload

.. code::

    curl  -X POST $base_url/api/3/action/resource_create
          -H "Authorization: $APIKEY"
          -F "name=national-parks" -F "package_id=the-population" -F "description=The number of national parks" -F "upload=@./national-parks.csv"



**Updating**  a DCAT resource

.. code::

    curl -X PATCH $base_url/api/3/action/resource_update
          -H "Authorization: $APIKEY"
          -F "id=xxxx-xxxx-xxxx" -F "description=The number of nationals in Sub Saharan Africa"


**Deleting**  a DCAT resource

.. code::

    curl -X POST $base_url/api/3/action/resource_delete
         -H "Authorization: $APIKEY" -d '{
         "id": "xxxx-xxxx-xxxx"
        }'


