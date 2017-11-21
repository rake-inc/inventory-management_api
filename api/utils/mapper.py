import logging


def re_map_user_roles(serializers_dict):
    try:
        result = {}
        for key in serializers_dict.keys():
            result[key] = serializers_dict.get(key)
        result['user'] = serializers_dict.get('user_id')
        result.pop("user_id")
        logging.info("Serializer remapped")
        return result
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
