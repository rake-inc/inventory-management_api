import logging
from datetime import datetime
from postgres import fields

DATE_FORMAT = '%d-%m-%Y'


def re_map_user_roles(request_data):
    """
    remaps request dict for creating user object entity and role entity
    :param request_data:
    :return result:
    """
    try:
        role_data = {}
        role_data.update(is_store_manager=request_data.pop(fields.IS_STORE_MANAGER))
        role_data.update(is_department_manager=request_data.pop(fields.IS_DEPARTMENT_MANAGER))
        return request_data, role_data
    except Exception as e:
        logging.error("MAPPER EXCEPTION REACHED in re_map_user_roles %s" % e)
        return {}


def re_map_role_params(query):
    """
    remapping url query for querying the models
    :param query:
    :return result:
    """
    try:
        result = {}
        if type(query) != dict:
            query_dict = dict(query)
        else:
            query_dict = query
        for key in query_dict.keys():
            print result
            if type(query_dict.get(key)) == list:
                result[key] = query_dict.get(key).pop()
            else:
                result[key] = query_dict.get(key)
            logging.info("Query remapped successfully")
        return result
    except Exception as e:
        logging.error("MAPPER EXCEPTION REACHED %s" % e)
        return {}


def re_map_role_response(serializer_dict, username):
    """
    remaps user_id with username for serialization
    :param serializer_dict:
    :param username:
    :return response:
    """
    try:
        response = serializer_dict.pop()
        response.pop(fields.USER)
        response[fields.USERNAME] = username
        return response
    except Exception as e:
        logging.error("MAPPER EXCEPTION REACHED %s" % e)
        return {}


def re_map_update_query(query_dict):
    """
    remaps pk and query dictionary
    :param query_dict:
    :return:
    """
    try:
        pk = dict()
        pk[fields.PRIMARY_KEY] = query_dict.pop(fields.PRIMARY_KEY)
        return pk, query_dict
    except Exception as e:
        logging.error("MAPPER EXCEPTION REACHED %s" % e)
        return {}
