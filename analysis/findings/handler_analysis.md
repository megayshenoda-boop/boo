# Deep Handler Analysis Report
# Generated: 2026-04-03 05:53:27
# Binary: D:\CascadeProjects\libgame.so


================================================================================
# 1. OPCODE 0x1B8B DEEP ANALYSIS
================================================================================

Known: MOVZ with 0x1B8B at 0x058EA650
Known: Calls function at 0x05C851B0

## 1.1 Finding Function Entry Point

Function prologue found at: **0x058EA548**
Distance from MOVZ: 264 bytes (66 instructions)

## 1.2 Full Disassembly: Before 0x1B8B MOVZ

```asm
; Region around 0x1B8B MOVZ (context window)
  0x058EA548:  stp        x29, x30, [sp, #-0x60]!  ; <<< FUNCTION ENTRY >>>
  0x058EA54C:  stp        x28, x27, [sp, #0x10]
  0x058EA550:  stp        x26, x25, [sp, #0x20]
  0x058EA554:  stp        x24, x23, [sp, #0x30]
  0x058EA558:  stp        x22, x21, [sp, #0x40]
  0x058EA55C:  stp        x20, x19, [sp, #0x50]
  0x058EA560:  mov        x29, sp
  0x058EA564:  ldr        x28, [x1, #8]
  0x058EA568:  ldr        x8, [x28, #0x3f8]
  0x058EA56C:  cbz        x8, #0x58ea658
  0x058EA570:  mov        x20, x5
  0x058EA574:  mov        x21, x4
  0x058EA578:  mov        x23, x3
  0x058EA57C:  mov        x19, x1
  0x058EA580:  mov        x24, x2
  0x058EA584:  mov        x25, x0
  0x058EA588:  bl         #0x5bdc580  ; CALL -> 0x5BDC580
  0x058EA58C:  add        x8, x20, x23
  0x058EA590:  mov        x26, x0
  0x058EA594:  adrp       x1, #0x25e8000  ; ADRP+ADD -> 0x25E8A85 = "ssl/ssl_lib.c"
  0x058EA598:  add        x1, x1, #0xa85
  0x058EA59C:  add        x27, x0, x8, lsl #1
  0x058EA5A0:  mov        w2, #0x1b76
  0x058EA5A4:  add        x0, x27, #3
  0x058EA5A8:  bl         #0x5c84ed0  ; CALL -> 0x5C84ED0
  0x058EA5AC:  cbz        x0, #0x58ea65c
  0x058EA5B0:  mov        x1, x25
  0x058EA5B4:  mov        x2, x26
  0x058EA5B8:  mov        x22, x0
  0x058EA5BC:  bl         #0x5bdc520  ; CALL -> 0x5BDC520
  0x058EA5C0:  add        x8, x22, x26
  0x058EA5C4:  mov        w10, #0x20
  0x058EA5C8:  adrp       x9, #0x2614000  ; ADRP+ADD -> 0x2614637 = "0123456789abcdef"
  0x058EA5CC:  add        x9, x9, #0x637
  0x058EA5D0:  strb       w10, [x8], #1
  0x058EA5D4:  cbz        x23, #0x58ea5fc
  0x058EA5D8:  ldrb       w11, [x24], #1
  0x058EA5DC:  subs       x23, x23, #1
  0x058EA5E0:  lsr        x12, x11, #4
  0x058EA5E4:  and        x11, x11, #0xf
  0x058EA5E8:  ldrb       w11, [x9, x11]
  0x058EA5EC:  ldrb       w12, [x9, x12]
  0x058EA5F0:  strb       w11, [x8, #1]
  0x058EA5F4:  strb       w12, [x8], #2
  0x058EA5F8:  b.ne       #0x58ea5d8
  0x058EA5FC:  strb       w10, [x8], #1
  0x058EA600:  cbz        x20, #0x58ea628
  0x058EA604:  ldrb       w10, [x21], #1
  0x058EA608:  subs       x20, x20, #1
  0x058EA60C:  lsr        x11, x10, #4
  0x058EA610:  and        x10, x10, #0xf
  0x058EA614:  ldrb       w10, [x9, x10]
  0x058EA618:  ldrb       w11, [x9, x11]
  0x058EA61C:  strb       w10, [x8, #1]
  0x058EA620:  strb       w11, [x8], #2
  0x058EA624:  b.ne       #0x58ea604
  0x058EA628:  strb       wzr, [x8]
  0x058EA62C:  ldr        x8, [x28, #0x3f8]
  0x058EA630:  cbz        x8, #0x58ea640
  0x058EA634:  ldr        x0, [x19, #0x40]
  0x058EA638:  mov        x1, x22
  0x058EA63C:  blr        x8
  0x058EA640:  adrp       x2, #0x25e8000  ; ADRP+ADD -> 0x25E8A85 = "ssl/ssl_lib.c"
  0x058EA644:  add        x2, x2, #0xa85
  0x058EA648:  add        x1, x27, #3
  0x058EA64C:  mov        x0, x22
  0x058EA650:  mov        w3, #0x1b8b  ; <<< 0x1B8B OPCODE MOVZ HERE >>>
  0x058EA654:  bl         #0x5c851b0  ; <<< CALL TO 0x1B8B HANDLER FUNCTION 0x5C851B0 >>>
  0x058EA658:  mov        w0, #1
  0x058EA65C:  ldp        x20, x19, [sp, #0x50]
  0x058EA660:  ldp        x22, x21, [sp, #0x40]
  0x058EA664:  ldp        x24, x23, [sp, #0x30]
  0x058EA668:  ldp        x26, x25, [sp, #0x20]
  0x058EA66C:  ldp        x28, x27, [sp, #0x10]
  0x058EA670:  ldp        x29, x30, [sp], #0x60
  0x058EA674:  ret        
  0x058EA678:  mov        x8, x0
  0x058EA67C:  mov        x5, x3
  0x058EA680:  mov        x4, x2
  0x058EA684:  add        x2, x0, #0x188
  0x058EA688:  mov        x0, x1
  0x058EA68C:  mov        x1, x8
  0x058EA690:  mov        w3, #0x20
  0x058EA694:  b          #0x58ea548
  0x058EA698:  stp        x29, x30, [sp, #-0x30]!
  0x058EA69C:  stp        x22, x21, [sp, #0x10]
  0x058EA6A0:  stp        x20, x19, [sp, #0x20]
  0x058EA6A4:  mov        x29, sp
  0x058EA6A8:  ldr        x8, [x1, #8]
  0x058EA6AC:  mov        x19, x0
  0x058EA6B0:  cbz        x8, #0x58ea6f8
  0x058EA6B4:  cmp        w2, #0
  0x058EA6B8:  mov        w9, #2
  0x058EA6BC:  cinc       x9, x9, ne
  0x058EA6C0:  udiv       x10, x8, x9
  0x058EA6C4:  msub       x8, x10, x9, x8
  0x058EA6C8:  cbz        x8, #0x58ea740
  0x058EA6CC:  bl         #0x5c84e80  ; CALL -> 0x5C84E80
  0x058EA6D0:  adrp       x0, #0x25e8000  ; ADRP+ADD -> 0x25E8A85 = "ssl/ssl_lib.c"
  0x058EA6D4:  add        x0, x0, #0xa85
  0x058EA6D8:  adrp       x2, #0x2587000  ; ADRP+ADD -> 0x2587688 = "ssl_cache_cipherlist"
  0x058EA6DC:  add        x2, x2, #0x688
  0x058EA6E0:  mov        w1, #0x1bbe
  0x058EA6E4:  bl         #0x5c84e90  ; CALL -> 0x5C84E90
  0x058EA6E8:  mov        x0, x19
  0x058EA6EC:  mov        w1, #0x32
  0x058EA6F0:  mov        w2, #0x97
  0x058EA6F4:  b          #0x58ea720
  0x058EA6F8:  bl         #0x5c84e80  ; CALL -> 0x5C84E80
  0x058EA6FC:  adrp       x0, #0x25e8000  ; ADRP+ADD -> 0x25E8A85 = "ssl/ssl_lib.c"
  0x058EA700:  add        x0, x0, #0xa85
  0x058EA704:  adrp       x2, #0x2587000  ; ADRP+ADD -> 0x2587688 = "ssl_cache_cipherlist"
  0x058EA708:  add        x2, x2, #0x688
  0x058EA70C:  mov        w1, #0x1bb9
  0x058EA710:  bl         #0x5c84e90  ; CALL -> 0x5C84E90
  0x058EA714:  mov        x0, x19
  0x058EA718:  mov        w1, #0x32
  0x058EA71C:  mov        w2, #0xb7
  0x058EA720:  mov        x3, xzr
  0x058EA724:  bl         #0x5c84ea0  ; CALL -> 0x5C84EA0
  0x058EA728:  mov        w8, wzr
  0x058EA72C:  mov        w0, w8
  0x058EA730:  ldp        x20, x19, [sp, #0x20]
  0x058EA734:  ldp        x22, x21, [sp, #0x10]
  0x058EA738:  ldp        x29, x30, [sp], #0x30
  0x058EA73C:  ret        
  0x058EA740:  ldr        x0, [x19, #0x3a0]
  0x058EA744:  mov        x20, x1
  0x058EA748:  adrp       x1, #0x25e8000  ; ADRP+ADD -> 0x25E8A85 = "ssl/ssl_lib.c"
  0x058EA74C:  add        x1, x1, #0xa85
  0x058EA750:  mov        w22, w2
  0x058EA754:  mov        w2, #0x1bc2
  0x058EA758:  add        x21, x19, #0x3a0
  0x058EA75C:  bl         #0x5c74fa0  ; CALL -> 0x5C74FA0
  0x058EA760:  movi       v0.2d, #0000000000000000
  0x058EA764:  str        q0, [x19, #0x3a0]
  0x058EA768:  cbz        w22, #0x58ea800
  0x058EA76C:  mov        x8, x20
  0x058EA770:  ldr        x20, [x20, #8]
  0x058EA774:  mov        x9, #-0x5555555555555556
  0x058EA778:  movk       x9, #0xaaab
  0x058EA77C:  ldr        x22, [x8]
  0x058EA780:  adrp       x1, #0x25e8000  ; ADRP+ADD -> 0x25E8A85 = "ssl/ssl_lib.c"
  0x058EA784:  add        x1, x1, #0xa85
  0x058EA788:  umulh      x8, x20, x9
  0x058EA78C:  mov        w2, #0x1bd3
```

## 1.3 Data Flow Analysis

Found 13 store instructions before 0x1B8B MOVZ:

| Address | Instruction | Size | Type |
|---------|-------------|------|------|
| 0x058EA548 | `stp x29, x30, [sp, #-0x60]!` | 16 | 2xu64 |
| 0x058EA54C | `stp x28, x27, [sp, #0x10]` | 16 | 2xu64 |
| 0x058EA550 | `stp x26, x25, [sp, #0x20]` | 16 | 2xu64 |
| 0x058EA554 | `stp x24, x23, [sp, #0x30]` | 16 | 2xu64 |
| 0x058EA558 | `stp x22, x21, [sp, #0x40]` | 16 | 2xu64 |
| 0x058EA55C | `stp x20, x19, [sp, #0x50]` | 16 | 2xu64 |
| 0x058EA5D0 | `strb w10, [x8], #1` | 1 | u8 |
| 0x058EA5F0 | `strb w11, [x8, #1]` | 1 | u8 |
| 0x058EA5F4 | `strb w12, [x8], #2` | 1 | u8 |
| 0x058EA5FC | `strb w10, [x8], #1` | 1 | u8 |
| 0x058EA61C | `strb w10, [x8, #1]` | 1 | u8 |
| 0x058EA620 | `strb w11, [x8], #2` | 1 | u8 |
| 0x058EA628 | `strb wzr, [x8]` | 1 | u8 |

