def extract_user_name(client_data):
    protocol, user_name, other_data = client_data.split(";")
    return user_name


    