# Deep Constructor & Vulnerability Analysis

# PART 1: Key Constructor Disassembly

## 0x0038 - CMSG_EXTRA_ATTRIBUTE_INFO (init data)
Constructor: 0x0505D838

### Disassembly
```asm
  0x0505D838: mov        w8, #0x380000
  0x0505D83C: str        xzr, [x0, #0x18]
  0x0505D840: str        w8, [x0]
  0x0505D844: mov        x8, x0
  0x0505D848: str        xzr, [x8, #0x10]!
  0x0505D84C: str        x8, [x0, #8]
  0x0505D850: ret        
  0x0505D854: ldr        x8, [x1]
  0x0505D858: cbz        x8, #0x505d8d4
  0x0505D85C: ldr        w9, [x1, #0xc]
  0x0505D860: cbnz       w9, #0x505d8a0
  0x0505D864: ldrh       w9, [x1, #0xa]
  0x0505D868: ldrh       w10, [x1, #8]
  0x0505D86C: add        w11, w9, #2
  0x0505D870: cmp        w11, w10
  0x0505D874: b.ls       #0x505d884
  0x0505D878: mov        w9, #1
  0x0505D87C: str        w9, [x1, #0xc]
  0x0505D880: b          #0x505d8a0
  0x0505D884: ldrh       w10, [x0]
  0x0505D888: strh       w10, [x8, w9, uxtw]
  0x0505D88C: ldrh       w9, [x1, #0xa]
  0x0505D890: ldr        w10, [x1, #0xc]
  0x0505D894: add        w9, w9, #2
  0x0505D898: strh       w9, [x1, #0xa]
  0x0505D89C: cbz        w10, #0x505d9b0
  0x0505D8A0: ldr        x11, [x0, #8]
  0x0505D8A4: add        x9, x0, #0x10
  0x0505D8A8: cmp        x11, x9
  0x0505D8AC: b.eq       #0x505d8b8
  0x0505D8B0: ldr        w10, [x1, #0xc]
  0x0505D8B4: cbz        w10, #0x505d8e0
  0x0505D8B8: ldr        x10, [x1]
  0x0505D8BC: cbz        x10, #0x505d8cc
  0x0505D8C0: ldrh       w9, [x1, #0xa]
  0x0505D8C4: strh       w9, [x10]
  0x0505D8C8: b          #0x505d8d0
  0x0505D8CC: mov        w9, wzr
  0x0505D8D0: strh       w9, [x0]
  0x0505D8D4: cmp        x8, #0
  0x0505D8D8: cset       w0, ne
  0x0505D8DC: ret        
  0x0505D8E0: mov        w13, wzr
  0x0505D8E4: mov        w10, #1
  0x0505D8E8: cbnz       wzr, #0x505d948
  0x0505D8EC: ldrh       w12, [x1, #0xa]
  0x0505D8F0: ldrh       w13, [x1, #8]
  0x0505D8F4: add        w14, w12, #4
  0x0505D8F8: cmp        w14, w13
  0x0505D8FC: b.ls       #0x505d910
  0x0505D900: str        w10, [x1, #0xc]
  0x0505D904: ldr        x13, [x11, #8]
  0x0505D908: cbnz       x13, #0x505d950
  0x0505D90C: b          #0x505d984
  0x0505D910: ldr        x13, [x1]
  0x0505D914: ldr        w14, [x11, #0x20]
  0x0505D918: str        w14, [x13, w12, uxtw]
  0x0505D91C: ldrh       w12, [x1, #0xa]
  0x0505D920: ldr        w13, [x1, #0xc]
  0x0505D924: add        w12, w12, #4
  0x0505D928: strh       w12, [x1, #0xa]
  0x0505D92C: cbnz       w13, #0x505d948
  0x0505D930: and        w13, w12, #0xffff
  0x0505D934: ldrh       w14, [x1, #8]
  0x0505D938: add        w13, w13, #8
  0x0505D93C: cmp        w13, w14
  0x0505D940: b.ls       #0x505d960
  0x0505D944: str        w10, [x1, #0xc]
  0x0505D948: ldr        x13, [x11, #8]
  0x0505D94C: cbz        x13, #0x505d984
  0x0505D950: mov        x12, x13
  0x0505D954: ldr        x13, [x13]
  0x0505D958: cbnz       x13, #0x505d950
  0x0505D95C: b          #0x505d998
  0x0505D960: ldr        x13, [x1]
  0x0505D964: ldr        x14, [x11, #0x28]
  0x0505D968: and        x12, x12, #0xffff
  0x0505D96C: str        x14, [x13, x12]
  0x0505D970: ldrh       w12, [x1, #0xa]
  0x0505D974: add        w12, w12, #8
  0x0505D978: strh       w12, [x1, #0xa]
  0x0505D97C: ldr        x13, [x11, #8]
  0x0505D980: cbnz       x13, #0x505d950
  0x0505D984: ldr        x12, [x11, #0x10]
  0x0505D988: ldr        x13, [x12]
  0x0505D98C: cmp        x13, x11
  0x0505D990: mov        x11, x12
  0x0505D994: b.ne       #0x505d984
  0x0505D998: cmp        x12, x9
  0x0505D99C: b.eq       #0x505d8b8
  0x0505D9A0: ldr        w13, [x1, #0xc]
  0x0505D9A4: mov        x11, x12
  0x0505D9A8: cbnz       w13, #0x505d948
  0x0505D9AC: b          #0x505d8ec
  0x0505D9B0: and        w10, w9, #0xffff
  0x0505D9B4: ldrh       w11, [x1, #8]
  0x0505D9B8: add        w10, w10, #2
  0x0505D9BC: cmp        w10, w11
  0x0505D9C0: b.hi       #0x505d878
  0x0505D9C4: ldr        x10, [x1]
  0x0505D9C8: ldrh       w11, [x0, #2]
  0x0505D9CC: and        x9, x9, #0xffff
  0x0505D9D0: strh       w11, [x10, x9]
  0x0505D9D4: ldrh       w9, [x1, #0xa]
  0x0505D9D8: ldr        w10, [x1, #0xc]
  0x0505D9DC: add        w9, w9, #2
  0x0505D9E0: strh       w9, [x1, #0xa]
  0x0505D9E4: cbnz       w10, #0x505d8a0
  0x0505D9E8: ldrh       w9, [x1, #0xa]
  0x0505D9EC: ldrh       w10, [x1, #8]
  0x0505D9F0: add        w11, w9, #2
  0x0505D9F4: cmp        w11, w10
  0x0505D9F8: b.hi       #0x505d878
  0x0505D9FC: ldr        x10, [x1]
  0x0505DA00: ldrh       w11, [x0, #0x18]
  0x0505DA04: strh       w11, [x10, w9, uxtw]
  0x0505DA08: ldrh       w9, [x1, #0xa]
  0x0505DA0C: add        w9, w9, #2
  0x0505DA10: strh       w9, [x1, #0xa]
  0x0505DA14: b          #0x505d8a0
  0x0505DA18: cbz        x1, #0x505da60
  0x0505DA1C: sub        sp, sp, #0x80
  0x0505DA20: stp        x29, x30, [sp, #0x20]
  0x0505DA24: stp        x28, x27, [sp, #0x30]
  0x0505DA28: stp        x26, x25, [sp, #0x40]
  0x0505DA2C: stp        x24, x23, [sp, #0x50]
  0x0505DA30: stp        x22, x21, [sp, #0x60]
  0x0505DA34: stp        x20, x19, [sp, #0x70]
  0x0505DA38: add        x29, sp, #0x20
  0x0505DA3C: ldrh       w9, [x1]
  0x0505DA40: mov        x20, x0
  0x0505DA44: str        x1, [sp, #8]
  0x0505DA48: cmp        w9, #2
  0x0505DA4C: stur       w9, [x29, #-0xc]
  0x0505DA50: b.hs       #0x505da68
  0x0505DA54: stur       xzr, [x29, #-8]
  0x0505DA58: mov        w23, wzr
  0x0505DA5C: b          #0x505daa0
  0x0505DA60: mov        w0, wzr
  0x0505DA64: ret        
  0x0505DA68: ldrh       w8, [x1]
  0x0505DA6C: cmp        w9, #4
  0x0505DA70: strh       w8, [x20]
  0x0505DA74: b.hs       #0x505da84
  0x0505DA78: mov        w23, wzr
  0x0505DA7C: mov        w8, #2
  0x0505DA80: b          #0x505da9c
  0x0505DA84: ldrh       w8, [x1, #2]
  0x0505DA88: cmp        w9, #6
  0x0505DA8C: strh       w8, [x20, #2]
```

