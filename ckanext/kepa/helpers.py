from ckan.common import config, asbool

def allow_resource_upload() -> bool:
    
    upload_config = config.get('ckan.allow_resource_upload', False)
    return asbool(upload_config)