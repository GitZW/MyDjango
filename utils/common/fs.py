import hmac
import json
from _sha1 import sha1
from base64 import urlsafe_b64encode, urlsafe_b64decode
from datetime import datetime

from utils.common.gf_conf import get_value

ENCODER = 'utf-8'

SECRET_KEY = get_value('fs_secret').encode(ENCODER)


class AuthError(Exception):
    pass


def get_token(key, deadline, privilege='upload', user_id=None):
    """

    :param key:
    :param deadline:
    :param privilege: upload|download
    :param user_id
    :return:
    """
    assert isinstance(key, str)
    assert isinstance(deadline, int)
    params = {
        'key': key,
        'deadline': deadline,
        'privilege': privilege
    }
    if user_id is not None:
        params['user_id'] = user_id
    json_data = json.dumps(params).encode(ENCODER)
    data = urlsafe_b64encode(json_data).decode(ENCODER)
    sign = urlsafe_b64encode(_sign(json_data)).decode(ENCODER)
    return '{}:{}'.format(sign, data)


def decode_token(token):
    assert isinstance(token, str)

    sign, data = token.split(':')
    sign = urlsafe_b64decode(sign)
    data = urlsafe_b64decode(data)

    sign1 = _sign(data)
    if sign != sign1:
        raise AuthError('upload token sign error')
    result = json.loads(data.decode(ENCODER))
    if datetime.fromtimestamp(result['deadline']) < datetime.now():
        raise AuthError('upload token expired')
    return result


def _sign(data):
    return hmac.new(SECRET_KEY, data, sha1).digest()
