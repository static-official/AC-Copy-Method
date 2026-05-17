# replace everything including photon (app id is fusion 2 and custom auth url is ur backend /auth)

from flask import Flask, request, jsonify, send_file
import requests
import json
import ipaddress
import secrets
import base64
import time
import sqlite3
import random
import os
import string
import hashlib
import uuid
from datetime import datetime, timezone



GENERATE_FRESH_TOKENS = True
DB_PATH = '/home/XeraCompany/mysite/userdata.db'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE'

# Directory paths for JSON data files
dih2 = '/home/XeraCompany/mysite'
dih3 = '/home/XeraCompany/mysite'



def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            ip TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            custom_id TEXT NOT NULL,
            create_time REAL NOT NULL
        )
    ''')
    
    # Banned IPs table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS banned_ips (
            ip TEXT PRIMARY KEY
        )
    ''')
    
    conn.commit()
    conn.close()



app = Flask(__name__)
init_db()


def b64decode_json(obj):
    """Decode base64 encoded JSON"""
    return json.loads(base64.urlsafe_b64decode(obj + '=' * (-len(obj) % 4)).decode())

def b64encode_json(obj):
    """Encode JSON to base64"""
    return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode().rstrip('=')

def log_to_discord(message: str):
    """Log message to Discord webhook"""
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"[Webhook Error] {e}")

def generate_username():
    """Generate random username"""
    return 'Xera+' + ''.join(random.choices(string.ascii_uppercase, k=6))

def generate_custom_id():
    """Generate random custom ID"""
    return ''.join(random.choices(string.digits, k=17))

def get_client_ip():
    """Get client IP address from request"""
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def is_trusted_ip(ip_address):
    """Check if IP address is trusted"""
    try:
        trusted_public_ips = {'YOUR_TRUSTED_IP_1', 'YOUR_TRUSTED_IP_2'}
        if ip_address in trusted_public_ips:
            return True
        ip = ipaddress.ip_address(ip_address)
        if ip.version == 4:
            return (
                ip in ipaddress.IPv4Network('YOUR_SUBNET_1/24') or
                ip in ipaddress.IPv4Network('YOUR_SUBNET_2/29')
            )
        return ip in ipaddress.IPv6Network('YOUR_IPV6_SUBNET/64')
    except ValueError:
        return False