## 1.4 Immediate Value Construction


## 1.5 String References

Strings referenced in the function:

  - 0x058EA594: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA5C8: `"0123456789abcdef"` (at 0x2614637)
  - 0x058EA640: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA6D0: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA6D8: `"ssl_cache_cipherlist"` (at 0x2587688)
  - 0x058EA6FC: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA704: `"ssl_cache_cipherlist"` (at 0x2587688)
  - 0x058EA748: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA780: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA800: `"include/internal/packet.h"` (at 0x260ED56)
  - 0x058EA828: `"include/internal/packet.h"` (at 0x260ED56)
  - 0x058EA87C: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA884: `"ssl_cache_cipherlist"` (at 0x2587688)
  - 0x058EA8AC: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA8B4: `"ssl_cache_cipherlist"` (at 0x2587688)
  - 0x058EA90C: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EA914: `"ssl_cache_cipherlist"` (at 0x2587688)
  - 0x058EAA18: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EAA20: `"ossl_bytes_to_cipher_list"` (at 0x25DB92D)
  - 0x058EAA48: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EAA50: `"ossl_bytes_to_cipher_list"` (at 0x25DB92D)
  - 0x058EAAB8: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EAAC0: `"ossl_bytes_to_cipher_list"` (at 0x25DB92D)
  - 0x058EAB18: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EAB20: `"ossl_bytes_to_cipher_list"` (at 0x25DB92D)
  - 0x058EACD4: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EACDC: `"ossl_bytes_to_cipher_list"` (at 0x25DB92D)
  - 0x058EAED8: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EAEE0: `"SSL_clear"` (at 0x25AE720)
  - 0x058EB034: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EB03C: `"SSL_verify_client_post_handshake"` (at 0x261B96E)
  - 0x058EB0E4: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EB0EC: `"SSL_verify_client_post_handshake"` (at 0x261B96E)
  - 0x058EB120: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EB128: `"SSL_verify_client_post_handshake"` (at 0x261B96E)
  - 0x058EB148: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EB150: `"SSL_verify_client_post_handshake"` (at 0x261B96E)
  - 0x058EB180: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EB188: `"SSL_verify_client_post_handshake"` (at 0x261B96E)
  - 0x058EB1A8: `"ssl/ssl_lib.c"` (at 0x25E8A85)
  - 0x058EB1B0: `"SSL_verify_client_post_handshake"` (at 0x261B96E)

================================================================================
# 2. FUNCTION 0x5C851B0 ANALYSIS (Called with 0x1B8B)
================================================================================

Disassembling 500 instructions at 0x05C851B0

Successfully disassembled 500 instructions
## 2.1 Disassembly Listing

```asm
; Function at 0x5C851B0
  0x05C851B0:  adrp       x16, #0x632b000  ; <<< FUNCTION ENTRY >>>
  0x05C851B4:  ldr        x17, [x16, #0x508]
  0x05C851B8:  add        x16, x16, #0x508
  0x05C851BC:  br         x17
  0x05C851C0:  adrp       x16, #0x632b000
  0x05C851C4:  ldr        x17, [x16, #0x510]
  0x05C851C8:  add        x16, x16, #0x510
  0x05C851CC:  br         x17
  0x05C851D0:  adrp       x16, #0x632b000
  0x05C851D4:  ldr        x17, [x16, #0x518]
  0x05C851D8:  add        x16, x16, #0x518
  0x05C851DC:  br         x17
  0x05C851E0:  adrp       x16, #0x632b000
  0x05C851E4:  ldr        x17, [x16, #0x520]
  0x05C851E8:  add        x16, x16, #0x520
  0x05C851EC:  br         x17
  0x05C851F0:  adrp       x16, #0x632b000
  0x05C851F4:  ldr        x17, [x16, #0x528]
  0x05C851F8:  add        x16, x16, #0x528
  0x05C851FC:  br         x17
  0x05C85200:  adrp       x16, #0x632b000
  0x05C85204:  ldr        x17, [x16, #0x530]
  0x05C85208:  add        x16, x16, #0x530
  0x05C8520C:  br         x17
  0x05C85210:  adrp       x16, #0x632b000
  0x05C85214:  ldr        x17, [x16, #0x538]
  0x05C85218:  add        x16, x16, #0x538
  0x05C8521C:  br         x17
  0x05C85220:  adrp       x16, #0x632b000
  0x05C85224:  ldr        x17, [x16, #0x540]
  0x05C85228:  add        x16, x16, #0x540
  0x05C8522C:  br         x17
  0x05C85230:  adrp       x16, #0x632b000
  0x05C85234:  ldr        x17, [x16, #0x548]
  0x05C85238:  add        x16, x16, #0x548
  0x05C8523C:  br         x17
  0x05C85240:  adrp       x16, #0x632b000
  0x05C85244:  ldr        x17, [x16, #0x550]
  0x05C85248:  add        x16, x16, #0x550
  0x05C8524C:  br         x17
  0x05C85250:  adrp       x16, #0x632b000
  0x05C85254:  ldr        x17, [x16, #0x558]
  0x05C85258:  add        x16, x16, #0x558
  0x05C8525C:  br         x17
  0x05C85260:  adrp       x16, #0x632b000
  0x05C85264:  ldr        x17, [x16, #0x560]
  0x05C85268:  add        x16, x16, #0x560
  0x05C8526C:  br         x17
  0x05C85270:  adrp       x16, #0x632b000
  0x05C85274:  ldr        x17, [x16, #0x568]
  0x05C85278:  add        x16, x16, #0x568
  0x05C8527C:  br         x17
  0x05C85280:  adrp       x16, #0x632b000
  0x05C85284:  ldr        x17, [x16, #0x570]
  0x05C85288:  add        x16, x16, #0x570
  0x05C8528C:  br         x17
  0x05C85290:  adrp       x16, #0x632b000
  0x05C85294:  ldr        x17, [x16, #0x578]
  0x05C85298:  add        x16, x16, #0x578
  0x05C8529C:  br         x17
  0x05C852A0:  adrp       x16, #0x632b000
  0x05C852A4:  ldr        x17, [x16, #0x580]
  0x05C852A8:  add        x16, x16, #0x580
  0x05C852AC:  br         x17
  0x05C852B0:  adrp       x16, #0x632b000
  0x05C852B4:  ldr        x17, [x16, #0x588]
  0x05C852B8:  add        x16, x16, #0x588
  0x05C852BC:  br         x17
  0x05C852C0:  adrp       x16, #0x632b000
  0x05C852C4:  ldr        x17, [x16, #0x590]
  0x05C852C8:  add        x16, x16, #0x590
  0x05C852CC:  br         x17
  0x05C852D0:  adrp       x16, #0x632b000
  0x05C852D4:  ldr        x17, [x16, #0x598]
  0x05C852D8:  add        x16, x16, #0x598
  0x05C852DC:  br         x17
  0x05C852E0:  adrp       x16, #0x632b000
  0x05C852E4:  ldr        x17, [x16, #0x5a0]
  0x05C852E8:  add        x16, x16, #0x5a0
  0x05C852EC:  br         x17
  0x05C852F0:  adrp       x16, #0x632b000
  0x05C852F4:  ldr        x17, [x16, #0x5a8]
  0x05C852F8:  add        x16, x16, #0x5a8
  0x05C852FC:  br         x17
  0x05C85300:  adrp       x16, #0x632b000
  0x05C85304:  ldr        x17, [x16, #0x5b0]
  0x05C85308:  add        x16, x16, #0x5b0
  0x05C8530C:  br         x17
  0x05C85310:  adrp       x16, #0x632b000
  0x05C85314:  ldr        x17, [x16, #0x5b8]
  0x05C85318:  add        x16, x16, #0x5b8
  0x05C8531C:  br         x17
  0x05C85320:  adrp       x16, #0x632b000
  0x05C85324:  ldr        x17, [x16, #0x5c0]
  0x05C85328:  add        x16, x16, #0x5c0
  0x05C8532C:  br         x17
  0x05C85330:  adrp       x16, #0x632b000
  0x05C85334:  ldr        x17, [x16, #0x5c8]
  0x05C85338:  add        x16, x16, #0x5c8
  0x05C8533C:  br         x17
  0x05C85340:  adrp       x16, #0x632b000
  0x05C85344:  ldr        x17, [x16, #0x5d0]
  0x05C85348:  add        x16, x16, #0x5d0
  0x05C8534C:  br         x17
  0x05C85350:  adrp       x16, #0x632b000
  0x05C85354:  ldr        x17, [x16, #0x5d8]
  0x05C85358:  add        x16, x16, #0x5d8
  0x05C8535C:  br         x17
  0x05C85360:  adrp       x16, #0x632b000
  0x05C85364:  ldr        x17, [x16, #0x5e0]
  0x05C85368:  add        x16, x16, #0x5e0
  0x05C8536C:  br         x17
  0x05C85370:  adrp       x16, #0x632b000
  0x05C85374:  ldr        x17, [x16, #0x5e8]
  0x05C85378:  add        x16, x16, #0x5e8
  0x05C8537C:  br         x17
  0x05C85380:  adrp       x16, #0x632b000
  0x05C85384:  ldr        x17, [x16, #0x5f0]
  0x05C85388:  add        x16, x16, #0x5f0
  0x05C8538C:  br         x17
  0x05C85390:  adrp       x16, #0x632b000
  0x05C85394:  ldr        x17, [x16, #0x5f8]
  0x05C85398:  add        x16, x16, #0x5f8
  0x05C8539C:  br         x17
  0x05C853A0:  adrp       x16, #0x632b000
  0x05C853A4:  ldr        x17, [x16, #0x600]
  0x05C853A8:  add        x16, x16, #0x600
  0x05C853AC:  br         x17
  0x05C853B0:  adrp       x16, #0x632b000
  0x05C853B4:  ldr        x17, [x16, #0x608]
  0x05C853B8:  add        x16, x16, #0x608
  0x05C853BC:  br         x17
  0x05C853C0:  adrp       x16, #0x632b000
  0x05C853C4:  ldr        x17, [x16, #0x610]
  0x05C853C8:  add        x16, x16, #0x610
  0x05C853CC:  br         x17
  0x05C853D0:  adrp       x16, #0x632b000
  0x05C853D4:  ldr        x17, [x16, #0x618]
  0x05C853D8:  add        x16, x16, #0x618
  0x05C853DC:  br         x17
  0x05C853E0:  adrp       x16, #0x632b000
  0x05C853E4:  ldr        x17, [x16, #0x620]
  0x05C853E8:  add        x16, x16, #0x620
  0x05C853EC:  br         x17
  0x05C853F0:  adrp       x16, #0x632b000
  0x05C853F4:  ldr        x17, [x16, #0x628]
  0x05C853F8:  add        x16, x16, #0x628
  0x05C853FC:  br         x17
  0x05C85400:  adrp       x16, #0x632b000
  0x05C85404:  ldr        x17, [x16, #0x630]
  0x05C85408:  add        x16, x16, #0x630
  0x05C8540C:  br         x17
  0x05C85410:  adrp       x16, #0x632b000
  0x05C85414:  ldr        x17, [x16, #0x638]
  0x05C85418:  add        x16, x16, #0x638
  0x05C8541C:  br         x17
  0x05C85420:  adrp       x16, #0x632b000
  0x05C85424:  ldr        x17, [x16, #0x640]
  0x05C85428:  add        x16, x16, #0x640
  0x05C8542C:  br         x17
  0x05C85430:  adrp       x16, #0x632b000
  0x05C85434:  ldr        x17, [x16, #0x648]
  0x05C85438:  add        x16, x16, #0x648
  0x05C8543C:  br         x17
  0x05C85440:  adrp       x16, #0x632b000
  0x05C85444:  ldr        x17, [x16, #0x650]
  0x05C85448:  add        x16, x16, #0x650
  0x05C8544C:  br         x17
  0x05C85450:  adrp       x16, #0x632b000
  0x05C85454:  ldr        x17, [x16, #0x658]
  0x05C85458:  add        x16, x16, #0x658
  0x05C8545C:  br         x17
  0x05C85460:  adrp       x16, #0x632b000
  0x05C85464:  ldr        x17, [x16, #0x660]
  0x05C85468:  add        x16, x16, #0x660
  0x05C8546C:  br         x17
  0x05C85470:  adrp       x16, #0x632b000
  0x05C85474:  ldr        x17, [x16, #0x668]
  0x05C85478:  add        x16, x16, #0x668
  0x05C8547C:  br         x17
  0x05C85480:  adrp       x16, #0x632b000
  0x05C85484:  ldr        x17, [x16, #0x670]
  0x05C85488:  add        x16, x16, #0x670
  0x05C8548C:  br         x17
  0x05C85490:  adrp       x16, #0x632b000
  0x05C85494:  ldr        x17, [x16, #0x678]
  0x05C85498:  add        x16, x16, #0x678
  0x05C8549C:  br         x17
  0x05C854A0:  adrp       x16, #0x632b000
  0x05C854A4:  ldr        x17, [x16, #0x680]
  0x05C854A8:  add        x16, x16, #0x680
  0x05C854AC:  br         x17
  0x05C854B0:  adrp       x16, #0x632b000
  0x05C854B4:  ldr        x17, [x16, #0x688]
  0x05C854B8:  add        x16, x16, #0x688
  0x05C854BC:  br         x17
  0x05C854C0:  adrp       x16, #0x632b000
  0x05C854C4:  ldr        x17, [x16, #0x690]
  0x05C854C8:  add        x16, x16, #0x690
  0x05C854CC:  br         x17
```