### Analysis
**Immediate values (potential field sizes/IDs):**
  - 0x0505DA7C: w8 = 2 (0x2)
  - 0x0505DA98: w8 = 4 (0x4)
  - 0x0505DB1C: w0 = 48 (0x30)
**Function calls:** 2
  - 0x0505DAB4: bl #0x32f61ec
  - 0x0505DB24: bl #0x5bdc440
**Store instructions:** 39

## 0x0042 - CMSG_KEEP_LIVE_TEST (heartbeat)
Constructor: 0x0527CA48

### Disassembly
```asm
  0x0527CA48: mov        w8, #0x420000
  0x0527CA4C: str        w8, [x0]
  0x0527CA50: ret        
  0x0527CA54: ldr        x8, [x1]
  0x0527CA58: cbz        x8, #0x527cabc
  0x0527CA5C: ldr        w9, [x1, #0xc]
  0x0527CA60: cbnz       w9, #0x527caa0
  0x0527CA64: ldrh       w9, [x1, #0xa]
  0x0527CA68: ldrh       w10, [x1, #8]
  0x0527CA6C: add        w11, w9, #2
  0x0527CA70: cmp        w11, w10
  0x0527CA74: b.ls       #0x527ca84
  0x0527CA78: mov        w9, #1
  0x0527CA7C: str        w9, [x1, #0xc]
  0x0527CA80: b          #0x527caa0
  0x0527CA84: ldrh       w10, [x0]
  0x0527CA88: strh       w10, [x8, w9, uxtw]
  0x0527CA8C: ldrh       w9, [x1, #0xa]
  0x0527CA90: ldr        w10, [x1, #0xc]
  0x0527CA94: add        w9, w9, #2
  0x0527CA98: strh       w9, [x1, #0xa]
  0x0527CA9C: cbz        w10, #0x527cac8
  0x0527CAA0: ldr        x10, [x1]
  0x0527CAA4: cbz        x10, #0x527cab4
  0x0527CAA8: ldrh       w9, [x1, #0xa]
  0x0527CAAC: strh       w9, [x10]
  0x0527CAB0: b          #0x527cab8
  0x0527CAB4: mov        w9, wzr
  0x0527CAB8: strh       w9, [x0]
  0x0527CABC: cmp        x8, #0
  0x0527CAC0: cset       w0, ne
  0x0527CAC4: ret        
  0x0527CAC8: and        w10, w9, #0xffff
  0x0527CACC: ldrh       w11, [x1, #8]
  0x0527CAD0: add        w10, w10, #2
  0x0527CAD4: cmp        w10, w11
  0x0527CAD8: b.hi       #0x527ca78
  0x0527CADC: ldr        x10, [x1]
  0x0527CAE0: ldrh       w11, [x0, #2]
  0x0527CAE4: and        x9, x9, #0xffff
  0x0527CAE8: strh       w11, [x10, x9]
  0x0527CAEC: ldrh       w9, [x1, #0xa]
  0x0527CAF0: ldr        w10, [x1, #0xc]
  0x0527CAF4: add        w9, w9, #2
  0x0527CAF8: strh       w9, [x1, #0xa]
  0x0527CAFC: cbnz       w10, #0x527caa0
  0x0527CB00: ldrh       w9, [x1, #0xa]
  0x0527CB04: ldrh       w10, [x1, #8]
  0x0527CB08: add        w11, w9, #8
  0x0527CB0C: cmp        w11, w10
  0x0527CB10: b.hi       #0x527ca78
  0x0527CB14: ldr        x10, [x1]
  0x0527CB18: ldr        x11, [x0, #8]
  0x0527CB1C: str        x11, [x10, w9, uxtw]
  0x0527CB20: ldrh       w9, [x1, #0xa]
  0x0527CB24: add        w9, w9, #8
  0x0527CB28: strh       w9, [x1, #0xa]
  0x0527CB2C: b          #0x527caa0
  0x0527CB30: cbz        x1, #0x527cb70
  0x0527CB34: ldrh       w8, [x1]
  0x0527CB38: cmp        w8, #2
  0x0527CB3C: b.lo       #0x527cb68
  0x0527CB40: ldrh       w9, [x1]
  0x0527CB44: cmp        w8, #4
  0x0527CB48: strh       w9, [x0]
  0x0527CB4C: b.lo       #0x527cb68
  0x0527CB50: ldrh       w9, [x1, #2]
  0x0527CB54: cmp        w8, #0xc
  0x0527CB58: strh       w9, [x0, #2]
  0x0527CB5C: b.lo       #0x527cb68
  0x0527CB60: ldur       x8, [x1, #4]
  0x0527CB64: str        x8, [x0, #8]
  0x0527CB68: mov        w0, #1
  0x0527CB6C: ret        
  0x0527CB70: mov        w0, wzr
  0x0527CB74: ret        
  0x0527CB78: mov        w8, #0x430000
  0x0527CB7C: stp        xzr, xzr, [x0, #8]
  0x0527CB80: str        w8, [x0]
  0x0527CB84: ret        
  0x0527CB88: ldr        x8, [x1]
  0x0527CB8C: cbz        x8, #0x527cbf0
  0x0527CB90: ldr        w9, [x1, #0xc]
  0x0527CB94: cbnz       w9, #0x527cbd4
  0x0527CB98: ldrh       w9, [x1, #0xa]
  0x0527CB9C: ldrh       w10, [x1, #8]
  0x0527CBA0: add        w11, w9, #2
  0x0527CBA4: cmp        w11, w10
  0x0527CBA8: b.ls       #0x527cbb8
  0x0527CBAC: mov        w9, #1
  0x0527CBB0: str        w9, [x1, #0xc]
  0x0527CBB4: b          #0x527cbd4
  0x0527CBB8: ldrh       w10, [x0]
  0x0527CBBC: strh       w10, [x8, w9, uxtw]
  0x0527CBC0: ldrh       w9, [x1, #0xa]
  0x0527CBC4: ldr        w10, [x1, #0xc]
  0x0527CBC8: add        w9, w9, #2
  0x0527CBCC: strh       w9, [x1, #0xa]
  0x0527CBD0: cbz        w10, #0x527cbfc
  0x0527CBD4: ldr        x10, [x1]
  0x0527CBD8: cbz        x10, #0x527cbe8
  0x0527CBDC: ldrh       w9, [x1, #0xa]
  0x0527CBE0: strh       w9, [x10]
  0x0527CBE4: b          #0x527cbec
  0x0527CBE8: mov        w9, wzr
  0x0527CBEC: strh       w9, [x0]
  0x0527CBF0: cmp        x8, #0
  0x0527CBF4: cset       w0, ne
  0x0527CBF8: ret        
  0x0527CBFC: and        w10, w9, #0xffff
  0x0527CC00: ldrh       w11, [x1, #8]
  0x0527CC04: add        w10, w10, #2
  0x0527CC08: cmp        w10, w11
  0x0527CC0C: b.hi       #0x527cbac
  0x0527CC10: ldr        x10, [x1]
  0x0527CC14: ldrh       w11, [x0, #2]
  0x0527CC18: and        x9, x9, #0xffff
  0x0527CC1C: strh       w11, [x10, x9]
  0x0527CC20: ldrh       w9, [x1, #0xa]
  0x0527CC24: ldr        w10, [x1, #0xc]
  0x0527CC28: add        w9, w9, #2
  0x0527CC2C: strh       w9, [x1, #0xa]
  0x0527CC30: cbnz       w10, #0x527cbd4
  0x0527CC34: ldrh       w9, [x1, #0xa]
  0x0527CC38: ldrh       w10, [x1, #8]
  0x0527CC3C: add        w11, w9, #8
  0x0527CC40: cmp        w11, w10
  0x0527CC44: b.hi       #0x527cbac
  0x0527CC48: ldr        x10, [x1]
  0x0527CC4C: ldr        x11, [x0, #8]
  0x0527CC50: str        x11, [x10, w9, uxtw]
  0x0527CC54: ldrh       w9, [x1, #0xa]
  0x0527CC58: ldr        w10, [x1, #0xc]
  0x0527CC5C: add        w9, w9, #8
  0x0527CC60: strh       w9, [x1, #0xa]
  0x0527CC64: cbnz       w10, #0x527cbd4
  0x0527CC68: ldrh       w9, [x1, #0xa]
  0x0527CC6C: ldrh       w10, [x1, #8]
  0x0527CC70: add        w11, w9, #8
  0x0527CC74: cmp        w11, w10
  0x0527CC78: b.hi       #0x527cbac
  0x0527CC7C: ldr        x10, [x1]
  0x0527CC80: ldr        x11, [x0, #0x10]
  0x0527CC84: str        x11, [x10, w9, uxtw]
  0x0527CC88: ldrh       w9, [x1, #0xa]
  0x0527CC8C: add        w9, w9, #8
  0x0527CC90: strh       w9, [x1, #0xa]
  0x0527CC94: b          #0x527cbd4
  0x0527CC98: cbz        x1, #0x527cce8
  0x0527CC9C: ldrh       w8, [x1]
```

