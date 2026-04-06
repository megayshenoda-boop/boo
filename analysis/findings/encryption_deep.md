# CMsgCodec Deep Analysis - ARM64 Disassembly Confirmed

## Functions Found

| Function | Address | Purpose |
|----------|---------|---------|
| doEncode | 0x04F97C24 | Encrypt outgoing packet |
| doDecode | 0x04F97D40 | Decrypt incoming packet |
| (checksum verify helper) | 0x04F97DA4 | SIMD-optimized checksum verification |
| doEncode variant 2 | 0x04F97F40 | Second encode variant (larger packets?) |

All functions reference CMSG_TABLE at 0x028B723A via ADRP+ADD.

---

## doEncode (0x04F97C24) - Full Analysis

### Function Signature
```c
// int doEncode(uint8_t* packet, uint32_t server_key)
// x0 = packet buffer pointer
// w1 = server_key (4 bytes, but our codec uses 1 repeating byte)
// Returns: w0 = 1 (success) or 0 (failure)
```

### Prologue
```asm
0x04F97C24:  sub sp, sp, #0x30
0x04F97C28:  stp x29, x30, [sp, #0x10]
0x04F97C2C:  stp x20, x19, [sp, #0x20]
0x04F97C30:  add x29, sp, #0x10
0x04F97C34:  mrs x19, tpidr_el0      ; thread-local storage
0x04F97C38:  ldr x8, [x19, #0x28]    ; stack canary
0x04F97C3C:  str x8, [sp, #8]        ; save canary
0x04F97C40:  str w1, [sp, #4]        ; save server_key at sp+4
```

### Validation
```asm
0x04F97C44:  cbz x0, #0x4f97d1c      ; if packet == NULL, skip
0x04F97C48:  ldrh w8, [x0]           ; w8 = packet length (u16 at offset 0)
0x04F97C4C:  cmp w8, #9              ; minimum packet size = 9 (8-byte header + 1 data byte)
0x04F97C50:  b.lo #0x4f97d18         ; if length < 9, return 0 (failure)
```

**FINDING: Minimum packet size is 9 bytes (8 header + 1 data)**

### Generate Random msg Byte
```asm
0x04F97C58:  bl 0x5bde0b0            ; call random generator
0x04F97C64:  str w0, [sp]            ; save result (msg bytes) at sp+0
```

### Encryption Loop Setup
```asm
0x04F97C74:  mov w10, #8             ; i = 8 (start after 8-byte header)
0x04F97C78:  mov w11, #0x2493        ; magic constant for i%7 computation
0x04F97C7C:  adrp x12, #0x28b7000   ; }
0x04F97C80:  add x12, x12, #0x23a   ; } x12 = &CMSG_TABLE[0]
```

**Key constant 0x2493 = 9363**: Used for compiler-optimized `i % 7` via `(i * 9363) >> 16`

### Encryption Loop Core
```asm
; For each byte from index 8 to packet_length:
0x04F97C8C:  ldrb w16, [x8, x10]      ; w16 = plaintext[i]

; Compute i % 7 using multiply trick:
0x04F97C90:  mul w13, w13, w11         ; w13 = i * 0x2493
0x04F97C9C:  lsr w13, w13, #0x10      ; w13 = (i * 0x2493) >> 16 ≈ i/7
0x04F97CA0-CBC: ...                    ; arithmetic to get i%7 from i/7
0x04F97CC4:  add w13, w10, w13        ; w13 = i % 7

; Load msg_byte from sp+0 (cycling through bytes with bfxil):
0x04F97CAC:  mov x14, sp
0x04F97CB0:  bfxil x14, x10, #0, #1   ; x14 = sp + (i & 1)
0x04F97CB8:  ldrb w14, [x14]          ; w14 = msg_byte (from random result)

; The *17 multiply:
0x04F97CC0:  add w14, w14, w14, lsl #4 ; w14 = w14 + w14*16 = w14 * 17

; Load server_key byte from sp+4 (cycling through bytes):
0x04F97C88:  add x15, sp, #4
0x04F97C94:  bfxil x15, x10, #0, #2   ; x15 = (sp+4) + (i & 3)
0x04F97C98:  ldrb w15, [x15]          ; w15 = sk_byte

; Combine:
0x04F97CCC:  add w14, w14, w16        ; w14 = (msg_byte * 17) + plaintext[i]
0x04F97CD0:  ldrb w13, [x12, x13]     ; w13 = CMSG_TABLE[i % 7]
0x04F97CD4:  eor w14, w14, w15        ; w14 ^= sk_byte
0x04F97CD8:  eor w13, w14, w13        ; w13 = result ^ CMSG_TABLE[i%7]
0x04F97CDC:  strb w13, [x8, x10]      ; encrypted[i] = w13

; Checksum accumulation:
0x04F97CE8:  add w9, w13, w9          ; checksum += encrypted_byte

; Loop control:
0x04F97CE0:  add x10, x10, #1         ; i++
0x04F97CE4:  ldrh w14, [x8]           ; reload packet length
0x04F97CEC:  cmp x10, x14             ; while (i < length)
0x04F97CF0:  b.lo #0x4f97c84
```

