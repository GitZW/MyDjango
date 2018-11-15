from core_video.service import videoservice
from utils.common.fs import get_token
from urllib.parse import urljoin, urlencode
from datetime import datetime


def full_domain(url, with_token=True, user_id=None):
    domain = videoservice.get_resource_domain()
    full_url = urljoin(domain, url)
    if not with_token:
        return full_url
    data = dict(
        token=get_token(url, deadline=int(datetime.now().timestamp() + 30 * 60), privilege='download', user_id=user_id))
    params = urlencode(data)

    return full_url + '?' + params
