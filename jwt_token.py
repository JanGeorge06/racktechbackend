import jwt


def generate_token(email):
    payload = {
        "email": email,
    }
    secret_key = 'hv7$#VZ#3SyWU&Q9B@Yb#7e!DkfZ%*nJ'
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token