### Analysis
**Store instructions:** 35

## 0x0CE7 - CMSG_BACK_DEFEND_NEW (cancel march)
Constructor: 0x05139714

### Disassembly
```asm
  0x05139714: mov        w8, #0xce70000
  0x05139718: str        w8, [x0]
  0x0513971C: stur       q0, [x0, #8]
  0x05139720: stur       q0, [x0, #0x18]
  0x05139724: ret        
  0x05139728: stp        x29, x30, [sp, #-0x30]!
  0x0513972C: stp        x22, x21, [sp, #0x10]
  0x05139730: stp        x20, x19, [sp, #0x20]
  0x05139734: mov        x29, sp
  0x05139738: ldr        x22, [x1]
  0x0513973C: cbz        x22, #0x5139890
  0x05139740: ldr        w9, [x1, #0xc]
  0x05139744: mov        x20, x1
  0x05139748: mov        x19, x0
  0x0513974C: cbnz       w9, #0x513978c
  0x05139750: ldrh       w8, [x20, #0xa]
  0x05139754: ldrh       w9, [x20, #8]
  0x05139758: add        w10, w8, #2
  0x0513975C: cmp        w10, w9
  0x05139760: b.ls       #0x5139770
  0x05139764: mov        w9, #1
  0x05139768: str        w9, [x20, #0xc]
  0x0513976C: b          #0x513978c
  0x05139770: ldrh       w9, [x19]
  0x05139774: strh       w9, [x22, w8, uxtw]
  0x05139778: ldrh       w8, [x20, #0xa]
  0x0513977C: ldr        w9, [x20, #0xc]
  0x05139780: add        w8, w8, #2
  0x05139784: strh       w8, [x20, #0xa]
  0x05139788: cbz        w9, #0x51398a8
  0x0513978C: mov        x8, x19
  0x05139790: ldp        x10, x11, [x8, #8]!
  0x05139794: sub        x11, x11, x10
  0x05139798: asr        x10, x11, #1
  0x0513979C: tst        x11, #0x1fffe
  0x051397A0: b.eq       #0x5139808
  0x051397A4: cbnz       w9, #0x5139828
  0x051397A8: mov        x9, xzr
  0x051397AC: and        x10, x10, #0xffff
  0x051397B0: mov        w11, #1
  0x051397B4: b          #0x51397e0
  0x051397B8: ldr        x13, [x8]
  0x051397BC: ldr        x14, [x20]
  0x051397C0: ldrh       w13, [x13, x9, lsl #1]
  0x051397C4: strh       w13, [x14, w12, uxtw]
  0x051397C8: ldrh       w12, [x20, #0xa]
  0x051397CC: add        w12, w12, #2
  0x051397D0: strh       w12, [x20, #0xa]
  0x051397D4: add        x9, x9, #1
  0x051397D8: cmp        x10, x9
  0x051397DC: b.eq       #0x5139804
  0x051397E0: ldr        w12, [x20, #0xc]
  0x051397E4: cbnz       w12, #0x51397d4
  0x051397E8: ldrh       w12, [x20, #0xa]
  0x051397EC: ldrh       w13, [x20, #8]
  0x051397F0: add        w14, w12, #2
  0x051397F4: cmp        w14, w13
  0x051397F8: b.ls       #0x51397b8
  0x051397FC: str        w11, [x20, #0xc]
  0x05139800: b          #0x51397d4
  0x05139804: ldr        w9, [x20, #0xc]
  0x05139808: cbnz       w9, #0x5139828
  0x0513980C: ldrh       w8, [x20, #0xa]
  0x05139810: ldrh       w9, [x20, #8]
  0x05139814: add        w10, w8, #8
  0x05139818: cmp        w10, w9
  0x0513981C: b.ls       #0x513983c
  0x05139820: mov        w8, #1
  0x05139824: str        w8, [x20, #0xc]
  0x05139828: ldr        x21, [x20]
  0x0513982C: cbz        x21, #0x513985c
  0x05139830: ldrh       w8, [x20, #0xa]
  0x05139834: strh       w8, [x21]
  0x05139838: b          #0x5139860
  0x0513983C: ldr        x9, [x20]
  0x05139840: ldr        x10, [x19, #0x20]
  0x05139844: str        x10, [x9, w8, uxtw]
  0x05139848: ldrh       w8, [x20, #0xa]
  0x0513984C: add        w8, w8, #8
  0x05139850: strh       w8, [x20, #0xa]
  0x05139854: ldr        x21, [x20]
  0x05139858: cbnz       x21, #0x5139830
  0x0513985C: mov        w8, wzr
  0x05139860: strh       w8, [x19]
  0x05139864: bl         #0x5c6dbc0
  0x05139868: mov        w1, w0
  0x0513986C: mov        x0, x21
  0x05139870: bl         #0x5c6dba0
  0x05139874: ldr        x9, [x20]
  0x05139878: cbz        x9, #0x5139888
  0x0513987C: ldrh       w8, [x20, #0xa]
  0x05139880: strh       w8, [x9]
  0x05139884: b          #0x513988c
  0x05139888: mov        w8, wzr
  0x0513988C: strh       w8, [x19]
  0x05139890: cmp        x22, #0
  0x05139894: cset       w0, ne
  0x05139898: ldp        x20, x19, [sp, #0x20]
  0x0513989C: ldp        x22, x21, [sp, #0x10]
  0x051398A0: ldp        x29, x30, [sp], #0x30
  0x051398A4: ret        
  0x051398A8: and        w9, w8, #0xffff
  0x051398AC: ldrh       w10, [x20, #8]
  0x051398B0: add        w9, w9, #2
  0x051398B4: cmp        w9, w10
  0x051398B8: b.hi       #0x5139764
  0x051398BC: ldr        x9, [x20]
  0x051398C0: ldrh       w10, [x19, #2]
  0x051398C4: and        x8, x8, #0xffff
  0x051398C8: strh       w10, [x9, x8]
  0x051398CC: ldrh       w8, [x20, #0xa]
  0x051398D0: ldr        w9, [x20, #0xc]
  0x051398D4: add        w8, w8, #2
  0x051398D8: strh       w8, [x20, #0xa]
  0x051398DC: cbnz       w9, #0x513978c
  0x051398E0: ldrh       w8, [x20, #0xa]
  0x051398E4: ldrh       w9, [x20, #8]
  0x051398E8: cmp        w8, w9
  0x051398EC: b.hs       #0x5139764
  0x051398F0: ldr        x9, [x20]
  0x051398F4: ldrb       w10, [x19, #4]
  0x051398F8: strb       w10, [x9, w8, uxtw]
  0x051398FC: ldrh       w8, [x20, #0xa]
  0x05139900: ldr        w9, [x20, #0xc]
  0x05139904: add        w8, w8, #1
  0x05139908: strh       w8, [x20, #0xa]
  0x0513990C: cbnz       w9, #0x513978c
  0x05139910: ldrh       w8, [x20, #0xa]
  0x05139914: ldrh       w9, [x20, #8]
  0x05139918: cmp        w8, w9
  0x0513991C: b.hs       #0x5139764
  0x05139920: ldr        x9, [x20]
  0x05139924: ldrb       w10, [x19, #5]
  0x05139928: strb       w10, [x9, w8, uxtw]
  0x0513992C: ldrh       w8, [x20, #0xa]
  0x05139930: ldr        w9, [x20, #0xc]
  0x05139934: add        w8, w8, #1
  0x05139938: strh       w8, [x20, #0xa]
  0x0513993C: cbnz       w9, #0x513978c
  0x05139940: ldrh       w8, [x20, #0xa]
  0x05139944: ldrh       w9, [x20, #8]
  0x05139948: cmp        w8, w9
  0x0513994C: b.hs       #0x5139764
  0x05139950: ldr        x9, [x20]
  0x05139954: ldrb       w10, [x19, #6]
  0x05139958: strb       w10, [x9, w8, uxtw]
  0x0513995C: ldrh       w8, [x20, #0xa]
  0x05139960: ldr        w9, [x20, #0xc]
  0x05139964: add        w8, w8, #1
  0x05139968: strh       w8, [x20, #0xa]
```

