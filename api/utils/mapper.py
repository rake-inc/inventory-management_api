import logging


def re_map_user_roles(request_data):
    try:
        role_data = {}
        role_data.update(store_manager=request_data.pop("store_manager"))
        role_data.update(department_manager=request_data.pop("department_manager"))
        return request_data, role_data
    except Exception as e:
        logging.error("EXCEPTION REACHED %s" % e)
        return {}


def re_map_role_params(query):
    try:
        result = {}
        query_dict = dict(query)
        print query_dict.keys()
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
