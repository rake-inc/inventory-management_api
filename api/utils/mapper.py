import logging
from postgres import fields


def re_map_user_roles(request_data):
    try:
        role_data = {}
        role_data.update(is_store_manager=request_data.pop(fields.IS_STORE_MANAGER))
        role_data.update(is_department_manager=request_data.pop(fields.IS_DEPARTMENT_MANAGER))
        return request_data, role_data
    except Exception as e:
        logging.error("EXCEPTION REACHED in re_map_user_roles %s" % e)
        return {}


def re_map_role_params(query):
    try:
        result = {}
        query_dict = dict(query)
        for key in query_dict.keys():
            if type(query_dict.get(key)) == list:
                result[key] = query_dict.get(key).pop()
            else:
                result[key] = query_dict.get(key)
            logging.info("Query remapped successfully")
        return result
    except Exception as e:
        logging.error("EXCEPTION REACHED %s" % e)
        return {}


def re_map_role_response(serializer_dict, username):
    try:
        response = serializer_dict.pop()
        response.pop(fields.USER)
        response[fields.USERNAME] = username
        return response
    except Exception as e:
        logging.error("EXCEPTION REACHED %s" % e)
        return {}