## 2.2 Call Graph


## 2.3 Function Classification

- Does NOT call GoSocket::sendData directly
- Total calls: 0 (one of these likely leads to sendData)
- Total stores: 0

================================================================================
# 3. OPCODE 0x0CE8 START_MARCH DEEP ANALYSIS
================================================================================

Known MOVZ references:
  - 0x0555FE3C
  - 0x05566714
  - 0x05566B68

### 3.1 Analysis of reference at 0x0555FE3C

Function entry: **0x0555FDDC** (96 bytes before MOVZ)

```asm
; 0x0CE8 handler context at ref 0x555FE3C
  0x0555FDDC:  sub        sp, sp, #0x70  ; FUNCTION ENTRY
  0x0555FDE0:  stp        x29, x30, [sp, #0x10]
  0x0555FDE4:  stp        x28, x27, [sp, #0x20]
  0x0555FDE8:  stp        x26, x25, [sp, #0x30]
  0x0555FDEC:  stp        x24, x23, [sp, #0x40]
  0x0555FDF0:  stp        x22, x21, [sp, #0x50]
  0x0555FDF4:  stp        x20, x19, [sp, #0x60]
  0x0555FDF8:  add        x29, sp, #0x10
  0x0555FDFC:  ldrb       w8, [x2]
  0x0555FE00:  tst        w1, #1
  0x0555FE04:  mov        w9, #0x13f8
  0x0555FE08:  mov        w10, #0x13f0
  0x0555FE0C:  str        w1, [sp, #4]
  0x0555FE10:  csel       x25, x10, x9, ne
  0x0555FE14:  str        x2, [sp, #8]
  0x0555FE18:  cbz        w8, #0x556017c
  0x0555FE1C:  ldr        w8, [sp, #4]
  0x0555FE20:  mov        w9, #0xd08
  0x0555FE24:  add        x26, x0, #0xa2c
  0x0555FE28:  mov        x27, x2
  0x0555FE2C:  mov        x20, x0
  0x0555FE30:  adrp       x21, #0x25fa000  ; -> "NTLM"
  0x0555FE34:  add        x21, x21, #0xb7e
  0x0555FE38:  tst        w8, #1
  0x0555FE3C:  mov        w8, #0xce8  ; <<< 0x0CE8 MOVZ HERE >>>
  0x0555FE40:  csel       x8, x9, x8, ne
  0x0555FE44:  adrp       x22, #0x2627000  ; -> "Digest"
  0x0555FE48:  add        x22, x22, #0x8c3
  0x0555FE4C:  adrp       x23, #0x25ee000  ; -> "Basic"
  0x0555FE50:  add        x23, x23, #0x3d5
  0x0555FE54:  adrp       x24, #0x2621000  ; -> "Bearer"
  0x0555FE58:  add        x24, x24, #0x2d0
  0x0555FE5C:  add        x28, x0, x8
  0x0555FE60:  add        x19, x26, #0x999
  0x0555FE64:  mov        x0, x21
  0x0555FE68:  mov        x1, x27
  0x0555FE6C:  mov        w2, #4
  0x0555FE70:  bl         #0x558b394  ; CALL -> 0x558B394
  0x0555FE74:  cbz        w0, #0x555ff44
  0x0555FE78:  ldrb       w8, [x27, #4]
  0x0555FE7C:  sub        w9, w8, #0x3a
  0x0555FE80:  cmn        w9, #0xb
  0x0555FE84:  b.hi       #0x555ff44
  0x0555FE88:  and        w8, w8, #0xffffffdf
  0x0555FE8C:  sub        w8, w8, #0x5b
  0x0555FE90:  cmn        w8, #0x1b
  0x0555FE94:  b.hi       #0x555ff44
  0x0555FE98:  ldr        x8, [x28, #0x10]
  0x0555FE9C:  ldr        x27, [sp, #8]
  0x0555FEA0:  tbnz       w8, #3, #0x555feb0
  0x0555FEA4:  bl         #0x559dde4  ; CALL -> 0x559DDE4
  0x0555FEA8:  tbz        w0, #0, #0x555ff44
  0x0555FEAC:  ldr        x8, [x28, #0x10]
  0x0555FEB0:  ldr        x10, [x28, #8]
  0x0555FEB4:  ldr        x9, [x20, x25]
  0x0555FEB8:  orr        x8, x8, #8
  0x0555FEBC:  str        x8, [x28, #0x10]
  0x0555FEC0:  cmp        x10, #8
  0x0555FEC4:  orr        x9, x9, #8
  0x0555FEC8:  str        x9, [x20, x25]
  0x0555FECC:  b.ne       #0x555ff44
  0x0555FED0:  ldr        w8, [sp, #4]
  0x0555FED4:  mov        x0, x20
  0x0555FED8:  mov        x2, x27
  0x0555FEDC:  and        w1, w8, #1
  0x0555FEE0:  bl         #0x55668ac  ; CALL -> 0x55668AC
  0x0555FEE4:  cbz        w0, #0x555ff28
  0x0555FEE8:  ldrb       w8, [x26, #3]
  0x0555FEEC:  tbz        w8, #5, #0x555ff14
  0x0555FEF0:  ldr        x8, [x20, #0x1318]
  0x0555FEF4:  cbz        x8, #0x555ff04
  0x0555FEF8:  ldr        w8, [x8, #8]
  0x0555FEFC:  cmp        w8, #1
  0x0555FF00:  b.lt       #0x555ff14
  0x0555FF04:  mov        x0, x20
  0x0555FF08:  adrp       x1, #0x2599000  ; -> "NTLM authentication problem, ignoring."
  0x0555FF0C:  add        x1, x1, #0xb40
  0x0555FF10:  bl         #0x5549818  ; CALL -> 0x5549818
  0x0555FF14:  ldrb       w8, [x19, #2]
  0x0555FF18:  ldrh       w9, [x19]
  0x0555FF1C:  orr        w8, w9, w8, lsl #16
  0x0555FF20:  orr        w8, w8, #0x80
  0x0555FF24:  b          #0x555ff38
  0x0555FF28:  ldrb       w8, [x19, #2]
```

**Conditional branches (may determine 0x0CE8 vs 0x0D08):**
  - `cmn w9, #0xb` at 0x555FE80 -> `b.hi #0x555ff44` -> 0x555FF44
  - `cmn w8, #0x1b` at 0x555FE90 -> `b.hi #0x555ff44` -> 0x555FF44
  - `cmp x10, #8` at 0x555FEC0 -> `b.ne #0x555ff44` -> 0x555FF44
  - `cmp w8, #1` at 0x555FEFC -> `b.lt #0x555ff14` -> 0x555FF14
  - `cmn w9, #0xb` at 0x555FF64 -> `b.hi #0x5560028` -> 0x5560028
  - `cmn w8, #0x1b` at 0x555FF74 -> `b.hi #0x5560028` -> 0x5560028
  - `cmp w8, #1` at 0x555FFD4 -> `b.lt #0x555ffec` -> 0x555FFEC
  - `cmp w8, #1` at 0x5560010 -> `b.lt #0x5560028` -> 0x5560028
  - `cmn w9, #0xb` at 0x5560048 -> `b.hi #0x55600bc` -> 0x55600BC
  - `cmn w8, #0x1b` at 0x5560058 -> `b.hi #0x55600bc` -> 0x55600BC
  - `cmp x10, #1` at 0x5560074 -> `b.ne #0x55600bc` -> 0x55600BC
  - `cmp w8, #1` at 0x5560098 -> `b.lt #0x55600b0` -> 0x55600B0
  - `cmn w9, #0xb` at 0x55600DC -> `b.hi #0x5560150` -> 0x5560150
  - `cmn w8, #0x1b` at 0x55600EC -> `b.hi #0x5560150` -> 0x5560150
  - `cmp x10, #0x40` at 0x5560108 -> `b.ne #0x5560150` -> 0x5560150
  - `cmp w8, #1` at 0x556012C -> `b.lt #0x5560144` -> 0x5560144
  - `cmp w8, #3` at 0x55601BC -> `b.eq #0x55601fc` -> 0x55601FC
  - `cmp w8, #2` at 0x55601C4 -> `b.eq #0x5560224` -> 0x5560224
  - `cmp w8, #1` at 0x55601E0 -> `b.lt #0x55601fc` -> 0x55601FC
  - `cmp w8, #2` at 0x556021C -> `b.ne #0x55601fc` -> 0x55601FC
  - `cmp w8, #1` at 0x5560238 -> `b.lt #0x556025c` -> 0x556025C
  - `cmp x21, x19` at 0x55602FC -> `b.hs #0x556031c` -> 0x556031C
  - `cmp w0, #0` at 0x5560334 -> `cbnz w8, #0x55602dc` -> 0x55602DC
  - `cmp x21, x9` at 0x5560354 -> `b.hs #0x5560324` -> 0x5560324
  - `cmp x8, #1` at 0x55603BC -> `b.ne #0x55603e0` -> 0x55603E0
  - `cmp w8, #2` at 0x55604EC -> `b.eq #0x55603fc` -> 0x55603FC
  - `cmp w8, #3` at 0x55604F4 -> `b.eq #0x556050c` -> 0x556050C
  - `cmp w8, #3` at 0x5560504 -> `b.ne #0x556051c` -> 0x556051C
  - `cmp w20, #0x14` at 0x5560554 -> `b.lt #0x5560570` -> 0x5560570
  - `cmp x24, #0` at 0x55605E4 -> `tbz w8, #0, #0x5560614` -> 0x5560614
  - `cmp w8, #2` at 0x5560728 -> `b.eq #0x5560638` -> 0x5560638
  - `cmp w8, #3` at 0x5560730 -> `b.eq #0x5560748` -> 0x5560748
  - `cmp w8, #3` at 0x5560740 -> `b.ne #0x5560758` -> 0x5560758
  - `cmp w20, #0x14` at 0x556078C -> `b.lt #0x55607a4` -> 0x55607A4
  - `cmp x8, x9` at 0x5560878 -> `b.eq #0x55608d8` -> 0x55608D8
  - `cmp w8, #2` at 0x556088C -> `b.hi #0x55608ec` -> 0x55608EC

