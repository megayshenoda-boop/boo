# PackData Analysis - Bot-Useful CMSG Formats

================================================================================
PACKDATA ANALYSIS - Bot-Useful CMSG Payload Formats
================================================================================

============================================================
  CMSG_START_MARCH_NEW
  Symbol: _ZN20CMSG_START_MARCH_NEW8packDataER8CIStream
  Address: 0x05212294, Size: 1252
============================================================

  Disassembly (313 insns):
    0x05212294: stp      x29, x30, [sp, #-0x30]!
    0x05212298: stp      x22, x21, [sp, #0x10]
    0x0521229C: stp      x20, x19, [sp, #0x20]
    0x052122A0: mov      x29, sp
    0x052122A4: ldr      x22, [x1]
    0x052122A8: cbz      x22, #0x5212400
    0x052122AC: ldr      w8, [x1, #0xc]
    0x052122B0: mov      x20, x1
    0x052122B4: mov      x19, x0
    0x052122B8: cbnz     w8, #0x52122f8
    0x052122BC: ldrh     w8, [x20, #0xa]
    0x052122C0: ldrh     w9, [x20, #8]
    0x052122C4: add      w10, w8, #2
    0x052122C8: cmp      w10, w9
    0x052122CC: b.ls     #0x52122dc
    0x052122D0: mov      w8, #1
    0x052122D4: str      w8, [x20, #0xc]
    0x052122D8: b        #0x52122f8
    0x052122DC: ldrh     w9, [x19]
    0x052122E0: strh     w9, [x22, w8, uxtw]
    0x052122E4: ldrh     w9, [x20, #0xa]
    0x052122E8: ldr      w8, [x20, #0xc]
    0x052122EC: add      w9, w9, #2
    0x052122F0: strh     w9, [x20, #0xa]
    0x052122F4: cbz      w8, #0x5212418
    0x052122F8: mov      x9, x19
    0x052122FC: ldp      x10, x11, [x9, #0x20]!
    0x05212300: sub      x11, x11, x10
    0x05212304: asr      x10, x11, #2
    0x05212308: tst      x11, #0x3fc
    0x0521230C: b.eq     #0x5212374
    0x05212310: cbnz     w8, #0x52123b8
    0x05212314: mov      x8, xzr
    0x05212318: and      x10, x10, #0xff
    0x0521231C: mov      w11, #1
    0x05212320: b        #0x521234c
    0x05212324: ldr      x13, [x9]
    0x05212328: ldr      x14, [x20]
    0x0521232C: ldr      w13, [x13, x8, lsl #2]
    0x05212330: str      w13, [x14, w12, uxtw]
    0x05212334: ldrh     w12, [x20, #0xa]
    0x05212338: add      w12, w12, #4
    0x0521233C: strh     w12, [x20, #0xa]
    0x05212340: add      x8, x8, #1
    0x05212344: cmp      x10, x8
    0x05212348: b.eq     #0x5212370
    0x0521234C: ldr      w12, [x20, #0xc]
    0x05212350: cbnz     w12, #0x5212340
    0x05212354: ldrh     w12, [x20, #0xa]
    0x05212358: ldrh     w13, [x20, #8]
    0x0521235C: add      w14, w12, #4
    0x05212360: cmp      w14, w13
    0x05212364: b.ls     #0x5212324
    0x05212368: str      w11, [x20, #0xc]
    0x0521236C: b        #0x5212340
    0x05212370: ldr      w8, [x20, #0xc]
    0x05212374: cbnz     w8, #0x52123b8
    0x05212378: ldrh     w8, [x20, #0xa]
    0x0521237C: ldrh     w9, [x20, #8]
    0x05212380: add      w10, w8, #4

  Struct field reads:
    [ldr] offset 0x02 (4B) @ 0x0521232C
    [ldrh] offset 0x08 (2B) @ 0x052122C0
    [ldrh] offset 0x0A (2B) @ 0x052122BC
    [ldr] offset 0x0C (4B) @ 0x052122AC
    [ldr] offset 0x38 (4B) @ 0x0521239C

  Function calls:
    0x052123D4: bl #0x5c6dbc0
    0x052123E0: bl #0x5c6dba0

============================================================
  CMSG_ITEM_USE
  Symbol: _ZN13CMSG_ITEM_USE8packDataER8CIStream
  Address: 0x050C0720, Size: 272
============================================================

  Disassembly (68 insns):
    0x050C0720: ldr      x8, [x1]
    0x050C0724: cbz      x8, #0x50c0788
    0x050C0728: ldr      w9, [x1, #0xc]
    0x050C072C: cbnz     w9, #0x50c076c
    0x050C0730: ldrh     w9, [x1, #0xa]
    0x050C0734: ldrh     w10, [x1, #8]
    0x050C0738: add      w11, w9, #2
    0x050C073C: cmp      w11, w10
    0x050C0740: b.ls     #0x50c0750
    0x050C0744: mov      w9, #1
    0x050C0748: str      w9, [x1, #0xc]
    0x050C074C: b        #0x50c076c
    0x050C0750: ldrh     w10, [x0]
    0x050C0754: strh     w10, [x8, w9, uxtw]
    0x050C0758: ldrh     w9, [x1, #0xa]
    0x050C075C: ldr      w10, [x1, #0xc]
    0x050C0760: add      w9, w9, #2
    0x050C0764: strh     w9, [x1, #0xa]
    0x050C0768: cbz      w10, #0x50c0794
    0x050C076C: ldr      x10, [x1]
    0x050C0770: cbz      x10, #0x50c0780
    0x050C0774: ldrh     w9, [x1, #0xa]
    0x050C0778: strh     w9, [x10]
    0x050C077C: b        #0x50c0784
    0x050C0780: mov      w9, wzr
    0x050C0784: strh     w9, [x0]
    0x050C0788: cmp      x8, #0
    0x050C078C: cset     w0, ne
    0x050C0790: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x050C0734
    [ldrh] offset 0x0A (2B) @ 0x050C0730
    [ldr] offset 0x0C (4B) @ 0x050C0728

============================================================
  CMSG_RECEIVE_REWARD_REQUEST
  Symbol: _ZN27CMSG_RECEIVE_REWARD_REQUEST8packDataER8CIStream
  Address: 0x0505E99C, Size: 216
============================================================

  Disassembly (54 insns):
    0x0505E99C: ldr      x8, [x1]
    0x0505E9A0: cbz      x8, #0x505ea04
    0x0505E9A4: ldr      w9, [x1, #0xc]
    0x0505E9A8: cbnz     w9, #0x505e9e8
    0x0505E9AC: ldrh     w9, [x1, #0xa]
    0x0505E9B0: ldrh     w10, [x1, #8]
    0x0505E9B4: add      w11, w9, #2
    0x0505E9B8: cmp      w11, w10
    0x0505E9BC: b.ls     #0x505e9cc
    0x0505E9C0: mov      w9, #1
    0x0505E9C4: str      w9, [x1, #0xc]
    0x0505E9C8: b        #0x505e9e8
    0x0505E9CC: ldrh     w10, [x0]
    0x0505E9D0: strh     w10, [x8, w9, uxtw]
    0x0505E9D4: ldrh     w9, [x1, #0xa]
    0x0505E9D8: ldr      w10, [x1, #0xc]
    0x0505E9DC: add      w9, w9, #2
    0x0505E9E0: strh     w9, [x1, #0xa]
    0x0505E9E4: cbz      w10, #0x505ea10
    0x0505E9E8: ldr      x10, [x1]
    0x0505E9EC: cbz      x10, #0x505e9fc
    0x0505E9F0: ldrh     w9, [x1, #0xa]
    0x0505E9F4: strh     w9, [x10]
    0x0505E9F8: b        #0x505ea00
    0x0505E9FC: mov      w9, wzr
    0x0505EA00: strh     w9, [x0]
    0x0505EA04: cmp      x8, #0
    0x0505EA08: cset     w0, ne
    0x0505EA0C: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x0505E9B0
    [ldrh] offset 0x0A (2B) @ 0x0505E9AC
    [ldr] offset 0x0C (4B) @ 0x0505E9A4

============================================================
  CMSG_RECEIVE_REWARD_BATCH_REQUEST
  Symbol: _ZN33CMSG_RECEIVE_REWARD_BATCH_REQUEST8packDataER8CIStream
  Address: 0x0505ECC4, Size: 216
============================================================

  Disassembly (54 insns):
    0x0505ECC4: ldr      x8, [x1]
    0x0505ECC8: cbz      x8, #0x505ed2c
    0x0505ECCC: ldr      w9, [x1, #0xc]
    0x0505ECD0: cbnz     w9, #0x505ed10
    0x0505ECD4: ldrh     w9, [x1, #0xa]
    0x0505ECD8: ldrh     w10, [x1, #8]
    0x0505ECDC: add      w11, w9, #2
    0x0505ECE0: cmp      w11, w10
    0x0505ECE4: b.ls     #0x505ecf4
    0x0505ECE8: mov      w9, #1
    0x0505ECEC: str      w9, [x1, #0xc]
    0x0505ECF0: b        #0x505ed10
    0x0505ECF4: ldrh     w10, [x0]
    0x0505ECF8: strh     w10, [x8, w9, uxtw]
    0x0505ECFC: ldrh     w9, [x1, #0xa]
    0x0505ED00: ldr      w10, [x1, #0xc]
    0x0505ED04: add      w9, w9, #2
    0x0505ED08: strh     w9, [x1, #0xa]
    0x0505ED0C: cbz      w10, #0x505ed38
    0x0505ED10: ldr      x10, [x1]
    0x0505ED14: cbz      x10, #0x505ed24
    0x0505ED18: ldrh     w9, [x1, #0xa]
    0x0505ED1C: strh     w9, [x10]
    0x0505ED20: b        #0x505ed28
    0x0505ED24: mov      w9, wzr
    0x0505ED28: strh     w9, [x0]
    0x0505ED2C: cmp      x8, #0
    0x0505ED30: cset     w0, ne
    0x0505ED34: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x0505ECD8
    [ldrh] offset 0x0A (2B) @ 0x0505ECD4
    [ldr] offset 0x0C (4B) @ 0x0505ECCC

============================================================
  CMSG_RECEIVE_SIGN_ACTIVITY
  Symbol: _ZN26CMSG_RECEIVE_SIGN_ACTIVITY8packDataER8CIStream
  Address: 0x0505CC20, Size: 180
============================================================

  Disassembly (45 insns):
    0x0505CC20: ldr      x8, [x1]
    0x0505CC24: cbz      x8, #0x505ccc8
    0x0505CC28: ldr      w9, [x1, #0xc]
    0x0505CC2C: cbnz     w9, #0x505cc74
    0x0505CC30: ldrh     w9, [x1, #0xa]
    0x0505CC34: ldrh     w10, [x1, #8]
    0x0505CC38: add      w11, w9, #2
    0x0505CC3C: cmp      w11, w10
    0x0505CC40: b.ls     #0x505cc58
    0x0505CC44: mov      w9, #1
    0x0505CC48: str      w9, [x1, #0xc]
    0x0505CC4C: ldr      x10, [x1]
    0x0505CC50: cbnz     x10, #0x505cc7c
    0x0505CC54: b        #0x505ccc0
    0x0505CC58: ldrh     w10, [x0]
    0x0505CC5C: strh     w10, [x8, w9, uxtw]
    0x0505CC60: ldrh     w9, [x1, #0xa]
    0x0505CC64: ldr      w10, [x1, #0xc]
    0x0505CC68: add      w9, w9, #2
    0x0505CC6C: strh     w9, [x1, #0xa]
    0x0505CC70: cbz      w10, #0x505cc88
    0x0505CC74: ldr      x10, [x1]
    0x0505CC78: cbz      x10, #0x505ccc0
    0x0505CC7C: ldrh     w9, [x1, #0xa]
    0x0505CC80: strh     w9, [x10]
    0x0505CC84: b        #0x505ccc4
    0x0505CC88: and      w10, w9, #0xffff
    0x0505CC8C: ldrh     w11, [x1, #8]
    0x0505CC90: add      w10, w10, #2
    0x0505CC94: cmp      w10, w11
    0x0505CC98: b.hi     #0x505cc44
    0x0505CC9C: ldr      x10, [x1]
    0x0505CCA0: ldrh     w11, [x0, #2]
    0x0505CCA4: and      x9, x9, #0xffff
    0x0505CCA8: strh     w11, [x10, x9]
    0x0505CCAC: ldrh     w9, [x1, #0xa]
    0x0505CCB0: add      w9, w9, #2
    0x0505CCB4: strh     w9, [x1, #0xa]
    0x0505CCB8: ldr      x10, [x1]
    0x0505CCBC: cbnz     x10, #0x505cc7c
    0x0505CCC0: mov      w9, wzr
    0x0505CCC4: strh     w9, [x0]
    0x0505CCC8: cmp      x8, #0
    0x0505CCCC: cset     w0, ne
    0x0505CCD0: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x0505CCA0
    [ldrh] offset 0x08 (2B) @ 0x0505CC34
    [ldrh] offset 0x0A (2B) @ 0x0505CC30
    [ldr] offset 0x0C (4B) @ 0x0505CC28

============================================================
  CMSG_SIGN_REQUEST
  Symbol: _ZN17CMSG_SIGN_REQUEST8packDataER8CIStream
  Address: 0x052C382C, Size: 180
============================================================

  Disassembly (45 insns):
    0x052C382C: ldr      x8, [x1]
    0x052C3830: cbz      x8, #0x52c38d4
    0x052C3834: ldr      w9, [x1, #0xc]
    0x052C3838: cbnz     w9, #0x52c3880
    0x052C383C: ldrh     w9, [x1, #0xa]
    0x052C3840: ldrh     w10, [x1, #8]
    0x052C3844: add      w11, w9, #2
    0x052C3848: cmp      w11, w10
    0x052C384C: b.ls     #0x52c3864
    0x052C3850: mov      w9, #1
    0x052C3854: str      w9, [x1, #0xc]
    0x052C3858: ldr      x10, [x1]
    0x052C385C: cbnz     x10, #0x52c3888
    0x052C3860: b        #0x52c38cc
    0x052C3864: ldrh     w10, [x0]
    0x052C3868: strh     w10, [x8, w9, uxtw]
    0x052C386C: ldrh     w9, [x1, #0xa]
    0x052C3870: ldr      w10, [x1, #0xc]
    0x052C3874: add      w9, w9, #2
    0x052C3878: strh     w9, [x1, #0xa]
    0x052C387C: cbz      w10, #0x52c3894
    0x052C3880: ldr      x10, [x1]
    0x052C3884: cbz      x10, #0x52c38cc
    0x052C3888: ldrh     w9, [x1, #0xa]
    0x052C388C: strh     w9, [x10]
    0x052C3890: b        #0x52c38d0
    0x052C3894: and      w10, w9, #0xffff
    0x052C3898: ldrh     w11, [x1, #8]
    0x052C389C: add      w10, w10, #2
    0x052C38A0: cmp      w10, w11
    0x052C38A4: b.hi     #0x52c3850
    0x052C38A8: ldr      x10, [x1]
    0x052C38AC: ldrh     w11, [x0, #2]
    0x052C38B0: and      x9, x9, #0xffff
    0x052C38B4: strh     w11, [x10, x9]
    0x052C38B8: ldrh     w9, [x1, #0xa]
    0x052C38BC: add      w9, w9, #2
    0x052C38C0: strh     w9, [x1, #0xa]
    0x052C38C4: ldr      x10, [x1]
    0x052C38C8: cbnz     x10, #0x52c3888
    0x052C38CC: mov      w9, wzr
    0x052C38D0: strh     w9, [x0]
    0x052C38D4: cmp      x8, #0
    0x052C38D8: cset     w0, ne
    0x052C38DC: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x052C38AC
    [ldrh] offset 0x08 (2B) @ 0x052C3840
    [ldrh] offset 0x0A (2B) @ 0x052C383C
    [ldr] offset 0x0C (4B) @ 0x052C3834

============================================================
  CMSG_DAY_REFRESH_REQUEST
  Symbol: _ZN24CMSG_DAY_REFRESH_REQUEST8packDataER8CIStream
  Address: 0x052C2E24, Size: 180
============================================================

  Disassembly (45 insns):
    0x052C2E24: ldr      x8, [x1]
    0x052C2E28: cbz      x8, #0x52c2ecc
    0x052C2E2C: ldr      w9, [x1, #0xc]
    0x052C2E30: cbnz     w9, #0x52c2e78
    0x052C2E34: ldrh     w9, [x1, #0xa]
    0x052C2E38: ldrh     w10, [x1, #8]
    0x052C2E3C: add      w11, w9, #2
    0x052C2E40: cmp      w11, w10
    0x052C2E44: b.ls     #0x52c2e5c
    0x052C2E48: mov      w9, #1
    0x052C2E4C: str      w9, [x1, #0xc]
    0x052C2E50: ldr      x10, [x1]
    0x052C2E54: cbnz     x10, #0x52c2e80
    0x052C2E58: b        #0x52c2ec4
    0x052C2E5C: ldrh     w10, [x0]
    0x052C2E60: strh     w10, [x8, w9, uxtw]
    0x052C2E64: ldrh     w9, [x1, #0xa]
    0x052C2E68: ldr      w10, [x1, #0xc]
    0x052C2E6C: add      w9, w9, #2
    0x052C2E70: strh     w9, [x1, #0xa]
    0x052C2E74: cbz      w10, #0x52c2e8c
    0x052C2E78: ldr      x10, [x1]
    0x052C2E7C: cbz      x10, #0x52c2ec4
    0x052C2E80: ldrh     w9, [x1, #0xa]
    0x052C2E84: strh     w9, [x10]
    0x052C2E88: b        #0x52c2ec8
    0x052C2E8C: and      w10, w9, #0xffff
    0x052C2E90: ldrh     w11, [x1, #8]
    0x052C2E94: add      w10, w10, #2
    0x052C2E98: cmp      w10, w11
    0x052C2E9C: b.hi     #0x52c2e48
    0x052C2EA0: ldr      x10, [x1]
    0x052C2EA4: ldrh     w11, [x0, #2]
    0x052C2EA8: and      x9, x9, #0xffff
    0x052C2EAC: strh     w11, [x10, x9]
    0x052C2EB0: ldrh     w9, [x1, #0xa]
    0x052C2EB4: add      w9, w9, #2
    0x052C2EB8: strh     w9, [x1, #0xa]
    0x052C2EBC: ldr      x10, [x1]
    0x052C2EC0: cbnz     x10, #0x52c2e80
    0x052C2EC4: mov      w9, wzr
    0x052C2EC8: strh     w9, [x0]
    0x052C2ECC: cmp      x8, #0
    0x052C2ED0: cset     w0, ne
    0x052C2ED4: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x052C2EA4
    [ldrh] offset 0x08 (2B) @ 0x052C2E38
    [ldrh] offset 0x0A (2B) @ 0x052C2E34
    [ldr] offset 0x0C (4B) @ 0x052C2E2C

============================================================
  CMSG_NEW_ONLINE_REWARD_REQUEST
  Symbol: _ZN30CMSG_NEW_ONLINE_REWARD_REQUEST8packDataER8CIStream
  Address: 0x052C3B4C, Size: 180
============================================================

  Disassembly (45 insns):
    0x052C3B4C: ldr      x8, [x1]
    0x052C3B50: cbz      x8, #0x52c3bf4
    0x052C3B54: ldr      w9, [x1, #0xc]
    0x052C3B58: cbnz     w9, #0x52c3ba0
    0x052C3B5C: ldrh     w9, [x1, #0xa]
    0x052C3B60: ldrh     w10, [x1, #8]
    0x052C3B64: add      w11, w9, #2
    0x052C3B68: cmp      w11, w10
    0x052C3B6C: b.ls     #0x52c3b84
    0x052C3B70: mov      w9, #1
    0x052C3B74: str      w9, [x1, #0xc]
    0x052C3B78: ldr      x10, [x1]
    0x052C3B7C: cbnz     x10, #0x52c3ba8
    0x052C3B80: b        #0x52c3bec
    0x052C3B84: ldrh     w10, [x0]
    0x052C3B88: strh     w10, [x8, w9, uxtw]
    0x052C3B8C: ldrh     w9, [x1, #0xa]
    0x052C3B90: ldr      w10, [x1, #0xc]
    0x052C3B94: add      w9, w9, #2
    0x052C3B98: strh     w9, [x1, #0xa]
    0x052C3B9C: cbz      w10, #0x52c3bb4
    0x052C3BA0: ldr      x10, [x1]
    0x052C3BA4: cbz      x10, #0x52c3bec
    0x052C3BA8: ldrh     w9, [x1, #0xa]
    0x052C3BAC: strh     w9, [x10]
    0x052C3BB0: b        #0x52c3bf0
    0x052C3BB4: and      w10, w9, #0xffff
    0x052C3BB8: ldrh     w11, [x1, #8]
    0x052C3BBC: add      w10, w10, #2
    0x052C3BC0: cmp      w10, w11
    0x052C3BC4: b.hi     #0x52c3b70
    0x052C3BC8: ldr      x10, [x1]
    0x052C3BCC: ldrh     w11, [x0, #2]
    0x052C3BD0: and      x9, x9, #0xffff
    0x052C3BD4: strh     w11, [x10, x9]
    0x052C3BD8: ldrh     w9, [x1, #0xa]
    0x052C3BDC: add      w9, w9, #2
    0x052C3BE0: strh     w9, [x1, #0xa]
    0x052C3BE4: ldr      x10, [x1]
    0x052C3BE8: cbnz     x10, #0x52c3ba8
    0x052C3BEC: mov      w9, wzr
    0x052C3BF0: strh     w9, [x0]
    0x052C3BF4: cmp      x8, #0
    0x052C3BF8: cset     w0, ne
    0x052C3BFC: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x052C3BCC
    [ldrh] offset 0x08 (2B) @ 0x052C3B60
    [ldrh] offset 0x0A (2B) @ 0x052C3B5C
    [ldr] offset 0x0C (4B) @ 0x052C3B54

============================================================
  CMSG_ACTIVEGIFTS_ACTION_REQUEST
  Symbol: _ZN31CMSG_ACTIVEGIFTS_ACTION_REQUEST8packDataER8CIStream
  Address: 0x04FA0950, Size: 220
============================================================

  Disassembly (55 insns):
    0x04FA0950: ldr      x8, [x1]
    0x04FA0954: cbz      x8, #0x4fa09b8
    0x04FA0958: ldr      w9, [x1, #0xc]
    0x04FA095C: cbnz     w9, #0x4fa099c
    0x04FA0960: ldrh     w9, [x1, #0xa]
    0x04FA0964: ldrh     w10, [x1, #8]
    0x04FA0968: add      w11, w9, #2
    0x04FA096C: cmp      w11, w10
    0x04FA0970: b.ls     #0x4fa0980
    0x04FA0974: mov      w9, #1
    0x04FA0978: str      w9, [x1, #0xc]
    0x04FA097C: b        #0x4fa099c
    0x04FA0980: ldrh     w10, [x0]
    0x04FA0984: strh     w10, [x8, w9, uxtw]
    0x04FA0988: ldrh     w9, [x1, #0xa]
    0x04FA098C: ldr      w10, [x1, #0xc]
    0x04FA0990: add      w9, w9, #2
    0x04FA0994: strh     w9, [x1, #0xa]
    0x04FA0998: cbz      w10, #0x4fa09c4
    0x04FA099C: ldr      x10, [x1]
    0x04FA09A0: cbz      x10, #0x4fa09b0
    0x04FA09A4: ldrh     w9, [x1, #0xa]
    0x04FA09A8: strh     w9, [x10]
    0x04FA09AC: b        #0x4fa09b4
    0x04FA09B0: mov      w9, wzr
    0x04FA09B4: strh     w9, [x0]
    0x04FA09B8: cmp      x8, #0
    0x04FA09BC: cset     w0, ne
    0x04FA09C0: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x04FA0964
    [ldrh] offset 0x0A (2B) @ 0x04FA0960
    [ldr] offset 0x0C (4B) @ 0x04FA0958

============================================================
  CMSG_CITY_BUFF_USE
  Symbol: _ZN18CMSG_CITY_BUFF_USE8packDataER8CIStream
  Address: 0x0527C1BC, Size: 320
============================================================

  Disassembly (80 insns):
    0x0527C1BC: ldr      x8, [x1]
    0x0527C1C0: cbz      x8, #0x527c224
    0x0527C1C4: ldr      w9, [x1, #0xc]
    0x0527C1C8: cbnz     w9, #0x527c208
    0x0527C1CC: ldrh     w9, [x1, #0xa]
    0x0527C1D0: ldrh     w10, [x1, #8]
    0x0527C1D4: add      w11, w9, #2
    0x0527C1D8: cmp      w11, w10
    0x0527C1DC: b.ls     #0x527c1ec
    0x0527C1E0: mov      w9, #1
    0x0527C1E4: str      w9, [x1, #0xc]
    0x0527C1E8: b        #0x527c208
    0x0527C1EC: ldrh     w10, [x0]
    0x0527C1F0: strh     w10, [x8, w9, uxtw]
    0x0527C1F4: ldrh     w9, [x1, #0xa]
    0x0527C1F8: ldr      w10, [x1, #0xc]
    0x0527C1FC: add      w9, w9, #2
    0x0527C200: strh     w9, [x1, #0xa]
    0x0527C204: cbz      w10, #0x527c230
    0x0527C208: ldr      x10, [x1]
    0x0527C20C: cbz      x10, #0x527c21c
    0x0527C210: ldrh     w9, [x1, #0xa]
    0x0527C214: strh     w9, [x10]
    0x0527C218: b        #0x527c220
    0x0527C21C: mov      w9, wzr
    0x0527C220: strh     w9, [x0]
    0x0527C224: cmp      x8, #0
    0x0527C228: cset     w0, ne
    0x0527C22C: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x0527C1D0
    [ldrh] offset 0x0A (2B) @ 0x0527C1CC
    [ldr] offset 0x0C (4B) @ 0x0527C1C4

============================================================
  CMSG_CITY_BUFF_GET_USE
  Symbol: _ZN22CMSG_CITY_BUFF_GET_USE8packDataER8CIStream
  Address: 0x0527C380, Size: 320
============================================================

  Disassembly (80 insns):
    0x0527C380: ldr      x8, [x1]
    0x0527C384: cbz      x8, #0x527c3e8
    0x0527C388: ldr      w9, [x1, #0xc]
    0x0527C38C: cbnz     w9, #0x527c3cc
    0x0527C390: ldrh     w9, [x1, #0xa]
    0x0527C394: ldrh     w10, [x1, #8]
    0x0527C398: add      w11, w9, #2
    0x0527C39C: cmp      w11, w10
    0x0527C3A0: b.ls     #0x527c3b0
    0x0527C3A4: mov      w9, #1
    0x0527C3A8: str      w9, [x1, #0xc]
    0x0527C3AC: b        #0x527c3cc
    0x0527C3B0: ldrh     w10, [x0]
    0x0527C3B4: strh     w10, [x8, w9, uxtw]
    0x0527C3B8: ldrh     w9, [x1, #0xa]
    0x0527C3BC: ldr      w10, [x1, #0xc]
    0x0527C3C0: add      w9, w9, #2
    0x0527C3C4: strh     w9, [x1, #0xa]
    0x0527C3C8: cbz      w10, #0x527c3f4
    0x0527C3CC: ldr      x10, [x1]
    0x0527C3D0: cbz      x10, #0x527c3e0
    0x0527C3D4: ldrh     w9, [x1, #0xa]
    0x0527C3D8: strh     w9, [x10]
    0x0527C3DC: b        #0x527c3e4
    0x0527C3E0: mov      w9, wzr
    0x0527C3E4: strh     w9, [x0]
    0x0527C3E8: cmp      x8, #0
    0x0527C3EC: cset     w0, ne
    0x0527C3F0: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x0527C394
    [ldrh] offset 0x0A (2B) @ 0x0527C390
    [ldr] offset 0x0C (4B) @ 0x0527C388

============================================================
  CMSG_LUCKY_SHOP_SCRATCH_CARD
  Symbol: _ZN28CMSG_LUCKY_SHOP_SCRATCH_CARD8packDataER8CIStream
  Address: 0x051DE56C, Size: 180
============================================================

  Disassembly (45 insns):
    0x051DE56C: ldr      x8, [x1]
    0x051DE570: cbz      x8, #0x51de614
    0x051DE574: ldr      w9, [x1, #0xc]
    0x051DE578: cbnz     w9, #0x51de5c0
    0x051DE57C: ldrh     w9, [x1, #0xa]
    0x051DE580: ldrh     w10, [x1, #8]
    0x051DE584: add      w11, w9, #2
    0x051DE588: cmp      w11, w10
    0x051DE58C: b.ls     #0x51de5a4
    0x051DE590: mov      w9, #1
    0x051DE594: str      w9, [x1, #0xc]
    0x051DE598: ldr      x10, [x1]
    0x051DE59C: cbnz     x10, #0x51de5c8
    0x051DE5A0: b        #0x51de60c
    0x051DE5A4: ldrh     w10, [x0]
    0x051DE5A8: strh     w10, [x8, w9, uxtw]
    0x051DE5AC: ldrh     w9, [x1, #0xa]
    0x051DE5B0: ldr      w10, [x1, #0xc]
    0x051DE5B4: add      w9, w9, #2
    0x051DE5B8: strh     w9, [x1, #0xa]
    0x051DE5BC: cbz      w10, #0x51de5d4
    0x051DE5C0: ldr      x10, [x1]
    0x051DE5C4: cbz      x10, #0x51de60c
    0x051DE5C8: ldrh     w9, [x1, #0xa]
    0x051DE5CC: strh     w9, [x10]
    0x051DE5D0: b        #0x51de610
    0x051DE5D4: and      w10, w9, #0xffff
    0x051DE5D8: ldrh     w11, [x1, #8]
    0x051DE5DC: add      w10, w10, #2
    0x051DE5E0: cmp      w10, w11
    0x051DE5E4: b.hi     #0x51de590
    0x051DE5E8: ldr      x10, [x1]
    0x051DE5EC: ldrh     w11, [x0, #2]
    0x051DE5F0: and      x9, x9, #0xffff
    0x051DE5F4: strh     w11, [x10, x9]
    0x051DE5F8: ldrh     w9, [x1, #0xa]
    0x051DE5FC: add      w9, w9, #2
    0x051DE600: strh     w9, [x1, #0xa]
    0x051DE604: ldr      x10, [x1]
    0x051DE608: cbnz     x10, #0x51de5c8
    0x051DE60C: mov      w9, wzr
    0x051DE610: strh     w9, [x0]
    0x051DE614: cmp      x8, #0
    0x051DE618: cset     w0, ne
    0x051DE61C: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x051DE5EC
    [ldrh] offset 0x08 (2B) @ 0x051DE580
    [ldrh] offset 0x0A (2B) @ 0x051DE57C
    [ldr] offset 0x0C (4B) @ 0x051DE574

============================================================
  CMSG_RECEIVE_FIRST_BIND_REWARD
  Symbol: _ZN30CMSG_RECEIVE_FIRST_BIND_REWARD8packDataER8CIStream
  Address: 0x052DA374, Size: 180
============================================================

  Disassembly (45 insns):
    0x052DA374: ldr      x8, [x1]
    0x052DA378: cbz      x8, #0x52da41c
    0x052DA37C: ldr      w9, [x1, #0xc]
    0x052DA380: cbnz     w9, #0x52da3c8
    0x052DA384: ldrh     w9, [x1, #0xa]
    0x052DA388: ldrh     w10, [x1, #8]
    0x052DA38C: add      w11, w9, #2
    0x052DA390: cmp      w11, w10
    0x052DA394: b.ls     #0x52da3ac
    0x052DA398: mov      w9, #1
    0x052DA39C: str      w9, [x1, #0xc]
    0x052DA3A0: ldr      x10, [x1]
    0x052DA3A4: cbnz     x10, #0x52da3d0
    0x052DA3A8: b        #0x52da414
    0x052DA3AC: ldrh     w10, [x0]
    0x052DA3B0: strh     w10, [x8, w9, uxtw]
    0x052DA3B4: ldrh     w9, [x1, #0xa]
    0x052DA3B8: ldr      w10, [x1, #0xc]
    0x052DA3BC: add      w9, w9, #2
    0x052DA3C0: strh     w9, [x1, #0xa]
    0x052DA3C4: cbz      w10, #0x52da3dc
    0x052DA3C8: ldr      x10, [x1]
    0x052DA3CC: cbz      x10, #0x52da414
    0x052DA3D0: ldrh     w9, [x1, #0xa]
    0x052DA3D4: strh     w9, [x10]
    0x052DA3D8: b        #0x52da418
    0x052DA3DC: and      w10, w9, #0xffff
    0x052DA3E0: ldrh     w11, [x1, #8]
    0x052DA3E4: add      w10, w10, #2
    0x052DA3E8: cmp      w10, w11
    0x052DA3EC: b.hi     #0x52da398
    0x052DA3F0: ldr      x10, [x1]
    0x052DA3F4: ldrh     w11, [x0, #2]
    0x052DA3F8: and      x9, x9, #0xffff
    0x052DA3FC: strh     w11, [x10, x9]
    0x052DA400: ldrh     w9, [x1, #0xa]
    0x052DA404: add      w9, w9, #2
    0x052DA408: strh     w9, [x1, #0xa]
    0x052DA40C: ldr      x10, [x1]
    0x052DA410: cbnz     x10, #0x52da3d0
    0x052DA414: mov      w9, wzr
    0x052DA418: strh     w9, [x0]
    0x052DA41C: cmp      x8, #0
    0x052DA420: cset     w0, ne
    0x052DA424: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x052DA3F4
    [ldrh] offset 0x08 (2B) @ 0x052DA388
    [ldrh] offset 0x0A (2B) @ 0x052DA384
    [ldr] offset 0x0C (4B) @ 0x052DA37C

============================================================
  CMSG_RECEIVE_FIRST_BIND_REWARD
  Symbol: _ZN30CMSG_RECEIVE_FIRST_BIND_REWARD8packDataER8CIStream
  Address: 0xB4610000B45B, Size: 198380244481128
============================================================
  Invalid address, skipping

============================================================
  CMSG_RECEIVE_FIRST_BIND_REWARD
  Symbol: N30CMSG_RECEIVE_FIRST_BIND_REWARD8packDataER8CIStream
  Address: 0xA7CF00000000, Size: 697919300698112
============================================================
  Invalid address, skipping

============================================================
  CMSG_RECEIVE_FIRST_BIND_REWARD
  Symbol: 0CMSG_RECEIVE_FIRST_BIND_REWARD8packDataER8CIStream
  Address: 0x0000FBF0, Size: 0
============================================================

  Disassembly (2 insns):
    0x0000FBF0: udf      #0xf
    0x0000FBF4: udf      #0

============================================================
  CMSG_DESERT_TRADE_START_MARCH_REQUEST
  Symbol: _ZN37CMSG_DESERT_TRADE_START_MARCH_REQUEST8packDataER8CIStream
  Address: 0x0502E374, Size: 944
============================================================

  Disassembly (236 insns):
    0x0502E374: stp      x29, x30, [sp, #-0x30]!
    0x0502E378: str      x21, [sp, #0x10]
    0x0502E37C: stp      x20, x19, [sp, #0x20]
    0x0502E380: mov      x29, sp
    0x0502E384: ldr      x21, [x1]
    0x0502E388: cbz      x21, #0x502e4bc
    0x0502E38C: ldr      w8, [x1, #0xc]
    0x0502E390: mov      x19, x1
    0x0502E394: mov      x20, x0
    0x0502E398: cbnz     w8, #0x502e3e4
    0x0502E39C: ldrh     w8, [x19, #0xa]
    0x0502E3A0: ldrh     w9, [x19, #8]
    0x0502E3A4: add      w10, w8, #2
    0x0502E3A8: cmp      w10, w9
    0x0502E3AC: b.ls     #0x502e3c8
    0x0502E3B0: mov      w8, #1
    0x0502E3B4: str      w8, [x19, #0xc]
    0x0502E3B8: bl       #0x5c6dbd0
    0x0502E3BC: ldr      w8, [x19, #0xc]
    0x0502E3C0: cbnz     w8, #0x502e42c
    0x0502E3C4: b        #0x502e3f0
    0x0502E3C8: ldrh     w9, [x20]
    0x0502E3CC: strh     w9, [x21, w8, uxtw]
    0x0502E3D0: ldrh     w8, [x19, #0xa]
    0x0502E3D4: ldr      w9, [x19, #0xc]
    0x0502E3D8: add      w8, w8, #2
    0x0502E3DC: strh     w8, [x19, #0xa]
    0x0502E3E0: cbz      w9, #0x502e55c
    0x0502E3E4: bl       #0x5c6dbd0
    0x0502E3E8: ldr      w8, [x19, #0xc]
    0x0502E3EC: cbnz     w8, #0x502e42c
    0x0502E3F0: ldrh     w8, [x19, #0xa]
    0x0502E3F4: ldrh     w9, [x19, #8]
    0x0502E3F8: add      w10, w8, #2
    0x0502E3FC: cmp      w10, w9
    0x0502E400: b.ls     #0x502e410
    0x0502E404: mov      w8, #1
    0x0502E408: str      w8, [x19, #0xc]
    0x0502E40C: b        #0x502e42c
    0x0502E410: ldr      x9, [x19]
    0x0502E414: strh     w0, [x9, w8, uxtw]
    0x0502E418: ldrh     w8, [x19, #0xa]
    0x0502E41C: ldr      w9, [x19, #0xc]
    0x0502E420: add      w8, w8, #2
    0x0502E424: strh     w8, [x19, #0xa]
    0x0502E428: cbz      w9, #0x502e59c
    0x0502E42C: bl       #0x5c6dbe0
    0x0502E430: ldr      w8, [x19, #0xc]
    0x0502E434: cbnz     w8, #0x502e474
    0x0502E438: ldrh     w8, [x19, #0xa]
    0x0502E43C: ldrh     w9, [x19, #8]
    0x0502E440: add      w10, w8, #8
    0x0502E444: cmp      w10, w9
    0x0502E448: b.ls     #0x502e458
    0x0502E44C: mov      w8, #1
    0x0502E450: str      w8, [x19, #0xc]
    0x0502E454: b        #0x502e474
    0x0502E458: ldr      x9, [x19]
    0x0502E45C: str      x0, [x9, w8, uxtw]
    0x0502E460: ldrh     w8, [x19, #0xa]

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x0502E3A0
    [ldrh] offset 0x0A (2B) @ 0x0502E39C
    [ldr] offset 0x0C (4B) @ 0x0502E38C
    [ldr] offset 0x10 (8B) @ 0x0502E4C8
    [ldr] offset 0x28 (8B) @ 0x0502E474

  Function calls:
    0x0502E3B8: bl #0x5c6dbd0
    0x0502E3E4: bl #0x5c6dbd0
    0x0502E42C: bl #0x5c6dbe0
    0x0502E49C: bl #0x5c6dbc0
    0x0502E4A8: bl #0x5c6dbb0

============================================================
  CMSG_OUTFIRE_REQUEST
  Symbol: _ZN20CMSG_OUTFIRE_REQUEST8packDataER8CIStream
  Address: 0x0505BE54, Size: 180
============================================================

  Disassembly (45 insns):
    0x0505BE54: ldr      x8, [x1]
    0x0505BE58: cbz      x8, #0x505befc
    0x0505BE5C: ldr      w9, [x1, #0xc]
    0x0505BE60: cbnz     w9, #0x505bea8
    0x0505BE64: ldrh     w9, [x1, #0xa]
    0x0505BE68: ldrh     w10, [x1, #8]
    0x0505BE6C: add      w11, w9, #2
    0x0505BE70: cmp      w11, w10
    0x0505BE74: b.ls     #0x505be8c
    0x0505BE78: mov      w9, #1
    0x0505BE7C: str      w9, [x1, #0xc]
    0x0505BE80: ldr      x10, [x1]
    0x0505BE84: cbnz     x10, #0x505beb0
    0x0505BE88: b        #0x505bef4
    0x0505BE8C: ldrh     w10, [x0]
    0x0505BE90: strh     w10, [x8, w9, uxtw]
    0x0505BE94: ldrh     w9, [x1, #0xa]
    0x0505BE98: ldr      w10, [x1, #0xc]
    0x0505BE9C: add      w9, w9, #2
    0x0505BEA0: strh     w9, [x1, #0xa]
    0x0505BEA4: cbz      w10, #0x505bebc
    0x0505BEA8: ldr      x10, [x1]
    0x0505BEAC: cbz      x10, #0x505bef4
    0x0505BEB0: ldrh     w9, [x1, #0xa]
    0x0505BEB4: strh     w9, [x10]
    0x0505BEB8: b        #0x505bef8
    0x0505BEBC: and      w10, w9, #0xffff
    0x0505BEC0: ldrh     w11, [x1, #8]
    0x0505BEC4: add      w10, w10, #2
    0x0505BEC8: cmp      w10, w11
    0x0505BECC: b.hi     #0x505be78
    0x0505BED0: ldr      x10, [x1]
    0x0505BED4: ldrh     w11, [x0, #2]
    0x0505BED8: and      x9, x9, #0xffff
    0x0505BEDC: strh     w11, [x10, x9]
    0x0505BEE0: ldrh     w9, [x1, #0xa]
    0x0505BEE4: add      w9, w9, #2
    0x0505BEE8: strh     w9, [x1, #0xa]
    0x0505BEEC: ldr      x10, [x1]
    0x0505BEF0: cbnz     x10, #0x505beb0
    0x0505BEF4: mov      w9, wzr
    0x0505BEF8: strh     w9, [x0]
    0x0505BEFC: cmp      x8, #0
    0x0505BF00: cset     w0, ne
    0x0505BF04: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x0505BED4
    [ldrh] offset 0x08 (2B) @ 0x0505BE68
    [ldrh] offset 0x0A (2B) @ 0x0505BE64
    [ldr] offset 0x0C (4B) @ 0x0505BE5C

============================================================
  CMSG_HERO_SOLDIER_RECRUIT_REQUEST
  Symbol: _ZN33CMSG_HERO_SOLDIER_RECRUIT_REQUEST8packDataER8CIStream
  Address: 0x050AF814, Size: 428
============================================================

  Disassembly (107 insns):
    0x050AF814: ldr      x8, [x1]
    0x050AF818: cbz      x8, #0x50af894
    0x050AF81C: ldr      w9, [x1, #0xc]
    0x050AF820: cbnz     w9, #0x50af860
    0x050AF824: ldrh     w9, [x1, #0xa]
    0x050AF828: ldrh     w10, [x1, #8]
    0x050AF82C: add      w11, w9, #2
    0x050AF830: cmp      w11, w10
    0x050AF834: b.ls     #0x50af844
    0x050AF838: mov      w9, #1
    0x050AF83C: str      w9, [x1, #0xc]
    0x050AF840: b        #0x50af860
    0x050AF844: ldrh     w10, [x0]
    0x050AF848: strh     w10, [x8, w9, uxtw]
    0x050AF84C: ldrh     w9, [x1, #0xa]
    0x050AF850: ldr      w10, [x1, #0xc]
    0x050AF854: add      w9, w9, #2
    0x050AF858: strh     w9, [x1, #0xa]
    0x050AF85C: cbz      w10, #0x50af928
    0x050AF860: ldr      x11, [x0, #8]
    0x050AF864: add      x9, x0, #0x10
    0x050AF868: cmp      x11, x9
    0x050AF86C: b.eq     #0x50af878
    0x050AF870: ldr      w10, [x1, #0xc]
    0x050AF874: cbz      w10, #0x50af8a0
    0x050AF878: ldr      x10, [x1]
    0x050AF87C: cbz      x10, #0x50af88c
    0x050AF880: ldrh     w9, [x1, #0xa]
    0x050AF884: strh     w9, [x10]
    0x050AF888: b        #0x50af890
    0x050AF88C: mov      w9, wzr
    0x050AF890: strh     w9, [x0]
    0x050AF894: cmp      x8, #0
    0x050AF898: cset     w0, ne
    0x050AF89C: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x050AF828
    [ldr] offset 0x08 (8B) @ 0x050AF860
    [ldrh] offset 0x0A (2B) @ 0x050AF824
    [ldr] offset 0x0C (4B) @ 0x050AF81C

============================================================
  CMSG_DAMAGE_HELP
  Symbol: _ZN16CMSG_DAMAGE_HELP8packDataER8CIStream
  Address: 0x05028D14, Size: 860
============================================================

  Disassembly (215 insns):
    0x05028D14: stp      x29, x30, [sp, #-0x30]!
    0x05028D18: stp      x22, x21, [sp, #0x10]
    0x05028D1C: stp      x20, x19, [sp, #0x20]
    0x05028D20: mov      x29, sp
    0x05028D24: ldr      x22, [x1]
    0x05028D28: cbz      x22, #0x5028e5c
    0x05028D2C: ldr      w8, [x1, #0xc]
    0x05028D30: mov      x20, x1
    0x05028D34: mov      x19, x0
    0x05028D38: cbnz     w8, #0x5028d84
    0x05028D3C: ldrh     w8, [x20, #0xa]
    0x05028D40: ldrh     w9, [x20, #8]
    0x05028D44: add      w10, w8, #2
    0x05028D48: cmp      w10, w9
    0x05028D4C: b.ls     #0x5028d68
    0x05028D50: mov      w8, #1
    0x05028D54: str      w8, [x20, #0xc]
    0x05028D58: bl       #0x5c6dbd0
    0x05028D5C: ldr      w8, [x20, #0xc]
    0x05028D60: cbnz     w8, #0x5028dcc
    0x05028D64: b        #0x5028d90
    0x05028D68: ldrh     w9, [x19]
    0x05028D6C: strh     w9, [x22, w8, uxtw]
    0x05028D70: ldrh     w8, [x20, #0xa]
    0x05028D74: ldr      w9, [x20, #0xc]
    0x05028D78: add      w8, w8, #2
    0x05028D7C: strh     w8, [x20, #0xa]
    0x05028D80: cbz      w9, #0x5028e74
    0x05028D84: bl       #0x5c6dbd0
    0x05028D88: ldr      w8, [x20, #0xc]
    0x05028D8C: cbnz     w8, #0x5028dcc
    0x05028D90: ldrh     w8, [x20, #0xa]
    0x05028D94: ldrh     w9, [x20, #8]
    0x05028D98: add      w10, w8, #2
    0x05028D9C: cmp      w10, w9
    0x05028DA0: b.ls     #0x5028db0
    0x05028DA4: mov      w8, #1
    0x05028DA8: str      w8, [x20, #0xc]
    0x05028DAC: b        #0x5028dcc
    0x05028DB0: ldr      x9, [x20]
    0x05028DB4: strh     w0, [x9, w8, uxtw]
    0x05028DB8: ldrh     w8, [x20, #0xa]
    0x05028DBC: ldr      w9, [x20, #0xc]
    0x05028DC0: add      w8, w8, #2
    0x05028DC4: strh     w8, [x20, #0xa]
    0x05028DC8: cbz      w9, #0x5028eb4
    0x05028DCC: bl       #0x5c6dbe0
    0x05028DD0: ldr      w8, [x20, #0xc]
    0x05028DD4: cbnz     w8, #0x5028e14
    0x05028DD8: ldrh     w8, [x20, #0xa]
    0x05028DDC: ldrh     w9, [x20, #8]
    0x05028DE0: add      w10, w8, #8
    0x05028DE4: cmp      w10, w9
    0x05028DE8: b.ls     #0x5028df8
    0x05028DEC: mov      w8, #1
    0x05028DF0: str      w8, [x20, #0xc]
    0x05028DF4: b        #0x5028e14
    0x05028DF8: ldr      x9, [x20]
    0x05028DFC: str      x0, [x9, w8, uxtw]
    0x05028E00: ldrh     w8, [x20, #0xa]

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x05028D40
    [ldrh] offset 0x0A (2B) @ 0x05028D3C
    [ldr] offset 0x0C (4B) @ 0x05028D2C

  Function calls:
    0x05028D58: bl #0x5c6dbd0
    0x05028D84: bl #0x5c6dbd0
    0x05028DCC: bl #0x5c6dbe0
    0x05028E30: bl #0x5c6dbc0
    0x05028E3C: bl #0x5c6dbb0

============================================================
  CMSG_DAMAGE_BUY
  Symbol: _ZN20CMSG_DAMAGE_BUY_ITEM8packDataER8CIStream
  Address: 0x050298D4, Size: 760
============================================================

  Disassembly (190 insns):
    0x050298D4: stp      x29, x30, [sp, #-0x30]!
    0x050298D8: stp      x22, x21, [sp, #0x10]
    0x050298DC: stp      x20, x19, [sp, #0x20]
    0x050298E0: mov      x29, sp
    0x050298E4: ldr      x22, [x1]
    0x050298E8: cbz      x22, #0x5029a1c
    0x050298EC: ldr      w8, [x1, #0xc]
    0x050298F0: mov      x20, x1
    0x050298F4: mov      x19, x0
    0x050298F8: cbnz     w8, #0x5029944
    0x050298FC: ldrh     w8, [x20, #0xa]
    0x05029900: ldrh     w9, [x20, #8]
    0x05029904: add      w10, w8, #2
    0x05029908: cmp      w10, w9
    0x0502990C: b.ls     #0x5029928
    0x05029910: mov      w8, #1
    0x05029914: str      w8, [x20, #0xc]
    0x05029918: bl       #0x5c6dbd0
    0x0502991C: ldr      w8, [x20, #0xc]
    0x05029920: cbnz     w8, #0x502998c
    0x05029924: b        #0x5029950
    0x05029928: ldrh     w9, [x19]
    0x0502992C: strh     w9, [x22, w8, uxtw]
    0x05029930: ldrh     w8, [x20, #0xa]
    0x05029934: ldr      w9, [x20, #0xc]
    0x05029938: add      w8, w8, #2
    0x0502993C: strh     w8, [x20, #0xa]
    0x05029940: cbz      w9, #0x5029a34
    0x05029944: bl       #0x5c6dbd0
    0x05029948: ldr      w8, [x20, #0xc]
    0x0502994C: cbnz     w8, #0x502998c
    0x05029950: ldrh     w8, [x20, #0xa]
    0x05029954: ldrh     w9, [x20, #8]
    0x05029958: add      w10, w8, #2
    0x0502995C: cmp      w10, w9
    0x05029960: b.ls     #0x5029970
    0x05029964: mov      w8, #1
    0x05029968: str      w8, [x20, #0xc]
    0x0502996C: b        #0x502998c
    0x05029970: ldr      x9, [x20]
    0x05029974: strh     w0, [x9, w8, uxtw]
    0x05029978: ldrh     w8, [x20, #0xa]
    0x0502997C: ldr      w9, [x20, #0xc]
    0x05029980: add      w8, w8, #2
    0x05029984: strh     w8, [x20, #0xa]
    0x05029988: cbz      w9, #0x5029a74
    0x0502998C: bl       #0x5c6dbe0
    0x05029990: ldr      w8, [x20, #0xc]
    0x05029994: cbnz     w8, #0x50299d4
    0x05029998: ldrh     w8, [x20, #0xa]
    0x0502999C: ldrh     w9, [x20, #8]
    0x050299A0: add      w10, w8, #8
    0x050299A4: cmp      w10, w9
    0x050299A8: b.ls     #0x50299b8
    0x050299AC: mov      w8, #1
    0x050299B0: str      w8, [x20, #0xc]
    0x050299B4: b        #0x50299d4
    0x050299B8: ldr      x9, [x20]
    0x050299BC: str      x0, [x9, w8, uxtw]
    0x050299C0: ldrh     w8, [x20, #0xa]

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x05029900
    [ldrh] offset 0x0A (2B) @ 0x050298FC
    [ldr] offset 0x0C (4B) @ 0x050298EC

  Function calls:
    0x05029918: bl #0x5c6dbd0
    0x05029944: bl #0x5c6dbd0
    0x0502998C: bl #0x5c6dbe0
    0x050299F0: bl #0x5c6dbc0
    0x050299FC: bl #0x5c6dbb0

============================================================
  CMSG_DAMAGE_BUY
  Symbol: _ZN15CMSG_DAMAGE_BUY8packDataER8CIStream
  Address: 0x05029400, Size: 668
============================================================

  Disassembly (167 insns):
    0x05029400: stp      x29, x30, [sp, #-0x30]!
    0x05029404: stp      x22, x21, [sp, #0x10]
    0x05029408: stp      x20, x19, [sp, #0x20]
    0x0502940C: mov      x29, sp
    0x05029410: ldr      x22, [x1]
    0x05029414: cbz      x22, #0x5029684
    0x05029418: ldr      w8, [x1, #0xc]
    0x0502941C: mov      x20, x1
    0x05029420: mov      x19, x0
    0x05029424: cbnz     w8, #0x5029470
    0x05029428: ldrh     w8, [x20, #0xa]
    0x0502942C: ldrh     w9, [x20, #8]
    0x05029430: add      w10, w8, #2
    0x05029434: cmp      w10, w9
    0x05029438: b.ls     #0x5029454
    0x0502943C: mov      w8, #1
    0x05029440: str      w8, [x20, #0xc]
    0x05029444: bl       #0x5c6dbd0
    0x05029448: ldr      w8, [x20, #0xc]
    0x0502944C: cbnz     w8, #0x50294b8
    0x05029450: b        #0x502947c
    0x05029454: ldrh     w9, [x19]
    0x05029458: strh     w9, [x22, w8, uxtw]
    0x0502945C: ldrh     w8, [x20, #0xa]
    0x05029460: ldr      w9, [x20, #0xc]
    0x05029464: add      w8, w8, #2
    0x05029468: strh     w8, [x20, #0xa]
    0x0502946C: cbz      w9, #0x502951c
    0x05029470: bl       #0x5c6dbd0
    0x05029474: ldr      w8, [x20, #0xc]
    0x05029478: cbnz     w8, #0x50294b8
    0x0502947C: ldrh     w8, [x20, #0xa]
    0x05029480: ldrh     w9, [x20, #8]
    0x05029484: add      w10, w8, #2
    0x05029488: cmp      w10, w9
    0x0502948C: b.ls     #0x502949c
    0x05029490: mov      w8, #1
    0x05029494: str      w8, [x20, #0xc]
    0x05029498: b        #0x50294b8
    0x0502949C: ldr      x9, [x20]
    0x050294A0: strh     w0, [x9, w8, uxtw]
    0x050294A4: ldrh     w8, [x20, #0xa]
    0x050294A8: ldr      w9, [x20, #0xc]
    0x050294AC: add      w8, w8, #2
    0x050294B0: strh     w8, [x20, #0xa]
    0x050294B4: cbz      w9, #0x502955c
    0x050294B8: bl       #0x5c6dbe0
    0x050294BC: ldr      w8, [x20, #0xc]
    0x050294C0: cbnz     w8, #0x5029508
    0x050294C4: ldrh     w8, [x20, #0xa]
    0x050294C8: ldrh     w9, [x20, #8]
    0x050294CC: add      w10, w8, #8
    0x050294D0: cmp      w10, w9
    0x050294D4: b.ls     #0x50294ec
    0x050294D8: mov      w8, #1
    0x050294DC: str      w8, [x20, #0xc]
    0x050294E0: ldr      x21, [x20]
    0x050294E4: cbnz     x21, #0x5029510
    0x050294E8: b        #0x5029650
    0x050294EC: ldr      x9, [x20]

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x05029534
    [ldrb] offset 0x06 (1B) @ 0x0502956C
    [ldrb] offset 0x07 (1B) @ 0x050295A0
    [ldrh] offset 0x08 (2B) @ 0x0502942C
    [ldrb] offset 0x08 (1B) @ 0x050295D0
    [ldrb] offset 0x09 (1B) @ 0x05029600
    [ldrh] offset 0x0A (2B) @ 0x05029428
    [ldr] offset 0x0C (4B) @ 0x05029418
    [ldr] offset 0x18 (4B) @ 0x05029630

  Function calls:
    0x05029444: bl #0x5c6dbd0
    0x05029470: bl #0x5c6dbd0
    0x050294B8: bl #0x5c6dbe0
    0x0502954C: bl #0x5c6dbd0
    0x05029658: bl #0x5c6dbc0
    0x05029664: bl #0x5c6dbb0

============================================================
  CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST
  Symbol: _ZN39CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST8packDataER8CIStream
  Address: 0x052861FC, Size: 220
============================================================

  Disassembly (55 insns):
    0x052861FC: ldr      x8, [x1]
    0x05286200: cbz      x8, #0x5286264
    0x05286204: ldr      w9, [x1, #0xc]
    0x05286208: cbnz     w9, #0x5286248
    0x0528620C: ldrh     w9, [x1, #0xa]
    0x05286210: ldrh     w10, [x1, #8]
    0x05286214: add      w11, w9, #2
    0x05286218: cmp      w11, w10
    0x0528621C: b.ls     #0x528622c
    0x05286220: mov      w9, #1
    0x05286224: str      w9, [x1, #0xc]
    0x05286228: b        #0x5286248
    0x0528622C: ldrh     w10, [x0]
    0x05286230: strh     w10, [x8, w9, uxtw]
    0x05286234: ldrh     w9, [x1, #0xa]
    0x05286238: ldr      w10, [x1, #0xc]
    0x0528623C: add      w9, w9, #2
    0x05286240: strh     w9, [x1, #0xa]
    0x05286244: cbz      w10, #0x5286270
    0x05286248: ldr      x10, [x1]
    0x0528624C: cbz      x10, #0x528625c
    0x05286250: ldrh     w9, [x1, #0xa]
    0x05286254: strh     w9, [x10]
    0x05286258: b        #0x5286260
    0x0528625C: mov      w9, wzr
    0x05286260: strh     w9, [x0]
    0x05286264: cmp      x8, #0
    0x05286268: cset     w0, ne
    0x0528626C: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x05286210
    [ldrh] offset 0x0A (2B) @ 0x0528620C
    [ldr] offset 0x0C (4B) @ 0x05286204

============================================================
  CMSG_CONTINUITY_GIFTPACK_ACTION_REQUEST
  Symbol: _ZN39CMSG_CONTINUITY_GIFTPACK_ACTION_REQUEST8packDataER8CIStream
  Address: 0x0500F814, Size: 220
============================================================

  Disassembly (55 insns):
    0x0500F814: ldr      x8, [x1]
    0x0500F818: cbz      x8, #0x500f87c
    0x0500F81C: ldr      w9, [x1, #0xc]
    0x0500F820: cbnz     w9, #0x500f860
    0x0500F824: ldrh     w9, [x1, #0xa]
    0x0500F828: ldrh     w10, [x1, #8]
    0x0500F82C: add      w11, w9, #2
    0x0500F830: cmp      w11, w10
    0x0500F834: b.ls     #0x500f844
    0x0500F838: mov      w9, #1
    0x0500F83C: str      w9, [x1, #0xc]
    0x0500F840: b        #0x500f860
    0x0500F844: ldrh     w10, [x0]
    0x0500F848: strh     w10, [x8, w9, uxtw]
    0x0500F84C: ldrh     w9, [x1, #0xa]
    0x0500F850: ldr      w10, [x1, #0xc]
    0x0500F854: add      w9, w9, #2
    0x0500F858: strh     w9, [x1, #0xa]
    0x0500F85C: cbz      w10, #0x500f888
    0x0500F860: ldr      x10, [x1]
    0x0500F864: cbz      x10, #0x500f874
    0x0500F868: ldrh     w9, [x1, #0xa]
    0x0500F86C: strh     w9, [x10]
    0x0500F870: b        #0x500f878
    0x0500F874: mov      w9, wzr
    0x0500F878: strh     w9, [x0]
    0x0500F87C: cmp      x8, #0
    0x0500F880: cset     w0, ne
    0x0500F884: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x0500F828
    [ldrh] offset 0x0A (2B) @ 0x0500F824
    [ldr] offset 0x0C (4B) @ 0x0500F81C

============================================================
  CMSG_RECEIVE_LUXURY_REWARD
  Symbol: _ZN26CMSG_RECEIVE_LUXURY_REWARD8packDataER8CIStream
  Address: 0x051E1B7C, Size: 220
============================================================

  Disassembly (55 insns):
    0x051E1B7C: ldr      x8, [x1]
    0x051E1B80: cbz      x8, #0x51e1be4
    0x051E1B84: ldr      w9, [x1, #0xc]
    0x051E1B88: cbnz     w9, #0x51e1bc8
    0x051E1B8C: ldrh     w9, [x1, #0xa]
    0x051E1B90: ldrh     w10, [x1, #8]
    0x051E1B94: add      w11, w9, #2
    0x051E1B98: cmp      w11, w10
    0x051E1B9C: b.ls     #0x51e1bac
    0x051E1BA0: mov      w9, #1
    0x051E1BA4: str      w9, [x1, #0xc]
    0x051E1BA8: b        #0x51e1bc8
    0x051E1BAC: ldrh     w10, [x0]
    0x051E1BB0: strh     w10, [x8, w9, uxtw]
    0x051E1BB4: ldrh     w9, [x1, #0xa]
    0x051E1BB8: ldr      w10, [x1, #0xc]
    0x051E1BBC: add      w9, w9, #2
    0x051E1BC0: strh     w9, [x1, #0xa]
    0x051E1BC4: cbz      w10, #0x51e1bf0
    0x051E1BC8: ldr      x10, [x1]
    0x051E1BCC: cbz      x10, #0x51e1bdc
    0x051E1BD0: ldrh     w9, [x1, #0xa]
    0x051E1BD4: strh     w9, [x10]
    0x051E1BD8: b        #0x51e1be0
    0x051E1BDC: mov      w9, wzr
    0x051E1BE0: strh     w9, [x0]
    0x051E1BE4: cmp      x8, #0
    0x051E1BE8: cset     w0, ne
    0x051E1BEC: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x051E1B90
    [ldrh] offset 0x0A (2B) @ 0x051E1B8C
    [ldr] offset 0x0C (4B) @ 0x051E1B84

============================================================
  CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST
  Symbol: _ZN40CMSG_RECEIVE_ACCUMULATION_REWARD_REQUEST8packDataER8CIStream
  Address: 0x04F9CFFC, Size: 264
============================================================

  Disassembly (66 insns):
    0x04F9CFFC: ldr      x8, [x1]
    0x04F9D000: cbz      x8, #0x4f9d064
    0x04F9D004: ldr      w9, [x1, #0xc]
    0x04F9D008: cbnz     w9, #0x4f9d048
    0x04F9D00C: ldrh     w9, [x1, #0xa]
    0x04F9D010: ldrh     w10, [x1, #8]
    0x04F9D014: add      w11, w9, #2
    0x04F9D018: cmp      w11, w10
    0x04F9D01C: b.ls     #0x4f9d02c
    0x04F9D020: mov      w9, #1
    0x04F9D024: str      w9, [x1, #0xc]
    0x04F9D028: b        #0x4f9d048
    0x04F9D02C: ldrh     w10, [x0]
    0x04F9D030: strh     w10, [x8, w9, uxtw]
    0x04F9D034: ldrh     w9, [x1, #0xa]
    0x04F9D038: ldr      w10, [x1, #0xc]
    0x04F9D03C: add      w9, w9, #2
    0x04F9D040: strh     w9, [x1, #0xa]
    0x04F9D044: cbz      w10, #0x4f9d070
    0x04F9D048: ldr      x10, [x1]
    0x04F9D04C: cbz      x10, #0x4f9d05c
    0x04F9D050: ldrh     w9, [x1, #0xa]
    0x04F9D054: strh     w9, [x10]
    0x04F9D058: b        #0x4f9d060
    0x04F9D05C: mov      w9, wzr
    0x04F9D060: strh     w9, [x0]
    0x04F9D064: cmp      x8, #0
    0x04F9D068: cset     w0, ne
    0x04F9D06C: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x04F9D010
    [ldrh] offset 0x0A (2B) @ 0x04F9D00C
    [ldr] offset 0x0C (4B) @ 0x04F9D004

============================================================
  CMSG_CAMEL_SHOP_BUY_REQUEST
  Symbol: _ZN27CMSG_CAMEL_SHOP_BUY_REQUEST8packDataER8CIStream
  Address: 0x04FD2164, Size: 324
============================================================

  Disassembly (81 insns):
    0x04FD2164: ldr      x8, [x1]
    0x04FD2168: cbz      x8, #0x4fd21cc
    0x04FD216C: ldr      w9, [x1, #0xc]
    0x04FD2170: cbnz     w9, #0x4fd21b0
    0x04FD2174: ldrh     w9, [x1, #0xa]
    0x04FD2178: ldrh     w10, [x1, #8]
    0x04FD217C: add      w11, w9, #2
    0x04FD2180: cmp      w11, w10
    0x04FD2184: b.ls     #0x4fd2194
    0x04FD2188: mov      w9, #1
    0x04FD218C: str      w9, [x1, #0xc]
    0x04FD2190: b        #0x4fd21b0
    0x04FD2194: ldrh     w10, [x0]
    0x04FD2198: strh     w10, [x8, w9, uxtw]
    0x04FD219C: ldrh     w9, [x1, #0xa]
    0x04FD21A0: ldr      w10, [x1, #0xc]
    0x04FD21A4: add      w9, w9, #2
    0x04FD21A8: strh     w9, [x1, #0xa]
    0x04FD21AC: cbz      w10, #0x4fd21d8
    0x04FD21B0: ldr      x10, [x1]
    0x04FD21B4: cbz      x10, #0x4fd21c4
    0x04FD21B8: ldrh     w9, [x1, #0xa]
    0x04FD21BC: strh     w9, [x10]
    0x04FD21C0: b        #0x4fd21c8
    0x04FD21C4: mov      w9, wzr
    0x04FD21C8: strh     w9, [x0]
    0x04FD21CC: cmp      x8, #0
    0x04FD21D0: cset     w0, ne
    0x04FD21D4: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x04FD2178
    [ldrh] offset 0x0A (2B) @ 0x04FD2174
    [ldr] offset 0x0C (4B) @ 0x04FD216C

============================================================
  CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST
  Symbol: _ZN38CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST8packDataER8CIStream
  Address: 0x05090758, Size: 180
============================================================

  Disassembly (45 insns):
    0x05090758: ldr      x8, [x1]
    0x0509075C: cbz      x8, #0x5090800
    0x05090760: ldr      w9, [x1, #0xc]
    0x05090764: cbnz     w9, #0x50907ac
    0x05090768: ldrh     w9, [x1, #0xa]
    0x0509076C: ldrh     w10, [x1, #8]
    0x05090770: add      w11, w9, #2
    0x05090774: cmp      w11, w10
    0x05090778: b.ls     #0x5090790
    0x0509077C: mov      w9, #1
    0x05090780: str      w9, [x1, #0xc]
    0x05090784: ldr      x10, [x1]
    0x05090788: cbnz     x10, #0x50907b4
    0x0509078C: b        #0x50907f8
    0x05090790: ldrh     w10, [x0]
    0x05090794: strh     w10, [x8, w9, uxtw]
    0x05090798: ldrh     w9, [x1, #0xa]
    0x0509079C: ldr      w10, [x1, #0xc]
    0x050907A0: add      w9, w9, #2
    0x050907A4: strh     w9, [x1, #0xa]
    0x050907A8: cbz      w10, #0x50907c0
    0x050907AC: ldr      x10, [x1]
    0x050907B0: cbz      x10, #0x50907f8
    0x050907B4: ldrh     w9, [x1, #0xa]
    0x050907B8: strh     w9, [x10]
    0x050907BC: b        #0x50907fc
    0x050907C0: and      w10, w9, #0xffff
    0x050907C4: ldrh     w11, [x1, #8]
    0x050907C8: add      w10, w10, #2
    0x050907CC: cmp      w10, w11
    0x050907D0: b.hi     #0x509077c
    0x050907D4: ldr      x10, [x1]
    0x050907D8: ldrh     w11, [x0, #2]
    0x050907DC: and      x9, x9, #0xffff
    0x050907E0: strh     w11, [x10, x9]
    0x050907E4: ldrh     w9, [x1, #0xa]
    0x050907E8: add      w9, w9, #2
    0x050907EC: strh     w9, [x1, #0xa]
    0x050907F0: ldr      x10, [x1]
    0x050907F4: cbnz     x10, #0x50907b4
    0x050907F8: mov      w9, wzr
    0x050907FC: strh     w9, [x0]
    0x05090800: cmp      x8, #0
    0x05090804: cset     w0, ne
    0x05090808: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x050907D8
    [ldrh] offset 0x08 (2B) @ 0x0509076C
    [ldrh] offset 0x0A (2B) @ 0x05090768
    [ldr] offset 0x0C (4B) @ 0x05090760

============================================================
  CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST
  Symbol: _ZN42CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST_NEW8packDataER8CIStream
  Address: 0x0509569C, Size: 180
============================================================

  Disassembly (45 insns):
    0x0509569C: ldr      x8, [x1]
    0x050956A0: cbz      x8, #0x5095744
    0x050956A4: ldr      w9, [x1, #0xc]
    0x050956A8: cbnz     w9, #0x50956f0
    0x050956AC: ldrh     w9, [x1, #0xa]
    0x050956B0: ldrh     w10, [x1, #8]
    0x050956B4: add      w11, w9, #2
    0x050956B8: cmp      w11, w10
    0x050956BC: b.ls     #0x50956d4
    0x050956C0: mov      w9, #1
    0x050956C4: str      w9, [x1, #0xc]
    0x050956C8: ldr      x10, [x1]
    0x050956CC: cbnz     x10, #0x50956f8
    0x050956D0: b        #0x509573c
    0x050956D4: ldrh     w10, [x0]
    0x050956D8: strh     w10, [x8, w9, uxtw]
    0x050956DC: ldrh     w9, [x1, #0xa]
    0x050956E0: ldr      w10, [x1, #0xc]
    0x050956E4: add      w9, w9, #2
    0x050956E8: strh     w9, [x1, #0xa]
    0x050956EC: cbz      w10, #0x5095704
    0x050956F0: ldr      x10, [x1]
    0x050956F4: cbz      x10, #0x509573c
    0x050956F8: ldrh     w9, [x1, #0xa]
    0x050956FC: strh     w9, [x10]
    0x05095700: b        #0x5095740
    0x05095704: and      w10, w9, #0xffff
    0x05095708: ldrh     w11, [x1, #8]
    0x0509570C: add      w10, w10, #2
    0x05095710: cmp      w10, w11
    0x05095714: b.hi     #0x50956c0
    0x05095718: ldr      x10, [x1]
    0x0509571C: ldrh     w11, [x0, #2]
    0x05095720: and      x9, x9, #0xffff
    0x05095724: strh     w11, [x10, x9]
    0x05095728: ldrh     w9, [x1, #0xa]
    0x0509572C: add      w9, w9, #2
    0x05095730: strh     w9, [x1, #0xa]
    0x05095734: ldr      x10, [x1]
    0x05095738: cbnz     x10, #0x50956f8
    0x0509573C: mov      w9, wzr
    0x05095740: strh     w9, [x0]
    0x05095744: cmp      x8, #0
    0x05095748: cset     w0, ne
    0x0509574C: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x0509571C
    [ldrh] offset 0x08 (2B) @ 0x050956B0
    [ldrh] offset 0x0A (2B) @ 0x050956AC
    [ldr] offset 0x0C (4B) @ 0x050956A4

============================================================
  CMSG_MONTH_REFRESH_REQUEST
  Symbol: _ZN26CMSG_MONTH_REFRESH_REQUEST8packDataER8CIStream
  Address: 0x052C2D2C, Size: 180
============================================================

  Disassembly (45 insns):
    0x052C2D2C: ldr      x8, [x1]
    0x052C2D30: cbz      x8, #0x52c2dd4
    0x052C2D34: ldr      w9, [x1, #0xc]
    0x052C2D38: cbnz     w9, #0x52c2d80
    0x052C2D3C: ldrh     w9, [x1, #0xa]
    0x052C2D40: ldrh     w10, [x1, #8]
    0x052C2D44: add      w11, w9, #2
    0x052C2D48: cmp      w11, w10
    0x052C2D4C: b.ls     #0x52c2d64
    0x052C2D50: mov      w9, #1
    0x052C2D54: str      w9, [x1, #0xc]
    0x052C2D58: ldr      x10, [x1]
    0x052C2D5C: cbnz     x10, #0x52c2d88
    0x052C2D60: b        #0x52c2dcc
    0x052C2D64: ldrh     w10, [x0]
    0x052C2D68: strh     w10, [x8, w9, uxtw]
    0x052C2D6C: ldrh     w9, [x1, #0xa]
    0x052C2D70: ldr      w10, [x1, #0xc]
    0x052C2D74: add      w9, w9, #2
    0x052C2D78: strh     w9, [x1, #0xa]
    0x052C2D7C: cbz      w10, #0x52c2d94
    0x052C2D80: ldr      x10, [x1]
    0x052C2D84: cbz      x10, #0x52c2dcc
    0x052C2D88: ldrh     w9, [x1, #0xa]
    0x052C2D8C: strh     w9, [x10]
    0x052C2D90: b        #0x52c2dd0
    0x052C2D94: and      w10, w9, #0xffff
    0x052C2D98: ldrh     w11, [x1, #8]
    0x052C2D9C: add      w10, w10, #2
    0x052C2DA0: cmp      w10, w11
    0x052C2DA4: b.hi     #0x52c2d50
    0x052C2DA8: ldr      x10, [x1]
    0x052C2DAC: ldrh     w11, [x0, #2]
    0x052C2DB0: and      x9, x9, #0xffff
    0x052C2DB4: strh     w11, [x10, x9]
    0x052C2DB8: ldrh     w9, [x1, #0xa]
    0x052C2DBC: add      w9, w9, #2
    0x052C2DC0: strh     w9, [x1, #0xa]
    0x052C2DC4: ldr      x10, [x1]
    0x052C2DC8: cbnz     x10, #0x52c2d88
    0x052C2DCC: mov      w9, wzr
    0x052C2DD0: strh     w9, [x0]
    0x052C2DD4: cmp      x8, #0
    0x052C2DD8: cset     w0, ne
    0x052C2DDC: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x052C2DAC
    [ldrh] offset 0x08 (2B) @ 0x052C2D40
    [ldrh] offset 0x0A (2B) @ 0x052C2D3C
    [ldr] offset 0x0C (4B) @ 0x052C2D34

============================================================
  CMSG_APPEND_SIGN_REQUEST
  Symbol: _ZN24CMSG_APPEND_SIGN_REQUEST8packDataER8CIStream
  Address: 0x052C3924, Size: 180
============================================================

  Disassembly (45 insns):
    0x052C3924: ldr      x8, [x1]
    0x052C3928: cbz      x8, #0x52c39cc
    0x052C392C: ldr      w9, [x1, #0xc]
    0x052C3930: cbnz     w9, #0x52c3978
    0x052C3934: ldrh     w9, [x1, #0xa]
    0x052C3938: ldrh     w10, [x1, #8]
    0x052C393C: add      w11, w9, #2
    0x052C3940: cmp      w11, w10
    0x052C3944: b.ls     #0x52c395c
    0x052C3948: mov      w9, #1
    0x052C394C: str      w9, [x1, #0xc]
    0x052C3950: ldr      x10, [x1]
    0x052C3954: cbnz     x10, #0x52c3980
    0x052C3958: b        #0x52c39c4
    0x052C395C: ldrh     w10, [x0]
    0x052C3960: strh     w10, [x8, w9, uxtw]
    0x052C3964: ldrh     w9, [x1, #0xa]
    0x052C3968: ldr      w10, [x1, #0xc]
    0x052C396C: add      w9, w9, #2
    0x052C3970: strh     w9, [x1, #0xa]
    0x052C3974: cbz      w10, #0x52c398c
    0x052C3978: ldr      x10, [x1]
    0x052C397C: cbz      x10, #0x52c39c4
    0x052C3980: ldrh     w9, [x1, #0xa]
    0x052C3984: strh     w9, [x10]
    0x052C3988: b        #0x52c39c8
    0x052C398C: and      w10, w9, #0xffff
    0x052C3990: ldrh     w11, [x1, #8]
    0x052C3994: add      w10, w10, #2
    0x052C3998: cmp      w10, w11
    0x052C399C: b.hi     #0x52c3948
    0x052C39A0: ldr      x10, [x1]
    0x052C39A4: ldrh     w11, [x0, #2]
    0x052C39A8: and      x9, x9, #0xffff
    0x052C39AC: strh     w11, [x10, x9]
    0x052C39B0: ldrh     w9, [x1, #0xa]
    0x052C39B4: add      w9, w9, #2
    0x052C39B8: strh     w9, [x1, #0xa]
    0x052C39BC: ldr      x10, [x1]
    0x052C39C0: cbnz     x10, #0x52c3980
    0x052C39C4: mov      w9, wzr
    0x052C39C8: strh     w9, [x0]
    0x052C39CC: cmp      x8, #0
    0x052C39D0: cset     w0, ne
    0x052C39D4: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x052C39A4
    [ldrh] offset 0x08 (2B) @ 0x052C3938
    [ldrh] offset 0x0A (2B) @ 0x052C3934
    [ldr] offset 0x0C (4B) @ 0x052C392C

============================================================
  CMSG_ARENA_BUY_TIMES_REQUEST
  Symbol: _ZN28CMSG_ARENA_BUY_TIMES_REQUEST8packDataER8CIStream
  Address: 0x04FAD628, Size: 180
============================================================

  Disassembly (45 insns):
    0x04FAD628: ldr      x8, [x1]
    0x04FAD62C: cbz      x8, #0x4fad6d0
    0x04FAD630: ldr      w9, [x1, #0xc]
    0x04FAD634: cbnz     w9, #0x4fad67c
    0x04FAD638: ldrh     w9, [x1, #0xa]
    0x04FAD63C: ldrh     w10, [x1, #8]
    0x04FAD640: add      w11, w9, #2
    0x04FAD644: cmp      w11, w10
    0x04FAD648: b.ls     #0x4fad660
    0x04FAD64C: mov      w9, #1
    0x04FAD650: str      w9, [x1, #0xc]
    0x04FAD654: ldr      x10, [x1]
    0x04FAD658: cbnz     x10, #0x4fad684
    0x04FAD65C: b        #0x4fad6c8
    0x04FAD660: ldrh     w10, [x0]
    0x04FAD664: strh     w10, [x8, w9, uxtw]
    0x04FAD668: ldrh     w9, [x1, #0xa]
    0x04FAD66C: ldr      w10, [x1, #0xc]
    0x04FAD670: add      w9, w9, #2
    0x04FAD674: strh     w9, [x1, #0xa]
    0x04FAD678: cbz      w10, #0x4fad690
    0x04FAD67C: ldr      x10, [x1]
    0x04FAD680: cbz      x10, #0x4fad6c8
    0x04FAD684: ldrh     w9, [x1, #0xa]
    0x04FAD688: strh     w9, [x10]
    0x04FAD68C: b        #0x4fad6cc
    0x04FAD690: and      w10, w9, #0xffff
    0x04FAD694: ldrh     w11, [x1, #8]
    0x04FAD698: add      w10, w10, #2
    0x04FAD69C: cmp      w10, w11
    0x04FAD6A0: b.hi     #0x4fad64c
    0x04FAD6A4: ldr      x10, [x1]
    0x04FAD6A8: ldrh     w11, [x0, #2]
    0x04FAD6AC: and      x9, x9, #0xffff
    0x04FAD6B0: strh     w11, [x10, x9]
    0x04FAD6B4: ldrh     w9, [x1, #0xa]
    0x04FAD6B8: add      w9, w9, #2
    0x04FAD6BC: strh     w9, [x1, #0xa]
    0x04FAD6C0: ldr      x10, [x1]
    0x04FAD6C4: cbnz     x10, #0x4fad684
    0x04FAD6C8: mov      w9, wzr
    0x04FAD6CC: strh     w9, [x0]
    0x04FAD6D0: cmp      x8, #0
    0x04FAD6D4: cset     w0, ne
    0x04FAD6D8: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x04FAD6A8
    [ldrh] offset 0x08 (2B) @ 0x04FAD63C
    [ldrh] offset 0x0A (2B) @ 0x04FAD638
    [ldr] offset 0x0C (4B) @ 0x04FAD630

============================================================
  CMSG_BUY_MOBILIZATION_TASK_TIMES_REQUEST
  Symbol: _ZN40CMSG_BUY_MOBILIZATION_TASK_TIMES_REQUEST8packDataER8CIStream
  Address: 0x0505B78C, Size: 180
============================================================

  Disassembly (45 insns):
    0x0505B78C: ldr      x8, [x1]
    0x0505B790: cbz      x8, #0x505b834
    0x0505B794: ldr      w9, [x1, #0xc]
    0x0505B798: cbnz     w9, #0x505b7e0
    0x0505B79C: ldrh     w9, [x1, #0xa]
    0x0505B7A0: ldrh     w10, [x1, #8]
    0x0505B7A4: add      w11, w9, #2
    0x0505B7A8: cmp      w11, w10
    0x0505B7AC: b.ls     #0x505b7c4
    0x0505B7B0: mov      w9, #1
    0x0505B7B4: str      w9, [x1, #0xc]
    0x0505B7B8: ldr      x10, [x1]
    0x0505B7BC: cbnz     x10, #0x505b7e8
    0x0505B7C0: b        #0x505b82c
    0x0505B7C4: ldrh     w10, [x0]
    0x0505B7C8: strh     w10, [x8, w9, uxtw]
    0x0505B7CC: ldrh     w9, [x1, #0xa]
    0x0505B7D0: ldr      w10, [x1, #0xc]
    0x0505B7D4: add      w9, w9, #2
    0x0505B7D8: strh     w9, [x1, #0xa]
    0x0505B7DC: cbz      w10, #0x505b7f4
    0x0505B7E0: ldr      x10, [x1]
    0x0505B7E4: cbz      x10, #0x505b82c
    0x0505B7E8: ldrh     w9, [x1, #0xa]
    0x0505B7EC: strh     w9, [x10]
    0x0505B7F0: b        #0x505b830
    0x0505B7F4: and      w10, w9, #0xffff
    0x0505B7F8: ldrh     w11, [x1, #8]
    0x0505B7FC: add      w10, w10, #2
    0x0505B800: cmp      w10, w11
    0x0505B804: b.hi     #0x505b7b0
    0x0505B808: ldr      x10, [x1]
    0x0505B80C: ldrh     w11, [x0, #2]
    0x0505B810: and      x9, x9, #0xffff
    0x0505B814: strh     w11, [x10, x9]
    0x0505B818: ldrh     w9, [x1, #0xa]
    0x0505B81C: add      w9, w9, #2
    0x0505B820: strh     w9, [x1, #0xa]
    0x0505B824: ldr      x10, [x1]
    0x0505B828: cbnz     x10, #0x505b7e8
    0x0505B82C: mov      w9, wzr
    0x0505B830: strh     w9, [x0]
    0x0505B834: cmp      x8, #0
    0x0505B838: cset     w0, ne
    0x0505B83C: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x0505B80C
    [ldrh] offset 0x08 (2B) @ 0x0505B7A0
    [ldrh] offset 0x0A (2B) @ 0x0505B79C
    [ldr] offset 0x0C (4B) @ 0x0505B794

============================================================
  CMSG_POWER_TASK_REWARD_REQUEST
  Symbol: _ZN30CMSG_POWER_TASK_REWARD_REQUEST8packDataER8CIStream
  Address: 0x0528697C, Size: 472
============================================================

  Disassembly (118 insns):
    0x0528697C: ldr      x8, [x1]
    0x05286980: cbz      x8, #0x5286b2c
    0x05286984: ldr      w10, [x1, #0xc]
    0x05286988: cbnz     w10, #0x52869c8
    0x0528698C: ldrh     w9, [x1, #0xa]
    0x05286990: ldrh     w10, [x1, #8]
    0x05286994: add      w11, w9, #2
    0x05286998: cmp      w11, w10
    0x0528699C: b.ls     #0x52869ac
    0x052869A0: mov      w10, #1
    0x052869A4: str      w10, [x1, #0xc]
    0x052869A8: b        #0x52869c8
    0x052869AC: ldrh     w10, [x0]
    0x052869B0: strh     w10, [x8, w9, uxtw]
    0x052869B4: ldrh     w9, [x1, #0xa]
    0x052869B8: ldr      w10, [x1, #0xc]
    0x052869BC: add      w9, w9, #2
    0x052869C0: strh     w9, [x1, #0xa]
    0x052869C4: cbz      w10, #0x5286a84
    0x052869C8: mov      x9, x0
    0x052869CC: ldp      x11, x12, [x9, #0x10]!
    0x052869D0: sub      x11, x12, x11
    0x052869D4: lsr      x11, x11, #2
    0x052869D8: cmp      w11, #0
    0x052869DC: b.le     #0x5286a44
    0x052869E0: cbnz     w10, #0x5286a70
    0x052869E4: mov      x10, xzr
    0x052869E8: and      x11, x11, #0x7fffffff
    0x052869EC: mov      w12, #1
    0x052869F0: b        #0x5286a1c
    0x052869F4: ldr      x14, [x9]
    0x052869F8: ldr      x15, [x1]
    0x052869FC: ldr      w14, [x14, x10, lsl #2]
    0x05286A00: str      w14, [x15, w13, uxtw]
    0x05286A04: ldrh     w13, [x1, #0xa]
    0x05286A08: add      w13, w13, #4
    0x05286A0C: strh     w13, [x1, #0xa]
    0x05286A10: add      x10, x10, #1
    0x05286A14: cmp      x11, x10
    0x05286A18: b.eq     #0x5286a40
    0x05286A1C: ldr      w13, [x1, #0xc]
    0x05286A20: cbnz     w13, #0x5286a10
    0x05286A24: ldrh     w13, [x1, #0xa]
    0x05286A28: ldrh     w14, [x1, #8]
    0x05286A2C: add      w15, w13, #4
    0x05286A30: cmp      w15, w14
    0x05286A34: b.ls     #0x52869f4
    0x05286A38: str      w12, [x1, #0xc]
    0x05286A3C: b        #0x5286a10
    0x05286A40: ldr      w10, [x1, #0xc]
    0x05286A44: cbnz     w10, #0x5286a70
    0x05286A48: ldrh     w9, [x1, #0xa]
    0x05286A4C: ldrh     w10, [x1, #8]
    0x05286A50: cmp      w9, w10
    0x05286A54: b.hs     #0x5286b14
    0x05286A58: ldr      x10, [x1]
    0x05286A5C: ldrb     w11, [x0, #8]
    0x05286A60: strb     w11, [x10, w9, uxtw]
    0x05286A64: ldrh     w9, [x1, #0xa]
    0x05286A68: add      w9, w9, #1

  Struct field reads:
    [ldr] offset 0x02 (4B) @ 0x052869FC
    [ldrh] offset 0x02 (2B) @ 0x05286A9C
    [ldr] offset 0x04 (4B) @ 0x05286AD4
    [ldrh] offset 0x08 (2B) @ 0x05286990
    [ldrb] offset 0x08 (1B) @ 0x05286A5C
    [ldrh] offset 0x0A (2B) @ 0x0528698C
    [ldr] offset 0x0C (4B) @ 0x05286984

============================================================
  CMSG_SERVER_MISSION_RECEIVE_REQUEST
  Symbol: _ZN35CMSG_SERVER_MISSION_RECEIVE_REQUEST8packDataER8CIStream
  Address: 0x0524EBAC, Size: 220
============================================================

  Disassembly (55 insns):
    0x0524EBAC: ldr      x8, [x1]
    0x0524EBB0: cbz      x8, #0x524ec14
    0x0524EBB4: ldr      w9, [x1, #0xc]
    0x0524EBB8: cbnz     w9, #0x524ebf8
    0x0524EBBC: ldrh     w9, [x1, #0xa]
    0x0524EBC0: ldrh     w10, [x1, #8]
    0x0524EBC4: add      w11, w9, #2
    0x0524EBC8: cmp      w11, w10
    0x0524EBCC: b.ls     #0x524ebdc
    0x0524EBD0: mov      w9, #1
    0x0524EBD4: str      w9, [x1, #0xc]
    0x0524EBD8: b        #0x524ebf8
    0x0524EBDC: ldrh     w10, [x0]
    0x0524EBE0: strh     w10, [x8, w9, uxtw]
    0x0524EBE4: ldrh     w9, [x1, #0xa]
    0x0524EBE8: ldr      w10, [x1, #0xc]
    0x0524EBEC: add      w9, w9, #2
    0x0524EBF0: strh     w9, [x1, #0xa]
    0x0524EBF4: cbz      w10, #0x524ec20
    0x0524EBF8: ldr      x10, [x1]
    0x0524EBFC: cbz      x10, #0x524ec0c
    0x0524EC00: ldrh     w9, [x1, #0xa]
    0x0524EC04: strh     w9, [x10]
    0x0524EC08: b        #0x524ec10
    0x0524EC0C: mov      w9, wzr
    0x0524EC10: strh     w9, [x0]
    0x0524EC14: cmp      x8, #0
    0x0524EC18: cset     w0, ne
    0x0524EC1C: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x0524EBC0
    [ldrh] offset 0x0A (2B) @ 0x0524EBBC
    [ldr] offset 0x0C (4B) @ 0x0524EBB4

============================================================
  CMSG_RANDOM_ONLINE_REWARD_REQUEST
  Symbol: _ZN33CMSG_RANDOM_ONLINE_REWARD_REQUEST8packDataER8CIStream
  Address: 0x052C4480, Size: 180
============================================================

  Disassembly (45 insns):
    0x052C4480: ldr      x8, [x1]
    0x052C4484: cbz      x8, #0x52c4528
    0x052C4488: ldr      w9, [x1, #0xc]
    0x052C448C: cbnz     w9, #0x52c44d4
    0x052C4490: ldrh     w9, [x1, #0xa]
    0x052C4494: ldrh     w10, [x1, #8]
    0x052C4498: add      w11, w9, #2
    0x052C449C: cmp      w11, w10
    0x052C44A0: b.ls     #0x52c44b8
    0x052C44A4: mov      w9, #1
    0x052C44A8: str      w9, [x1, #0xc]
    0x052C44AC: ldr      x10, [x1]
    0x052C44B0: cbnz     x10, #0x52c44dc
    0x052C44B4: b        #0x52c4520
    0x052C44B8: ldrh     w10, [x0]
    0x052C44BC: strh     w10, [x8, w9, uxtw]
    0x052C44C0: ldrh     w9, [x1, #0xa]
    0x052C44C4: ldr      w10, [x1, #0xc]
    0x052C44C8: add      w9, w9, #2
    0x052C44CC: strh     w9, [x1, #0xa]
    0x052C44D0: cbz      w10, #0x52c44e8
    0x052C44D4: ldr      x10, [x1]
    0x052C44D8: cbz      x10, #0x52c4520
    0x052C44DC: ldrh     w9, [x1, #0xa]
    0x052C44E0: strh     w9, [x10]
    0x052C44E4: b        #0x52c4524
    0x052C44E8: and      w10, w9, #0xffff
    0x052C44EC: ldrh     w11, [x1, #8]
    0x052C44F0: add      w10, w10, #2
    0x052C44F4: cmp      w10, w11
    0x052C44F8: b.hi     #0x52c44a4
    0x052C44FC: ldr      x10, [x1]
    0x052C4500: ldrh     w11, [x0, #2]
    0x052C4504: and      x9, x9, #0xffff
    0x052C4508: strh     w11, [x10, x9]
    0x052C450C: ldrh     w9, [x1, #0xa]
    0x052C4510: add      w9, w9, #2
    0x052C4514: strh     w9, [x1, #0xa]
    0x052C4518: ldr      x10, [x1]
    0x052C451C: cbnz     x10, #0x52c44dc
    0x052C4520: mov      w9, wzr
    0x052C4524: strh     w9, [x0]
    0x052C4528: cmp      x8, #0
    0x052C452C: cset     w0, ne
    0x052C4530: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x052C4500
    [ldrh] offset 0x08 (2B) @ 0x052C4494
    [ldrh] offset 0x0A (2B) @ 0x052C4490
    [ldr] offset 0x0C (4B) @ 0x052C4488

============================================================
  CMSG_GAIN_REWARD_REQUEST_CHAMPIONSHIP
  Symbol: _ZN37CMSG_GAIN_REWARD_REQUEST_CHAMPIONSHIP8packDataER8CIStream
  Address: 0x04FD4458, Size: 516
============================================================

  Disassembly (129 insns):
    0x04FD4458: ldr      x8, [x1]
    0x04FD445C: cbz      x8, #0x4fd45e4
    0x04FD4460: ldr      w10, [x1, #0xc]
    0x04FD4464: cbnz     w10, #0x4fd44a4
    0x04FD4468: ldrh     w9, [x1, #0xa]
    0x04FD446C: ldrh     w10, [x1, #8]
    0x04FD4470: add      w11, w9, #2
    0x04FD4474: cmp      w11, w10
    0x04FD4478: b.ls     #0x4fd4488
    0x04FD447C: mov      w10, #1
    0x04FD4480: str      w10, [x1, #0xc]
    0x04FD4484: b        #0x4fd44a4
    0x04FD4488: ldrh     w10, [x0]
    0x04FD448C: strh     w10, [x8, w9, uxtw]
    0x04FD4490: ldrh     w9, [x1, #0xa]
    0x04FD4494: ldr      w10, [x1, #0xc]
    0x04FD4498: add      w9, w9, #2
    0x04FD449C: strh     w9, [x1, #0xa]
    0x04FD44A0: cbz      w10, #0x4fd45f0
    0x04FD44A4: ldr      x11, [x0, #8]
    0x04FD44A8: add      x9, x0, #0x10
    0x04FD44AC: cmp      x11, x9
    0x04FD44B0: b.eq     #0x4fd4588
    0x04FD44B4: cbnz     w10, #0x4fd45a8
    0x04FD44B8: mov      w10, #1
    0x04FD44BC: b        #0x4fd44cc
    0x04FD44C0: cmp      x12, x9
    0x04FD44C4: mov      x11, x12
    0x04FD44C8: b.eq     #0x4fd4584
    0x04FD44CC: ldr      w12, [x1, #0xc]
    0x04FD44D0: cbnz     w12, #0x4fd4530
    0x04FD44D4: ldrh     w12, [x1, #0xa]
    0x04FD44D8: ldrh     w13, [x1, #8]
    0x04FD44DC: add      w14, w12, #4
    0x04FD44E0: cmp      w14, w13
    0x04FD44E4: b.ls     #0x4fd44f8
    0x04FD44E8: str      w10, [x1, #0xc]
    0x04FD44EC: ldr      x13, [x11, #8]
    0x04FD44F0: cbnz     x13, #0x4fd4538
    0x04FD44F4: b        #0x4fd456c
    0x04FD44F8: ldr      x13, [x1]
    0x04FD44FC: ldr      w14, [x11, #0x1c]
    0x04FD4500: str      w14, [x13, w12, uxtw]
    0x04FD4504: ldrh     w12, [x1, #0xa]
    0x04FD4508: ldr      w13, [x1, #0xc]
    0x04FD450C: add      w12, w12, #4
    0x04FD4510: strh     w12, [x1, #0xa]
    0x04FD4514: cbnz     w13, #0x4fd4530
    0x04FD4518: and      w13, w12, #0xffff
    0x04FD451C: ldrh     w14, [x1, #8]
    0x04FD4520: add      w13, w13, #4
    0x04FD4524: cmp      w13, w14
    0x04FD4528: b.ls     #0x4fd4548
    0x04FD452C: str      w10, [x1, #0xc]
    0x04FD4530: ldr      x13, [x11, #8]
    0x04FD4534: cbz      x13, #0x4fd456c
    0x04FD4538: mov      x12, x13
    0x04FD453C: ldr      x13, [x13]
    0x04FD4540: cbnz     x13, #0x4fd4538
    0x04FD4544: b        #0x4fd44c0

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x04FD446C
    [ldr] offset 0x08 (8B) @ 0x04FD44A4
    [ldrh] offset 0x0A (2B) @ 0x04FD4468
    [ldr] offset 0x0C (4B) @ 0x04FD4460
    [ldr] offset 0x10 (8B) @ 0x04FD456C
    [ldr] offset 0x1C (4B) @ 0x04FD44FC
    [ldr] offset 0x20 (4B) @ 0x04FD454C

============================================================
  CMSG_MOBILIZATION_GET_REWARD_REQUEST
  Symbol: _ZN36CMSG_MOBILIZATION_GET_REWARD_REQUEST8packDataER8CIStream
  Address: 0x05251E9C, Size: 376
============================================================

  Disassembly (94 insns):
    0x05251E9C: ldr      x8, [x1]
    0x05251EA0: cbz      x8, #0x5251f20
    0x05251EA4: ldr      w9, [x1, #0xc]
    0x05251EA8: cbnz     w9, #0x5251ee8
    0x05251EAC: ldrh     w9, [x1, #0xa]
    0x05251EB0: ldrh     w10, [x1, #8]
    0x05251EB4: add      w11, w9, #2
    0x05251EB8: cmp      w11, w10
    0x05251EBC: b.ls     #0x5251ecc
    0x05251EC0: mov      w9, #1
    0x05251EC4: str      w9, [x1, #0xc]
    0x05251EC8: b        #0x5251ee8
    0x05251ECC: ldrh     w10, [x0]
    0x05251ED0: strh     w10, [x8, w9, uxtw]
    0x05251ED4: ldrh     w9, [x1, #0xa]
    0x05251ED8: ldr      w10, [x1, #0xc]
    0x05251EDC: add      w9, w9, #2
    0x05251EE0: strh     w9, [x1, #0xa]
    0x05251EE4: cbz      w10, #0x5251f98
    0x05251EE8: mov      x9, x0
    0x05251EEC: ldp      x10, x11, [x9, #8]!
    0x05251EF0: sub      x10, x11, x10
    0x05251EF4: tst      x10, #0xffff
    0x05251EF8: b.eq     #0x5251f04
    0x05251EFC: ldr      w11, [x1, #0xc]
    0x05251F00: cbz      w11, #0x5251f2c
    0x05251F04: ldr      x10, [x1]
    0x05251F08: cbz      x10, #0x5251f18
    0x05251F0C: ldrh     w9, [x1, #0xa]
    0x05251F10: strh     w9, [x10]
    0x05251F14: b        #0x5251f1c
    0x05251F18: mov      w9, wzr
    0x05251F1C: strh     w9, [x0]
    0x05251F20: cmp      x8, #0
    0x05251F24: cset     w0, ne
    0x05251F28: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x05251EB0
    [ldrh] offset 0x0A (2B) @ 0x05251EAC
    [ldr] offset 0x0C (4B) @ 0x05251EA4

============================================================
  CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST
  Symbol: _ZN38CMSG_MICROPAYMENT_DAILY_REWARD_REQUEST8packDataER8CIStream
  Address: 0x0505CE48, Size: 180
============================================================

  Disassembly (45 insns):
    0x0505CE48: ldr      x8, [x1]
    0x0505CE4C: cbz      x8, #0x505cef0
    0x0505CE50: ldr      w9, [x1, #0xc]
    0x0505CE54: cbnz     w9, #0x505ce9c
    0x0505CE58: ldrh     w9, [x1, #0xa]
    0x0505CE5C: ldrh     w10, [x1, #8]
    0x0505CE60: add      w11, w9, #2
    0x0505CE64: cmp      w11, w10
    0x0505CE68: b.ls     #0x505ce80
    0x0505CE6C: mov      w9, #1
    0x0505CE70: str      w9, [x1, #0xc]
    0x0505CE74: ldr      x10, [x1]
    0x0505CE78: cbnz     x10, #0x505cea4
    0x0505CE7C: b        #0x505cee8
    0x0505CE80: ldrh     w10, [x0]
    0x0505CE84: strh     w10, [x8, w9, uxtw]
    0x0505CE88: ldrh     w9, [x1, #0xa]
    0x0505CE8C: ldr      w10, [x1, #0xc]
    0x0505CE90: add      w9, w9, #2
    0x0505CE94: strh     w9, [x1, #0xa]
    0x0505CE98: cbz      w10, #0x505ceb0
    0x0505CE9C: ldr      x10, [x1]
    0x0505CEA0: cbz      x10, #0x505cee8
    0x0505CEA4: ldrh     w9, [x1, #0xa]
    0x0505CEA8: strh     w9, [x10]
    0x0505CEAC: b        #0x505ceec
    0x0505CEB0: and      w10, w9, #0xffff
    0x0505CEB4: ldrh     w11, [x1, #8]
    0x0505CEB8: add      w10, w10, #2
    0x0505CEBC: cmp      w10, w11
    0x0505CEC0: b.hi     #0x505ce6c
    0x0505CEC4: ldr      x10, [x1]
    0x0505CEC8: ldrh     w11, [x0, #2]
    0x0505CECC: and      x9, x9, #0xffff
    0x0505CED0: strh     w11, [x10, x9]
    0x0505CED4: ldrh     w9, [x1, #0xa]
    0x0505CED8: add      w9, w9, #2
    0x0505CEDC: strh     w9, [x1, #0xa]
    0x0505CEE0: ldr      x10, [x1]
    0x0505CEE4: cbnz     x10, #0x505cea4
    0x0505CEE8: mov      w9, wzr
    0x0505CEEC: strh     w9, [x0]
    0x0505CEF0: cmp      x8, #0
    0x0505CEF4: cset     w0, ne
    0x0505CEF8: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x0505CEC8
    [ldrh] offset 0x08 (2B) @ 0x0505CE5C
    [ldrh] offset 0x0A (2B) @ 0x0505CE58
    [ldr] offset 0x0C (4B) @ 0x0505CE50

============================================================
  CMSG_TEAM_RECHARGE_QUICK_REWARD_REQUEST
  Symbol: _ZN39CMSG_TEAM_RECHARGE_QUICK_REWARD_REQUEST8packDataER8CIStream
  Address: 0x052DF0EC, Size: 600
============================================================

  Disassembly (150 insns):
    0x052DF0EC: stp      x29, x30, [sp, #-0x30]!
    0x052DF0F0: stp      x22, x21, [sp, #0x10]
    0x052DF0F4: stp      x20, x19, [sp, #0x20]
    0x052DF0F8: mov      x29, sp
    0x052DF0FC: ldr      x22, [x1]
    0x052DF100: cbz      x22, #0x52df230
    0x052DF104: ldr      w8, [x1, #0xc]
    0x052DF108: mov      x20, x1
    0x052DF10C: mov      x19, x0
    0x052DF110: cbnz     w8, #0x52df15c
    0x052DF114: ldrh     w8, [x20, #0xa]
    0x052DF118: ldrh     w9, [x20, #8]
    0x052DF11C: add      w10, w8, #2
    0x052DF120: cmp      w10, w9
    0x052DF124: b.ls     #0x52df140
    0x052DF128: mov      w8, #1
    0x052DF12C: str      w8, [x20, #0xc]
    0x052DF130: bl       #0x5c6dbd0
    0x052DF134: ldr      w8, [x20, #0xc]
    0x052DF138: cbnz     w8, #0x52df1a4
    0x052DF13C: b        #0x52df168
    0x052DF140: ldrh     w9, [x19]
    0x052DF144: strh     w9, [x22, w8, uxtw]
    0x052DF148: ldrh     w8, [x20, #0xa]
    0x052DF14C: ldr      w9, [x20, #0xc]
    0x052DF150: add      w8, w8, #2
    0x052DF154: strh     w8, [x20, #0xa]
    0x052DF158: cbz      w9, #0x52df248
    0x052DF15C: bl       #0x5c6dbd0
    0x052DF160: ldr      w8, [x20, #0xc]
    0x052DF164: cbnz     w8, #0x52df1a4
    0x052DF168: ldrh     w8, [x20, #0xa]
    0x052DF16C: ldrh     w9, [x20, #8]
    0x052DF170: add      w10, w8, #2
    0x052DF174: cmp      w10, w9
    0x052DF178: b.ls     #0x52df188
    0x052DF17C: mov      w8, #1
    0x052DF180: str      w8, [x20, #0xc]
    0x052DF184: b        #0x52df1a4
    0x052DF188: ldr      x9, [x20]
    0x052DF18C: strh     w0, [x9, w8, uxtw]
    0x052DF190: ldrh     w8, [x20, #0xa]
    0x052DF194: ldr      w9, [x20, #0xc]
    0x052DF198: add      w8, w8, #2
    0x052DF19C: strh     w8, [x20, #0xa]
    0x052DF1A0: cbz      w9, #0x52df288
    0x052DF1A4: bl       #0x5c6dbe0
    0x052DF1A8: ldr      w8, [x20, #0xc]
    0x052DF1AC: cbnz     w8, #0x52df1cc
    0x052DF1B0: ldrh     w8, [x20, #0xa]
    0x052DF1B4: ldrh     w9, [x20, #8]
    0x052DF1B8: add      w10, w8, #8
    0x052DF1BC: cmp      w10, w9
    0x052DF1C0: b.ls     #0x52df1e0
    0x052DF1C4: mov      w8, #1
    0x052DF1C8: str      w8, [x20, #0xc]
    0x052DF1CC: ldr      x21, [x20]
    0x052DF1D0: cbz      x21, #0x52df1fc
    0x052DF1D4: ldrh     w8, [x20, #0xa]
    0x052DF1D8: strh     w8, [x21]

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x052DF118
    [ldrh] offset 0x0A (2B) @ 0x052DF114
    [ldr] offset 0x0C (4B) @ 0x052DF104

  Function calls:
    0x052DF130: bl #0x5c6dbd0
    0x052DF15C: bl #0x5c6dbd0
    0x052DF1A4: bl #0x5c6dbe0
    0x052DF204: bl #0x5c6dbc0
    0x052DF210: bl #0x5c6dbb0

============================================================
  CMSG_WHEEL_REWARD_REQUEST
  Symbol: _ZN25CMSG_WHEEL_REWARD_REQUEST8packDataER8CIStream
  Address: 0x052F2A58, Size: 272
============================================================

  Disassembly (68 insns):
    0x052F2A58: ldr      x8, [x1]
    0x052F2A5C: cbz      x8, #0x52f2ac0
    0x052F2A60: ldr      w9, [x1, #0xc]
    0x052F2A64: cbnz     w9, #0x52f2aa4
    0x052F2A68: ldrh     w9, [x1, #0xa]
    0x052F2A6C: ldrh     w10, [x1, #8]
    0x052F2A70: add      w11, w9, #2
    0x052F2A74: cmp      w11, w10
    0x052F2A78: b.ls     #0x52f2a88
    0x052F2A7C: mov      w9, #1
    0x052F2A80: str      w9, [x1, #0xc]
    0x052F2A84: b        #0x52f2aa4
    0x052F2A88: ldrh     w10, [x0]
    0x052F2A8C: strh     w10, [x8, w9, uxtw]
    0x052F2A90: ldrh     w9, [x1, #0xa]
    0x052F2A94: ldr      w10, [x1, #0xc]
    0x052F2A98: add      w9, w9, #2
    0x052F2A9C: strh     w9, [x1, #0xa]
    0x052F2AA0: cbz      w10, #0x52f2acc
    0x052F2AA4: ldr      x10, [x1]
    0x052F2AA8: cbz      x10, #0x52f2ab8
    0x052F2AAC: ldrh     w9, [x1, #0xa]
    0x052F2AB0: strh     w9, [x10]
    0x052F2AB4: b        #0x52f2abc
    0x052F2AB8: mov      w9, wzr
    0x052F2ABC: strh     w9, [x0]
    0x052F2AC0: cmp      x8, #0
    0x052F2AC4: cset     w0, ne
    0x052F2AC8: ret      

  Struct field reads:
    [ldrh] offset 0x08 (2B) @ 0x052F2A6C
    [ldrh] offset 0x0A (2B) @ 0x052F2A68
    [ldr] offset 0x0C (4B) @ 0x052F2A60

============================================================
  CMSG_PASSWORD_CHECK_REQUEST - NOT FOUND in .dynsym

============================================================
  CMSG_EXPEDITION_INFO_REQUEST
  Symbol: _ZN28CMSG_EXPEDITION_INFO_REQUEST8packDataER8CIStream
  Address: 0x0523D958, Size: 180
============================================================

  Disassembly (45 insns):
    0x0523D958: ldr      x8, [x1]
    0x0523D95C: cbz      x8, #0x523da00
    0x0523D960: ldr      w9, [x1, #0xc]
    0x0523D964: cbnz     w9, #0x523d9ac
    0x0523D968: ldrh     w9, [x1, #0xa]
    0x0523D96C: ldrh     w10, [x1, #8]
    0x0523D970: add      w11, w9, #2
    0x0523D974: cmp      w11, w10
    0x0523D978: b.ls     #0x523d990
    0x0523D97C: mov      w9, #1
    0x0523D980: str      w9, [x1, #0xc]
    0x0523D984: ldr      x10, [x1]
    0x0523D988: cbnz     x10, #0x523d9b4
    0x0523D98C: b        #0x523d9f8
    0x0523D990: ldrh     w10, [x0]
    0x0523D994: strh     w10, [x8, w9, uxtw]
    0x0523D998: ldrh     w9, [x1, #0xa]
    0x0523D99C: ldr      w10, [x1, #0xc]
    0x0523D9A0: add      w9, w9, #2
    0x0523D9A4: strh     w9, [x1, #0xa]
    0x0523D9A8: cbz      w10, #0x523d9c0
    0x0523D9AC: ldr      x10, [x1]
    0x0523D9B0: cbz      x10, #0x523d9f8
    0x0523D9B4: ldrh     w9, [x1, #0xa]
    0x0523D9B8: strh     w9, [x10]
    0x0523D9BC: b        #0x523d9fc
    0x0523D9C0: and      w10, w9, #0xffff
    0x0523D9C4: ldrh     w11, [x1, #8]
    0x0523D9C8: add      w10, w10, #2
    0x0523D9CC: cmp      w10, w11
    0x0523D9D0: b.hi     #0x523d97c
    0x0523D9D4: ldr      x10, [x1]
    0x0523D9D8: ldrh     w11, [x0, #2]
    0x0523D9DC: and      x9, x9, #0xffff
    0x0523D9E0: strh     w11, [x10, x9]
    0x0523D9E4: ldrh     w9, [x1, #0xa]
    0x0523D9E8: add      w9, w9, #2
    0x0523D9EC: strh     w9, [x1, #0xa]
    0x0523D9F0: ldr      x10, [x1]
    0x0523D9F4: cbnz     x10, #0x523d9b4
    0x0523D9F8: mov      w9, wzr
    0x0523D9FC: strh     w9, [x0]
    0x0523DA00: cmp      x8, #0
    0x0523DA04: cset     w0, ne
    0x0523DA08: ret      

  Struct field reads:
    [ldrh] offset 0x02 (2B) @ 0x0523D9D8
    [ldrh] offset 0x08 (2B) @ 0x0523D96C
    [ldrh] offset 0x0A (2B) @ 0x0523D968
    [ldr] offset 0x0C (4B) @ 0x0523D960