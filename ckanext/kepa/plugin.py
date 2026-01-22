import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.kepa.helpers as helpers
from ckan.lib.plugins import DefaultTranslation
from ckan.lib import i18n
import json

SUPPORTED_LANGS = ["en", "sq", "sr_Latn"]
DEFAULT_LANG = "en"


class KepaPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IFacets)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "kepa")

    def update_config_schema(self, schema):

        ignore_missing = toolkit.get_validator('ignore_missing')
        validators = [ignore_missing]
        schema.update({
            'footer_social_en': validators,
            'footer_dataportal_en': validators,
            'footer_toolbox_en': validators,
            'footer_social_sq': validators,
            'footer_dataportal_sq': validators,
            'footer_toolbox_sq': validators,
            'footer_social_sr': validators,
            'footer_dataportal_sr': validators,
            'footer_toolbox_sr': validators,
        })

        return schema

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'allow_resource_upload': helpers.allow_resource_upload,
            'organization_show_full': helpers.organization_show_full,
            'group_show_full': helpers.group_show_full,
        }

    # IPackageController
    def before_dataset_index(self, pkg_dict):
        """
        Create language-specific facet fields from fluent_tags.

        Input (Fluent):
            keywords = {
              "en": ["water"],
              "sq": ["ujë"],
              "sr_Latn": ["voda"]
            }

        Output (Solr):
            keywords_facet_en = ["water"]
            keywords_facet_sq = ["ujë"]
            keywords_facet_sr_Latn = ["voda"]
        """

        keywords = pkg_dict.get("keywords")
        if not keywords:
            return pkg_dict

        if isinstance(keywords, str):
            try:
                keywords = json.loads(keywords)
            except ValueError:
                return pkg_dict

        if not isinstance(keywords, dict):
            return pkg_dict

        for lang in SUPPORTED_LANGS:
            values = keywords.get(lang)

            if isinstance(values, list) and values:
                pkg_dict[f"keywords_facet_{lang}"] = values

        # Optional: fallback field (union of all languages)
        fallback = []
        for values in keywords.values():
            if isinstance(values, list):
                fallback.extend(values)

        if fallback:
            pkg_dict["keywords_facet"] = fallback

        return pkg_dict

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        """
        Select the facet field based on current UI language.
        """

        lang = i18n.get_lang()

        if lang not in SUPPORTED_LANGS:
            lang = DEFAULT_LANG

        facet_field = f"keywords_facet_{lang}"

        facets_dict = facets_dict.copy()
        facets_dict[facet_field] = toolkit._("Keywords")
        
        return facets_dict