def get_or_create_user(ip):
    """Get or create user from database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('SELECT 1 FROM banned_ips WHERE ip = ?', (ip,))
    if cur.fetchone():
        conn.close()
        return None, True

    cur.execute('SELECT username, custom_id FROM users WHERE ip = ?', (ip,))
    result = cur.fetchone()

    if result:
        username, custom_id = result
    else:
        if ip == '127.0.0.1':
            username = '<color=red>0x11'
        else:
            username = generate_username()
        custom_id = generate_custom_id()
        cur.execute(
            'INSERT INTO users (ip, username, custom_id, create_time) VALUES (?, ?, ?, ?)',
            (ip, username, custom_id, time.time())
        )
        conn.commit()

    conn.close()
    return {'username': username, 'custom_id': custom_id}, False

def generate_jwt(user_id):
    """Generate JWT token"""
    header = {'alg': 'HS256', 'typ': 'JWT'}
    now = int(time.time())
    payload = {
        'tid': secrets.token_hex(16),
        'uid': user_id,
        'usn': secrets.token_hex(5),
        'vrs': {
            'authID': secrets.token_hex(20),
            'clientUserAgent': 'MetaQuest 1.16.3.1138_5edcbd98',
            'deviceID': secrets.token_hex(20),
            'loginType': 'meta_quest'
        },
        'exp': now + 72000,
        'iat': now
    }

    def b64encode(obj):
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode().rstrip('=')

    signature = secrets.token_urlsafe(32)
    return f"{b64encode(header)}.{b64encode(payload)}.{signature}"

def generate_token_pair():
    """Generate token pair"""
    user_id = secrets.token_hex(16)
    return {
        'token': generate_jwt(user_id),
        'refresh_token': generate_jwt(user_id)
    }

def BearerGeneration(ussername):
    """Generate bearer token for specific username"""
    header = {'alg': 'HS256', 'typ': 'JWT'}
    now = int(time.time())
    if ussername == "unitygame":
        id = "8c1acc32f2454fb9a9a76fb6dfbf572f"
        id2 = "f6ac88a5575546c2b2b7ca93d3e3f488"
    else:
        id = uuid.uuid4().hex
        id2 = uuid.uuid4().hex
    refreshpayload = {
        'tid': id2,
        'uid': id,
        'usn': ussername,
        'vrs': {
            'authID': secrets.token_hex(16),
            'clientUserAgent': "MetaQuest 0.16.0.6767_3e923582",
            'loginType': "meta_quest"
        },
        'exp': now + 3600,
        'iat': now
    }
    signature = secrets.token_urlsafe(32)
    token = f"{b64encode_json(header)}.{b64encode_json(refreshpayload)}.{signature}"
    return jsonify({"token": token}), 200

def SessionRefresh(token):
    """Refresh session token"""
    changetoken = b64decode_json(token)
    now = int(time.time())
    changetoken['exp'] = now + 3600
    header = {'alg': 'HS256', 'typ': 'JWT'}
    signature = secrets.token_urlsafe(32)
    Bearer = f"{b64encode_json(header)}.{b64encode_json(changetoken)}.{signature}"
    return jsonify({
        "token": Bearer
    }), 200

def generate_gameplay_loadout():
    """Generate random gameplay loadout"""
    try:
        with open('/home/XeraCompany/mysite/econ_gameplay_items.json', 'r') as f:
            data = json.load(f)
        item_ids = [item['id'] for item in data if 'id' in item]
    except Exception as e:
        print(f"Failed to load econ_gameplay_items.json: {e}")
        item_ids = [
            'item_jetpack', 'item_flaregun', 'item_dynamite', 'item_tablet',
            'item_flashlight_mega', 'item_plunger', 'item_crossbow',
            'item_revolver', 'item_shotgun', 'item_pickaxe'
        ]

    children = []
    for _ in range(20):
        if random.random() < 0.7 and 'item_arena_pistol' in item_ids:
            selected_item = 'item_arena_pistol'
        else:
            selected_item = random.choice(item_ids)
        children.append({
            'itemID': selected_item,
            'scaleModifier': 100,
            'colorHue': random.randint(10, 111),
            'colorSaturation': random.randint(10, 111)
        })

    payload = {
        'objects': [{
            'collection': 'user_inventory',
            'key': 'gameplay_loadout',
            'permission_read': 1,
            'permission_write': 1,
            'value': json.dumps({
                'version': 1,
                'back': {
                    'itemID': 'item_backpack_large_base',
                    'scaleModifier': 120,
                    'colorHue': 50,
                    'colorSaturation': 50,
                    'children': children
                }
            })
        }]
    }
    return payload

def skidatoken(clankersfuckassid, diddyid, metaupdate):
    """Generate skida token"""
    data = f"{clankersfuckassid}|{diddyid}|{metaupdate}"
    salt = os.urandom(16)
    digest = hashlib.sha256(salt + data.encode()).digest()
    token = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    mid = len(token) // 2
    token = token[:mid] + "-" + token[mid:]
    return token

def ilowkeydontknowwhy():
    """Generate expiration time"""
    efsfdfsdsdf = int(time.time())
    gfshrtfhfghjfgd = efsfdfsdsdf + 86400
    return "gfshrtfhfghjfgd"

def noncevalidation(nonce, oculus_id):
    """Validate nonce with Oculus"""
    response = requests.post(
        url=f'https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={oculus_id}&access_token={""}',
        headers={"content-type": "application/json"}
    )
    return response.json().get("is_valid")

# ═══════════════════════════════════════════════════════════════════════════
# STATIC DATA
# ═══════════════════════════════════════════════════════════════════════════

STATIC_TOKEN_PAIR = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiI3OGU0NDBiOS00NWZjLTRhODYtOTllMy02ZGM5Y2RjN2M1N2UiLCJ1aWQiOiJmM2E1NjE4YS1hMzNmLTQyMDAtYThiYS1lYjM3YzdiZmJmOWMiLCJ1c24iOiJ4ZW5pdHl5dCIsInZycyI6eyJhdXRoSUQiOiJkYTEzZjU4YzJiMjU0ZTgwYTM5YzA3YzRlNzkyNjlmOSIsImNsaWVudFVzZXJBZ2VudCI6Ik1ldGFRdWVzdCAxLjE2LjMuMTEzOF81ZWRjYmQ5OCIsImRldmljZUlEIjoiMTcyZjZjMmU3MWE5NGMwMTBjMWY2Mjk5OWJjM2QzMjEiLCJsb2dpblR5cGUiOiJtZXRhX3F1ZXN0In0sImV4cCI6MTc0NDA2MzQwNiwiaWF0IjoxNzQzOTk0MzE4fQ.nRJLbep6nCGeBTwruOunyNjDUiLxfcvpAJHl7E6n3m8',
    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiI3OGU0NDBiOS00NWZjLTRhODYtOTllMy02ZGM5Y2RjN2M1N2UiLCJ1aWQiOiJmM2E1NjE4YS1hMzNmLTQyMDAtYThiYS1lYjM3YzdiZmJmOWMiLCJ1c24iOiJ4ZW5pdHl5dCIsInZycyI6eyJhdXRoSUQiOiJkYTEzZjU4YzJiMjU0ZTgwYTM5YzA3YzRlNzkyNjlmOSIsImNsaWVudFVzZXJBZ2VudCI6Ik1ldGFRdWVzdCAxLjE2LjMuMTEzOF81ZWRjYmQ5OCIsImRldmljZUlEIjoiMTcyZjZjMmU3MWE5NGMwMTBjMWY2Mjk5OWJjM2QzMjEiLCJsb2dpblR5cGUiOiJtZXRhX3F1ZXN0In0sImV4cCI6MTc0NDE0NjIwNiwiaWF0IjoxNzQzOTk0MzE4fQ.f7nTHNnPrJW6oYYo54RDks1iDvntTP2yiBfpHdH-ygQ'
}

CLIENT_BOOTSTRAP_RESPONSE = {
    'payload': '{"updateType":"Optional","attestResult":"Valid","attestTokenExpiresAt":1820877961,"photonAppID":"YOUR_PHOTON_APP_ID","photonVoiceAppID":"YOUR_PHOTON_VOICE_APP_ID","termsAcceptanceNeeded":[],"dailyMissionDateKey":"","dailyMissions":null,"dailyMissionResetTime":0,"serverTimeUnix":1720877961,"gameDataURL":"https://xeracompany.pythonanywhere.com/game-data-prod.zip"}'
}

ECON_ITEMS_RESPONSE = {
    'payload': '[{"id":"item_apple","netID":71,"name":"Apple","description":"An apple a day keeps the doctor away!","category":"Consumables","price":200,"value":7,"isLoot":true,"isPurchasable":false,"isUnique":false,"isDevOnly":false}]'
}

SERVER_TIME_RESPONSE = {
    'payload': '{"serverTimeUnix":1720877961,"cachedExpiresAt":1820877961}'
}

STATIC_STORAGE_OBJECTS = {
    'objects': [
        {
            'collection': 'user_avatar',
            'key': '0',
            'user_id': '2e8aace0-282d-4c3d-b9d4-6a3b3ba2c2a6',
            'value': '{"butt":"bp_butt_gorilla","head":"bp_head_gorilla","tail":"","torso":"bp_torso_gorilla","armLeft":"bp_arm_l_gorilla","eyeLeft":"bp_eye_gorilla","armRight":"bp_arm_r_gorilla","eyeRight":"bp_eye_gorilla","accessories":["acc_fit_varsityjacket"],"primaryColor":"604170"}',
            'version': '7a326a2a4d0639a5f08e3116bb99a3bf',
            'permission_read': 2,
            'create_time': '2024-10-29T00:22:08Z',
            'update_time': '2025-04-04T03:55:19Z'
        }
    ]
}

STATIC_ACCOUNT_RESPONSE = {
    'user': {
        'id': '2e8aace0-282d-4c3d-b9d4-6a3b3ba2c2a6',
        'username': 'ERROR',
        'lang_tag': 'en',
        'metadata': '{}',
        'edge_count': 4,
        'create_time': '2024-08-24T07:30:12Z',
        'update_time': '2025-04-05T21:00:27Z'
    },
    'wallet': '{"stashCols": 4, "stashRows": 2, "hardCurrency": 30000000, "softCurrency": 20000000, "researchPoints": 500000}',
    'custom_id': '26344644298513663'
}

def autism():
    """Return default storage objects"""
    return {
        "objects": [
            {
                "collection": "user_avatar",
                "key": "0",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{}",
                "version": "e897bbeb9a5d4364d73dee44c2d4e6e4",
                "permission_read": 2,
                "create_time": "2024-09-20T21:26:18Z",
                "update_time": "2025-08-08T09:22:23Z"
            },
            {
                "collection": "user_inventory",
                "key": "avatar",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{}",
                "version": "277a87beb4905dbe2333d5cd55a7e5be",
                "permission_read": 1,
                "create_time": "2024-09-20T21:26:18Z",
                "update_time": "2025-08-07T01:22:02Z"
            },
            {
                "collection": "user_inventory",
                "key": "research",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{\"nodes\": [\"node_dynamite\", \"node_teleport_grenade\", \"node_glowsticks\", \"node_skill_backpack_cap_1\", \"node_skill_health_1\", \"node_crowbar\", \"node_flaregun\", \"node_ogre_hands\", \"node_revolver\", \"node_skill_gundamage_1\", \"node_skill_explosive_1\", \"node_rpg\", \"node_skill_selling_1\", \"node_revolver_ammo\", \"node_rpg_ammo\", \"node_flashbang\", \"node_impact_grenade\", \"node_cluster_grenade\", \"node_jetpack\", \"node_shotgun\", \"node_tripwire_explosive\", \"node_crossbow\", \"node_tablet\", \"node_plunger\", \"node_umbrella\", \"node_backpack\", \"node_flashlight_mega\", \"node_lance\", \"node_balloon\", \"node_saddle\", \"node_skill_right_hip_attachment\", \"node_skill_left_hip_attachment\", \"node_sticky_dynamite\", \"node_rpg_cny\", \"node_zipline_gun\", \"node_zipline_rope\", \"node_company_ration\", \"node_balloon_heart\", \"node_crossbow_heart\", \"node_arrow\", \"node_arrow_heart\", \"node_hoverpad\", \"node_quiver\", \"node_backpack_large\", \"node_shield\", \"node_shield_police\", \"node_hookshot\", \"node_baseball_bat\", \"node_police_baton\", \"node_heart_gun\", \"node_pogostick\", \"node_boxfan\", \"node_mega_broccoli\", \"node_mini_broccoli\", \"node_dynamite_cube\", \"node_skill_backpack_cap_2\", \"node_whoopie\", \"node_disposable_camera\", \"node_sticker_dispenser\", \"node_impulse_grenade\", \"node_stash_grenade\", \"node_cardboardbox\", \"node_rpg_easter\", \"node_rpg_ammo_egg\", \"node_pinata_bat\", \"node_hawaiian_drum\", \"node_ukulele\", \"node_anti_gravity_grenade\", \"node_antigrav_grenade\", \"node_football\", \"node_skill_backpack_cap_3\", \"node_item_nut_shredder\", \"node_hookshot_sword\", \"node_rpg_spear\", \"node_rpg_ammo_spear\", \"node_skill_health_2\", \"node_skill_selling_2\", \"node_skill_selling_3\", \"node_frying_pan\", \"node_skill_melee_1\", \"node_skill_melee_2\", \"node_skill_melee_3\", \"node_viking_hammer\", \"node_viking_hammer_twilight\", \"node_mega_broccoli_bomb\", \"node_micro_broccoli_bomb\", \"node_teleport_gun\", \"node_arrow_bomb\", \"node_robo_monke\", \"node_friend_launcher\", \"node_grenade_launcher\"]}",
                "version": "58c1d1c4ade0e8e205939be8a07ce49b",
                "permission_read": 1,
                "create_time": "2024-11-25T17:55:33Z",
                "update_time": "2025-07-14T21:34:27Z"
            },
            {
                "collection": "user_inventory",
                "key": "stash",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{\"items\": []}",
                "version": "d1315c03b540bef68ce4742d46e77cc0",
                "permission_read": 1,
                "permission_write": 1,
                "create_time": "2025-02-11T22:35:00Z",
                "update_time": "2025-08-07T17:14:27Z"
            },
            {
                "collection": "user_inventory",
                "key": "stash_upgrades",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{\"upgrades\": [\"col_1\", \"col_2\", \"col_3\", \"col_4\", \"col_5\", \"col_6\", \"col_7\", \"col_8\", \"row_1\", \"row_2\", \"row_3\", \"row_4\", \"row_5\", \"row_6\", \"row_7\", \"row_8\", \"mtl_1\", \"mtl_2\", \"mtl_3\", \"mtl_4\", \"mtl_5\", \"mtl_6\", \"mtl_7\", \"mtl_8\"]}",
                "version": "af1feb89bd8c849f5f16a4754577be04",
                "permission_read": 1,
                "create_time": "2025-07-23T23:32:02Z",
                "update_time": "2025-08-07T17:05:15Z"
            },
            {
                "collection": "user_inventory",
                "key": "gameplay_loadout",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{\"version\": 1}",
                "version": "3846efa925d304495efbfed41eaafe74",
                "permission_read": 1,
                "permission_write": 1,
                "create_time": "2024-10-30T01:21:34Z",
                "update_time": "2025-08-08T20:34:56Z"
            },
            {
                "collection": "user_preferences",
                "key": "gameplay_items",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{\"recents\": []}",
                "version": "fe9acf47fd31aeb3ea1aa209e6485ce3",
                "permission_read": 1,
                "permission_write": 1,
                "create_time": "2024-12-10T20:44:21Z",
                "update_time": "2025-08-09T07:39:43Z"
            },
            {
                "collection": "user_preferences",
                "key": "common",
                "user_id": "3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236",
                "value": "{\"appearOffline\": false}",
                "version": "d56295314bb7a4c43e13da9c446a77a8",
                "permission_read": 1,
                "permission_write": 1,
                "create_time": "2025-06-11T03:57:33Z",
                "update_time": "2025-08-07T18:09:40Z"
            }
        ]
    }

def storage166():
    """Extended storage response with avatar items"""
    base_storage = autism()
    # Add extended avatar inventory
    for obj in base_storage["objects"]:
        if obj["collection"] == "user_inventory" and obj["key"] == "avatar":
            obj["value"] = "{\"items\": [\"acc_ear_l_earring_banana\", \"acc_ear_l_earring_roundgold\", \"acc_face_glasses_blue\", \"acc_fit_varsityjacket\", \"acc_head_cap\", \"animal_gorilla\", \"bp_arm_l_gorilla\", \"bp_arm_r_gorilla\", \"bp_butt_gorilla\", \"bp_eye_gorilla\", \"bp_head_gorilla\", \"bp_tail_cat\", \"bp_torso_gorilla\"]}"
    return base_storage

# ═══════════════════════════════════════════════════════════════════════════
# LOGGING MIDDLEWARE
# ═══════════════════════════════════════════════════════════════════════════

@app.before_request
def log_request_before():
    """Log incoming request details"""
    try:
        headers = dict(request.headers)
        path = request.path
        queries = request.args.to_dict()
        body = request.get_json(silent=True)
        if body is None and request.form:
            body = request.form.to_dict()
        if body is None:
            body = request.data.decode(errors="ignore") or "(empty)"
        else:
            body = json.dumps(body, indent=2)

        message = (
            f"📨 **{request.method} {path}**\n"
            f"🔍 Query: ```json\n{json.dumps(queries, indent=2)}\n```\n"
            f"🧾 Headers: ```json\n{json.dumps(headers, indent=2)}\n```\n"
            f"📦 Body: ```json\n{body}\n```"
        )

        log_to_discord(message)
    except Exception as e:
        print(f"[Log Error] {e}")

@app.after_request
def log_request_after(response):
    """Log all requests to Discord webhook after processing"""
    method = request.method
    url = request.url
    path = request.path
    headers = dict(request.headers)
    body = request.get_data(as_text=True)
    query_params = dict(request.args)
    status_code = response.status_code

    message = {
        'content': f"📡 **Request to: {path}**",
        'embeds': [{
            'title': 'Request Details',
            'fields': [
                {'name': 'Method', 'value': method, 'inline': True},
                {'name': 'Path', 'value': path, 'inline': True},
                {'name': 'Status Code', 'value': str(status_code), 'inline': True},
                {'name': 'Full URL', 'value': url, 'inline': False},
                {'name': 'Query Params', 'value': f"```json\n{json.dumps(query_params, indent=2)}```" if query_params else '*(none)*', 'inline': False},
                {'name': 'Headers', 'value': f"```json\n{json.dumps(headers, indent=2)}```", 'inline': False},
                {'name': 'Body', 'value': f"```json\n{body}```" if body else '*(empty)*', 'inline': False}
            ],
            'color': 65280 if status_code < 400 else 16711680
        }]
    }
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=message)
    except Exception:
        pass
    
    return response



@app.route('/', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/', methods=['GET', 'POST'])
def root_endpoint():
    """Root endpoint"""
    return jsonify({"token": "b"}), 200

@app.route('/Halloween/authenticEate/Redo/Sigma', methods=['GET', 'POST'])
def halloween_auth():
    """Halloween authentication endpoint"""
    userid = secrets.token_hex(16)
    sessionid = secrets.token_hex(16)
    return jsonify({
        "Authenticated": "true",
        "ResultCode": 1,
        "UserId": userid,
        "SessionID": sessionid,
        "Message": "Authenticated successfully"
    })

@app.route('/3/v2/account/authenticate/custom', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/account/authenticate/custom', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/account/authenticate/custom', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def authenticate_custom():
    """Custom authentication endpoint"""
    username = request.args.get("username", "")
    
    # Check for banned users
    if username == "xmissalexanderx":
        return jsonify({"error": "banned for 48 hours REASON: racism"}), 403
    
    # Generate loadout
    generate_gameplay_loadout()
    
    # Return bearer token or token pair based on request
    if username:
        return BearerGeneration(username)
    
    return jsonify(generate_token_pair() if GENERATE_FRESH_TOKENS else STATIC_TOKEN_PAIR)

@app.route('/3/v2/account/session/refresh', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/account/session/refresh', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/account/session/refresh', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def session_refresh():
    """Session refresh endpoint"""
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    
    if token:
        try:
            payload = b64decode_json(token.split(".")[1])
            now = int(time.time())
            payload['exp'] = now + 3600
            return SessionRefresh(token.split(".")[1])
        except Exception:
            pass
    
    return jsonify(generate_token_pair() if GENERATE_FRESH_TOKENS else STATIC_TOKEN_PAIR)

@app.route('/3/v2/account/link/device', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/account/link/device', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/account/link/device', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def link_device():
    """Link device endpoint"""
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    
    try:
        payload = b64decode_json(token.split(".")[1])
        user_id = payload["uid"]
    except Exception:
        user_id = secrets.token_hex(16)
    
    return jsonify({
        'id': secrets.token_hex(16),
        'user_id': user_id,
        'linked': True,
        'create_time': datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })

@app.route('/auth', methods=['GET', 'POST'])
def photon_auth():
    """Photon authentication endpoint"""
    auth_token = request.args.get('auth_token')
    print('🔐 Photon Auth Request Received')

    if auth_token:
        print(f"auth_token: {auth_token}")
        message = 'Authentication successful'
    else:
        print('⚠️ No auth_token provided')
        message = 'Authenticated without token'

    return jsonify({
        'ResultCode': 1,
        'Message': message,
        'UserId': secrets.token_hex(16),
        'SessionID': secrets.token_hex(12),
        'Authenticated': True
    }), 200

@app.route('/nnnnaakamacloud/api/v1/preauth', methods=['POST'])
def preauth():
    """Preauth endpoint"""
    playershit = request.get_json()
    CurrentPlayerVersion = "Skidding"
    AttestID = str(uuid.uuid4())
    PUI = playershit.get("platformUserID")
    DeviceID = request.headers.get("X-Device-Id")
    FBItypeshit = request.headers.get("User-Agent")
    expiration = ilowkeydontknowwhy()
    attestNonce = skidatoken(PUI, DeviceID, FBItypeshit)
    return jsonify({
        "time": expiration,
        "updateType": CurrentPlayerVersion,
        "attestID": AttestID,
        "attestNonce": attestNonce
    })



@app.route('/3/v2/account', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/account', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/account', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def account():
    """Main account endpoint"""
    if request.method == 'PUT':
        response = jsonify({})
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response.headers['Content-Type'] = 'application/json'
        response.headers['Grpc-Metadata-Content-Type'] = 'application/grpc'
        return response

    # Extract token and username
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    
    username = ""
    try:
        payload = b64decode_json(token.split(".")[1])
        username = payload.get("usn", "")
    except Exception:
        pass

    # Special user handling
    custom_id = secrets.token_hex(8)
    
    special_users = {
        "unitygame": {
            "username": "<color=purple>Exploding_Car</color>",
            "display_name": "<color=purple>Exploding_Car</color>",
            "custom_id": "24968022896116226"
        },
        "skibb.ok": {
            "username": "<color=yellow>Skibb.Gay</color>",
            "display_name": "<color=yellow>Skibb.Gay</color>",
            "custom_id": "24968022896116226"
        },
        "Omelette180": {
            "username": "<color=purple>COOL PERSON</color>:Omelette",
            "display_name": "<color=purple>COOL PERSON</color>Omelette180",
            "custom_id": "24968022896116226"
        },
        "sergiovr": {
            "username": "<color=red>SKIBIDI RIZZ</color>",
            "display_name": "<color=red>SKIBIDI RIZZ</color>",
            "custom_id": custom_id
        },
        "FakeXera": {
            "username": "<color=purple>Fake Xera</color>",
            "display_name": "<color=purple>Fake Xera</color>",
            "custom_id": custom_id
        },
        "GunyahJohnVr": {
            "username": "<size=5><color=green>Gunyah</color></size>",
            "display_name": "<size=5><color=green>Gunyah</color></size>",
            "custom_id": custom_id
        },
        "SD_WatchOD": {
            "username": "<color=blue>Watch</color>",
            "display_name": "<color=blue>Watch</color>",
            "custom_id": custom_id
        },
        "kris_kovidov": {
            "username": "<color=purple>kris_kovidov</color>",
            "display_name": "<color=purple>kris_kovidov</color>",
            "custom_id": custom_id
        },
        "N5.tuff": {
            "username": "<color=red>OWNER</color>: N5",
            "display_name": "<color=red>OWNER</color> N5",
            "custom_id": "4938276150923746"
        }
    }
    
    if username in special_users:
        user_data = special_users[username]
        return jsonify({
            "user": {
                "id": uuid.uuid4().hex if username != "unitygame" else "8c1acc32f2454fb9a9a76fb6dfbf572f",
                "username": user_data["username"],
                "display_name": user_data["display_name"],
                "lang_tag": "en",
                "metadata": {"isDeveloper": True},
                "edge_count": 240,
                "create_time": "2024-08-24T04:20:56Z",
                "update_time": "2025-07-25T18:41:17Z"
            },
            "wallet": {
                "stashCols": 8, "stashRows": 8,
                "hardCurrency": 99999999999 if username in ["unitygame", "skibb.ok"] else 1000000,
                "softCurrency": 99999999999 if username in ["unitygame", "skibb.ok"] else 1000000,
                "researchPoints": 9999999999 if username in ["unitygame", "skibb.ok"] else 1000000
            },
            "custom_id": user_data["custom_id"]
        })
    
    # Default IP-based account handling
    try:
        ip = get_client_ip()
        user, banned = get_or_create_user(ip)

        if banned or user is None:
            print(f"[ERROR] User banned or None - IP: {ip}, banned: {banned}, user: {user}")
            raise Exception('User is banned or DB failed')

        display_username = 'XERA COMPANY'
        if is_trusted_ip(ip):
            display_username = 'ALEX [HELPER]'

        return jsonify({
            'user': {
                'id': '2e8aace0-282d-4c3d-b9d4-6a3b3ba2c2a6',
                'username': display_username,
                'lang_tag': 'en',
                'metadata': json.dumps({'isDeveloper': str(is_trusted_ip(ip))}),
                'edge_count': 4,
                'create_time': '2024-08-24T07:30:12Z',
                'update_time': '2025-04-05T21:00:27Z'
            },
            'wallet': '{"stashCols": 16, "stashRows": 8, "hardCurrency": 0, "softCurrency": 20000000, "researchPoints": 69420}',
            'custom_id': user['custom_id']
        })

    except Exception as e:
        print(f"[FALLBACK] DB failed or user banned: {e}")
        import traceback
        traceback.print_exc()
        
        # Return generic account for unknown users
        return jsonify({
            "user": {
                "id": uuid.uuid4().hex,
                "username": username if username else "Player",
                "display_name": username if username else "Player",
                "lang_tag": "en",
                "metadata": {"isDeveloper": True},
                "edge_count": 240,
                "create_time": "2024-08-24T04:20:56Z",
                "update_time": "2025-07-25T18:41:17Z"
            },
            "wallet": {
                "stashCols": 8, "stashRows": 8,
                "hardCurrency": 1000000,
                "softCurrency": 1000000,
                "researchPoints": 1000000
            },
            "custom_id": custom_id
        })

@app.route('/3/v2/account1', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/account1', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def account_alt():
    """Alternate account endpoint"""
    return jsonify(STATIC_ACCOUNT_RESPONSE)

@app.route('/3/v2/account/alt2', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/account/alt2', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def account_alt2():
    """Second alternate account endpoint"""
    return jsonify(STATIC_STORAGE_OBJECTS)

@app.route('/v2/user', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/v2/user', methods=['GET', 'POST'])
def get_user():
    """Get user by ID"""
    id = request.args.get("ids")
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    try:
        payload = b64decode_json(token.split(".")[1])
        username = payload["usn"]
    except Exception:
        return jsonify({"error": "invalid token"}), 403
    return jsonify({"username": username, "id": id})

@app.route('/v2/friends', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/v2/friends', methods=['GET', 'POST'])
def friends():
    """Get friends list"""
    return jsonify({
        "friends": [
            {
                "user": {
                    "id": "8c1acc32f2454fb9a9a76fb6dfbf572f",
                    "username": "<color=red>OWNER</color>: THUNDA",
                    "display_name": "<color=red>OWNER</color>: THUNDA",
                    "lang_tag": "en",
                    "metadata": "{\"IsDeveloper\": true}",
                    "create_time": "2024-10-19T10:33:56Z",
                    "update_time": "2025-07-23T17:58:40Z"
                },
                "state": 1,
                "update_time": "2025-02-20T13:46:53Z",
                "metadata": "{\"IsDeveloper\": true}"
            }
        ],
        "cursor": "M_-DAwEBDmVkZ2VMaXN0Q3Vyc29yAf-EAAECAQVTdGF0ZQEEAAEIUG9zaXRpb24BBAAAAA3_hAL4MIT4gPadsnQA"
    })

# ═══════════════════════════════════════════════════════════════════════════
# RPC ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/3/v2/rpc/attest.start', methods=['POST'])
@app.route('/v2/rpc/attest.start', methods=['POST'])
@app.route('/nnnnaakamacloud.c/v2/rpc/attest.start', methods=['POST'])
def attest_start():
    """Attestation start endpoint"""
    return jsonify({
        'payload': json.dumps({
            'status': 'success',
            'attestResult': 'Valid',
            'message': 'Attestation validated'
        })
    })

@app.route('/3/v2/rpc/clientBootstrap', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/rpc/clientBootstrap', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/rpc/clientBootstrap', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def client_bootstrap():
    """Client bootstrap endpoint"""
    if request.path.startswith("/nnnnaakamacloud.c"):
        payload = {
            "updateType": "None",
            "attestResult": "Valid",
            "attestTokenExpiresAt": 1786139899,
            "photonAppID": "photon-fusion-here",
            "photonVoiceAppID": "photon-voice-here",
            "metadataHash": "3225b4ed43082cec01c79acd8b1c09ea335f77870663342a5dededf6f4979f66",
            "termsAcceptanceNeeded": [],
            "dailyMissionDateKey": "",
            "dailyMissions": None,
            "dailyMissionResetTime": 0,
            "serverTimeUnix": 1786139899,
            "gameDataURL": "https://github.com/evan758321-source/Animal-Company-Copy-Tutorial-actually-good/raw/refs/heads/main/game-data/Zombie%20Update.zip"
        }
        return json.dumps({"payload": json.dumps(payload)}), 200, {'Content-Type': 'application/json'}
    return jsonify(CLIENT_BOOTSTRAP_RESPONSE)

@app.route('/3/v2/rpc/avatar.update', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/rpc/avatar.update', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/rpc/avatar.update', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def avatar_update():
    """Avatar update endpoint"""
    return jsonify({'payload': '{"succeeded":true,"errorCode":""}'})

@app.route('/3/v2/rpc/purchase.avatarItems', methods=['POST'])
@app.route('/v2/rpc/purchase.avatarItems', methods=['POST'])
def purchase_avatar_items():
    """Purchase avatar items endpoint"""
    return jsonify({'payload': ''})

@app.route('/3/v2/rpc/purchase.gameplayItems', methods=['POST'])
@app.route('/v2/rpc/purchase.gameplayItems', methods=['POST'])
def purchase_gameplay_items():
    """Purchase gameplay items endpoint"""
    return jsonify({'payload': ''})

@app.route('/3/v2/rpc/research.unlock', methods=['POST'])
@app.route('/v2/rpc/research.unlock', methods=['POST'])
@app.route('/nnnnaakamacloud.c/v2/rpc/research.unlock', methods=['POST'])
def research_unlock():
    """Research unlock endpoint"""
    return jsonify({
        "payload": "{\"succeeded\":true,\"wallet\":{\"softCurrency\":418291,\"hardCurrency\":418291,\"researchPoints\":418291}}"
    })

@app.route('/v2/rpc/mining.balance', methods=['GET', 'POST'])
@app.route('/nnnnaakamacloud.c/v2/rpc/mining.balance', methods=['GET', 'POST'])
def mining_balance():
    """Mining balance endpoint"""
    return jsonify({
        'payload': json.dumps({
            'hardCurrency': 30000,
            'researchPoints': 40000
        })
    })

@app.route('/3/v2/rpc/updateWalletSoftCurrency', methods=['GET', 'POST'])
@app.route('/v2/rpc/updateWalletSoftCurrency', methods=['GET', 'POST'])
def update_wallet_soft_currency():
    """Update wallet soft currency endpoint"""
    return jsonify({
        "Payload": "{\"ok\"}"
    })

@app.route('/3/v2/rpc/promo.redeem', methods=['GET', 'POST'])
def promo_redeem():
    """Promo code redemption endpoint"""
    token = request.args.get("token", "") or request.headers.get("Authorization", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    try:
        payload = b64decode_json(token.split(".")[1])
        username = payload["usn"]
    except Exception:
        return jsonify({"error": "invalid token"}), 403
    
    aa = request.data.decode("utf-8", errors="ignore")
    
    return jsonify({
        "payload": "{\"succeeded\":true}"
    })

@app.route('/3/v2/rpc/purchase.list', methods=['GET'])
@app.route('/v2/rpc/purchase.list', methods=['GET'])
@app.route('/nnnnaakamacloud.c/v2/rpc/purchase.list', methods=['GET'])
def purchase_list():
    """Purchase list endpoint"""
    return jsonify({
        "payload": "{\"purchases\":[{\"user_id\":\"3560fe2e-015c-4d2b-b2a6-6eb9f8d6a236\",\"product_id\":\"KPOP_GOLD\",\"transaction_id\":\"716802304855579\",\"store\":3,\"purchase_time\":{\"seconds\":1754458259},\"create_time\":{\"seconds\":1754458305,\"nanos\":154543000},\"update_time\":{\"seconds\":1754458305,\"nanos\":154543000},\"refund_time\":{},\"provider_response\":\"{\\\"success\\\": true, \\\"grant_time\\\": 1754458259}\",\"environment\":2}]}"
    })

@app.route('/3/v2/rpc/user.getActiveSanctions', methods=['GET'])
@app.route('/v2/rpc/user.getActiveSanctions', methods=['GET'])
@app.route('/nnnnaakamacloud.c/v2/rpc/user.getActiveSanctions', methods=['GET'])
def get_active_sanctions():
    """Get active sanctions endpoint"""
    return jsonify({
        "payload": "[]"
    })



@app.route('/3/v2/storage', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/storage', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/storage', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def storage():
    """Main storage endpoint"""
    if request.method == 'PUT':
        return "ok", 200
    
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            if data and 'object_ids' in data:
                user_id = data['object_ids'][0].get('user_id') if data['object_ids'] else None
                if user_id:
                    response_objects = []
                    for obj in STATIC_STORAGE_OBJECTS['objects']:
                        new_obj = obj.copy()
                        new_obj['user_id'] = user_id
                        if obj.get('key') == 'gameplay_loadout':
                            payload = generate_gameplay_loadout()
                            new_obj['value'] = payload['objects'][0]['value']
                        response_objects.append(new_obj)
                    return jsonify({'objects': response_objects})
                else:
                    return jsonify({'objects': []})
            else:
                return jsonify({'objects': []})
        except Exception as e:
            print(f"Storage error: {e}")
            return jsonify({'objects': []})
    
    # GET request - check for special handling
    if request.path.startswith("/nnnnaakamacloud.c"):
        token = request.args.get("token", "") or request.headers.get("Authorization", "")
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        try:
            payload = b64decode_json(token.split(".")[1])
            username = payload.get("usn", "unknown")
            if username == "unitygame":
                return jsonify(storage166())
        except Exception:
            pass
        return jsonify(storage166())
    
    return jsonify(autism())

@app.route('/3/v2/storage/econ_avatar_items', methods=['GET', 'POST', 'PUT'])
@app.route('/v2/storage/econ_avatar_items', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_avatar_items', methods=['GET', 'POST', 'PUT'])
def econ_avatar_items():
    """Economy avatar items endpoint"""
    if request.path.startswith("/nnnnaakamacloud.c"):
        ballsjr = os.path.join(dih3, "econ_avatar_items.json")
    else:
        ballsjr = os.path.join(dih2, "econ_avatar_items.json")
    
    try:
        with open(ballsjr, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
    except:
        data = []
    
    newdata = {"objects": []}
    for e in data:
        newdata["objects"].append({
            "collection": "econ_avatar_items",
            "key": e.get("id", "unknown"),
            "user_id": "00000000-0000-0000-0000-000000000000",
            "value": json.dumps(e),
            "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
            "permission_read": 2,
            "create_time": "2025-05-28T16:03:59Z",
            "update_time": "2025-06-11T16:16:56Z"
        })
    
    return jsonify(newdata)

@app.route('/3/v2/storage/econ_gameplay_items', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/v2/storage/econ_gameplay_items', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_gameplay_items', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def econ_gameplay_items():
    """Economy gameplay items endpoint"""
    if request.path.startswith("/nnnnaakamacloud.c"):
        ballsjr = os.path.join(dih3, "econ_gameplay_items.json")
    else:
        ballsjr = os.path.join(dih2, "econ_gameplay_items.json")
    
    try:
        with open(ballsjr, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
    except:
        data = []
        
    newdata = {"objects": []}
    for e in data:
        newdata["objects"].append({
            "collection": "econ_gameplay_items",
            "key": e.get("id", "unknown"),
            "user_id": "00000000-0000-0000-0000-000000000000",
            "value": json.dumps(e),
            "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
            "permission_read": 2,
            "create_time": "2025-05-28T16:03:59Z",
            "update_time": "2025-06-11T16:16:56Z"
        })
    
    return jsonify(newdata)

@app.route('/3/v2/storage/econ_research_nodes', methods=['GET', 'POST', 'PUT'])
@app.route('/v2/storage/econ_research_nodes', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_research_nodes', methods=['GET', 'POST', 'PUT'])
def econ_research_nodes():
    """Economy research nodes endpoint"""
    if request.path.startswith("/nnnnaakamacloud.c"):
        ballsjr = os.path.join(dih3, "econ_research_nodes.json")
    else:
        ballsjr = os.path.join(dih2, "econ_research_nodes.json")
    
    try:
        with open(ballsjr, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
    except:
        data = []
    
    newdata = {"objects": []}
    for e in data:
        newdata["objects"].append({
            "collection": "econ_research_nodes",
            "key": e.get("id", "unknown"),
            "user_id": "00000000-0000-0000-0000-000000000000",
            "value": json.dumps(e),
            "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
            "permission_read": 2,
            "create_time": "2025-05-28T16:03:59Z",
            "update_time": "2025-06-11T16:16:56Z"
        })
    
    return jsonify(newdata)

@app.route('/3/v2/storage/econ_products', methods=['GET', 'POST', 'PUT'])
@app.route('/v2/storage/econ_products', methods=['GET', 'POST', 'PUT'])
@app.route('/nnnnaakamacloud.c/v2/storage/econ_products', methods=['GET', 'POST', 'PUT'])
def econ_products():
    """Economy products endpoint"""
    if request.path.startswith("/nnnnaakamacloud.c"):
        ballsjr = os.path.join(dih3, "econ_products.json")
    else:
        ballsjr = os.path.join(dih2, "econ_products.json")
    
    try:
        with open(ballsjr, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
    except:
        data = []
    
    newdata = {"objects": []}
    for e in data:
        newdata["objects"].append({
            "collection": "econ_products",
            "key": e.get("id", "unknown"),
            "user_id": "00000000-0000-0000-0000-000000000000",
            "value": json.dumps(e),
            "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
            "permission_read": 2,
            "create_time": "2025-05-28T16:03:59Z",
            "update_time": "2025-06-11T16:16:56Z"
        })
    
    return jsonify(newdata)

@app.route('/v2/storage/econ_stash_upgrades', methods=['GET', 'POST', 'PUT'])
def econ_stash_upgrades():
    """Economy stash upgrades endpoint"""
    if request.path.startswith("/nnnnaakamacloud.c"):
        ballsjr = os.path.join(dih3, "econ_stash_upgrades.json")
    else:
        ballsjr = os.path.join(dih2, "econ_stash_upgrades.json")
    
    try:
        with open(ballsjr, 'r', encoding='utf-8') as f:
            data = json.load(f) or []
    except:
        data = []
    
    newdata = {"objects": []}
    for e in data:
        newdata["objects"].append({
            "collection": "econ_stash_upgrades",
            "key": e.get("id", "unknown"),
            "user_id": "00000000-0000-0000-0000-000000000000",
            "value": json.dumps(e),
            "version": "5c8518bd84cdb43a4e057cb62ca8d5b1",
            "permission_read": 2,
            "create_time": "2025-05-28T16:03:59Z",
            "update_time": "2025-06-11T16:16:56Z"
        })
    
    return jsonify(newdata)



@app.route('/game-data-prod.zip')
def serve_game_data():
    """Serve game data zip file"""
    client_ip = request.remote_addr
    print(f"Request from IP: {client_ip}")

    file_name = 'Zombie.zip'
    file_path = os.path.join('/home/XeraCompany/mysite', file_name)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 'File not found', 404

    file_size = os.path.getsize(file_path)
    print(f"Serving {file_name}, size: {file_size} bytes")

    try:
        return send_file(file_path, mimetype='application/zip', as_attachment=False,
                         download_name=file_name, max_age=3600)
    except Exception as e:
        print(f"Error serving file: {e}")
        return f"Error: {str(e)}", 500



@app.route('/debug', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def debug():
    """Debug endpoint for logging requests"""
    method = request.method
    url = request.url
    headers = dict(request.headers)
    body = request.get_data(as_text=True)

    message = {
        'content': '📡 **/debug request received**',
        'embeds': [{
            'title': 'Request Info',
            'fields': [
                {'name': 'Method', 'value': method, 'inline': True},
                {'name': 'URL', 'value': url, 'inline': False},
                {'name': 'Headers', 'value': f"```json\n{json.dumps(headers, indent=2)}```", 'inline': False},
                {'name': 'Body', 'value': f"```json\n{body}```" if body else '*(empty)*', 'inline': False}
            ],
            'color': 65484
        }]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=message)
    except Exception as e:
        return f"Failed to send to Discord: {e}", 500

    return 'Sent debug to discord', 200


# WSGI application reference for deployment
application = app