### CONFIRMED ENCRYPTION FORMULA
```
encrypted[i] = ((msg_byte * 17 + plaintext[i]) ^ sk_byte ^ CMSG_TABLE[i % 7]) & 0xFF
```

**This EXACTLY matches our Python codec implementation!**

### Header Writing (after encryption loop)
```asm
0x04F97CF4:  mov w10, #0xb7           ; VERIFY constant = 0xB7
0x04F97CF8:  strb w9, [x8, #4]        ; header[4] = checksum (sum of encrypted bytes)
0x04F97CFC:  lsr w9, w0, #8           ; w9 = msg >> 8 (msg_high)
0x04F97D00:  strb w0, [x8, #5]        ; header[5] = msg_low
0x04F97D04:  eor w10, w0, w10         ; w10 = msg_low ^ 0xB7
0x04F97D08:  mov w0, #1               ; return 1 (success)
0x04F97D0C:  strb w10, [x8, #6]       ; header[6] = verify = msg_low ^ 0xB7
0x04F97D10:  strb w9, [x8, #7]        ; header[7] = msg_high
```

### CONFIRMED PACKET HEADER LAYOUT
```
Offset  Size  Field       Notes
------  ----  -----       -----
0       2     length      u16 LE, total packet length
2       2     opcode      u16 LE, set before encode is called
4       1     checksum    sum of all encrypted bytes (& 0xFF)
5       1     msg_low     random msg byte (low byte)
6       1     verify      msg_low ^ 0xB7
7       1     msg_high    msg >> 8 (high byte)
8+      N     data        encrypted payload
```

---

## doDecode (0x04F97D40) - Full Analysis

### Function Signature
```c
// int doDecode(uint8_t* packet, uint32_t server_key, uint16_t* opcode_out)
// x0 = packet buffer pointer
// w1 = server_key
// x2 = pointer to store extracted opcode
// Returns: w0 = 1 (success) or 0 (failure)
```

### Entry
```asm
0x04F97D40:  sub sp, sp, #0x20
0x04F97D44:  stp x29, x30, [sp, #0x10]
0x04F97D48:  add x29, sp, #0x10
0x04F97D58:  str w1, [sp, #4]         ; save server_key at sp+4
0x04F97D5C:  cbz x0, #0x4f97f24      ; null check
```

### Extract Opcode and msg Bytes
```asm
0x04F97D60:  ldrh w9, [x0, #2]        ; w9 = opcode (u16 at offset 2)
0x04F97D64:  strh w9, [x2]            ; *opcode_out = opcode
```

### Extract msg Bytes and Store
```asm
0x04F97D68:  ldrh w10, [x0]           ; w10 = packet length
0x04F97D6C:  ldrb w11, [x0, #5]       ; w11 = msg_low (from header offset 5)
0x04F97D70:  ldrb w9, [x0, #7]        ; w9 = msg_high (from header offset 7)
0x04F97D74:  orr w9, w11, w9, lsl #8  ; w9 = msg_low | (msg_high << 8) = full msg u16
0x04F97D78:  sub w11, w10, #8         ; w11 = data length (total - 8 header bytes)
0x04F97D7C:  strb w9, [sp]            ; store msg_low at sp+0
0x04F97D80:  lsr w12, w9, #8          ; w12 = msg_high
0x04F97D84:  strb w12, [sp, #1]       ; store msg_high at sp+1
```