**String references:**
  - `"NTLM"` at 0x25FAB7E
  - `"Digest"` at 0x26278C3
  - `"Basic"` at 0x25EE3D5
  - `"Bearer"` at 0x26212D0
  - `"NTLM authentication problem, ignoring."` at 0x2599B40
  - `"Digest authentication problem, ignoring."` at 0x25FAD0E
  - `"Ignoring duplicate digest auth header."` at 0x25DABD3
  - `"Basic authentication problem, ignoring."` at 0x25EE40A
  - `"Bearer authentication problem, ignoring."` at 0x25A6F33
  - `"Stick to %s instead of GET"` at 0x25F4716
  - `"Switch to GET because of %d response"` at 0x257FE3E
  - `"Content-Type"` at 0x25E1168
  - `"Host"` at 0x2599B31
  - `"Content-Length"` at 0x261499B
  - `"Connection"` at 0x25C70F1
  - `"Transfer-Encoding"` at 0x25CD73B
  - `"Authorization"` at 0x2586804
  - `"Cookie"` at 0x2607827
  - `"Content-Type"` at 0x25E1168
  - `"Transfer-Encoding"` at 0x25CD73B
  - `"Content-Length"` at 0x261499B
  - `"Host"` at 0x2599B31
  - `"Connection"` at 0x25C70F1
  - `"Authorization"` at 0x2586804
  - `"Cookie"` at 0x2607827
  - `"Invalid TIMEVALUE"` at 0x26212D7

### 3.2 Analysis of reference at 0x05566714

Function entry: **0x055666C0** (84 bytes before MOVZ)

```asm
; 0x0CE8 handler context at ref 0x5566714
  0x055666C0:  sub        sp, sp, #0x70  ; FUNCTION ENTRY
  0x055666C4:  stp        x29, x30, [sp, #0x10]
  0x055666C8:  stp        x28, x27, [sp, #0x20]
  0x055666CC:  stp        x26, x25, [sp, #0x30]
  0x055666D0:  stp        x24, x23, [sp, #0x40]
  0x055666D4:  stp        x22, x21, [sp, #0x50]
  0x055666D8:  stp        x20, x19, [sp, #0x60]
  0x055666DC:  add        x29, sp, #0x10
  0x055666E0:  mov        w8, #0x1360
  0x055666E4:  tst        w1, #1
  0x055666E8:  mov        w9, #0x13a8
  0x055666EC:  adrp       x15, #0x62d3000
  0x055666F0:  csel       x25, x9, x8, ne
  0x055666F4:  mov        w8, #0x1398
  0x055666F8:  mov        w9, #0x13a0
  0x055666FC:  mov        w12, #0x13b8
  0x05566700:  mov        w13, #0x13b0
  0x05566704:  ldr        x15, [x15, #0x568]
  0x05566708:  csel       x9, x12, x9, ne
  0x0556670C:  csel       x8, x13, x8, ne
  0x05566710:  mov        x19, x0
  0x05566714:  mov        w12, #0xce8  ; <<< 0x0CE8 MOVZ HERE >>>
  0x05566718:  mov        w14, #0xd08
  0x0556671C:  ldr        x24, [x0, x9]
  0x05566720:  ldr        x23, [x0, x8]
  0x05566724:  ldr        x8, [x15]
  0x05566728:  ldr        x0, [x0, x25]
  0x0556672C:  mov        w10, #0xc78
  0x05566730:  mov        w11, #0xcb0
  0x05566734:  csel       x12, x14, x12, ne
  0x05566738:  mov        x22, x3
  0x0556673C:  mov        x21, x2
  0x05566740:  mov        w20, w1
  0x05566744:  csel       x27, x11, x10, ne
  0x05566748:  add        x26, x19, x12
  0x0556674C:  blr        x8
  0x05566750:  adrp       x28, #0x258f000
  0x05566754:  add        x28, x28, #0xace
  0x05566758:  cmp        x23, #0
  0x0556675C:  ldr        x9, [x19, x27]
  0x05566760:  csel       x23, x28, x23, eq
  0x05566764:  cmp        x24, #0
  0x05566768:  ldrb       w8, [x26, #0x18]
  0x0556676C:  csel       x24, x28, x24, eq
  0x05566770:  str        xzr, [x19, x25]
  0x05566774:  cbz        x9, #0x5566850
  0x05566778:  tbz        w8, #2, #0x55667ac
  0x0556677C:  mov        x0, x22
  0x05566780:  mov        w1, #0x3f
  0x05566784:  bl         #0x5c2b590  ; CALL -> 0x5C2B590
  0x05566788:  cbz        x0, #0x55667ac
  0x0556678C:  sub        w1, w0, w22
  0x05566790:  adrp       x0, #0x25c6000  ; -> "%.*s"
  0x05566794:  add        x0, x0, #0xfdd
  0x05566798:  mov        x2, x22
  0x0556679C:  bl         #0x556f738  ; CALL -> 0x556F738
  0x055667A0:  mov        x22, x0
  0x055667A4:  cbnz       x0, #0x55667c8
  0x055667A8:  b          #0x5566860
  0x055667AC:  adrp       x8, #0x62d3000
  0x055667B0:  mov        x0, x22
  0x055667B4:  ldr        x8, [x8, #0x570]
  0x055667B8:  ldr        x8, [x8]
  0x055667BC:  blr        x8
  0x055667C0:  mov        x22, x0
  0x055667C4:  cbz        x0, #0x5566860
  0x055667C8:  add        x5, x19, x27
  0x055667CC:  add        x6, sp, #8
  0x055667D0:  mov        x7, sp
  0x055667D4:  mov        x0, x19
  0x055667D8:  mov        x1, x23
  0x055667DC:  mov        x2, x24
  0x055667E0:  mov        x3, x21
  0x055667E4:  mov        x4, x22
  0x055667E8:  bl         #0x559ca08  ; CALL -> 0x559CA08
  0x055667EC:  adrp       x23, #0x62d3000
  0x055667F0:  mov        w21, w0
  0x055667F4:  mov        x0, x22
  0x055667F8:  ldr        x23, [x23, #0x568]
  0x055667FC:  ldr        x8, [x23]
  0x05566800:  blr        x8
```

**Conditional branches (may determine 0x0CE8 vs 0x0D08):**
  - `cmp x24, #0` at 0x5566764 -> `cbz x9, #0x5566850` -> 0x5566850
  - `cmp w8, #3` at 0x55669BC -> `b.eq #0x5566a10` -> 0x5566A10
  - `cmp w8, #4` at 0x55669C4 -> `b.ne #0x5566a50` -> 0x5566A50
  - `cmp w8, #1` at 0x55669E0 -> `b.lt #0x55669f8` -> 0x55669F8
  - `cmp w8, #1` at 0x5566A24 -> `b.lt #0x5566a3c` -> 0x5566A3C
  - `cmp w8, #1` at 0x5566A64 -> `b.lt #0x5566a7c` -> 0x5566A7C
  - `cmp w8, #2` at 0x5566BB0 -> `b.eq #0x5566c20` -> 0x5566C20
  - `cmp w8, #4` at 0x5566BB8 -> `b.eq #0x5566bd0` -> 0x5566BD0
  - `cmp w8, #3` at 0x5566BC0 -> `b.ne #0x5566ce8` -> 0x5566CE8
  - `cmp w10, #1` at 0x5566E20 -> `b.ne #0x5566e64` -> 0x5566E64
  - `cmp x21, x9` at 0x5566E34 -> `b.ne #0x5566e7c` -> 0x5566E7C
  - `cmp w10, #1` at 0x5566E48 -> `b.ne #0x5566e68` -> 0x5566E68
  - `cmp x21, x9` at 0x5566E58 -> `b.ne #0x5566e7c` -> 0x5566E7C
  - `cmp x21, x9` at 0x5566E74 -> `b.eq #0x5566ea4` -> 0x5566EA4
  - `cmp x21, x9` at 0x5566E9C -> `b.ne #0x5566e7c` -> 0x5566E7C
  - `cmp w23, #1` at 0x5566F4C -> `b.ne #0x5566f70` -> 0x5566F70
  - `cmp w23, #1` at 0x5566FA4 -> `b.ne #0x5566fc8` -> 0x5566FC8
  - `tst w8, #0x40` at 0x5566FD0 -> `cbz x23, #0x556724c` -> 0x556724C
  - `cmp x25, #5` at 0x55670C0 -> `b.ne #0x556712c` -> 0x556712C
  - `cmp w8, #2` at 0x5567130 -> `b.ne #0x5567148` -> 0x5567148
  - `cmp x25, #0xd` at 0x5567138 -> `b.eq #0x5567050` -> 0x5567050
  - `cmp w8, #3` at 0x5567148 -> `b.ne #0x556716c` -> 0x556716C
  - `cmp x25, #0xd` at 0x5567150 -> `b.ne #0x556716c` -> 0x556716C
  - `cmp x25, #0xf` at 0x5567174 -> `b.ne #0x5567190` -> 0x5567190
  - `cmp x25, #0xb` at 0x5567198 -> `b.ne #0x55671b4` -> 0x55671B4

**String references:**
  - `"%.*s"` at 0x25C6FDD
  - `"Proxy-"` at 0x2600FF6
  - `"NTLM"` at 0x25FAB7E
  - `"NTLM auth restarted"` at 0x258D0EC
  - `"NTLM handshake rejected"` at 0x256BB33
  - `"NTLM handshake failure (internal error)"` at 0x256595A
  - `"HTTP"` at 0x258D100
  - `"Proxy-"` at 0x2600FF6
  - `"Proxy-"` at 0x2600FF6
  - `"["` at 0x25A3730
  - `"%s%s%s:%d"` at 0x259382C
  - `"]"` at 0x25DDB16
  - `"CONNECT"` at 0x259366E
  - `"Host"` at 0x2599B31
  - `"User-Agent"` at 0x2600FFD
  - `"Proxy-Connection"` at 0x25CD755
  - `"Content-Type:"` at 0x26149F8
  - `"Host:"` at 0x25CD766
  - `"Content-Type:"` at 0x26149F8
  - `"Content-Length:"` at 0x25656E4
  - `"Connection:"` at 0x25C0734

### 3.3 Analysis of reference at 0x05566B68

Function entry: **0x05566AB8** (176 bytes before MOVZ)

