# IGG Conquerors (الفاتحون) - الدليل الشامل النهائي
### كل ما اكتشفناه من الصفر حتى إرسال أكشنات مشفرة للسيرفر

> **آخر تحديث:** 16 مارس 2026
> **الحالة:** ✅ HTTP Login + Gateway + Game Server + Encryption = ALL CRACKED
> **الملف التنفيذي:** `COMPLETE_BOT.py`

---

## فهرس المحتويات

1. [نظرة عامة - Connection Flow الكامل](#1-نظرة-عامة)
2. [بيانات الحساب والمفاتيح السرية](#2-بيانات-الحساب-والمفاتيح-السرية)
3. [المرحلة 1: HTTP Login (4 خطوات)](#3-المرحلة-1-http-login)
4. [المرحلة 2: Gateway Auth (TCP)](#4-المرحلة-2-gateway-auth)
5. [المرحلة 3: Game Server Login](#5-المرحلة-3-game-server-login)
6. [المرحلة 4: استقبال بيانات اللعبة + استخراج Server Key](#6-المرحلة-4-استقبال-بيانات-اللعبة)
7. [المرحلة 5: خوارزمية التشفير CMsgCodec (CRACKED)](#7-المرحلة-5-خوارزمية-التشفير)
8. [المرحلة 6: إرسال أكشنات مشفرة (جمع/تدريب/بناء)](#8-المرحلة-6-إرسال-أكشنات-مشفرة)
9. [بنية الباكتات بالتفصيل](#9-بنية-الباكتات-بالتفصيل)
10. [المشاكل والحلول](#10-المشاكل-والحلول)
11. [ملفات المشروع](#11-ملفات-المشروع)

---

## 1. نظرة عامة

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONNECTION FLOW الكامل                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HTTP Login (4 خطوات)                                           │
│  ┌──────────────────────────────────────────────────┐           │
│  │ Step 1: GET  account.igg.com/embed/entry         │→ PHPSESSID│
│  │ Step 2: POST account.igg.com/embed/login/email   │→ SSO      │
│  │ Step 3: POST account.igg.com/embed/login/user_id │→ JWT      │
│  │ Step 4: POST apis-dsa.iggapis.com/ums/...        │→ access_  │
│  │                                              token│           │
│  └──────────────────────────────────────────────────┘           │
│         │                                                       │
│         ▼                                                       │
│  Gateway Auth (TCP)                                             │
│  ┌──────────────────────────────────────────────────┐           │
│  │ token = XOR(access_token, "CQ_secret" * 4)       │           │
│  │ TCP → 54.93.167.80:5997                           │           │
│  │ Send 0x000B (79B) → Recv 0x000C (68B)             │           │
│  │ Result: redirect_ip:port + session_token          │           │
│  └──────────────────────────────────────────────────┘           │
│         │                                                       │
│         ▼                                                       │
│  Game Server (TCP)                                              │
│  ┌──────────────────────────────────────────────────┐           │
│  │ TCP → {redirect_ip}:{redirect_port}               │           │
│  │ Send 0x001F (64B) → Recv 0x0020 (5B, status=1)   │           │
│  │ Send 0x0021 (21B) → Recv ~95KB game data flood    │           │
│  │ Extract server_key from 0x0038 packet             │           │
│  └──────────────────────────────────────────────────┘           │
│         │                                                       │
│         ▼                                                       │
│  Encrypted Actions (CMsgCodec)                                  │
│  ┌──────────────────────────────────────────────────┐           │
│  │ enc[i] = ((plain[i] + msg*17) ^ sk ^ TABLE) & FF │           │
│  │ Send 0x0CEB (Train), 0x0CED (Build), 0x0CE8 etc  │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. بيانات الحساب والمفاتيح السرية

### بيانات الحساب:
| البيان | القيمة |
|--------|--------|
| **Email** | `minaadelzx12@gmail.com` |
| **Password** | `U112233u` |
| **IGG User ID** | `2082384585` (0x7c1eaac9) |
| **World/Kingdom** | `211` |

### المفاتيح السرية المستخرجة (ثوابت لا تتغير):
| المفتاح | القيمة | المصدر | الاستخدام |
|---------|--------|--------|-----------|
| **GAME_ID** | `1057029902` | Headers | معرف اللعبة |
| **HMAC Secret** | `07Z8D2AoYFGGivw40fEOj9swnpyF7Pw3ilKpVKnJ` | Frida hook | توقيع Step 4 |
| **CQ_XOR_KEY** | `"CQ_secretCQ_secretCQ_secretCQ_se"` | PCAP analysis | تشفير token للـ Gateway |
| **Gateway IP** | `54.93.167.80` | PCAP | بوابة اللعبة |
| **Gateway Port** | `5997` | PCAP | بورت البوابة |
| **GAME_ID_HEX** | `0x3F00FF0E` | PCAP | tail bytes في الباكتات |
| **CMsgCodec TABLE** | `[0x58,0xef,0xd7,0x14,0xa2,0x3b,0x9c]` | libgame.so | 7-byte lookup للتشفير |
| **User-Agent** | `1057029902/6.1.0 Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G9880 Build/N2G47H)` | PCAP | تقليد أندرويد |

---

## 3. المرحلة 1: HTTP Login

### الخطوة 1: جلب PHPSESSID
```
GET https://account.igg.com/embed/entry?scenario=sign_in&for_audting=0&x_gpc_jsbridge=gpc_jsbridge_common%2F2.0.0_2%3B
```

**Headers المطلوبة:**
```
User-Agent:        1057029902/6.1.0 Dalvik/2.1.0 ...
X-Requested-With:  com.igg.android.conquerors
x-gpc-game-id:     1057029902
x-gpc-sign:        {MD5(sorted_params + MD5(GAME_ID)).upper()}
x-gpc-nonce:       {timestamp}
x-gpc-ver:         3.0
x-gpc-udid:        {random UUID}
x-gpc-uiid:        {random UUID}
```

**حساب x-gpc-sign:**
```python
params = sorted(all_query_params + header_params)
joined = "&".join(f"{k}={v}" for k, v in params)
sign = MD5(joined + MD5("1057029902")).upper()
```

**النتيجة:** Cookie `PHPSESSID`

### الخطوة 2: تسجيل الدخول بالإيميل
```
POST https://account.igg.com/embed/login/email
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

email={EMAIL}&password={MD5(PASSWORD)}&token=
```

> **الباسوورد MD5 مش نص عادي!**

**النتيجة:** `{"error":{"code":0}, "data":{...}}`

### الخطوة 3: جلب Platform JWT
```
POST https://account.igg.com/embed/login/user_id
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

user_id=2082384585
```

**النتيجة:** `{"data":{"redirectUrl":"...?token=eyJhbGciOiJSUzI1NiI..."}}`
نستخرج JWT من الـ URL بـ regex: `/token=([^&]+)/`

### الخطوة 4: جلب Access Token (HMAC-SHA256)
```
POST https://apis-dsa.iggapis.com/ums/member/access_token/platform
Content-Type: application/x-www-form-urlencoded

type=gpcaccount&platform_token={"token":"JWT_VALUE"}
```

**Canonical String للتوقيع (الترتيب مهم!):**
```
x-gpc-uiid: {uiid}
x-gpc-nonce: {timestamp}
x-gpc-evo: 1;gpc=s2
x-gpc-game-id: 1057029902
x-gpc-udid: {udid}
digest: SHA-256={base64(sha256(body))}
date: {UTC date string}
POST /ums/member/access_token/platform HTTP/1.1
```

**التوقيع:**
```python
signature = base64(HMAC_SHA256(canonical_string, HMAC_KEY))
```

**Authorization Header:**
```
hmac username="1057029902", algorithm="hmac-sha256",
  headers="x-gpc-uiid x-gpc-nonce x-gpc-evo x-gpc-game-id x-gpc-udid digest date request-line",
  signature="{signature}"
```

**Headers إضافية:**
```
x-gpc-ver: 2.5
x-gpc-family: bmbkf3
Host: apis-dsa.iggapis.com
User-Agent: {UA} GPCSDK/2.29.0-su.1-beta.1.0+137
```

**النتيجة:** `{"data":{"access_token":"460706de63fb05d0c8caae02b9e19a99"}}`

---

## 4. المرحلة 2: Gateway Auth

### توليد الـ Token:
```python
CQ_XOR_KEY = ("CQ_secret" * 4)[:32]  # = "CQ_secretCQ_secretCQ_secretCQ_se"
token = bytes(a ^ b for a, b in zip(access_token.encode('ascii'), CQ_XOR_KEY.encode('ascii')))
```

### بنية 0x000B (79 bytes):
```
Offset  Bytes  الوصف
0-1     2      طول الباكت LE = 79
2-3     2      Opcode = 0x000B
4-7     4      Version = 1
8-11    4      Padding = 0
12-15   4      IGG ID LE
16-19   4      Padding = 0
20-21   2      Token length = 32
22-53   32     Token المشفر بـ XOR
54-57   4      Padding = 0
58-61   4      Platform = 2 (Android)
62-65   4      Padding = 0
66-69   4      World ID LE = 211
70-73   4      GAME_ID_HEX = 0x3F00FF0E
74-77   4      Padding = 0
78      1      Tail = 0x01
```

### الاتصال:
```python
sock = socket.connect(("54.93.167.80", 5997))
sock.send(build_000B(IGG_ID, token, WORLD_ID))
response = sock.recv()  # → 0x000C
```

### تحليل 0x000C (68 bytes):
```
Offset  الوصف
0-1     طول الباكت LE
2-3     Opcode = 0x000C
4-7     IGG ID
8-11    Padding
12-13   IP string length
14-N    Redirect IP (ASCII)
N+0..1  Redirect Port LE
N+2..3  Token length
N+4..35 Session Token (32 ASCII hex chars)
+1      Status byte
+2..5   World ID
```

**مثال:** IP=`54.93.192.240`, Port=`7000`, Session=`b52c0f41ce7a2dec3b0d5a77e29ab1f2`

---

## 5. المرحلة 3: Game Server Login

### 0x001F - Login (64 bytes):
```python
pkt = struct.pack('<HH', 64, 0x001F)
pkt += struct.pack('<I', 1)          # version
pkt += struct.pack('<I', 0)          # padding
pkt += struct.pack('<I', IGG_ID)
pkt += struct.pack('<I', 0)          # padding
pkt += struct.pack('<H', 32)         # session token length
pkt += session_token.encode('ascii') # 32 bytes
pkt += bytes([0x0e])
pkt += struct.pack('<I', 0x3F00FF0E) # GAME_ID_HEX
pkt += struct.pack('<I', 0)
pkt += bytes([0x00])
```

**الرد:** `0x0020` (5 bytes) → `status=1` يعني OK

### 0x0021 - World Entry (21 bytes):
```python
pkt = struct.pack('<HH', 21, 0x0021)
pkt += struct.pack('<I', IGG_ID)
pkt += struct.pack('<I', 0)
pkt += bytes([0x0e])
pkt += struct.pack('<I', 0x3F00FF0E)
pkt += bytes([0xb0, 0x02, 0x5c, 0x00])
```

**الرد:** فيضان بيانات اللعبة (~95KB, ~60+ packets)

---

## 6. المرحلة 4: استقبال بيانات اللعبة

### الباكتات اللي بتيجي بعد 0x0021:
| الترتيب | Opcode | الحجم | المحتوى |
|---------|--------|-------|---------|
| 1 | 0x039B | 44B | Timestamp |
| 2 | 0x0654 | 288B | Guild Tech |
| 3 | 0x004A | 36B | World Resources |
| 4 | 0x0034 | 403B | Player Profile (اسم, قوة, موارد) |
| 5 | 0x01D4 | 8B | Unknown |
| 6 | 0x0A00 | 40B | Resource Timers |
| ... | ... | ... | ... |
| ~55 | **0x0038** | **834B** | **Castle Data (فيه الـ SERVER KEY!)** |

### استخراج Server Key من 0x0038:
الباكت 0x0038 (830B تقريباً) بنيته:
```
[2 bytes LE]  entry_count (مثال: 69 = 0x0045)
[count * 12B] entries, كل واحد:
    [4 bytes LE] Field ID (u32)
    [8 bytes LE] Value (u64)
```
الحجم الكلي = 2 + count*12 (مثال: 2 + 69*12 = 830)

**Field ID 0x4F (79) = Server Key!** (عند entry index 49, offset 590)

```python
def extract_server_key_from_0x0038(payload):
    entry_count = struct.unpack('<H', payload[0:2])[0]
    for idx in range(entry_count):
        off = 2 + idx * 12
        if off + 12 > len(payload):
            break
        field_id = struct.unpack('<I', payload[off:off+4])[0]
        if field_id == 0x4F:
            return struct.unpack('<I', payload[off+4:off+8])[0]
    return None
```

**مثال 1 (capture1.pcap):** `server_key = 0x228b1d9b` → `[0x9b, 0x1d, 0x8b, 0x22]`
**مثال 2 (live session):** `server_key = 0xe858ed75` → `[0x75, 0xed, 0x58, 0xe8]`

> **ملاحظة:** الـ server_key بيتغير كل session! لازم يتستخرج من 0x0038 كل مرة.

---

## 7. المرحلة 5: خوارزمية التشفير CMsgCodec (CRACKED!)

### الخوارزمية (مؤكدة 100% بـ roundtrip test):
```
enc[i] = ((plain[i] + msg_byte * 17) ^ sk_byte ^ table_byte) & 0xFF
```

| المتغير | التعريف |
|---------|---------|
| `i` | byte offset من بداية الباكت الكامل (التشفير يبدأ من i=8) |
| `table_byte` | `TABLE[i % 7]` حيث TABLE = `[0x58, 0xef, 0xd7, 0x14, 0xa2, 0x3b, 0x9c]` |
| `sk_byte` | `server_key[i % 4]` (4 بايت من السيرفر) |
| `msg_byte` | `msg_value_bytes[i % 2]` (2 بايت عشوائية لكل باكت) |
| **Period** | LCM(2, 4, 7) = **28 bytes** |

### فك التشفير (العكس):
```python
def decode(payload, server_key):
    msg = [payload[1], payload[3]]  # msg_value bytes from metadata
    dec = bytearray(len(payload) - 4)
    for p in range(4, len(payload)):
        i = p + 4  # full packet offset
        table_b = TABLE[i % 7]
        sk_b = server_key[i % 4]
        msg_b = msg[i % 2]
        intermediate = (payload[p] ^ sk_b ^ table_b) & 0xFF
        dec[p - 4] = (intermediate - msg_b * 17) & 0xFF
    return bytes(dec)
```

### التشفير:
```python
def encode(opcode, action_data, server_key, msg_value=random):
    msg_lo = msg_value & 0xFF
    msg_hi = (msg_value >> 8) & 0xFF
    msg = [msg_lo, msg_hi]

    total_len = 4 + 4 + len(action_data)  # header + metadata + data
    pkt = bytearray(total_len)
    struct.pack_into('<H', pkt, 0, total_len)
    struct.pack_into('<H', pkt, 2, opcode)

    # Copy plaintext to positions 8+
    for j, b in enumerate(action_data):
        pkt[8 + j] = b

    # Encrypt bytes 8+
    checksum = 0
    for i in range(8, total_len):
        p = i - 4
        table_b = TABLE[i % 7]
        sk_b = server_key[i % 4]
        msg_b = msg[i % 2]
        enc_byte = (((pkt[i] + msg_b * 17) & 0xFF) ^ sk_b ^ table_b) & 0xFF
        pkt[i] = enc_byte
        checksum += enc_byte

    # Write metadata at bytes 4-7
    pkt[4] = checksum & 0xFF          # checksum
    pkt[5] = msg_lo                    # msg_value low byte
    pkt[6] = msg_lo ^ 0xB7            # verification pattern
    pkt[7] = msg_hi                    # msg_value high byte

    return bytes(pkt)
```

### Packet Metadata (bytes 4-7):
```
byte[4] = checksum (low byte of sum of all encrypted bytes)
byte[5] = msg_value & 0xFF
byte[6] = (msg_value & 0xFF) ^ 0xB7    ← verification pattern!
byte[7] = (msg_value >> 8) & 0xFF
```

### كيف اكتشفنا الخوارزمية:
1. **ARM64 disassembly** لـ `libgame.so` باستخدام **capstone**
2. حللنا functions: `CMsgCodec::Encode`, `Encryption::doDecode`, `KeyMode::parseMode`
3. استخرجنا TABLE من البايناري عند address `0x028b723a`
4. عملنا **brute-force** للـ server_key من 6 captured packets
5. تأكدنا بـ **roundtrip test** (encrypt → decrypt = original) ✅

---

## 8. المرحلة 6: إرسال أكشنات مشفرة

### Opcodes المكتشفة:
| Opcode | الحجم | الوظيفة | مجرب؟ |
|--------|-------|---------|-------|
| **0x0CEB** | 10B | Train (تدريب) | ✅ Decoded |
| **0x0CED** | 19B | Build (بناء) | ✅ Decoded |
| **0x0CE8** | 62B | Gather (جمع موارد) | ✅ Decoded |
| **0x0CEF** | 22B | Unknown action | ✅ Decoded |

### 0x0CEB - Train (تدريب) - 10 bytes:
```
Offset  Size  الوصف
0       1     Type (0x01)
1-4     4     IGG ID (LE)
5-8     4     Zeros
9       1     Flag (0x01)
```
```python
def build_train_action(igg_id):
    data = bytearray(10)
    data[0] = 0x01
    struct.pack_into('<I', data, 1, igg_id)
    data[9] = 0x01
    return bytes(data)
```

### 0x0CED - Build (بناء) - 19 bytes:
```
Offset  Size  الوصف
0-3     4     Building type (LE)
4-7     4     Building ID (LE)
8       1     Zero
9-12    4     IGG ID (LE)
13-18   6     Zeros
```
```python
def build_build_action(igg_id, building_type=1, building_id=480):
    data = bytearray(19)
    struct.pack_into('<I', data, 0, building_type)
    struct.pack_into('<I', data, 4, building_id)
    struct.pack_into('<I', data, 9, igg_id)
    return bytes(data)
```

### 0x0CE8 - Gather (جمع موارد) - 62 bytes:
```
Offset  Size  الوصف
0       1     March slot (1 or 2)
1-3     3     Variable nonce
4-5     2     March type ID (0x1748)
6-8     3     Zeros
9-11    3     Target tile info
12      1     Constant 0x02
13      1     Constant 0x05
14-37   24    6x u32 troop type IDs
38-41   4     Troop count (LE)
42-48   7     Flags
49-52   4     IGG ID (LE)
53-61   9     Zeros
```

### 0x0CEF - Unknown Action - 22 bytes:
```
Offset  Size  الوصف
0       1     Sub-type (2 or 8)
1-2     2     Constant 0x0037
3       1     Constant 0x34
4-6     3     Zeros
7-10    4     Variable
11      1     Flag (0 or 1)
12-15   4     IGG ID (LE)
16-21   6     Zeros
```

### طريقة الإرسال:
```python
from codec import CMsgCodec, extract_server_key_from_0x0038, build_train_action

# بعد الاتصال واستخراج server_key من 0x0038
codec = CMsgCodec.from_u32(server_key)

# بناء وتشفير أكشن تدريب
train_data = build_train_action(IGG_ID)
encrypted_packet = codec.encode(0x0CEB, train_data)

# إرسال
game_socket.sendall(encrypted_packet)
```

---

## 9. بنية الباكتات بالتفصيل

### Format عام لكل الباكتات:
```
[2 bytes LE] Total length (يشمل الـ 2 bytes دول)
[2 bytes LE] Opcode
[variable]   Payload
```

### الباكتات المشفرة (0x0CE*) - format إضافي:
```
[2 bytes LE] Total length
[2 bytes LE] Opcode (0x0CE*)
[1 byte]     Checksum (low byte of sum of encrypted bytes)
[1 byte]     msg_value & 0xFF
[1 byte]     (msg_value & 0xFF) ^ 0xB7
[1 byte]     (msg_value >> 8) & 0xFF
[variable]   Encrypted action data
```

### Heartbeat (0x0042):
```python
payload = struct.pack('<I', ms_elapsed) + struct.pack('<I', 0)
packet = struct.pack('<HH', 12, 0x0042) + payload
# يُرسل كل 15 ثانية للحفاظ على الاتصال
```

---

## 10. المشاكل والحلول

### Access Token منتهي الصلاحية:
| المشكلة | الحل |
|---------|------|
| Gateway يرجع redirect فاضي | الـ access_token قديم - لازم HTTP login جديد أو ADB extraction |
| الـ weg_Accesskey قديم | استخرج واحد جديد من المحاكي بـ ADB |

### طريقة استخراج access_key من المحاكي:
```bash
adb -s 127.0.0.1:21503 shell cat /data/data/com.igg.android.conquerors/shared_prefs/weg_login_file.xml
# ابحث عن: weg_Accesskey">VALUE<
```

### Rate Limiting:
| المشكلة | الحل |
|---------|------|
| `error.code: 100283` + hCaptcha | استنى 15 دقيقة |
| Cloudflare blocking | استخدم Node.js بدل Python للـ HTTP |

### Gateway لا يرد:
| المشكلة | الحل |
|---------|------|
| Port 5993 مقفول | جرب 5997 |
| الباكت أكبر/أصغر من 79B | تحقق من الحجم بالظبط |
| Token غلط | تحقق من XOR formula |

### Server Key مش موجود:
| المشكلة | الحل |
|---------|------|
| 0x0038 مش في الباكتات الأولى | استنى أكتر أو ابعت initial requests |
| Field 0x4F مش موجود | scan الباكت byte-by-byte |

---

## 11. ملفات المشروع

### الملفات الأساسية:
| الملف | الوصف |
|-------|-------|
| **`COMPLETE_BOT.py`** | البوت الكامل - من HTTP login لحد إرسال أكشنات مشفرة |
| **`codec.py`** | CMsgCodec Encoder/Decoder module |
| **`MASTER_GUIDE.md`** | هذا الملف - الدليل الشامل |

### ملفات التحليل والـ Reverse Engineering:
| الملف | الوصف |
|-------|-------|
| `disasm_capstone.py` | ARM64 disassembly لـ libgame.so |
| `bruteforce_sk.py` | Brute-force الـ server key |
| `analyze_actions.py` | تحليل بيانات الأكشنات المفكوكة |
| `analyze_0x0038.py` | تحليل باكت 0x0038 واستخراج Server Key |
| `scan_all_pcaps.py` | مسح كل ملفات PCAP للأكشنات |

### ملفات سابقة (مرجعية):
| الملف | الوصف |
|-------|-------|
| `persistent_bot.py` | بوت مع heartbeat و interactive shell (بدون تشفير) |
| `full_bot.py` | بوت كامل مع HTTP login (بدون تشفير) |
| `test_gateway.py` | اختبار Gateway مباشر |
| `Node-Attachment-Manager/server/bot.ts` | نسخة Node.js للبوت مع واجهة ويب |
| `config-decryptor/LORDS_MOBILE_COMPLETE_GUIDE.md` | دليل قديم (قبل كسر التشفير) |

### ملفات البيانات:
| الملف | الوصف |
|-------|-------|
| `config-decryptor/capture1.pcap` | PCAP فيه 6 action packets مشفرة |
| `libgame.so` | البايناري اللي حللناه (ARM64) |
| `bot.txt` | ملف الاكتشافات القديم |

---

## كيف تعيد بناء كل شيء من الصفر

1. **انسخ `codec.py` و `COMPLETE_BOT.py`**
2. **شغل البوت:** `python COMPLETE_BOT.py`
3. لو الـ access_key قديم:
   - **Option A:** افتح اللعبة على المحاكي واستخرج الـ key بـ ADB
   - **Option B:** شغل HTTP login من البوت (محتاج Node.js لتجنب Cloudflare)
4. البوت هيعمل كل حاجة أوتوماتيك:
   - Gateway Auth → Game Server → Extract server_key → Send actions

> **هذا الملف هو المرجع الكامل النهائي. كل المعلومات اللي محتاجها عشان تعيد بناء البوت من الصفر موجودة هنا.**
