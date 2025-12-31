from ckan.common import config, asbool
from ckan.plugins.toolkit import get_action
from ckan import model

def allow_resource_upload() -> bool:
    
    upload_config = config.get('ckan.allow_resource_upload', False)
    return asbool(upload_config)


def organization_show_full(org_id):
    context = {
        'model': model,
        'ignore_auth': True,
    }

    return get_action('organization_show')(
        context,
        {'id': org_id, 'include_extras': True}
    )