```asm
; 0x0CE8 handler context at ref 0x5566B68
  0x05566AB8:  sub        sp, sp, #0x90  ; FUNCTION ENTRY
  0x05566ABC:  stp        x29, x30, [sp, #0x30]
  0x05566AC0:  stp        x28, x27, [sp, #0x40]
  0x05566AC4:  stp        x26, x25, [sp, #0x50]
  0x05566AC8:  stp        x24, x23, [sp, #0x60]
  0x05566ACC:  stp        x22, x21, [sp, #0x70]
  0x05566AD0:  stp        x20, x19, [sp, #0x80]
  0x05566AD4:  add        x29, sp, #0x30
  0x05566AD8:  mov        w8, #0x1360
  0x05566ADC:  tst        w1, #1
  0x05566AE0:  mov        w9, #0x13a8
  0x05566AE4:  mov        w10, #0x1398
  0x05566AE8:  csel       x28, x9, x8, ne
  0x05566AEC:  mov        w8, #0x13b0
  0x05566AF0:  mov        w12, #0x720
  0x05566AF4:  mov        w13, #0x788
  0x05566AF8:  mov        w9, #0x13a0
  0x05566AFC:  mov        w11, #0x13b8
  0x05566B00:  csel       x8, x8, x10, ne
  0x05566B04:  csel       x10, x13, x12, ne
  0x05566B08:  ldr        x21, [x0, #0x20]
  0x05566B0C:  csel       x9, x11, x9, ne
  0x05566B10:  mov        w11, #0xa0
  0x05566B14:  mov        w12, #0x128
  0x05566B18:  ldr        x10, [x0, x10]
  0x05566B1C:  stur       xzr, [x29, #-8]
  0x05566B20:  csel       x11, x12, x11, ne
  0x05566B24:  mov        w12, #0x428
  0x05566B28:  mov        w13, #0x42c
  0x05566B2C:  mov        x19, x0
  0x05566B30:  csel       x27, x13, x12, ne
  0x05566B34:  cmp        x10, #0
  0x05566B38:  ldr        x26, [x0, x9]
  0x05566B3C:  ldr        x25, [x0, x8]
  0x05566B40:  ldr        x23, [x21, x11]
  0x05566B44:  adrp       x8, #0x258d000  ; -> "HTTP"
  0x05566B48:  add        x8, x8, #0x100
  0x05566B4C:  mov        x0, x21
  0x05566B50:  mov        w20, w1
  0x05566B54:  stur       xzr, [x29, #-0x10]
  0x05566B58:  csel       x24, x8, x10, eq
  0x05566B5C:  bl         #0x559e9d8  ; CALL -> 0x559E9D8
  0x05566B60:  cbz        x0, #0x5566c18
  0x05566B64:  tst        w20, #1
  0x05566B68:  mov        w8, #0xce8  ; <<< 0x0CE8 MOVZ HERE >>>
  0x05566B6C:  mov        w9, #0xd08
  0x05566B70:  csel       x8, x9, x8, ne
  0x05566B74:  str        x28, [sp]
  0x05566B78:  adrp       x9, #0x258f000
  0x05566B7C:  add        x9, x9, #0xace
  0x05566B80:  add        x28, x19, x8
  0x05566B84:  cmp        x25, #0
  0x05566B88:  ldrb       w8, [x28, #0x18]
  0x05566B8C:  mov        x22, x0
  0x05566B90:  csel       x25, x9, x25, eq
  0x05566B94:  cmp        x26, #0
  0x05566B98:  add        x0, sp, #8
  0x05566B9C:  and        w8, w8, #0xfe
  0x05566BA0:  csel       x26, x9, x26, eq
  0x05566BA4:  strb       w8, [x28, #0x18]
  0x05566BA8:  bl         #0x5536098  ; CALL -> 0x5536098
  0x05566BAC:  ldr        w8, [x21, x27]
  0x05566BB0:  cmp        w8, #2
  0x05566BB4:  b.eq       #0x5566c20
  0x05566BB8:  cmp        w8, #4
  0x05566BBC:  b.eq       #0x5566bd0
  0x05566BC0:  cmp        w8, #3
  0x05566BC4:  b.ne       #0x5566ce8
  0x05566BC8:  mov        w8, #4
  0x05566BCC:  str        w8, [x21, x27]
  0x05566BD0:  adrp       x8, #0x62d3000
  0x05566BD4:  tst        w20, #1
  0x05566BD8:  mov        w9, #0x1408
  0x05566BDC:  ldr        x8, [x8, #0x568]
  0x05566BE0:  ldr        x20, [sp]
  0x05566BE4:  mov        w10, #0x1400
  0x05566BE8:  csel       x9, x10, x9, ne
  0x05566BEC:  mov        w10, #8
  0x05566BF0:  ldr        x8, [x8]
  0x05566BF4:  ldr        x0, [x19, x20]
  0x05566BF8:  str        x10, [x19, x9]
  0x05566BFC:  blr        x8
  0x05566C00:  ldrb       w8, [x28, #0x18]
  0x05566C04:  mov        w22, wzr
  0x05566C08:  str        xzr, [x19, x20]
  0x05566C0C:  orr        w8, w8, #1
  0x05566C10:  strb       w8, [x28, #0x18]
  0x05566C14:  b          #0x5566da8
  0x05566C18:  mov        w22, #0x1b
  0x05566C1C:  b          #0x5566db0
  0x05566C20:  add        x4, sp, #8
  0x05566C24:  mov        x0, x19
  0x05566C28:  mov        x1, x25
  0x05566C2C:  mov        x2, x26
  0x05566C30:  mov        x3, x22
  0x05566C34:  bl         #0x559e154  ; CALL -> 0x559E154
  0x05566C38:  mov        w22, w0
  0x05566C3C:  cbnz       w0, #0x5566da8
  0x05566C40:  add        x0, sp, #8
  0x05566C44:  bl         #0x5536130  ; CALL -> 0x5536130
  0x05566C48:  cbz        x0, #0x5566da4
  0x05566C4C:  add        x0, sp, #8
  0x05566C50:  bl         #0x5536128  ; CALL -> 0x5536128
  0x05566C54:  mov        x22, x0
```

**Conditional branches (may determine 0x0CE8 vs 0x0D08):**
  - `cmp w8, #2` at 0x5566BB0 -> `b.eq #0x5566c20` -> 0x5566C20
  - `cmp w8, #4` at 0x5566BB8 -> `b.eq #0x5566bd0` -> 0x5566BD0
  - `cmp w8, #3` at 0x5566BC0 -> `b.ne #0x5566ce8` -> 0x5566CE8
  - `cmp w10, #1` at 0x5566E20 -> `b.ne #0x5566e64` -> 0x5566E64
  - `cmp x21, x9` at 0x5566E34 -> `b.ne #0x5566e7c` -> 0x5566E7C
  - `cmp w10, #1` at 0x5566E48 -> `b.ne #0x5566e68` -> 0x5566E68
  - `cmp x21, x9` at 0x5566E58 -> `b.ne #0x5566e7c` -> 0x5566E7C
  - `cmp x21, x9` at 0x5566E74 -> `b.eq #0x5566ea4` -> 0x5566EA4
  - `cmp x21, x9` at 0x5566E9C -> `b.ne #0x5566e7c` -> 0x5566E7C
  - `cmp w23, #1` at 0x5566F4C -> `b.ne #0x5566f70` -> 0x5566F70
  - `cmp w23, #1` at 0x5566FA4 -> `b.ne #0x5566fc8` -> 0x5566FC8
  - `tst w8, #0x40` at 0x5566FD0 -> `cbz x23, #0x556724c` -> 0x556724C
  - `cmp x25, #5` at 0x55670C0 -> `b.ne #0x556712c` -> 0x556712C
  - `cmp w8, #2` at 0x5567130 -> `b.ne #0x5567148` -> 0x5567148
  - `cmp x25, #0xd` at 0x5567138 -> `b.eq #0x5567050` -> 0x5567050
  - `cmp w8, #3` at 0x5567148 -> `b.ne #0x556716c` -> 0x556716C
  - `cmp x25, #0xd` at 0x5567150 -> `b.ne #0x556716c` -> 0x556716C
  - `cmp x25, #0xf` at 0x5567174 -> `b.ne #0x5567190` -> 0x5567190
  - `cmp x25, #0xb` at 0x5567198 -> `b.ne #0x55671b4` -> 0x55671B4
  - `cmp w8, #0x14` at 0x55671B8 -> `b.lt #0x5567200` -> 0x5567200
  - `cmp x25, #0x12` at 0x55671C0 -> `b.ne #0x5567200` -> 0x5567200
  - `cmp x25, #7` at 0x5567200 -> `b.eq #0x5567224` -> 0x5567224
  - `cmp x25, #0xe` at 0x5567208 -> `b.ne #0x55671e0` -> 0x55671E0
  - `cmp w2, #0xb` at 0x55672CC -> `b.ne #0x55672f4` -> 0x55672F4
  - `cmp w9, #1` at 0x5567330 -> `b.lt #0x5567378` -> 0x5567378
  - `cmp w9, #1` at 0x5567340 -> `b.lt #0x5567378` -> 0x5567378
  - `cmp w8, #1` at 0x55673D0 -> `b.lt #0x55673fc` -> 0x55673FC
  - `cmp w8, #1` at 0x55673E0 -> `b.lt #0x55673fc` -> 0x55673FC
  - `cmp w22, #2` at 0x5567494 -> `b.hi #0x5567624` -> 0x5567624
  - `cmp w8, #1` at 0x55674C0 -> `b.lt #0x55674f0` -> 0x55674F0
  - `cmp w8, #1` at 0x55674D0 -> `b.lt #0x55674f0` -> 0x55674F0
  - `cmp w8, #1` at 0x55674FC -> `b.lt #0x5567518` -> 0x5567518
  - `cmp w22, #2` at 0x5567584 -> `b.ls #0x5567594` -> 0x5567594

**String references:**
  - `"HTTP"` at 0x258D100
  - `"Proxy-"` at 0x2600FF6
  - `"Proxy-"` at 0x2600FF6
  - `"["` at 0x25A3730
  - `"%s%s%s:%d"` at 0x259382C
  - `"]"` at 0x25DDB16
  - `"CONNECT"` at 0x259366E
  - `"Host"` at 0x2599B31
  - `"User-Agent"` at 0x2600FFD
  - `"Proxy-Connection"` at 0x25CD755
  - `"Content-Type:"` at 0x26149F8
  - `"Host:"` at 0x25CD766
  - `"Content-Type:"` at 0x26149F8
  - `"Content-Length:"` at 0x25656E4
  - `"Connection:"` at 0x25C0734
  - `"Transfer-Encoding:"` at 0x25866AF
  - `"Authorization:"` at 0x256BB4B
  - `"Cookie:"` at 0x25E7CF8
  - `"User-Agent"` at 0x2600FFD
  - `"Host"` at 0x2599B31
  - `"Proxy-Connection"` at 0x25CD755
  - `"Keep-Alive"` at 0x25C0A2C
  - `"destroy"` at 0x25FAAA2
  - `"connect"` at 0x260761C
  - `"installing subfilter for HTTP/1.1"` at 0x256BB5A
  - `"CONNECT tunnel: HTTP/1.%d negotiated"` at 0x2614A15

## 3.4 Cross-reference: 0x0CE8 vs 0x0D08 Selection

0x0D08 not found in the immediate vicinity of 0x0CE8 references.
The conditional selection may happen in a caller function or through
an indirect mechanism (e.g., vtable or function pointer).