### Analysis
**Function calls:** 2
  - 0x05139864: bl #0x5c6dbc0
  - 0x05139870: bl #0x5c6dba0
**Store instructions:** 37

## 0x0CE8 - CMSG_START_MARCH_NEW
Constructor: 0x05212268

### Disassembly
```asm
  0x05212268: mov        w8, #0xce80000
  0x0521226C: strb       wzr, [x0, #8]
  0x05212270: str        w8, [x0]
  0x05212274: str        xzr, [x0, #0x10]
  0x05212278: strh       wzr, [x0, #0x48]
  0x0521227C: str        xzr, [x0, #0x50]
  0x05212280: strb       wzr, [x0, #0x58]
  0x05212284: stp        xzr, xzr, [x0, #0x28]
  0x05212288: str        xzr, [x0, #0x20]
  0x0521228C: stur       xzr, [x0, #0x35]
  0x05212290: ret        
  ; --- END OF FUNCTION ---
```

### Analysis
**Store instructions:** 9

## 0x0CEB - CMSG_ENABLE_VIEW_NEW
Constructor: 0x051F53FC

### Disassembly
```asm
  0x051F53FC: mov        w8, #0xceb0000
  0x051F5400: strb       wzr, [x0, #8]
  0x051F5404: str        w8, [x0]
  0x051F5408: str        xzr, [x0, #0x10]
  0x051F540C: strb       wzr, [x0, #0x18]
  0x051F5410: ret        
  ; --- END OF FUNCTION ---
```

### Analysis
**Store instructions:** 4

## 0x0CED - CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW (train)
Constructor: 0x052C6740

### Disassembly
```asm
  0x052C6740: mov        w8, #0xced0000
  0x052C6744: str        xzr, [x0, #8]
  0x052C6748: str        w8, [x0]
  0x052C674C: strb       wzr, [x0, #0x10]
  0x052C6750: stur       q0, [x0, #0x18]
  0x052C6754: stur       q0, [x0, #0x28]
  0x052C6758: ret        
  ; --- END OF FUNCTION ---
```

### Analysis
**Store instructions:** 5

## 0x0CEE - CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW (research)
Constructor: 0x052B4EFC

### Disassembly
```asm
  0x052B4EFC: mov        w8, #0xcee0000
  0x052B4F00: strh       wzr, [x0, #8]
  0x052B4F04: str        w8, [x0]
  0x052B4F08: strb       wzr, [x0, #0xa]
  0x052B4F0C: stp        q0, q0, [x0, #0x10]
  0x052B4F10: ret        
  ; --- END OF FUNCTION ---
```

### Analysis
**Store instructions:** 4

## 0x0CEF - CMSG_BUILDING_OPERAT_REQUEST_NEW (build)
Constructor: 0x04FCC358

