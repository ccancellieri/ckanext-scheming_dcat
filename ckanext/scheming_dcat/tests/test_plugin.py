'''Tests for plugin.py.'''
import ckan.plugins
from ckan.plugins import toolkit
import pytest
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.model as model
from ckan.plugins.toolkit import NotAuthorized, ValidationError, ObjectNotFound
ckan_29_or_higher = toolkit.check_ckan_version(u'2.9')

class TestSchemingDcat(object):
    admin = None
    package = None
    context = None
    owner_org = None

    @classmethod
    def setup_class(cls):
        helpers.reset_db()
        '''Nose runs this method once to setup our test class.'''
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        if not ckan.plugins.plugin_loaded('dcat'):
            ckan.plugins.load('dcat')
        if not ckan.plugins.plugin_loaded('scheming_dcat'):
            ckan.plugins.load('scheming_dcat')
        if not ckan.plugins.plugin_loaded('scheming_datasets'):
            ckan.plugins.load('scheming_datasets')
        # Create user and package
        cls.admin = factories.User()
        cls.context = {
            'ignore_auth': False,
            'user': cls.admin['name']
        }
        cls.owner_org = factories.Organization(
            users=[{'name': cls.admin['id'], 'capacity': 'admin'}]
        )


    def setup_method(self):
        self.package = {
            'title': 'My test package',
            'name': 'test_package',
            'notes': 'This is a national dataset',
            'owner_org': self.owner_org['id'],
            'private': True,
            'state': 'active',
            'type': 'dcat',
            'admin_name': 'John Doe',
            'tags': [
                {
                    'name': 'population'
                }
            ]
        }

    def test_can_create_a_resource_with_file(self):
        package = helpers.call_action('package_create', self.context, **self.package)
        resource = factories.Resource(package_id=package['id'], format='pdf')
        res = helpers.call_action('resource_create', self.context, **resource)
        assert (res['id'], None)

    def test_can_not_create_a_dcat_resource_without_name_and_url(self):
        package = helpers.call_action('package_create', self.context, **self.package)
        resource = factories.Resource(package_id=package['id'], format='pdf')
        resource.pop('name')
        resource.pop('url')
        with pytest.raises(ValidationError) as e:
            helpers.call_action('resource_create', self.context, **resource)

    def test_can_create_a_dcat_resource_with_name_and_url(self):
        package = helpers.call_action('package_create', self.context, **self.package)
        res = helpers.call_action('resource_create', self.context, name='test',url='http://www.test.org/test', package_id = package['id'])
        assert (res['name'], 'test')

    #https://github.com/ckan/ckanext-scheming/issues/286
    # Commenting out the fields causing this were removed
    def _test_can_not_define_our_own_mandatory_fields_due_to_286(self, app):
        # Todo using the app post
        # env = {'REMOTE_USER': self.admin['name'].encode('ascii')}
        # page = 'api/action/package_create'
        # page = '/' + page if not ckan_29_or_higher else page
        # response = app.post(
        #     url=page,
        #     params= json.dumps(self.package),
        #     extra_environ=env,
        # )
        # if not ckan_29_or_higher:
        #     response = response.follow(extra_environ=env)
        #
        # # assert '<h1 class="page-heading">Page Title</h1>' in response.body
        # assert 1==1
        res = helpers.call_action('package_create', self.context, **self.package)

    # https://github.com/ckan/ckanext-scheming/issues/286
    # Commenting out the fields causing this were removed
    def _test_can_not_define_our_own_mandatory_fields_in_a_resouce_due_to_286(self):
        pass

    def test_can_create_and_delete_a_dcat_package_with_un_official_languages(self):
        package = helpers.call_action('package_create', self.context, **self.package)
        resource = helpers.call_action('resource_create', self.context, name='test', url='http://www.test.org/test', package_id=package['id'], language=['ENG','ZHO'])
        assert (resource['name'], 'test')
        # Delete resource
        helpers.call_action('resource_delete', self.context, **resource)
        with pytest.raises(ObjectNotFound) as e:
            helpers.call_action('resource_show', self.context, **resource)
        # It is still there but with state=deleted
        resource_object = model.Resource.get(resource['id'])
        assert (resource_object.state, 'deleted')



    def test_can_not_create_a_dcat_package_with_none_un_official_languages(self):
        # Can create a dcat dataset
        self.package['language'] = ['ZULU','SHO']
        with pytest.raises(ValidationError) as e:
            helpers.call_action('package_create', self.context, **self.package)

    def test_can_create_and_delete_a_dcat_resource_with_licences_defined_on_the_list(self):
        # Create dataset
        dataset = factories.Dataset(owner_org=self.owner_org['id'])

        # Create resource
        resource = helpers.call_action(
            'resource_create',
            context=self.context,
            package_id=dataset['id'],
            name='created new resourced',
            license='http://www.opendefinition.org/licenses/odc-odbl',
            url='https://example.com/test1')

        assert resource['name'] == 'created new resourced'

        # Delete package
        helpers.call_action('resource_delete', self.context, **resource)
        with pytest.raises(ObjectNotFound) as e:
            helpers.call_action('resource_show', self.context, **resource)
        # It is still there but with state=deleted
        resource_object = model.Resource.get(resource['id'])
        assert (resource_object.state, 'deleted')


    def test_can_not_create_a_dcat_resource_with_licences_not_defined_on_the_list(self):
        # Create resource
        self.package['name'] = 'test00'
        package = helpers.call_action('package_create', self.context, **self.package)
        # Create resource
        new_context = {
            'ignore_auth': False,
            'user': self.admin['name']
        }
        with pytest.raises(ValidationError) as e:
            helpers.call_action('resource_create', new_context, name='test00',
                                url='http://www.test.org/test00',
                                package_id=package['id'], license='http://creativecommons.org/custom_licenses')

    def test_can_create_a_dcat_resouce_with_un_official_languages(self):
        # Create resource
        package = factories.Dataset(owner_org=self.owner_org['id'])
        # Create resource
        new_context = {
            'ignore_auth': False,
            'user': self.admin['name']
        }

        resource = helpers.call_action('resource_create', new_context, name='orange',
                            url='http://www.test.org/orange',
                            package_id=package['id'], language=['ENG', 'ARA'])
        assert (resource['name'], 'test')

    def test_can_not_create_a_dcat_resource_with_none_un_official_languages(self):
        # Create resource
        self.package['name'] = 'test0'
        package = helpers.call_action('package_create', self.context, **self.package)
        # Create resource
        new_context = {
            'ignore_auth': False,
            'user': self.admin['name']
        }
        with pytest.raises(ValidationError) as e:
            helpers.call_action('resource_create', new_context, name='test0',
                                url='http://www.test.org/test0',
                                package_id=package['id'], language=['ZULU','SHONA'])