## 3.5 Packet Field Analysis (Store Instructions)

**Stores near 0x555FE3C:**

| Address | Type | Size | Instruction |
|---------|------|------|-------------|
| 0x0555FF3C | u16 | 2B | `strh w8, [x19]` |
| 0x0555FF40 | u8 | 1B | `strb w9, [x19, #2]` |
| 0x0555FFA4 | u64 | 8B | `str x8, [x20, x25]` |
| 0x0555FFAC | u64 | 8B | `str x8, [x28, #0x10]` |
| 0x0555FFF4 | u16 | 2B | `strh w8, [x19]` |
| 0x0556006C | u64 | 8B | `str x8, [x20, x25]` |
| 0x05560078 | u64 | 8B | `str x8, [x28, #0x10]` |
| 0x05560084 | u64 | 8B | `str xzr, [x28, #0x10]` |
| 0x055600B8 | u16 | 2B | `strh w8, [x19]` |
| 0x05560100 | u64 | 8B | `str x8, [x20, x25]` |
| 0x0556010C | u64 | 8B | `str x8, [x28, #0x10]` |
| 0x05560118 | u64 | 8B | `str xzr, [x28, #0x10]` |
| 0x0556014C | u16 | 2B | `strh w8, [x19]` |
| 0x05560168 | u64 | 8B | `str x8, [sp, #8]` |
| 0x055601A0 | 2xu64 | 16B | `stp x29, x30, [sp, #-0x20]!` |
| 0x055601A4 | 2xu64 | 16B | `stp x20, x19, [sp, #0x10]` |
| 0x05560200 | u8 | 1B | `strb wzr, [x20, #0x998]` |
| 0x05560274 | u8 | 1B | `strb w8, [x20, #0x99b]` |
| 0x0556027C | u8 | 1B | `strb wzr, [x20, #0x998]` |
| 0x05560290 | 2xu64 | 16B | `stp x29, x30, [sp, #0x20]` |
| 0x05560294 | 2xu64 | 16B | `stp x22, x21, [sp, #0x30]` |
| 0x05560298 | 2xu64 | 16B | `stp x20, x19, [sp, #0x40]` |
| 0x055602CC | u64 | 8B | `stur x8, [x29, #-8]` |
| 0x05560320 | u64 | 8B | `stur x8, [x29, #-8]` |
| 0x05560358 | u64 | 8B | `stur x8, [x29, #-8]` |
| 0x05560368 | 2xu64 | 16B | `stp x29, x30, [sp, #0x30]` |
| 0x0556036C | 2xu64 | 16B | `stp x28, x27, [sp, #0x40]` |
| 0x05560370 | 2xu64 | 16B | `stp x26, x25, [sp, #0x50]` |
| 0x05560374 | 2xu64 | 16B | `stp x24, x23, [sp, #0x60]` |
| 0x05560378 | 2xu64 | 16B | `stp x22, x21, [sp, #0x70]` |
| 0x0556037C | 2xu64 | 16B | `stp x20, x19, [sp, #0x80]` |
| 0x05560390 | u64 | 8B | `str x3, [sp]` |
| 0x0556042C | u64 | 8B | `str x25, [sp, #0x18]` |
| 0x0556047C | u64 | 8B | `str x25, [sp, #0x18]` |
| 0x05560668 | u64 | 8B | `str x25, [sp, #0x18]` |
| 0x055606B8 | u64 | 8B | `str x25, [sp, #0x18]` |
| 0x0556081C | 2xu64 | 16B | `stp x29, x30, [sp, #0xb0]` |
| 0x05560820 | 2xu64 | 16B | `stp x22, x21, [sp, #0xc0]` |
| 0x05560824 | 2xu64 | 16B | `stp x20, x19, [sp, #0xd0]` |
| 0x05560834 | u64 | 8B | `stur x8, [x29, #-8]` |

**Stores near 0x5566714:**

| Address | Type | Size | Instruction |
|---------|------|------|-------------|
| 0x05566888 | u64 | 8B | `str x19, [sp, #0x10]` |
| 0x055668B0 | 2xu64 | 16B | `stp x29, x30, [sp, #0x30]` |
| 0x055668B4 | 2xu64 | 16B | `stp x24, x23, [sp, #0x40]` |
| 0x055668B8 | 2xu64 | 16B | `stp x22, x21, [sp, #0x50]` |
| 0x055668BC | 2xu64 | 16B | `stp x20, x19, [sp, #0x60]` |
| 0x05566918 | u64 | 8B | `stur x8, [x29, #-8]` |
| 0x05566A48 | u32 | 4B | `str wzr, [x19, x24]` |
| 0x05566A9C | u32 | 4B | `str w8, [x19, x24]` |
| 0x05566ABC | 2xu64 | 16B | `stp x29, x30, [sp, #0x30]` |
| 0x05566AC0 | 2xu64 | 16B | `stp x28, x27, [sp, #0x40]` |
| 0x05566AC4 | 2xu64 | 16B | `stp x26, x25, [sp, #0x50]` |
| 0x05566AC8 | 2xu64 | 16B | `stp x24, x23, [sp, #0x60]` |
| 0x05566ACC | 2xu64 | 16B | `stp x22, x21, [sp, #0x70]` |
| 0x05566AD0 | 2xu64 | 16B | `stp x20, x19, [sp, #0x80]` |
| 0x05566B1C | u64 | 8B | `stur xzr, [x29, #-8]` |
| 0x05566B54 | u64 | 8B | `stur xzr, [x29, #-0x10]` |
| 0x05566B74 | u64 | 8B | `str x28, [sp]` |
| 0x05566BA4 | u8 | 1B | `strb w8, [x28, #0x18]` |
| 0x05566BCC | u32 | 4B | `str w8, [x21, x27]` |
| 0x05566BF8 | u64 | 8B | `str x10, [x19, x9]` |
| 0x05566C08 | u64 | 8B | `str xzr, [x19, x20]` |
| 0x05566C10 | u8 | 1B | `strb w8, [x28, #0x18]` |
| 0x05566CBC | u64 | 8B | `str x0, [x19, x23]` |
| 0x05566CD8 | u32 | 4B | `str w8, [x21, x27]` |
| 0x05566D80 | u64 | 8B | `str x0, [x19, x22]` |
| 0x05566DE0 | 2xu64 | 16B | `stp x29, x30, [sp, #0x20]` |
| 0x05566DE4 | 2xu64 | 16B | `stp x28, x27, [sp, #0x30]` |
| 0x05566DE8 | 2xu64 | 16B | `stp x26, x25, [sp, #0x40]` |
| 0x05566DEC | 2xu64 | 16B | `stp x24, x23, [sp, #0x50]` |
| 0x05566DF0 | 2xu64 | 16B | `stp x22, x21, [sp, #0x60]` |
| 0x05566DF4 | 2xu64 | 16B | `stp x20, x19, [sp, #0x70]` |
| 0x05566E10 | u64 | 8B | `str xzr, [sp, #0x10]` |
| 0x05566F14 | u64 | 8B | `str xzr, [sp]` |
| 0x05566FF0 | u32 | 4B | `str w8, [sp, #0xc]` |
| 0x0556700C | u64 | 8B | `str xzr, [sp, #0x10]` |
| 0x0556702C | u64 | 8B | `str x8, [x19]` |
| 0x0556707C | u64 | 8B | `stur x0, [x29, #-8]` |
| 0x05567094 | u64 | 8B | `stur x8, [x29, #-8]` |
| 0x055670E8 | u64 | 8B | `stur x0, [x29, #-8]` |
| 0x05567100 | u64 | 8B | `stur x8, [x29, #-8]` |

**Stores near 0x5566B68:**

| Address | Type | Size | Instruction |
|---------|------|------|-------------|
| 0x05566B1C | u64 | 8B | `stur xzr, [x29, #-8]` |
| 0x05566B54 | u64 | 8B | `stur xzr, [x29, #-0x10]` |
| 0x05566B74 | u64 | 8B | `str x28, [sp]` |
| 0x05566BA4 | u8 | 1B | `strb w8, [x28, #0x18]` |
| 0x05566BCC | u32 | 4B | `str w8, [x21, x27]` |
| 0x05566BF8 | u64 | 8B | `str x10, [x19, x9]` |
| 0x05566C08 | u64 | 8B | `str xzr, [x19, x20]` |
| 0x05566C10 | u8 | 1B | `strb w8, [x28, #0x18]` |
| 0x05566CBC | u64 | 8B | `str x0, [x19, x23]` |
| 0x05566CD8 | u32 | 4B | `str w8, [x21, x27]` |
| 0x05566D80 | u64 | 8B | `str x0, [x19, x22]` |
| 0x05566DE0 | 2xu64 | 16B | `stp x29, x30, [sp, #0x20]` |
| 0x05566DE4 | 2xu64 | 16B | `stp x28, x27, [sp, #0x30]` |
| 0x05566DE8 | 2xu64 | 16B | `stp x26, x25, [sp, #0x40]` |
| 0x05566DEC | 2xu64 | 16B | `stp x24, x23, [sp, #0x50]` |
| 0x05566DF0 | 2xu64 | 16B | `stp x22, x21, [sp, #0x60]` |
| 0x05566DF4 | 2xu64 | 16B | `stp x20, x19, [sp, #0x70]` |
| 0x05566E10 | u64 | 8B | `str xzr, [sp, #0x10]` |
| 0x05566F14 | u64 | 8B | `str xzr, [sp]` |
| 0x05566FF0 | u32 | 4B | `str w8, [sp, #0xc]` |
| 0x0556700C | u64 | 8B | `str xzr, [sp, #0x10]` |
| 0x0556702C | u64 | 8B | `str x8, [x19]` |
| 0x0556707C | u64 | 8B | `stur x0, [x29, #-8]` |
| 0x05567094 | u64 | 8B | `stur x8, [x29, #-8]` |
| 0x055670E8 | u64 | 8B | `stur x0, [x29, #-8]` |
| 0x05567100 | u64 | 8B | `stur x8, [x29, #-8]` |
| 0x055672E8 | u32 | 4B | `str w9, [x3]` |
| 0x055672EC | u64 | 8B | `str x8, [x4]` |
| 0x05567348 | 2xu64 | 16B | `stp x29, x30, [sp, #-0x20]!` |
| 0x0556734C | u64 | 8B | `str x19, [sp, #0x10]` |
| 0x05567388 | 2xu64 | 16B | `stp x29, x30, [sp, #-0x50]!` |
| 0x0556738C | 2xu64 | 16B | `stp x26, x25, [sp, #0x10]` |
| 0x05567390 | 2xu64 | 16B | `stp x24, x23, [sp, #0x20]` |
| 0x05567394 | 2xu64 | 16B | `stp x22, x21, [sp, #0x30]` |
| 0x05567398 | 2xu64 | 16B | `stp x20, x19, [sp, #0x40]` |
| 0x05567438 | u8 | 1B | `strb w8, [x20]` |
| 0x05567478 | u8 | 1B | `strb wzr, [x20]` |
| 0x05567540 | u64 | 8B | `str x0, [x25]` |
| 0x05567544 | u32 | 4B | `str w9, [x25, #8]` |
| 0x05567568 | u8 | 1B | `strb wzr, [x20]` |


================================================================================
# 4. OPCODE 0x0CE7 CANCEL_MARCH ANALYSIS
================================================================================

Known: MOVZ at 0x05AFE404