### Disassembly
```asm
  0x04FCC358: mov        w8, #0xcef0000
  0x04FCC35C: strb       wzr, [x0, #8]
  0x04FCC360: str        w8, [x0]
  0x04FCC364: strh       wzr, [x0, #0xa]
  0x04FCC368: str        wzr, [x0, #0xc]
  0x04FCC36C: strb       wzr, [x0, #0x14]
  0x04FCC370: stur       q0, [x0, #0x18]
  0x04FCC374: stur       q0, [x0, #0x28]
  0x04FCC378: ret        
  ; --- END OF FUNCTION ---
```

### Analysis
**Store instructions:** 7

## 0x1B8B - CMSG_PASSWORD_CHECK_REQUEST
Constructor: 0x0527367C

### Disassembly
```asm
  0x0527367C: mov        w8, #0x1b8b0000
  0x05273680: strh       wzr, [x0, #4]
  0x05273684: str        w8, [x0]
  0x05273688: stp        xzr, xzr, [x0, #0x10]
  0x0527368C: ret        
  0x05273690: stp        x29, x30, [sp, #-0x30]!
  0x05273694: stp        x22, x21, [sp, #0x10]
  0x05273698: stp        x20, x19, [sp, #0x20]
  0x0527369C: mov        x29, sp
  0x052736A0: ldr        x22, [x1]
  0x052736A4: cbz        x22, #0x5273914
  0x052736A8: ldr        w8, [x1, #0xc]
  0x052736AC: mov        x20, x1
  0x052736B0: mov        x19, x0
  0x052736B4: cbnz       w8, #0x5273700
  0x052736B8: ldrh       w8, [x20, #0xa]
  0x052736BC: ldrh       w9, [x20, #8]
  0x052736C0: add        w10, w8, #2
  0x052736C4: cmp        w10, w9
  0x052736C8: b.ls       #0x52736e4
  0x052736CC: mov        w8, #1
  0x052736D0: str        w8, [x20, #0xc]
  0x052736D4: bl         #0x5c6dbd0
  0x052736D8: ldr        w8, [x20, #0xc]
  0x052736DC: cbnz       w8, #0x5273748
  0x052736E0: b          #0x527370c
  0x052736E4: ldrh       w9, [x19]
  0x052736E8: strh       w9, [x22, w8, uxtw]
  0x052736EC: ldrh       w8, [x20, #0xa]
  0x052736F0: ldr        w9, [x20, #0xc]
  0x052736F4: add        w8, w8, #2
  0x052736F8: strh       w8, [x20, #0xa]
  0x052736FC: cbz        w9, #0x52737ac
  0x05273700: bl         #0x5c6dbd0
  0x05273704: ldr        w8, [x20, #0xc]
  0x05273708: cbnz       w8, #0x5273748
  0x0527370C: ldrh       w8, [x20, #0xa]
  0x05273710: ldrh       w9, [x20, #8]
  0x05273714: add        w10, w8, #2
  0x05273718: cmp        w10, w9
  0x0527371C: b.ls       #0x527372c
  0x05273720: mov        w8, #1
  0x05273724: str        w8, [x20, #0xc]
  0x05273728: b          #0x5273748
  0x0527372C: ldr        x9, [x20]
  0x05273730: strh       w0, [x9, w8, uxtw]
  0x05273734: ldrh       w8, [x20, #0xa]
  0x05273738: ldr        w9, [x20, #0xc]
  0x0527373C: add        w8, w8, #2
  0x05273740: strh       w8, [x20, #0xa]
  0x05273744: cbz        w9, #0x52737ec
  0x05273748: bl         #0x5c6dbe0
  0x0527374C: ldr        w8, [x20, #0xc]
  0x05273750: cbnz       w8, #0x5273798
  0x05273754: ldrh       w8, [x20, #0xa]
  0x05273758: ldrh       w9, [x20, #8]
  0x0527375C: add        w10, w8, #8
  0x05273760: cmp        w10, w9
  0x05273764: b.ls       #0x527377c
  0x05273768: mov        w8, #1
  0x0527376C: str        w8, [x20, #0xc]
  0x05273770: ldr        x21, [x20]
  0x05273774: cbnz       x21, #0x52737a0
  0x05273778: b          #0x52738e0
  0x0527377C: ldr        x9, [x20]
  0x05273780: str        x0, [x9, w8, uxtw]
  0x05273784: ldrh       w8, [x20, #0xa]
  0x05273788: ldr        w9, [x20, #0xc]
  0x0527378C: add        w8, w8, #8
  0x05273790: strh       w8, [x20, #0xa]
  0x05273794: cbz        w9, #0x52738a8
  0x05273798: ldr        x21, [x20]
  0x0527379C: cbz        x21, #0x52738e0
  0x052737A0: ldrh       w8, [x20, #0xa]
  0x052737A4: strh       w8, [x21]
  0x052737A8: b          #0x52738e4
  0x052737AC: and        w9, w8, #0xffff
  0x052737B0: ldrh       w10, [x20, #8]
  0x052737B4: add        w9, w9, #2
  0x052737B8: cmp        w9, w10
  0x052737BC: b.hi       #0x52736cc
  0x052737C0: ldr        x9, [x20]
  0x052737C4: ldrh       w10, [x19, #2]
  0x052737C8: and        x8, x8, #0xffff
  0x052737CC: strh       w10, [x9, x8]
  0x052737D0: ldrh       w8, [x20, #0xa]
  0x052737D4: add        w8, w8, #2
  0x052737D8: strh       w8, [x20, #0xa]
  0x052737DC: bl         #0x5c6dbd0
  0x052737E0: ldr        w8, [x20, #0xc]
  0x052737E4: cbnz       w8, #0x5273748
  0x052737E8: b          #0x527370c
  0x052737EC: ldrh       w9, [x20, #8]
  0x052737F0: cmp        w9, w8, uxth
  0x052737F4: b.ls       #0x5273720
  0x052737F8: ldr        x9, [x20]
  0x052737FC: ldrb       w10, [x19, #6]
  0x05273800: and        x8, x8, #0xffff
  0x05273804: strb       w10, [x9, x8]
  0x05273808: ldrh       w8, [x20, #0xa]
  0x0527380C: ldr        w9, [x20, #0xc]
  0x05273810: add        w8, w8, #1
  0x05273814: strh       w8, [x20, #0xa]
  0x05273818: cbnz       w9, #0x5273748
  0x0527381C: ldrh       w8, [x20, #0xa]
  0x05273820: ldrh       w9, [x20, #8]
  0x05273824: cmp        w8, w9
  0x05273828: b.hs       #0x5273720
  0x0527382C: ldr        x9, [x20]
  0x05273830: ldrb       w10, [x19, #7]
  0x05273834: strb       w10, [x9, w8, uxtw]
  0x05273838: ldrh       w8, [x20, #0xa]
  0x0527383C: ldr        w9, [x20, #0xc]
  0x05273840: add        w8, w8, #1
  0x05273844: strh       w8, [x20, #0xa]
  0x05273848: cbnz       w9, #0x5273748
  0x0527384C: ldrh       w8, [x20, #0xa]
  0x05273850: ldrh       w9, [x20, #8]
  0x05273854: cmp        w8, w9
  0x05273858: b.hs       #0x5273720
  0x0527385C: ldr        x9, [x20]
  0x05273860: ldrb       w10, [x19, #8]
  0x05273864: strb       w10, [x9, w8, uxtw]
  0x05273868: ldrh       w8, [x20, #0xa]
  0x0527386C: ldr        w9, [x20, #0xc]
  0x05273870: add        w8, w8, #1
  0x05273874: strh       w8, [x20, #0xa]
  0x05273878: cbnz       w9, #0x5273748
  0x0527387C: ldrh       w8, [x20, #0xa]
  0x05273880: ldrh       w9, [x20, #8]
  0x05273884: cmp        w8, w9
  0x05273888: b.hs       #0x5273720
  0x0527388C: ldr        x9, [x20]
  0x05273890: ldrb       w10, [x19, #9]
  0x05273894: strb       w10, [x9, w8, uxtw]
  0x05273898: ldrh       w8, [x20, #0xa]
  0x0527389C: add        w8, w8, #1
  0x052738A0: strh       w8, [x20, #0xa]
  0x052738A4: b          #0x5273748
  0x052738A8: and        w9, w8, #0xffff
  0x052738AC: ldrh       w10, [x20, #8]
  0x052738B0: add        w9, w9, #8
  0x052738B4: cmp        w9, w10
  0x052738B8: b.hi       #0x5273768
  0x052738BC: ldr        x9, [x20]
  0x052738C0: ldr        x10, [x19, #0x18]
  0x052738C4: and        x8, x8, #0xffff
  0x052738C8: str        x10, [x9, x8]
  0x052738CC: ldrh       w8, [x20, #0xa]
  0x052738D0: add        w8, w8, #8
```

