"""
Crack 0x1B8B verify byte formula.

Step A: Decrypt 0x1B8B from PCAP, verify plaintext matches seed formula
Step B: Re-encrypt same plaintext with same msg_value, compare byte-by-byte
Step C: Across ALL PCAPs, find the verify byte formula
"""
import struct, sys, os
from pathlib import Path

sys.path.insert(0, r'D:\CascadeProjects\claude')
from protocol import CMSG_TABLE as TABLE

# ══════════════════════════════════════════════════════════════
# PCAP PARSING (same as analyze_1b8b.py)
# ══════════════════════════════════════════════════════════════

def read_pcap_streams(filepath):
    with open(filepath, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        endian = '<' if magic == 0xa1b2c3d4 else '>'
        f.read(20)
        streams = {}
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            ip_data = data
            if len(ip_data) < 20:
                continue
            ihl = (ip_data[0] & 0x0F) * 4
            protocol = ip_data[9]
            if protocol != 6:
                continue
            tcp = ip_data[ihl:]
            if len(tcp) < 20:
                continue
            src_port = struct.unpack('>H', tcp[0:2])[0]
            dst_port = struct.unpack('>H', tcp[2:4])[0]
            tcp_off = ((tcp[12] >> 4) & 0xF) * 4
            payload = tcp[tcp_off:]
            if len(payload) == 0:
                continue
            game_ports = set(range(5990, 5999)) | set(range(7001, 7011))
            if dst_port in game_ports:
                streams.setdefault('C2S', bytearray()).extend(payload)
            elif src_port in game_ports:
                streams.setdefault('S2C', bytearray()).extend(payload)
    return streams


def parse_packets(raw):
    packets = []
    pos = 0
    while pos + 4 <= len(raw):
        pkt_len = struct.unpack('<H', raw[pos:pos+2])[0]
        opcode = struct.unpack('<H', raw[pos+2:pos+4])[0]
        if pkt_len < 4 or pkt_len > 65535 or pos + pkt_len > len(raw):
            break
        payload = bytes(raw[pos+4:pos+pkt_len])
        packets.append((opcode, payload))
        pos += pkt_len
    return packets


def extract_server_key(s2c_pkts):
    for op, pl in s2c_pkts:
        if op == 0x0038 and len(pl) > 100:
            entry_count = struct.unpack('<H', pl[0:2])[0]
            for idx in range(entry_count):
                off = 2 + idx * 12
                if off + 12 > len(pl):
                    break
                field_id = struct.unpack('<I', pl[off:off+4])[0]
                value = struct.unpack('<I', pl[off+4:off+8])[0]
                if field_id == 0x4F:
                    return value
    return None


# ══════════════════════════════════════════════════════════════
# ENCRYPTION / DECRYPTION
# ══════════════════════════════════════════════════════════════

def decrypt_payload(payload, server_key_u32):
    """Decrypt CMsgCodec payload. Returns (plaintext, msg_lo, msg_hi, verify, checksum, calc_checksum)."""
    if len(payload) < 5:
        return None
    sk = [server_key_u32 & 0xFF, (server_key_u32 >> 8) & 0xFF,
          (server_key_u32 >> 16) & 0xFF, (server_key_u32 >> 24) & 0xFF]
    checksum_byte = payload[0]
    msg_lo = payload[1]
    verify = payload[2]
    msg_hi = payload[3]
    msg = [msg_lo, msg_hi]
    enc_data = payload[4:]

    plain = bytearray(len(enc_data))
    calc_checksum = 0
    for i in range(len(enc_data)):
        abs_i = i + 8
        table_b = TABLE[abs_i % 7]
        sk_b = sk[abs_i % 4]
        msg_b = msg[abs_i % 2]
        enc_byte = enc_data[i]
        calc_checksum = (calc_checksum + enc_byte) & 0xFFFFFFFF
        intermediate = enc_byte ^ sk_b ^ table_b
        plain_byte = (intermediate - msg_b * 17) & 0xFF
        plain[i] = plain_byte

    return plain, msg_lo, msg_hi, verify, checksum_byte, (calc_checksum & 0xFF)


def encrypt_plaintext(plaintext, server_key_u32, msg_lo, msg_hi):
    """Encrypt plaintext using CMsgCodec formula. Returns (encrypted_bytes, checksum)."""
    sk = [server_key_u32 & 0xFF, (server_key_u32 >> 8) & 0xFF,
          (server_key_u32 >> 16) & 0xFF, (server_key_u32 >> 24) & 0xFF]
    msg = [msg_lo, msg_hi]
    enc = bytearray(len(plaintext))
    checksum = 0
    for i in range(len(plaintext)):
        abs_i = i + 8
        table_b = TABLE[abs_i % 7]
        sk_b = sk[abs_i % 4]
        msg_b = msg[abs_i % 2]
        intermediate = (plaintext[i] + msg_b * 17) & 0xFF
        enc_byte = (intermediate ^ sk_b ^ table_b) & 0xFF
        enc[i] = enc_byte
        checksum = (checksum + enc_byte) & 0xFFFFFFFF
    return enc, (checksum & 0xFF)


def check_seed_formula(plain):
    """Check if plaintext matches 0x1B8B seed formula."""
    if len(plain) != 18:
        return False, "wrong length"
    seed = plain[0:4]
    mid = struct.unpack('<H', plain[4:6])[0]
    x1 = struct.unpack('<H', plain[6:8])[0]
    x2 = struct.unpack('<H', plain[8:10])[0]
    y1 = struct.unpack('<H', plain[10:12])[0]
    y2 = struct.unpack('<H', plain[12:14])[0]
    y3 = struct.unpack('<H', plain[14:16])[0]
    y4 = struct.unpack('<H', plain[16:18])[0]

    # Expected: x_lo = (seed[2]+0x13)&0xFF, x_hi = (seed[3]-0x02)&0xFF
    exp_x_lo = (seed[2] + 0x13) & 0xFF
    exp_x_hi = (seed[3] - 0x02) & 0xFF
    exp_x = exp_x_lo | (exp_x_hi << 8)

    # Expected: mid = ((x_hi+0x22)&0xFF)<<8 | ((x_lo+0x73)&0xFF)
    exp_mid = (((exp_x_hi + 0x22) & 0xFF) << 8) | ((exp_x_lo + 0x73) & 0xFF)

    # Expected: y = ((x_hi-0x01)&0xFF)<<8 | ((x_lo-0x01)&0xFF)
    exp_y = (((exp_x_hi - 0x01) & 0xFF) << 8) | ((exp_x_lo - 0x01) & 0xFF)

    checks = {
        'x1==x2': x1 == x2,
        'x1==exp_x': x1 == exp_x,
        'mid==exp_mid': mid == exp_mid,
        'y1==y2==y3==y4': y1 == y2 == y3 == y4,
        'y1==exp_y': y1 == exp_y,
    }

    all_ok = all(checks.values())
    return all_ok, checks


# ══════════════════════════════════════════════════════════════
# MAIN ANALYSIS
# ══════════════════════════════════════════════════════════════

def main():
    print("=" * 80)
    print("STEP A: Decrypt 0x1B8B from NEW PCAP")
    print("=" * 80)

    # New PCAP data
    pcap_path = r'D:\CascadeProjects\PCAPdroid_27_Mar_09_17_04.pcap'
    raw_payload = bytes.fromhex("da3d3e3a8d3a8bf65f1ddabd24b3236a6cfc6e86e406")
    server_key = 0x88587D29

    result = decrypt_payload(raw_payload, server_key)
    plain, msg_lo, msg_hi, verify, ck_byte, calc_ck = result

    print(f"Server key: 0x{server_key:08X}")
    print(f"Raw payload ({len(raw_payload)}B): {raw_payload.hex()}")
    print(f"  checksum_byte=0x{ck_byte:02X} msg_lo=0x{msg_lo:02X} verify=0x{verify:02X} msg_hi=0x{msg_hi:02X}")
    print(f"  msg_value=0x{msg_hi:02X}{msg_lo:02X} ({msg_lo | (msg_hi << 8)})")
    print(f"  std_verify=0x{(msg_lo ^ 0xB7) & 0xFF:02X} (msg_lo^0xB7)")
    print(f"  verify MATCHES standard: {verify == (msg_lo ^ 0xB7) & 0xFF}")
    print(f"  calc_checksum=0x{calc_ck:02X} matches_header: {calc_ck == ck_byte}")
    print(f"  Decrypted plaintext ({len(plain)}B): {bytes(plain).hex()}")

    # Check seed formula
    ok, checks = check_seed_formula(plain)
    print(f"\n  Seed formula check: {'PASS' if ok else 'FAIL'}")
    for name, val in checks.items():
        print(f"    {name}: {'OK' if val else 'FAIL'}")

    print(f"\n  Plaintext breakdown:")
    seed = plain[0:4]
    print(f"    seed32:  {bytes(seed).hex()} = {struct.unpack('<I', seed)[0]}")
    print(f"    mid:     {bytes(plain[4:6]).hex()} = {struct.unpack('<H', plain[4:6])[0]}")
    print(f"    x (×2):  {bytes(plain[6:8]).hex()} = {struct.unpack('<H', plain[6:8])[0]}")
    print(f"    y (×4):  {bytes(plain[10:12]).hex()} = {struct.unpack('<H', plain[10:12])[0]}")

    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("STEP B: Re-encrypt and compare byte-by-byte")
    print("=" * 80)

    our_enc, our_ck = encrypt_plaintext(plain, server_key, msg_lo, msg_hi)
    pcap_enc = raw_payload[4:]  # encrypted data after 4-byte CMsgCodec header

    print(f"PCAP encrypted ({len(pcap_enc)}B):  {bytes(pcap_enc).hex()}")
    print(f"Our  encrypted ({len(our_enc)}B):  {bytes(our_enc).hex()}")
    print(f"PCAP checksum: 0x{ck_byte:02X}")
    print(f"Our  checksum: 0x{our_ck:02X}")

    match = pcap_enc == our_enc
    print(f"\nEncrypted bytes IDENTICAL: {match}")

    if not match:
        print("\nByte-by-byte comparison:")
        for i in range(len(pcap_enc)):
            marker = " <<<" if pcap_enc[i] != our_enc[i] else ""
            print(f"  [{i:2d}] abs_i={i+8:2d} PCAP=0x{pcap_enc[i]:02X} OURS=0x{our_enc[i]:02X}{marker}")

    # ══════════════════════════════════════════════════════════════
    print("\n" + "=" * 80)
    print("STEP C: Analyze verify byte across ALL PCAPs")
    print("=" * 80)

    pcap_dir = Path(r'D:\CascadeProjects')
    pcaps = sorted(pcap_dir.glob('*.pcap'))
    for subdir in ['rebel_attack', 'codex_lab']:
        sub = pcap_dir / subdir
        if sub.exists():
            pcaps.extend(sorted(sub.glob('*.pcap')))

    all_results = []

    for pcap in pcaps:
        try:
            streams = read_pcap_streams(pcap)
            if 'C2S' not in streams or 'S2C' not in streams:
                continue
            c2s = parse_packets(streams['C2S'])
            s2c = parse_packets(streams['S2C'])
            sk = extract_server_key(s2c)
            if not sk:
                continue

            for op, pl in c2s:
                if op == 0x1B8B and len(pl) == 22:
                    r = decrypt_payload(pl, sk)
                    if r:
                        p, ml, mh, v, ck, calc_ck = r
                        # Re-encrypt to verify
                        re_enc, re_ck = encrypt_plaintext(p, sk, ml, mh)
                        pcap_enc_data = pl[4:]
                        enc_match = (re_enc == pcap_enc_data)
                        ck_match = (re_ck == ck)
                        seed_ok, _ = check_seed_formula(p)

                        all_results.append({
                            'pcap': pcap.name,
                            'sk': sk,
                            'msg_lo': ml,
                            'msg_hi': mh,
                            'verify': v,
                            'checksum': ck,
                            'calc_ck': calc_ck,
                            'enc_match': enc_match,
                            'ck_match': ck_match,
                            'seed_ok': seed_ok,
                            'plain': bytes(p),
                        })
        except Exception as e:
            continue

    print(f"\nFound {len(all_results)} 0x1B8B packets across all PCAPs\n")

    # Summary table
    enc_match_count = sum(1 for r in all_results if r['enc_match'])
    ck_match_count = sum(1 for r in all_results if r['ck_match'])
    seed_ok_count = sum(1 for r in all_results if r['seed_ok'])
    std_verify_count = sum(1 for r in all_results if r['verify'] == (r['msg_lo'] ^ 0xB7) & 0xFF)

    print(f"Encryption matches:   {enc_match_count}/{len(all_results)}")
    print(f"Checksum matches:     {ck_match_count}/{len(all_results)}")
    print(f"Seed formula matches: {seed_ok_count}/{len(all_results)}")
    print(f"Standard verify:      {std_verify_count}/{len(all_results)}")

    # ── VERIFY BYTE CRACKING ──
    print(f"\n{'='*80}")
    print("VERIFY BYTE FORMULA SEARCH")
    print(f"{'='*80}\n")

    # For each result, compute what XOR mask would produce the verify byte
    xor_masks = []
    for r in all_results:
        ml = r['msg_lo']
        mh = r['msg_hi']
        v = r['verify']
        ck = r['checksum']
        sk0 = r['sk'] & 0xFF
        sk1 = (r['sk'] >> 8) & 0xFF
        sk2 = (r['sk'] >> 16) & 0xFF
        sk3 = (r['sk'] >> 24) & 0xFF
        p = r['plain']

        # What XOR mask makes v = ml ^ mask?
        mask = (v ^ ml) & 0xFF
        xor_masks.append(mask)

        # Try many formulas
        formulas = {
            'ml^0xB7':        (ml ^ 0xB7) & 0xFF,
            'mh^0xB7':        (mh ^ 0xB7) & 0xFF,
            'ml^mh':          (ml ^ mh) & 0xFF,
            'ck^ml':          (ck ^ ml) & 0xFF,
            'ck^mh':          (ck ^ mh) & 0xFF,
            'ck^0xB7':        (ck ^ 0xB7) & 0xFF,
            '(ml+mh)&FF':     (ml + mh) & 0xFF,
            '(ml*17)&FF':     (ml * 17) & 0xFF,
            'ml^sk0':         (ml ^ sk0) & 0xFF,
            'ml^sk1':         (ml ^ sk1) & 0xFF,
            'ml^sk2':         (ml ^ sk2) & 0xFF,
            'ml^sk3':         (ml ^ sk3) & 0xFF,
            'mh^sk0':         (mh ^ sk0) & 0xFF,
            'ck':             ck,
            'p[0]':           p[0] if len(p) > 0 else -1,
            'p[0]^ml':        (p[0] ^ ml) & 0xFF if len(p) > 0 else -1,
            'p[0]^mh':        (p[0] ^ mh) & 0xFF if len(p) > 0 else -1,
            'p[0]^0xB7':      (p[0] ^ 0xB7) & 0xFF if len(p) > 0 else -1,
            'p[1]^ml':        (p[1] ^ ml) & 0xFF if len(p) > 1 else -1,
            'p[2]^ml':        (p[2] ^ ml) & 0xFF if len(p) > 2 else -1,
            'p[3]^ml':        (p[3] ^ ml) & 0xFF if len(p) > 3 else -1,
            '(p[0]+ml)&FF':   (p[0] + ml) & 0xFF if len(p) > 0 else -1,
            '(p[0]+mh)&FF':   (p[0] + mh) & 0xFF if len(p) > 0 else -1,
            'ml^(ck+mh)':     (ml ^ ((ck + mh) & 0xFF)) & 0xFF,
            '(ml+ck)&FF':     (ml + ck) & 0xFF,
            '(mh+ck)&FF':     (mh + ck) & 0xFF,
            'ml^(p[0]+p[1])': (ml ^ ((p[0]+p[1]) & 0xFF)) & 0xFF if len(p) > 1 else -1,
            'p[0]^p[1]^ml':   (p[0] ^ p[1] ^ ml) & 0xFF if len(p) > 1 else -1,
            '~ml&FF':         (~ml) & 0xFF,
            'ml^0x89':        (ml ^ 0x89) & 0xFF,
            'ml^0x03':        (ml ^ 0x03) & 0xFF,
        }

        r['formula_results'] = formulas

    # Check which formula is consistent across ALL results
    if all_results:
        formula_names = list(all_results[0]['formula_results'].keys())
        print(f"Testing {len(formula_names)} formulas across {len(all_results)} packets:\n")

        for fname in formula_names:
            matches = sum(1 for r in all_results if r['formula_results'][fname] == r['verify'])
            if matches > 0:
                pct = matches * 100 // len(all_results)
                marker = " <<<< FOUND!" if matches == len(all_results) else ""
                print(f"  {fname:<25} {matches:3d}/{len(all_results)} ({pct:3d}%){marker}")

    # Show XOR masks to look for pattern
    print(f"\n\nXOR masks (v ^ ml for each packet):")
    unique_masks = set(xor_masks)
    print(f"  Unique values: {len(unique_masks)} ({', '.join(f'0x{m:02X}' for m in sorted(unique_masks))})")
    if len(unique_masks) == 1:
        print(f"  *** CONSTANT MASK: 0x{xor_masks[0]:02X} ***")
        print(f"  Formula: verify = msg_lo ^ 0x{xor_masks[0]:02X}")

    # Detailed per-packet output for first 10
    print(f"\n\nDetailed (first 20 packets):")
    print(f"{'PCAP':<45} {'ml':>4} {'mh':>4} {'v':>4} {'ck':>4} {'v^ml':>5} {'seed':>5}")
    print("-" * 80)
    for r in all_results[:20]:
        mask = (r['verify'] ^ r['msg_lo']) & 0xFF
        print(f"{r['pcap']:<45} 0x{r['msg_lo']:02X} 0x{r['msg_hi']:02X} 0x{r['verify']:02X} 0x{r['checksum']:02X} 0x{mask:02X}  {'OK' if r['seed_ok'] else 'NO'}")

    # ── DEEP PATTERN SEARCH ──
    # Maybe verify depends on server_key bytes?
    print(f"\n\nCheck if XOR mask relates to server key:")
    for r in all_results[:20]:
        mask = (r['verify'] ^ r['msg_lo']) & 0xFF
        sk = r['sk']
        sk_bytes = [sk & 0xFF, (sk >> 8) & 0xFF, (sk >> 16) & 0xFF, (sk >> 24) & 0xFF]
        print(f"  mask=0x{mask:02X} sk={[f'0x{b:02X}' for b in sk_bytes]} "
              f"mask^sk0=0x{mask^sk_bytes[0]:02X} mask^sk1=0x{mask^sk_bytes[1]:02X} "
              f"mask^sk2=0x{mask^sk_bytes[2]:02X} mask^sk3=0x{mask^sk_bytes[3]:02X}")


if __name__ == '__main__':
    main()
