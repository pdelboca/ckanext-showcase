import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import validate

from ckanext.showcase.logic.schema import showcase_package_list_schema
from ckanext.showcase.model import ShowcasePackageAssociation

import logging
log = logging.getLogger(__name__)


def showcase_package_list(context, data_dict):
    '''List packages associated with a showcase.

    :param showcase_id: id or name of the showcase
    :type showcase_id: string

    :rtype: list of dictionaries
    '''

    toolkit.check_access('ckanext_showcase_package_list', context, data_dict)

    # validate the incoming data_dict
    validated_data_dict, errors = validate(data_dict, showcase_package_list_schema(), context)

    if errors:
        raise toolkit.ValidationError(errors)

    # get a list of package ids associated with showcase id
    pkg_id_list = ShowcasePackageAssociation.get_package_ids(validated_data_dict['showcase_id'])

    pkg_list = []
    if pkg_id_list is not None:
        # for each package id, get the package dict and append to list
        for pkg_id in pkg_id_list:
            pkg = toolkit.get_action('package_show')(context, {'id': pkg_id})
            pkg_list.append(pkg)

    return pkg_list