### Analysis
**Function calls:** 6
  - 0x052736D4: bl #0x5c6dbd0
  - 0x05273700: bl #0x5c6dbd0
  - 0x05273748: bl #0x5c6dbe0
  - 0x052737DC: bl #0x5c6dbd0
  - 0x052738E8: bl #0x5c6dbc0
  - 0x052738F4: bl #0x5c6dbb0
**Store instructions:** 37

# PART 2: CMSG Symbol Analysis

Found 289 relevant CMSG symbols:

| Symbol | Address | Size |
|--------|---------|------|
| `_ZN10AFAppEvent22onMsgSynSingleBuildingERK27CMSG_BUILDING_OPERAT_RETURN` | 0x032EAF3C | 104 |
| `_ZN13LogicPassword17respCheckPasswordERK26CMSG_PASSWORD_CHECK_RETURN` | 0x039FA52C | 268 |
| `_ZN14LogicLordSkill22onMsgSynSingleBuildingERK27CMSG_BUILDING_OPERAT_RETURN` | 0x038C3A2C | 1236 |
| `_ZN14MessageSubject16registerListenerI19CMSG_KEEP_LIVE_TESTEEvPvRKNSt6__ndk18fun` | 0x03806E60 | 548 |
| `_ZN14MessageSubject16registerListenerI26CMSG_PASSWORD_CHECK_RETURNEEvPvRKNSt6__n` | 0x039FA308 | 548 |
| `_ZN14MessageSubject16registerListenerI27CMSG_BUILDING_OPERAT_RETURNEEvPvRKNSt6__` | 0x032EAD18 | 548 |
| `_ZN14MessageSubject16registerListenerI34CMSG_LEAGUE_BUILDING_OPERAT_RETURNEEvPvR` | 0x036EA634 | 588 |
| `_ZN14MessageSubject16registerListenerI34CMSG_SOLDIER_NORMAL_PRODUCE_RETURNEEvPvR` | 0x037E5858 | 548 |
| `_ZN15LogicNewSoldier31onSOLDIER_NORMAL_PRODUCE_RETURNERK34CMSG_SOLDIER_NORMAL_PR` | 0x037E5A7C | 460 |
| `_ZN16CMSG_BACK_DEFEND7getDataEPKc` | 0x05215B34 | 316 |
| `_ZN16CMSG_BACK_DEFEND8packDataER8CIStream` | 0x052159AC | 392 |
| `_ZN16CMSG_BACK_DEFENDC1Ev` | 0x05215998 | 20 |
| `_ZN16CMSG_BACK_DEFENDC2Ev` | 0x05215998 | 20 |
| `_ZN16SMSG_BACK_DEFEND7getDataEPKc` | 0x05225B84 | 1060 |
| `_ZN16SMSG_BACK_DEFEND8packDataER8CIStream` | 0x05225604 | 1408 |
| `_ZN16SMSG_BACK_DEFENDC1Ev` | 0x052255D4 | 48 |
| `_ZN16SMSG_BACK_DEFENDC2Ev` | 0x052255D4 | 48 |
| `_ZN17CSocialityManager24onMainBuildingInfoChangeERK27CMSG_BUILDING_OPERAT_RETURN` | 0x039D5D64 | 280 |
| `_ZN18CHeroLegendManager25_onMainBuildingInfoChangeERK27CMSG_BUILDING_OPERAT_RETU` | 0x037F0854 | 156 |
| `_ZN19CMSG_KEEP_LIVE_TEST7getDataEPKc` | 0x0527CB30 | 72 |
| `_ZN19CMSG_KEEP_LIVE_TEST8packDataER8CIStream` | 0x0527CA54 | 220 |
| `_ZN19CMSG_KEEP_LIVE_TESTC1Ev` | 0x0527CA48 | 12 |
| `_ZN19CMSG_KEEP_LIVE_TESTC2Ev` | 0x0527CA48 | 12 |
| `_ZN20CBuildingDataManager32onSendCMsgBuildingOperateRequestER32CMSG_BUILDING_OPE` | 0x038F5B3C | 300 |
| `_ZN20CMSG_BACK_DEFEND_NEW7getDataEPKc` | 0x051399E4 | 468 |
| `_ZN20CMSG_BACK_DEFEND_NEW8packDataER8CIStream` | 0x05139728 | 700 |
| `_ZN20CMSG_BACK_DEFEND_NEWC1Ev` | 0x05139710 | 24 |
| `_ZN20CMSG_BACK_DEFEND_NEWC2Ev` | 0x05139710 | 24 |
| `_ZN20CMSG_ENABLE_VIEW_NEW7getDataEPKc` | 0x051F5660 | 168 |
| `_ZN20CMSG_ENABLE_VIEW_NEW8packDataER8CIStream` | 0x051F5414 | 588 |
| `_ZN20CMSG_ENABLE_VIEW_NEWC1Ev` | 0x051F53FC | 24 |
| `_ZN20CMSG_ENABLE_VIEW_NEWC2Ev` | 0x051F53FC | 24 |
| `_ZN20CMSG_START_MARCH_NEW7getDataEPKc` | 0x05212778 | 848 |
| `_ZN20CMSG_START_MARCH_NEW8packDataER8CIStream` | 0x05212294 | 1252 |
| `_ZN20CMSG_START_MARCH_NEWC1Ev` | 0x05212268 | 44 |
| `_ZN20CMSG_START_MARCH_NEWC2Ev` | 0x05212268 | 44 |
| `_ZN24CDominionBuildingManager30request_LEAGUE_BUILDING_OPERATEaittPN7cocos2d4Nod` | 0x036EF450 | 212 |
| `_ZN24CDominionBuildingManager38_on_CMSG_LEAGUE_BUILDING_OPERAT_RETURNERK34CMSG_L` | 0x036EA880 | 712 |
| `_ZN26CMSG_PASSWORD_CHECK_RETURN7getDataEPKc` | 0x05273AC0 | 72 |
| `_ZN26CMSG_PASSWORD_CHECK_RETURN8packDataER8CIStream` | 0x052739E4 | 220 |
| `_ZN26CMSG_PASSWORD_CHECK_RETURNC1Ev` | 0x052739D4 | 16 |
| `_ZN26CMSG_PASSWORD_CHECK_RETURNC2Ev` | 0x052739D4 | 16 |
| `_ZN27CMSG_BACK_DEFEND_KING_CHESS7getDataEPKc` | 0x050C94C0 | 316 |
| `_ZN27CMSG_BACK_DEFEND_KING_CHESS8packDataER8CIStream` | 0x050C9338 | 392 |
| `_ZN27CMSG_BACK_DEFEND_KING_CHESSC1Ev` | 0x050C9324 | 20 |
| `_ZN27CMSG_BACK_DEFEND_KING_CHESSC2Ev` | 0x050C9324 | 20 |
| `_ZN27CMSG_BUILDING_OPERAT_RETURN7getDataEPKc` | 0x04FCD040 | 200 |
| `_ZN27CMSG_BUILDING_OPERAT_RETURN8packDataER8CIStream` | 0x04FCCDCC | 628 |
| `_ZN27CMSG_BUILDING_OPERAT_RETURNC1Ev` | 0x04FCCDB4 | 24 |
| `_ZN27CMSG_BUILDING_OPERAT_RETURNC2Ev` | 0x04FCCDB4 | 24 |

