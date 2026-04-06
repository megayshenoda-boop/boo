"""
IGG Conquerors Bot - Authentication
=====================================
HTTP 4-step login flow + ADB key extraction.
Pure Python implementation (no Node.js required).
"""
import hashlib
import hmac as hmac_module
import base64
import json
import re
import time
import uuid
import subprocess
import urllib.request
from urllib.request import Request
from urllib.parse import quote
from urllib.error import HTTPError
from http.cookiejar import CookieJar
from datetime import datetime

from config import (
    GAME_ID, HMAC_KEY, ADB_PATH, ADB_DEVICE,
    EMAIL, PASSWORD, IGG_ID, USER_AGENT,
)


def _log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] [{level}] {msg}")


def _md5(s):
    return hashlib.md5(s.encode('utf-8') if isinstance(s, str) else s).hexdigest()


def _generate_sign(params, game_id):
    keys = sorted(params.keys())
    parts = [f"{k}={params[k]}" for k in keys]
    joined = "&".join(parts)
    return _md5(joined + _md5(game_id)).upper()


def http_login(email=None, password=None, igg_id=None, game_id=None, hmac_key=None):
    """Full HTTP login flow (4 steps). Returns access_token or None.

    Steps:
        1. GET  /embed/entry          -> PHPSESSID cookie
        2. POST /embed/login/email    -> SSO auth
        3. POST /embed/login/user_id  -> Platform JWT
        4. POST /ums/member/access_token/platform -> access_token (HMAC-SHA256)
    """
    email = email or EMAIL
    password = password or PASSWORD
    igg_id = igg_id or IGG_ID
    game_id = game_id or GAME_ID
    hmac_key = hmac_key or HMAC_KEY

    _log("=== HTTP LOGIN START ===")
    udid = str(uuid.uuid4())
    uiid = str(uuid.uuid4())
    ua = f"{game_id}/6.1.0 Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G9880 Build/N2G47H)"

    cookie_jar = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    # Step 1: Get PHPSESSID
    _log("Step 1: Getting PHPSESSID...")
    nonce1 = str(int(time.time() * 1000))
    sign1 = _generate_sign({
        'for_audting': '0', 'resource': 'embed/entry', 'scenario': 'sign_in',
        'x-gpc-game-id': game_id, 'x-gpc-nonce': nonce1,
        'x-gpc-udid': udid, 'x-gpc-uiid': uiid,
        'x_gpc_jsbridge': 'gpc_jsbridge_common/2.0.0_2;'
    }, game_id)

    url1 = "https://account.igg.com/embed/entry?scenario=sign_in&for_audting=0&x_gpc_jsbridge=gpc_jsbridge_common%2F2.0.0_2%3B"
    req1 = Request(url1, headers={
        "User-Agent": ua, "X-Requested-With": "com.igg.android.conquerors",
        "x-gpc-game-id": game_id, "x-gpc-sign": sign1,
        "x-gpc-nonce": nonce1, "x-gpc-ver": "3.0",
        "x-gpc-udid": udid, "x-gpc-uiid": uiid
    })

    try:
        resp1 = opener.open(req1, timeout=15)
        resp1.read()
    except Exception as e:
        _log(f"Step 1 error: {e}", "ERROR")
        return None

    phpsessid = None
    for cookie in cookie_jar:
        if cookie.name == "PHPSESSID":
            phpsessid = cookie.value
    if not phpsessid:
        _log("Step 1: PHPSESSID not found!", "ERROR")
        return None
    _log(f"Step 1: PHPSESSID = {phpsessid}")

    # Step 2: Email login
    _log("Step 2: Email login...")
    login_body = f"email={quote(email)}&password={_md5(password)}&token="
    req2 = Request("https://account.igg.com/embed/login/email", data=login_body.encode(), headers={
        "User-Agent": ua, "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://account.igg.com/embed/login/index",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    })

    try:
        resp2 = opener.open(req2, timeout=15)
        data2 = json.loads(resp2.read())
    except HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        _log(f"Step 2 HTTP error {e.code}: {body[:200]}", "ERROR")
        return None
    except Exception as e:
        _log(f"Step 2 error: {e}", "ERROR")
        return None

    if data2.get("error", {}).get("code") != 0:
        _log(f"Step 2: Login failed: {json.dumps(data2, ensure_ascii=False)[:200]}", "ERROR")
        return None
    _log("Step 2: Login OK!")

    # Step 3: Get Platform JWT
    _log("Step 3: Getting Platform JWT...")
    req3_body = f"user_id={igg_id}"
    req3 = Request("https://account.igg.com/embed/login/user_id", data=req3_body.encode(), headers={
        "User-Agent": ua, "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://account.igg.com/embed/login/index",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    })

    try:
        resp3 = opener.open(req3, timeout=15)
        data3 = json.loads(resp3.read())
    except Exception as e:
        _log(f"Step 3 error: {e}", "ERROR")
        return None

    redirect_url = data3.get("data", {}).get("redirectUrl", "")
    jwt_match = re.search(r'token=([^&]+)', redirect_url)
    if not jwt_match:
        _log("Step 3: JWT not found", "ERROR")
        return None
    platform_jwt = jwt_match.group(1)
    _log(f"Step 3: JWT ({len(platform_jwt)} chars)")

    # Step 4: Get Access Token (HMAC-SHA256)
    _log("Step 4: Getting Access Token...")
    step4_body = f"type=gpcaccount&platform_token={quote(json.dumps({'token': platform_jwt}))}"
    body_digest = base64.b64encode(hashlib.sha256(step4_body.encode()).digest()).decode()
    nonce4 = str(int(time.time() * 1000))
    utc_date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

    canonical = "\n".join([
        f"x-gpc-uiid: {uiid}", f"x-gpc-nonce: {nonce4}",
        "x-gpc-evo: 1;gpc=s2", f"x-gpc-game-id: {game_id}",
        f"x-gpc-udid: {udid}", f"digest: SHA-256={body_digest}",
        f"date: {utc_date}", "POST /ums/member/access_token/platform HTTP/1.1"
    ])

    sig = base64.b64encode(
        hmac_module.new(hmac_key.encode(), canonical.encode(), hashlib.sha256).digest()
    ).decode()

    auth_header = (
        f'hmac username="{game_id}", algorithm="hmac-sha256", '
        f'headers="x-gpc-uiid x-gpc-nonce x-gpc-evo x-gpc-game-id x-gpc-udid digest date request-line", '
        f'signature="{sig}"'
    )

    req4 = Request("https://apis-dsa.iggapis.com/ums/member/access_token/platform",
                   data=step4_body.encode(), headers={
        "x-gpc-uiid": uiid, "x-gpc-nonce": nonce4,
        "x-gpc-evo": "1;gpc=s2", "x-gpc-game-id": game_id,
        "x-gpc-udid": udid, "x-gpc-ver": "2.5", "x-gpc-family": "bmbkf3",
        "Date": utc_date, "Digest": f"SHA-256={body_digest}",
        "User-Agent": f"{ua} GPCSDK/2.29.0-su.1-beta.1.0+137",
        "Authorization": auth_header,
        "Host": "apis-dsa.iggapis.com",
        "Content-Type": "application/x-www-form-urlencoded"
    })

    try:
        resp4 = opener.open(req4, timeout=15)
        data4 = json.loads(resp4.read())
    except HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        _log(f"Step 4 HTTP error {e.code}: {body[:300]}", "ERROR")
        return None
    except Exception as e:
        _log(f"Step 4 error: {e}", "ERROR")
        return None

    access_token = data4.get("data", {}).get("access_token")
    if not access_token:
        _log(f"Step 4: No access_token: {json.dumps(data4)[:200]}", "ERROR")
        return None

    _log(f"Step 4: Access Token = {access_token}")
    _log("=== HTTP LOGIN SUCCESS ===")
    return access_token


def extract_key_from_adb(adb_path=None, device=None):
    """Extract weg_Accesskey from device/emulator via ADB."""
    adb_path = adb_path or ADB_PATH
    device = device or ADB_DEVICE
    _log("Extracting access key from device via ADB...")
    try:
        cmd = [adb_path, "-s", device, "shell",
               "cat /data/data/com.igg.android.conquerors/shared_prefs/weg_login_file.xml"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        match = re.search(r'weg_Accesskey">(.*?)<', result.stdout)
        if match:
            key = match.group(1)
            _log(f"ADB: Extracted key = {key}")
            return key
    except Exception as e:
        _log(f"ADB extraction failed: {e}", "ERROR")
    return None
