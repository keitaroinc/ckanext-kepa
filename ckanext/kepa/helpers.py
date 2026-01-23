from ckan.common import config, asbool
import ckan.plugins.toolkit as toolkit


def allow_resource_upload() -> bool:

    upload_config = config.get('ckan.allow_resource_upload', False)
    return asbool(upload_config)


def group_show_full(group_id):
    try:
        return toolkit.get_action('group_show')(
            {'ignore_auth': True},
            {'id': group_id}
        )
    except Exception:
        return None


def organization_show_full(org_id):
    try:
        return toolkit.get_action('organization_show')(
            {'ignore_auth': True},
            {'id': org_id}
        )
    except Exception:
        return None


def homepage_facets(lang):
    facet_field = f"keywords_facet_{lang}"

    data_dict = {
        "rows": 0,
        "facet.field": [facet_field],
        "include_private": False,
    }

    result = toolkit.get_action("package_search")({}, data_dict)
    return result.get("search_facets", {})
