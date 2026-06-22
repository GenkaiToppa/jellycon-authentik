from urllib.parse import quote

import xbmcaddon
from base64 import b64encode

_addon = xbmcaddon.Addon()
_user = _addon.getSetting('authentik_username')
_password = _addon.getSetting('authentik_password')

ACTIVE = _user and _password

if ACTIVE:
    _creds = f"{_user}:{_password}".encode('utf-8')
    BASIC = f"Basic {b64encode(_creds).decode()}"

else:
    BASIC = None

TOKEN_HEADER = 'X-Jellyfin-Auth' if ACTIVE else 'Authorization'

def pipe(url: str, transcode: bool = False) -> str:
    if not ACTIVE:
        return url

    parts = [f"Authorization={quote(BASIC, safe='')}"]

    if transcode:
        from .jellyfin import api  # lazy: jellyfin.py imports this module
        token = api.headers.get('X-Jellyfin-Auth', '')
        if token:
            parts.append(f"!X-Jellyfin-Auth={quote(token, safe='')}")

    return f"{url}|{'&'.join(parts)}"

def basic_headers() -> dict[str, str]:
    return {'Authorization': BASIC} if ACTIVE else {}
