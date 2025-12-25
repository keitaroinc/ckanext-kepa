import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.kepa.helpers as helpers
from ckan.lib.plugins import DefaultTranslation



class KepaPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "kepa")

    def update_config_schema(self, schema):

        ignore_missing = toolkit.get_validator('ignore_missing')
        validators = [ignore_missing]
        schema.update({
            'footer_social': validators,
            'footer_dataportal': validators,
            'footer_toolbox': validators,
        })

        return schema

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'allow_resource_upload': helpers.allow_resource_upload,
        }