```asm
; 0x0CE7 CANCEL_MARCH handler
  0x05AFE364:  cmlt       v19.8h, v17.8h, #0
  0x05AFE368:  smax       v17.8h, v17.8h, v1.8h
  0x05AFE36C:  and        v6.16b, v19.16b, v6.16b
  0x05AFE370:  cmlt       v18.8h, v7.8h, #0
  0x05AFE374:  smax       v7.8h, v7.8h, v1.8h
  0x05AFE378:  orr        v6.16b, v6.16b, v17.16b
  0x05AFE37C:  and        v16.16b, v18.16b, v16.16b
  0x05AFE380:  stur       q6, [x5, #-0x100]
  0x05AFE384:  orr        v7.16b, v16.16b, v7.16b
  0x05AFE388:  str        q7, [x5], #0x10
  0x05AFE38C:  b.ne       #0x5afe308
  0x05AFE390:  cmp        x3, x2
  0x05AFE394:  b.eq       #0x5afe29c
  0x05AFE398:  ldrh       w1, [x16]
  0x05AFE39C:  ldrh       w2, [x0, x14]
  0x05AFE3A0:  sub        w3, w1, w2
  0x05AFE3A4:  add        w1, w2, w1
  0x05AFE3A8:  add        w3, w3, #0xd01
  0x05AFE3AC:  sub        w2, w1, #0xd01
  0x05AFE3B0:  mul        w3, w3, w15
  0x05AFE3B4:  umull      x4, w3, w9
  0x05AFE3B8:  lsr        x4, x4, #0x18
  0x05AFE3BC:  madd       w3, w4, w13, w3
  0x05AFE3C0:  sxth       w4, w2
  0x05AFE3C4:  and        w1, w1, w4, lsr #15
  0x05AFE3C8:  bic        w2, w2, w4, asr #31
  0x05AFE3CC:  sub        w5, w3, #0xd01
  0x05AFE3D0:  sxth       w6, w5
  0x05AFE3D4:  orr        w1, w1, w2
  0x05AFE3D8:  and        w3, w3, w6, lsr #15
  0x05AFE3DC:  bic        w4, w5, w6, asr #31
  0x05AFE3E0:  orr        w2, w3, w4
  0x05AFE3E4:  strh       w2, [x0, x14]
  0x05AFE3E8:  add        x14, x14, #2
  0x05AFE3EC:  strh       w1, [x16], #2
  0x05AFE3F0:  cmp        x16, x17
  0x05AFE3F4:  b.lo       #0x5afe398
  0x05AFE3F8:  sub        x15, x14, #2
  0x05AFE3FC:  cmp        x15, #0x1fe
  0x05AFE400:  b.lt       #0x5afe2ac
  0x05AFE404:  mov        w8, #0xce7  ; <<< 0x0CE7 CANCEL_MARCH MOVZ >>>
  0x05AFE408:  mov        w9, #0x13af
  0x05AFE40C:  movi       v0.4s, #0xf2, msl #8
  0x05AFE410:  movi       v1.2d, #0000000000000000
  0x05AFE414:  dup        v2.8h, w8
  0x05AFE418:  dup        v3.4s, w9
  0x05AFE41C:  mvni       v4.8h, #0xd, lsl #8
  0x05AFE420:  mov        x8, xzr
  0x05AFE424:  ldr        q5, [x0, x8]
  0x05AFE428:  umull      v6.4s, v5.4h, v2.4h
  0x05AFE42C:  umull2     v7.4s, v5.8h, v2.8h
  0x05AFE430:  umull      v16.2d, v6.2s, v3.2s
  0x05AFE434:  umull      v17.2d, v7.2s, v3.2s
  0x05AFE438:  umull2     v6.2d, v6.4s, v3.4s
  0x05AFE43C:  umull2     v7.2d, v7.4s, v3.4s
  0x05AFE440:  shrn       v17.2s, v17.2d, #0x18
  0x05AFE444:  shrn       v16.2s, v16.2d, #0x18
  0x05AFE448:  shrn2      v17.4s, v7.2d, #0x18
  0x05AFE44C:  shrn2      v16.4s, v6.2d, #0x18
  0x05AFE450:  mul        v6.4s, v16.4s, v0.4s
  0x05AFE454:  mul        v7.4s, v17.4s, v0.4s
  0x05AFE458:  umlal2     v7.4s, v5.8h, v2.8h
  0x05AFE45C:  umlal      v6.4s, v5.4h, v2.4h
  0x05AFE460:  uzp1       v5.8h, v6.8h, v7.8h
  0x05AFE464:  add        v6.8h, v5.8h, v4.8h
  0x05AFE468:  cmlt       v7.8h, v6.8h, #0
  0x05AFE46C:  smax       v6.8h, v6.8h, v1.8h
  0x05AFE470:  and        v5.16b, v7.16b, v5.16b
  0x05AFE474:  orr        v5.16b, v5.16b, v6.16b
  0x05AFE478:  str        q5, [x0, x8]
  0x05AFE47C:  add        x8, x8, #0x10
  0x05AFE480:  cmp        x8, #0x200
  0x05AFE484:  b.ne       #0x5afe424
  0x05AFE488:  ldp        x20, x19, [sp, #0x20]
  0x05AFE48C:  ldp        x22, x21, [sp, #0x10]
  0x05AFE490:  ldr        x23, [sp], #0x30
  0x05AFE494:  ret        
  0x05AFE498:  ldr        x0, [x0, #8]
  0x05AFE49C:  ret        
  0x05AFE4A0:  ldr        x0, [x0, #0xb0]
```

## 4.1 Cancellation Packet Fields

| Address | Type | Size | Instruction |
|---------|------|------|-------------|
| 0x05AFE3E4 | u16 | 2B | `strh w2, [x0, x14]` |
| 0x05AFE3EC | u16 | 2B | `strh w1, [x16], #2` |
| 0x05AFE478 | unknown | 0B | `str q5, [x0, x8]` |
| 0x05AFE4C4 | 2xu64 | 16B | `stp x29, x30, [sp, #-0x40]!` |
| 0x05AFE4C8 | 2xu64 | 16B | `stp x24, x23, [sp, #0x10]` |
| 0x05AFE4CC | 2xu64 | 16B | `stp x22, x21, [sp, #0x20]` |
| 0x05AFE4D0 | 2xu64 | 16B | `stp x20, x19, [sp, #0x30]` |
| 0x05AFE570 | u64 | 8B | `str x8, [x20]` |
| 0x05AFE5B0 | u64 | 8B | `str x8, [x21, #0xb0]` |
| 0x05AFE5C4 | u32 | 4B | `str w8, [x0, #0xb8]` |
| 0x05AFE614 | 2xu64 | 16B | `stp xzr, xzr, [x20]` |
| 0x05AFE62C | 2xu64 | 16B | `stp x29, x30, [sp, #-0x30]!` |
| 0x05AFE630 | 2xu64 | 16B | `stp x22, x21, [sp, #0x10]` |
| 0x05AFE634 | 2xu64 | 16B | `stp x20, x19, [sp, #0x20]` |
| 0x05AFE670 | 2xu64 | 16B | `stp x20, x21, [x0]` |
| 0x05AFE67C | u32 | 4B | `str w8, [x0, #0xb8]` |
| 0x05AFE694 | u64 | 8B | `str x0, [x22, #0x10]` |
| 0x05AFE6B4 | u64 | 8B | `str x19, [x22, #0x18]` |
| 0x05AFE718 | 2xu64 | 16B | `stp x29, x30, [sp, #-0x20]!` |
| 0x05AFE71C | u64 | 8B | `str x19, [sp, #0x10]` |

## 4.2 String References

  - `"crypto/ml_dsa/ml_dsa_key.c"` at 0x26098F7
  - `"crypto/ml_dsa/ml_dsa_key.c"` at 0x26098F7
  - `"crypto/ml_dsa/ml_dsa_key.c"` at 0x26098F7
  - `"crypto/ml_dsa/ml_dsa_key.c"` at 0x26098F7
  - `"SHAKE-128"` at 0x2574D96
  - `"SHAKE-256"` at 0x259BF19
  - `"crypto/ml_dsa/ml_dsa_key.c"` at 0x26098F7

## 4.3 Functions Called

  - 0x5C74FA0 x3
  - 0x5C84D90 x1
  - 0x5C85340 x2
  - 0x5C861B0 x2
  - 0x5C86860 x2
  - 0x5C93260 x1
  - 0x5C93410 x1

================================================================================
# 5. GoSocket::sendData (0x4F95CA8) ANALYSIS
================================================================================