# PART 3: Vulnerability Analysis

## 3a. Hardcoded Secrets & Crypto References

**secret** (5 unique):
  - `rate_secret`
  - `Text_secret_title`
  - `rive_secret_key_and_iv`
  - `/ui3/secret_task/secret_task_img_bg5.png`
  - `/map_secret_task.csb`
**password** (5 unique):
  - `dary_password_input.csb`
  - `heck password, OpenSSL error %s`
  - `rong password`
  - `dary_password_setting.csb`
  - `dary_password_update.csb`
**token** (5 unique):
  - `alid_token`
  - `ward_token.xml`
  - `gift_token_enter_1`
  - `gift_token_enter_2`
  - `gift_token.xml`
**private** (5 unique):
  - `o %s private key %s formats are enabled`
  - `/src/private_typeinfo.cpp`
  - `lock_privateChat`
  - `/ssl/private`
  - `thin private range`
**AES reference** (5 unique):
  - `AEAD_AES_256_GCM`
  - `WITH_AES_256_CCM_8`
  - `WITH_AES_256_GCM_SHA384`
  - `SRTP_AES128_CM_SHA1_32`
  - `WITH_AES_256_CBC_SHA384`
**RSA reference** (5 unique):
  - `CDHE-RSA-CAMELLIA256-SHA384`
  - `_DHE_RSA_WITH_ARIA_256_GCM_SHA384`
  - `CDHE_RSA_WITH_AES_128_CBC_SHA`
  - `_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256`
  - `_DHE_RSA_WITH_AES_128_GCM_SHA256`
**SHA256** (5 unique):
  - `A128-SHA256`
  - `S256-SHA256`
  - `_GCM_SHA256`
  - `_CBC_SHA256`
  - `-GCM-SHA256`
**HMAC** (5 unique):
  - `_CTR_HMAC_SHA1_32`
  - `KDF2_HMAC`
  - `-CBC-HMAC-SHA1`
  - `-CBC-HMAC-SHA256`
  - `_CTR_HMAC_SHA1_80`

## 3b. Protocol Vulnerabilities

### Known Weaknesses
1. **Weak encryption**: XOR + add*17 with static 7-byte table - trivially reversible
2. **Hardcoded CQ_secret**: Gateway token XOR key is in .rodata
3. **No TLS**: Game protocol uses raw TCP with custom encoding
4. **Single-byte server key**: Server key from 0x0038 is reused for all packets
5. **Predictable checksum**: Just sum of encrypted bytes mod 256
6. **Static CMSG_TABLE**: XOR table never changes, shared across all connections
7. **No replay protection**: No nonce/sequence number in protocol (except msg random byte)

## 3c. Interesting Opcodes for Bot/Exploit

### Free Resources / Rewards (109 C2S opcodes)
  - `0x0051` = CMSG_NPC_REWARD_REQUEST
  - `0x0222` = CMSG_GUIDE_TASKS_RECEIVE_REWARD_REQUEST
  - `0x0224` = CMSG_ACHIEVEMENT_RECEIVE_REWARD_REQUEST
  - `0x0226` = CMSG_ACHIEVEMENT_SCORE_RECEIVE_REWARD_REQUEST
  - `0x028F` = CMSG_NEW_ONLINE_REWARD_REQUEST
  - `0x0292` = CMSG_RANDOM_ONLINE_REWARD_REQUEST
  - `0x0310` = CMSG_GIFTPACK_RECEIVE_FREE_REQUEST
  - `0x0312` = CMSG_EVERY_DAY_GIFTPACK_REWARD_REQUEST
  - `0x060E` = CMSG_KING_REWARD_INFO_REQUEST
  - `0x0624` = CMSG_RECEIVE_LEAGUE_GIFT_REQUEST
  - `0x0626` = CMSG_RECEIVE_ALL_LEAGUE_GIFT_REQUEST
  - `0x062C` = CMSG_RECEIVE_REWARD_REQUEST
  - `0x062F` = CMSG_RECEIVE_REWARD_BATCH_REQUEST
  - `0x0637` = CMSG_COLLECTION_DELETE_RECORD_REQUEST
  - `0x0638` = CMSG_COLLECTION_RECORD_SET_FLAG_REQUEST
  - ... and 94 more

### Speed / Skip (8 C2S opcodes)
  - `0x0023` = CMSG_QUICK_LOGIN_REQUEST
  - `0x00A4` = CMSG_BUILDING_OPERAT_ONEKEY_REQUEST
  - `0x06CE` = CMSG_SOLDIER_GOLD_SPEED_CURE_REQUEST
  - `0x06CF` = CMSG_SOLDIER_ITEM_SPEED_CURE_REQUEST
  - `0x06D4` = CMSG_SOLDIER_ITEM_SPEED_PRODUCE_ONEKEY_REQUESTC1E
  - `0x06D6` = CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_REQUEST
  - `0x0BC3` = CMSG_PET_HUNT_QUICK_REQUEST
  - `0x1A01` = CMSG_RED_PAPER_QUICK_GAME_REQUEST

### Item Manipulation (1 C2S opcodes)
  - `0x1DB0` = CMSG_LEAGUE_BOSS_ITEM_USE_REQUEST

