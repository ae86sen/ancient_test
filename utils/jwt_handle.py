def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'user_id': user.id,
        'user_name': user.username,
        'token': token
    }