### Checksum Verification (SIMD-optimized!)
The code at 0x04F97DCC-0x04F97E08 uses NEON SIMD instructions to sum encrypted bytes fast:
```asm
; Process 32 bytes at a time using NEON vector addition:
0x04F97DE0:  ldp q2, q3, [x12, #-0x10]  ; load 32 bytes
0x04F97DEC:  add v0.16b, v2.16b, v0.16b ; vector byte-add
0x04F97DF0:  add v1.16b, v3.16b, v1.16b
; ...
0x04F97E00:  addv b0, v0.16b            ; horizontal sum of 16 bytes

; Then verify:
0x04F97E70:  ldrb w10, [x0, #4]          ; w10 = stored checksum
0x04F97E74:  cmp w10, w12, uxtb          ; compare with computed checksum
0x04F97E78:  b.ne #0x4f97f20             ; if mismatch, return 0 (failure)
```

### Verify Byte Check
```asm
0x04F97E7C:  ldrb w10, [x0, #6]          ; w10 = verify byte
0x04F97E80:  eor w9, w10, w9             ; w9 = verify ^ msg
0x04F97E84:  cmp w9, #0xb7              ; should equal 0xB7
0x04F97E88:  b.ne #0x4f97d74            ; if not, return 0
```

### Decryption Loop
```asm
0x04F97E8C:  mov w9, #8                  ; i = 8
0x04F97E90:  mov w10, #0x2493            ; modulo-7 constant
0x04F97E94:  adrp x11, #0x28b7000       ; }
0x04F97E98:  add x11, x11, #0x23a       ; } x11 = &CMSG_TABLE

; Loop body:
0x04F97EA4:  ldrb w15, [x0, x9]          ; w15 = encrypted[i]
0x04F97EB8:  add w14, w14, w14, lsl #4   ; w14 = msg_byte * 17
; ... compute i%7 ...
0x04F97EDC:  eor w13, w13, w15           ; w13 = sk_byte ^ encrypted[i]
0x04F97EE8:  ldrb w12, [x11, x12]        ; w12 = CMSG_TABLE[i%7]
0x04F97EEC:  eor w12, w13, w12           ; w12 = (sk ^ enc) ^ table
0x04F97EF0:  sub w12, w12, w14           ; w12 = result - (msg*17) = plaintext
0x04F97EF4:  strb w12, [x0, x9]          ; plaintext[i] = w12
```

### CONFIRMED DECRYPTION FORMULA
```
plaintext[i] = ((encrypted[i] ^ sk_byte ^ CMSG_TABLE[i%7]) - msg_byte * 17) & 0xFF
```

This is the algebraic inverse of the encryption formula. **100% confirmed match with our codec.py!**

---

## Summary of Confirmations

| Aspect | Our Implementation | ARM64 Disassembly | Match? |
|--------|-------------------|-------------------|--------|
| Table bytes | [0x58,0xEF,0xD7,0x14,0xA2,0x3B,0x9C] | Loaded from 0x028B723A | YES |
| Table cycle | i % 7 | Computed via 0x2493 multiply trick | YES |
| Multiply constant | *17 | `add w, w, w, lsl #4` = x*17 | YES |
| Verify constant | 0xB7 | `mov w10, #0xb7` | YES |
| Header size | 8 bytes | Loop starts at offset 8 | YES |
| Header layout | [len:2][op:2][ck:1][ml:1][v:1][mh:1] | Confirmed by strb offsets | YES |
| Min packet size | - | 9 bytes (header + 1) | NEW INFO |
| Checksum | Sum of encrypted bytes | SIMD-optimized sum + verify | YES |
| NEON optimization | - | Uses vector ops for checksum | NEW INFO |

### Key Addresses
```
doEncode:     0x04F97C24  (encode outgoing packets)
doDecode:     0x04F97D40  (decode incoming packets)
CMSG_TABLE:   0x028B723A  (7-byte XOR table in .rodata)
random_gen:   0x5BDE0B0   (generates msg random byte)
```

### Note on Server Key
The server key parameter (w1) is stored as a 32-bit word and accessed byte-by-byte using `bfxil` with different bit widths:
- In encode: `bfxil x15, x10, #0, #2` (4-byte cycle from server key)
- In decode: `bfxil x13, x9, #0, #2` (same pattern)

When our bot passes a single-byte server key as `sk | (sk << 8) | (sk << 16) | (sk << 24)`, all 4 bytes are identical, so every cycle gives the same byte. This is correct behavior.