### VIP / Premium (14 C2S opcodes)
  - `0x01D1` = CMSG_VIP_ITEM_END_REQUEST
  - `0x064B` = CMSG_CHARGE_DAILY_SING_REQUESTC1E
  - `0x064D` = CMSG_CHARGE_DAILY_REWARD_REQUEST
  - `0x067C` = CMSG_VIP_BOX_INFO_REQUEST
  - `0x0C1C` = CMSG_VIP_SHOP_BUY_REQUEST
  - `0x0C1E` = CMSG_VIP_SHOP_ITEM_INFO_REQUEST
  - `0x0EA7` = CMSG_DAILY_RECHARGE_REWARD_REQUEST
  - `0x11CB` = CMSG_DAILY_VIP_REWARD_REQUEST
  - `0x11CC` = CMSG_DAILY_RECHARGE_GET_REWARD_REQUEST
  - `0x1774` = CMSG_RECHARGEBONUS_REWARD_REQUEST
  - `0x1CB7` = CMSG_LORD_GEM_HOLE_UNLOCK_REQUEST
  - `0x1CB9` = CMSG_LORD_GEM_HOLE_LV_UP_REQUEST
  - `0x1CE9` = CMSG_LEAGUE_RECHARGE_REWARD_REQUEST
  - `0x1CEC` = CMSG_LEAGUE_RECHARGE_POINT_REQUESTC1E

### Auto / Helper (6 C2S opcodes)
  - `0x1933` = CMSG_AUTO_HANDUP_CHANGE_REQUEST
  - `0x1B0E` = CMSG_CLANPK_SET_ASSIST_HERO_REQUEST
  - `0x1B10` = CMSG_CLANPK_GIVE_ASSIST_HERO_REQUEST
  - `0x1B14` = CMSG_CLANPK_ASSIST_HERO_REQUEST
  - `0x1EAB` = CMSG_AUTO_JOIN_BUILDUP_OPEN_REQUEST
  - `0x1EAD` = CMSG_AUTO_JOIN_BUILDUP_CLOSE_REQUEST

### March / Attack (7 C2S opcodes)
  - `0x06EC` = CMSG_ATTACK_SECRET_BOSS_REQUEST
  - `0x06EE` = CMSG_ATTACK_SECRET_BOSS_TEN_REQUESTC1E
  - `0x075E` = CMSG_START_TRADE_MARCH_REQUEST
  - `0x0762` = CMSG_BACK_TRADE_MARCH_REQUEST
  - `0x082A` = CMSG_SELF_MARCH_QUEUE_REQUEST
  - `0x14B9` = CMSG_OPEN_SESAME_ATTACK_MONSTER_REQUEST
  - `0x1B0C` = CMSG_CLANPK_SET_ATTACK_HERO_REQUEST

### Troop / Army (18 C2S opcodes)
  - `0x0323` = CMSG_HERO_SOLDIER_RECRUIT_REQUEST
  - `0x06C3` = CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST
  - `0x06C5` = CMSG_SOLDIER_GOLD_PRODUCE_REQUEST
  - `0x06C9` = CMSG_SOLDIER_PRODUCE_OVER_REQUEST
  - `0x06CB` = CMSG_SOLDIER_NORMAL_CURE_REQUEST
  - `0x06CD` = CMSG_SOLDIER_GOLD_CURE_REQUEST
  - `0x06CE` = CMSG_SOLDIER_GOLD_SPEED_CURE_REQUEST
  - `0x06CF` = CMSG_SOLDIER_ITEM_SPEED_CURE_REQUEST
  - `0x06D1` = CMSG_SOLDIER_CURE_OVER_REQUEST
  - `0x06D4` = CMSG_SOLDIER_ITEM_SPEED_PRODUCE_ONEKEY_REQUESTC1E
  - `0x06D6` = CMSG_SOLDIER_ITEM_SPEED_CURE_ONEKEY_REQUEST
  - `0x06F4` = CMSG_ARMY_LOSS_REWARD_REQUEST
  - `0x0CED` = CMSG_SOLDIER_NORMAL_PRODUCE_REQUEST_NEW
  - `0x1D7F` = CMSG_SOLDIER_UP_REQUEST
  - `0x1D81` = CMSG_SOLDIER_UP_BREAK_LEVEL_REQUEST
  - ... and 3 more

### Building (23 C2S opcodes)
  - `0x009D` = CMSG_BUILDING_OPERAT_REQUEST
  - `0x009F` = CMSG_BUILDING_HELP_REQUEST
  - `0x00A1` = CMSG_EXCHANGE_BUILDING_REQUEST
  - `0x00A4` = CMSG_BUILDING_OPERAT_ONEKEY_REQUEST
  - `0x0705` = CMSG_LORD_SKILL_UPGRADE_BATCH_REQUEST
  - `0x0BBD` = CMSG_PET_UPGRADE_SKILL_REQUEST
  - `0x0CEF` = CMSG_BUILDING_OPERAT_REQUEST_NEW
  - `0x0CF9` = CMSG_BUILDING_OPERAT_REQUEST_FIX_NEW
  - `0x15E0` = CMSG_LEAGUE_BUILDING_OPERAT_REQUEST
  - `0x15E4` = CMSG_LEAGUE_BUILDING_DETAIL_REQUEST
  - `0x15FA` = CMSG_LOSTLAND_BUILDING_INDEX_OPEN_REQUEST
  - `0x17D6` = CMSG_HONOR_SOUL_UPGRADE_REQUEST
  - `0x1B04` = CMSG_CLANPK_BUILDING_REQUEST
  - `0x1B06` = CMSG_CLANPK_BUILD_UPGRADE_REQUEST
  - `0x1B12` = CMSG_CLANPK_BUILDING_DETAIL_REQUEST
  - ... and 8 more

### Research (6 C2S opcodes)
  - `0x00BF` = CMSG_SCIENCE_NORMAL_STUDY_REQUEST
  - `0x00C0` = CMSG_SCIENCE_GOLD_STUDY_REQUEST
  - `0x00C1` = CMSG_SCIENCE_CANCEL_STUDY_REQUEST
  - `0x00C6` = CMSG_SCIENCE_HELP_REQUEST
  - `0x092E` = CMSG_LEAGUE_SCIENCE_DONATE_NEW_REQUEST
  - `0x0CEE` = CMSG_SCIENCE_NORMAL_STUDY_REQUEST_NEW

### Alliance (4 C2S opcodes)
  - `0x0624` = CMSG_RECEIVE_LEAGUE_GIFT_REQUEST
  - `0x0626` = CMSG_RECEIVE_ALL_LEAGUE_GIFT_REQUEST
  - `0x0930` = CMSG_DO_LEAGUE_DONATE_CRIT_NEW_REQUEST
  - `0x0CEC` = CMSG_DO_LEAGUE_DONATE_CRIT_NEW_REQUEST_NEW

# PART 4: Key Insights

## 0x1B8B (PASSWORD_CHECK_REQUEST)
- This is NOT a session heartbeat - it's a password/auth verification
- Server sends this to verify account ownership mid-session
- Sending wrong data causes immediate disconnect
- Need to find: what hash/token format is expected

## 0x0CE8 (START_MARCH_NEW)
- Constructor sets up march parameters
- Conditional opcode: bit flag selects 0x0CE8 vs 0x0D08
- Fields likely include: target coords, march type, troop composition, hero IDs

## Bot Automation Priority
1. Fix 0x1B8B response (password check) - stops disconnects
2. Implement reward collection (ACTIVITY_GAIN, REWARD_INFO)
3. Implement item usage (ITEM_USE for speedups)
4. Implement alliance help (AUTO_JOIN_BUILDUP)
5. Implement march/gather once 0x1B8B is fixed