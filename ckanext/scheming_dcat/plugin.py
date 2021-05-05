import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class Scheming_DcatPlugin(plugins.SingletonPlugin,toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'scheming_dcat')