```asm
; GoSocket::sendData
  0x04F95CA8:  stp        x29, x30, [sp, #-0x10]!  ; <<< GoSocket::sendData ENTRY >>>
  0x04F95CAC:  mov        x29, sp
  0x04F95CB0:  ldr        w0, [x0, #8]
  0x04F95CB4:  mov        x4, xzr
  0x04F95CB8:  mov        w5, wzr
  0x04F95CBC:  sxtw       x2, w2
  0x04F95CC0:  bl         #0x5c6db10  ; CALL -> 0x5C6DB10
  0x04F95CC4:  cmn        x0, #1
  0x04F95CC8:  b.eq       #0x4f95cd8
  0x04F95CCC:  mov        w0, #1
  0x04F95CD0:  ldp        x29, x30, [sp], #0x10
  0x04F95CD4:  ret          ; RETURN
  0x04F95CD8:  bl         #0x5bdc5b0  ; CALL -> 0x5BDC5B0
  0x04F95CDC:  ldr        w8, [x0]
  0x04F95CE0:  cmp        w8, #0x73
  0x04F95CE4:  ccmp       w8, #0xb, #4, ne
  0x04F95CE8:  cset       w0, eq
  0x04F95CEC:  ldp        x29, x30, [sp], #0x10
  0x04F95CF0:  ret          ; RETURN
  0x04F95CF4:  stp        x29, x30, [sp, #-0x20]!
  0x04F95CF8:  str        x19, [sp, #0x10]
  0x04F95CFC:  mov        x29, sp
  0x04F95D00:  adrp       x8, #0x62d2000
  0x04F95D04:  mov        w1, wzr
  0x04F95D08:  mov        w2, #0x800
  0x04F95D0C:  ldr        x8, [x8, #0x830]
  0x04F95D10:  mov        x19, x0
  0x04F95D14:  str        xzr, [x0, #0x808]
  0x04F95D18:  add        x8, x8, #0x10
  0x04F95D1C:  str        x8, [x0], #8
  0x04F95D20:  bl         #0x5bdc510  ; CALL -> 0x5BDC510
  0x04F95D24:  str        wzr, [x19, #8]
  0x04F95D28:  ldr        x19, [sp, #0x10]
  0x04F95D2C:  ldp        x29, x30, [sp], #0x20
  0x04F95D30:  ret          ; RETURN
  0x04F95D34:  stp        x29, x30, [sp, #-0x20]!
  0x04F95D38:  str        x19, [sp, #0x10]
  0x04F95D3C:  mov        x29, sp
  0x04F95D40:  mov        x19, x0
  0x04F95D44:  add        x0, x0, #8
  0x04F95D48:  mov        w1, wzr
  0x04F95D4C:  mov        w2, #0x800
  0x04F95D50:  bl         #0x5bdc510  ; CALL -> 0x5BDC510
  0x04F95D54:  str        wzr, [x19, #8]
  0x04F95D58:  ldr        x19, [sp, #0x10]
  0x04F95D5C:  ldp        x29, x30, [sp], #0x20
  0x04F95D60:  ret          ; RETURN
  0x04F95D64:  stp        x29, x30, [sp, #-0x20]!
  0x04F95D68:  str        x19, [sp, #0x10]
  0x04F95D6C:  mov        x29, sp
  0x04F95D70:  adrp       x8, #0x62d2000
  0x04F95D74:  mov        x19, x0
  0x04F95D78:  ldr        x8, [x8, #0x830]
  0x04F95D7C:  ldr        x0, [x0, #0x808]
  0x04F95D80:  add        x8, x8, #0x10
  0x04F95D84:  str        x8, [x19]
  0x04F95D88:  cbz        x0, #0x4f95d94
  0x04F95D8C:  bl         #0x5be2e10  ; CALL -> 0x5BE2E10
  0x04F95D90:  str        xzr, [x19, #0x808]
  0x04F95D94:  ldr        x19, [sp, #0x10]
  0x04F95D98:  ldp        x29, x30, [sp], #0x20
  0x04F95D9C:  ret          ; RETURN
  0x04F95DA0:  stp        x29, x30, [sp, #-0x20]!
  0x04F95DA4:  str        x19, [sp, #0x10]
  0x04F95DA8:  mov        x29, sp
  0x04F95DAC:  mov        x19, x0
  0x04F95DB0:  bl         #0x5c6db30  ; CALL -> 0x5C6DB30
  0x04F95DB4:  mov        x0, x19
  0x04F95DB8:  ldr        x19, [sp, #0x10]
  0x04F95DBC:  ldp        x29, x30, [sp], #0x20
  0x04F95DC0:  b          #0x5bdc460
  0x04F95DC4:  ldrh       w8, [x0, #8]
  0x04F95DC8:  ldrh       w9, [x0, #0xa]
  0x04F95DCC:  cmp        w8, #4
  0x04F95DD0:  ccmp       w9, #0, #4, hi
  0x04F95DD4:  cset       w0, ne
  0x04F95DD8:  ret          ; RETURN
  0x04F95DDC:  cbz        x1, #0x4f95e60
  0x04F95DE0:  stp        x29, x30, [sp, #-0x30]!
  0x04F95DE4:  str        x21, [sp, #0x10]
  0x04F95DE8:  stp        x20, x19, [sp, #0x20]
  0x04F95DEC:  mov        x29, sp
  0x04F95DF0:  ldrh       w8, [x1]
  0x04F95DF4:  and        w19, w2, #0xffff
  0x04F95DF8:  cmp        w8, w19
  0x04F95DFC:  b.ne       #0x4f95e4c
  0x04F95E00:  ldrh       w8, [x1, #2]
  0x04F95E04:  cbz        w8, #0x4f95e4c
  0x04F95E08:  cmp        w19, #0x800
  0x04F95E0C:  b.ls       #0x4f95e68
  0x04F95E10:  mov        x20, x0
  0x04F95E14:  ldr        x0, [x0, #0x808]
  0x04F95E18:  mov        x21, x1
  0x04F95E1C:  cbz        x0, #0x4f95e28
  0x04F95E20:  bl         #0x5be2e10  ; CALL -> 0x5BE2E10
  0x04F95E24:  str        xzr, [x20, #0x808]
  0x04F95E28:  mov        x0, x19
  0x04F95E2C:  bl         #0x5be5460  ; CALL -> 0x5BE5460
  0x04F95E30:  ldrh       w8, [x21]
  0x04F95E34:  mov        x1, x21
  0x04F95E38:  str        x0, [x20, #0x808]
  0x04F95E3C:  strh       w8, [x20, #8]
  0x04F95E40:  ldrh       w8, [x21, #2]
  0x04F95E44:  strh       w8, [x20, #0xa]
  0x04F95E48:  b          #0x4f95e6c
  0x04F95E4C:  mov        w0, wzr
  0x04F95E50:  ldp        x20, x19, [sp, #0x20]
  0x04F95E54:  ldr        x21, [sp, #0x10]
  0x04F95E58:  ldp        x29, x30, [sp], #0x30
  0x04F95E5C:  ret          ; RETURN
  0x04F95E60:  mov        w0, wzr
  0x04F95E64:  ret          ; RETURN
  0x04F95E68:  add        x0, x0, #8
  0x04F95E6C:  mov        x2, x19
  0x04F95E70:  bl         #0x5bdc520  ; CALL -> 0x5BDC520
  0x04F95E74:  mov        w0, #1
  0x04F95E78:  ldp        x20, x19, [sp, #0x20]
  0x04F95E7C:  ldr        x21, [sp, #0x10]
  0x04F95E80:  ldp        x29, x30, [sp], #0x30
  0x04F95E84:  ret          ; RETURN
  0x04F95E88:  ldr        x8, [x0, #0x808]
  0x04F95E8C:  add        x9, x0, #8
  0x04F95E90:  cmp        x8, #0
  0x04F95E94:  csel       x0, x9, x8, eq
  0x04F95E98:  ret          ; RETURN
  0x04F95E9C:  stp        x29, x30, [sp, #-0x20]!
  0x04F95EA0:  stp        x20, x19, [sp, #0x10]
  0x04F95EA4:  mov        x29, sp
  0x04F95EA8:  adrp       x20, #0x63f8000
  0x04F95EAC:  ldr        x0, [x20, #0x200]
  0x04F95EB0:  cbz        x0, #0x4f95ec0
  0x04F95EB4:  ldp        x20, x19, [sp, #0x10]
  0x04F95EB8:  ldp        x29, x30, [sp], #0x20
  0x04F95EBC:  ret          ; RETURN
  0x04F95EC0:  mov        w0, #0x40b8
  0x04F95EC4:  movk       w0, #8, lsl #16
  0x04F95EC8:  bl         #0x5bdc440  ; CALL -> 0x5BDC440
  0x04F95ECC:  mov        x19, x0
  0x04F95ED0:  bl         #0x5c6db50  ; CALL -> 0x5C6DB50
  0x04F95ED4:  mov        x0, x19
  0x04F95ED8:  str        x19, [x20, #0x200]
  0x04F95EDC:  ldp        x20, x19, [sp, #0x10]
  0x04F95EE0:  ldp        x29, x30, [sp], #0x20
  0x04F95EE4:  ret          ; RETURN
  0x04F95EE8:  mov        x20, x0
  0x04F95EEC:  mov        x0, x19
  0x04F95EF0:  bl         #0x5bdc460  ; CALL -> 0x5BDC460
  0x04F95EF4:  mov        x0, x20
  0x04F95EF8:  bl         #0x5bd84ac  ; CALL -> 0x5BD84AC
  0x04F95EFC:  stp        x29, x30, [sp, #-0x30]!
```

## 5.2 Call Graph

  - 0x4F9609C x1
  - 0x5BD84AC x2
  - 0x5BDC440 x1
  - 0x5BDC460 x2
  - 0x5BDC510 x2
  - 0x5BDC520 x1
  - 0x5BDC5B0 x1
  - 0x5BDF8C0 x1
  - 0x5BDF8D0 x2
  - 0x5BE2E10 x2
  - 0x5BE5460 x1
  - 0x5C6DA10 x1
  - 0x5C6DB10 x1
  - 0x5C6DB20 x1
  - 0x5C6DB30 x1
  - 0x5C6DB50 x1
  - 0x5C6DB60 x1

================================================================================
# 6. NEARBY OPCODE SCAN
================================================================================

Scanning for game opcode values (0x0C00-0x0FFF range) near known handlers...

No game opcodes found in scan regions

================================================================================
# 7. DEEP PACKET LAYOUT TRACE: 0x0CE8 (First Reference)
================================================================================

Function starts at: 0x0555FDDC
Disassembled 324 instructions from 0x555FDDC

## 7.1 Buffer Store Analysis

Stores grouped by base register (excluding SP):

### Base register: `x20` (7 stores)

| Offset | Type | Size | Address | Instruction |
|--------|------|------|---------|-------------|
| +0x0 (0) | u64 | 8B | 0x0555FEC8 | `x9, [x20, x25]` |
| +0x0 (0) | u64 | 8B | 0x0555FFA4 | `x8, [x20, x25]` |
| +0x0 (0) | u64 | 8B | 0x0556006C | `x8, [x20, x25]` |
| +0x0 (0) | u64 | 8B | 0x05560100 | `x8, [x20, x25]` |
| +0x998 (2456) | u8 | 1B | 0x05560200 | `wzr, [x20, #0x998]` |
| +0x998 (2456) | u8 | 1B | 0x0556027C | `wzr, [x20, #0x998]` |
| +0x99B (2459) | u8 | 1B | 0x05560274 | `w8, [x20, #0x99b]` |

### Base register: `x28` (6 stores)

| Offset | Type | Size | Address | Instruction |
|--------|------|------|---------|-------------|
| +0x10 (16) | u64 | 8B | 0x0555FEBC | `x8, [x28, #0x10]` |
| +0x10 (16) | u64 | 8B | 0x0555FFAC | `x8, [x28, #0x10]` |
| +0x10 (16) | u64 | 8B | 0x05560078 | `x8, [x28, #0x10]` |
| +0x10 (16) | u64 | 8B | 0x05560084 | `xzr, [x28, #0x10]` |
| +0x10 (16) | u64 | 8B | 0x0556010C | `x8, [x28, #0x10]` |
| +0x10 (16) | u64 | 8B | 0x05560118 | `xzr, [x28, #0x10]` |

### Base register: `x19` (5 stores)

| Offset | Type | Size | Address | Instruction |
|--------|------|------|---------|-------------|
| +0x0 (0) | u16 | 2B | 0x0555FF3C | `w8, [x19]` |
| +0x0 (0) | u16 | 2B | 0x0555FFF4 | `w8, [x19]` |
| +0x0 (0) | u16 | 2B | 0x055600B8 | `w8, [x19]` |
| +0x0 (0) | u16 | 2B | 0x0556014C | `w8, [x19]` |
| +0x2 (2) | u8 | 1B | 0x0555FF40 | `w9, [x19, #2]` |

## 7.2 Potential Coordinate Fields

Looking for paired stores (x, y coordinates typically stored adjacently)...


================================================================================
# 8. COMPARISON: KNOWN WORKING OPCODES vs MARCH
================================================================================

Scanning for known opcode MOVZ instructions in executable segments...

Scanning segment at 0x0 (size: 0x5C97F00, flags: XR)
  0x0CED (TRAIN): not found via MOVZ scan
  0x0CEF (BUILD): not found via MOVZ scan
  0x0CEE (RESEARCH): not found via MOVZ scan
  0x0CEB (ENABLE_VIEW): not found via MOVZ scan


================================================================================
# 9. SUMMARY & KEY FINDINGS
================================================================================

## Key Addresses

| Address | Description |
|---------|-------------|
| 0x058EA650 | 0x1B8B opcode MOVZ |
| 0x05C851B0 | Function called with 0x1B8B |
| 0x0555FE3C | 0x0CE8 START_MARCH ref #1 |
| 0x05566714 | 0x0CE8 START_MARCH ref #2 |
| 0x05566B68 | 0x0CE8 START_MARCH ref #3 |
| 0x05AFE404 | 0x0CE7 CANCEL_MARCH |
| 0x04F95CA8 | GoSocket::sendData |

## Analysis completed. See sections above for detailed findings.

## Next Steps

1. Use the identified send wrapper chain to understand buffer construction
2. Map the exact byte layout of the START_MARCH packet from store analysis
3. Cross-reference coordinate fields with known protocol format
4. Test packet construction based on the identified field layout

---
Analysis completed in 7.0 seconds