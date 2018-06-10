def response_JO_N(user_data, db):
    match_protocol, user_name, user_psw = user_data.split(";")
    user_name_duplicated = db.check_name_duplicate(user_name)
    if user_name_duplicated:
        return 'N_ER'
    else:
        db.add_user_to_db(user_name, user_psw)
        J_OK = 'J_OK' + ';' + user_name
        return J_OK


def response_JOIN(user_data, db):
    match_protocol, user_name, user_psw = user_data.split(";")
    result = db.verify_user(user_name, user_psw)
    if result:
        J_OK = 'J_OK' + ';' + user_name
        return J_OK
    else:
        return 'J_ER'


def response_DATA(user_data):
    match_protocol, user_name, user_msg = user_data.split(";")
    broadcast_msg = match_protocol + ';' + user_name + ": " + user_msg
    return broadcast_msg


def response_QUIT(user_data):
    match_protocol, user_name = user_data.split(";")
    return match_protocol, user_name





