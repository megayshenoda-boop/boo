# LogicPassword Local Call Paths

## Resolved Password-Related PLT Thunks

- `0x05C21690` -> `_ZN13LogicPassword18delayResetPasswordEv` (`0x039F9F14` via GOT `0x062F9778`)
- `0x05C216A0` -> `_ZN7CMainUI23updateSecondaryPasswordEv` (`0x0487AEB0` via GOT `0x062F9780`)
- `0x05C216B0` -> `_ZN26SecondaryPasswordSettingUI11updateStateEv` (`0x04AC7320` via GOT `0x062F9788`)
- `0x05C216D0` -> `_ZN26CMSG_PASSWORD_RESET_CD_END8packDataER8CIStream` (`0x052744B0` via GOT `0x062F9798`)
- `0x05C216E0` -> `_ZN25SecondaryPasswordUpdateUI11updateStateEv` (`0x04AC9488` via GOT `0x062F97A0`)
- `0x05C21700` -> `_ZN13LogicPassword17loadLocalPasswordEv` (`0x039FB2C8` via GOT `0x062F97B0`)
- `0x05C21710` -> `_ZN26CMSG_PASSWORD_CHECK_RETURNC1Ev` (`0x052739D4` via GOT `0x062F97B8`)
- `0x05C21720` -> `_ZN13LogicPassword30setSecondaryPasswordErrorCountEi` (`0x039FADE8` via GOT `0x062F97C0`)
- `0x05C21730` -> `_ZN13LogicPassword14decodePasswordEli` (`0x039FAF90` via GOT `0x062F97C8`)
- `0x05C21740` -> `_ZN13LogicPassword17saveLocalPasswordEv` (`0x039FC4E4` via GOT `0x062F97D0`)
- `0x05C21750` -> `_ZN24SecondaryPasswordInputUI11updateStateEv` (`0x04AC1F98` via GOT `0x062F97D8`)
- `0x05C21760` -> `_ZN24CMSG_PASSWORD_SET_RETURNC1Ev` (`0x05273E9C` via GOT `0x062F97E0`)
- `0x05C21770` -> `_ZN26CMSG_PASSWORD_RESET_RETURNC1Ev` (`0x05274324` via GOT `0x062F97E8`)
- `0x05C21780` -> `_ZN24SecondaryPasswordResetUI8updateUIEv` (`0x04AC4288` via GOT `0x062F97F0`)
- `0x05C21790` -> `_ZN27CMSG_PASSWORD_CHECK_REQUESTC1Ev` (`0x0527367C` via GOT `0x062F97F8`)
- `0x05C217A0` -> `_ZN13LogicPassword14encodePasswordERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi` (`0x039FAD00` via GOT `0x062F9800`)
- `0x05C217B0` -> `_ZN27CMSG_PASSWORD_CHECK_REQUEST8packDataER8CIStream` (`0x05273690` via GOT `0x062F9808`)
- `0x05C217E0` -> `_ZN25CMSG_PASSWORD_SET_REQUESTC1Ev` (`0x05273B08` via GOT `0x062F9820`)
- `0x05C217F0` -> `_ZN25CMSG_PASSWORD_SET_REQUEST8packDataER8CIStream` (`0x05273B20` via GOT `0x062F9828`)
- `0x05BDD240` -> `_ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc` (`0x05B720CC` via GOT `0x062D7550`)
- `0x05BDCA50` -> `_ZN14MessageSubject9singletonEv` (`0x03B83964` via GOT `0x062D7158`)
- `0x05BDCD10` -> `_ZN14MessageSubject7sendMsgEPKvi` (`0x03B842E4` via GOT `0x062D72B8`)
- `0x05BDCD20` -> `_ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_` (`0x05B72290` via GOT `0x062D72C0`)
- `0x05BDC440` -> `_Znwm` (`0x05BDC2DC` via GOT `0x062D6E50`)
- `0x05BDC460` -> `_ZdlPv` (`0x05BD4DE8` via GOT `0x062D6E60`)
- `0x05BDE2C0` -> `_ZN13IUniqueDialog8_closeUIEb` (`0x04305A6C` via GOT `0x062D7D90`)
- `0x05BDE480` -> `_ZN10CSystemTip7showTidERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb` (`0x04B2AC6C` via GOT `0x062D7E70`)

## Key Local Findings

- `LogicPassword::respCheckPassword` calls:
  - `setSecondaryPasswordErrorCount(0)`
  - `decodePassword(packet_value, 1_000_000)`
  - `saveLocalPassword()`
  - `CMainUI::updateSecondaryPassword()`
  - `SecondaryPasswordInputUI::updateState()`
- `LogicPassword::respUpdatePassword` calls:
  - `setSecondaryPasswordErrorCount(0)`
  - `decodePassword(packet_value, 10_000)`
  - `saveLocalPassword()`
  - `CMainUI::updateSecondaryPassword()`
  - `CSystemTip::showTid(...)`
- Local helper `0x039FAC60` builds/sends `CMSG_PASSWORD_CHECK_REQUEST` with:
  - `CMSG_PASSWORD_CHECK_REQUEST::C1`
  - `LogicPassword::encodePassword(password, 1_000_000)`
  - `MessageSubject::singleton()`
  - `CMSG_PASSWORD_CHECK_REQUEST::packData(...)`
  - `MessageSubject::sendMsg(...)`
- Local helper `0x039FB1A0` builds/sends `CMSG_PASSWORD_SET_REQUEST` with:
  - `LogicPassword::encodePassword(old_password, 100_000)`
  - `LogicPassword::encodePassword(new_password, 10_000)`
  - `MessageSubject::singleton()`
  - `CMSG_PASSWORD_SET_REQUEST::packData(...)`
  - `MessageSubject::sendMsg(...)`
- `LogicPassword::encodePassword` itself still has no direct `BL` callers in the binary.
- The request helpers above also have no direct `BL` callers in the scanned regions.
- Raw 8-byte literal hits for these function addresses exist elsewhere in the ELF,
  but nearby dumps show at least some of them are plain symbol-table metadata,
  so they should not be over-read as runtime dispatch tables by themselves.

## Raw 8-Byte Address Hits

- `send_check_password_helper` (`0x039FAC60`): 0x00082DB8
- `send_set_password_helper` (`0x039FB1A0`): none
- `handle_check_return_ui` (`0x039FA308`): 0x00382368
- `handle_set_return_ui` (`0x039FA638`): 0x002E4790
- `respPasswordInfo` (`0x039FA2A0`): 0x0007C680

## Annotated Call Snippets

### LogicPassword::respPasswordInfo (`0x039FA2A0`)

```text
039fa2d4: bl      #0x5c21690    ; _ZN13LogicPassword18delayResetPasswordEv @ 0x039F9F14
039fa2dc: bl      #0x5c21700    ; _ZN13LogicPassword17loadLocalPasswordEv @ 0x039FB2C8
039fa2f8: b       #0x5c216a0
```

### Password check return UI helper (`0x039FA308`)

```text
039fa338: bl      #0x5c21710    ; _ZN26CMSG_PASSWORD_CHECK_RETURNC1Ev @ 0x052739D4
039fa33c: bl      #0x5bdca50    ; _ZN14MessageSubject9singletonEv @ 0x03B83964
039fa364: blr     x9
039fa36c: b       #0x39fa394
039fa374: b       #0x39fa394
039fa390: blr     x8
039fa39c: bl      #0x5bdc440    ; _Znwm @ 0x05BDC2DC
039fa3d4: blr     x8
039fa3dc: b       #0x39fa3f4
039fa3f0: blr     x8
039fa40c: bl      #0x5bdcb50    ; _ZN14MessageSubject16registerListenerEjPvRKNSt6__ndk18functionIFvPKcEEE @ 0x03B83E60
039fa424: b       #0x39fa430
039fa438: blr     x8
039fa454: b       #0x39fa460
039fa468: blr     x8
039fa49c: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fa4a0: b       #0x39fa4e0
039fa4bc: b       #0x39fa4c8
039fa4d4: blr     x9
```

### LogicPassword::respCheckPassword (`0x039FA52C`)

```text
039fa558: bl      #0x5c21720    ; _ZN13LogicPassword30setSecondaryPasswordErrorCountEi @ 0x039FADE8
039fa570: bl      #0x5c21730    ; _ZN13LogicPassword14decodePasswordEli @ 0x039FAF90
039fa57c: bl      #0x5bdcd20    ; _ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_ @ 0x05B72290
039fa584: bl      #0x5c21740    ; _ZN13LogicPassword17saveLocalPasswordEv @ 0x039FC4E4
039fa594: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fa5a8: bl      #0x5c216a0    ; _ZN7CMainUI23updateSecondaryPasswordEv @ 0x0487AEB0
039fa5bc: bl      #0x5c21750    ; _ZN24SecondaryPasswordInputUI11updateStateEv @ 0x04AC1F98
039fa5d0: bl      #0x5c216e0    ; _ZN25SecondaryPasswordUpdateUI11updateStateEv @ 0x04AC9488
039fa5e0: bl      #0x5bde2c0    ; _ZN13IUniqueDialog8_closeUIEb @ 0x04305A6C
039fa618: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fa630: bl      #0x5bd84ac
039fa634: bl      #0x5bdc4a0    ; __stack_chk_fail @ 0x00000000
```

### Password set return UI helper (`0x039FA638`)

```text
039fa668: bl      #0x5c21760    ; _ZN24CMSG_PASSWORD_SET_RETURNC1Ev @ 0x05273E9C
039fa66c: bl      #0x5bdca50    ; _ZN14MessageSubject9singletonEv @ 0x03B83964
039fa694: blr     x9
039fa69c: b       #0x39fa6c4
039fa6a4: b       #0x39fa6c4
039fa6c0: blr     x8
039fa6cc: bl      #0x5bdc440    ; _Znwm @ 0x05BDC2DC
039fa704: blr     x8
039fa70c: b       #0x39fa724
039fa720: blr     x8
039fa73c: bl      #0x5bdcb50    ; _ZN14MessageSubject16registerListenerEjPvRKNSt6__ndk18functionIFvPKcEEE @ 0x03B83E60
039fa754: b       #0x39fa760
039fa768: blr     x8
039fa784: b       #0x39fa790
039fa798: blr     x8
039fa7cc: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fa7d0: b       #0x39fa810
```

### LogicPassword::respUpdatePassword (`0x039FA85C`)

```text
039fa890: bl      #0x5c21720    ; _ZN13LogicPassword30setSecondaryPasswordErrorCountEi @ 0x039FADE8
039fa8a4: bl      #0x5c21730    ; _ZN13LogicPassword14decodePasswordEli @ 0x039FAF90
039fa8b0: bl      #0x5bdcd20    ; _ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_ @ 0x05B72290
039fa8b8: bl      #0x5c21740    ; _ZN13LogicPassword17saveLocalPasswordEv @ 0x039FC4E4
039fa8c8: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fa8dc: bl      #0x5c216a0    ; _ZN7CMainUI23updateSecondaryPasswordEv @ 0x0487AEB0
039fa8f0: bl      #0x5c216e0    ; _ZN25SecondaryPasswordUpdateUI11updateStateEv @ 0x04AC9488
039fa908: bl      #0x5bde2c0    ; _ZN13IUniqueDialog8_closeUIEb @ 0x04305A6C
039fa93c: bl      #0x5bde480    ; _ZN10CSystemTip7showTidERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEb @ 0x04B2AC6C
039fa94c: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fa974: b       #0x39fa978
039fa988: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
```

### LogicPassword send-check helper (`0x039FAC60`)

```text
039fac8c: bl      #0x5bdd240    ; _ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc @ 0x05B720CC
039fac94: bl      #0x5c21790    ; _ZN27CMSG_PASSWORD_CHECK_REQUESTC1Ev @ 0x0527367C
039fac98: mov     w2, #0x4240
039faca4: bl      #0x5c217a0    ; _ZN13LogicPassword14encodePasswordERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi @ 0x039FAD00
039facac: bl      #0x5bdca50    ; _ZN14MessageSubject9singletonEv @ 0x03B83964
039facb8: blr     x8
039facc8: bl      #0x5c217b0    ; _ZN27CMSG_PASSWORD_CHECK_REQUEST8packDataER8CIStream @ 0x05273690
039faccc: bl      #0x5bdca50    ; _ZN14MessageSubject9singletonEv @ 0x03B83964
039facd8: bl      #0x5bdcd10    ; _ZN14MessageSubject7sendMsgEPKvi @ 0x03B842E4
```

### LogicPassword::encodePassword (`0x039FAD00`)

```text
039fad48: bl      #0x5bde040    ; atoi @ 0x00000000
039fad5c: bl      #0x5be1130    ; _ZN7cocos2d12RandomHelper9getEngineEv @ 0x057DA9F8
039fad6c: bl      #0x5beb7f0    ; _ZNSt6__ndk124uniform_int_distributionIiEclINS_23mersenne_twister_engineImLm32ELm624ELm397ELm31ELm2567483615ELm11ELm4294967295ELm7ELm2636928640ELm15ELm4022730752ELm18ELm1812433253EEEEEiRT_RKNS1_10param_typeE @ 0x034616E0
039fad84: bl      #0x5be1130    ; _ZN7cocos2d12RandomHelper9getEngineEv @ 0x057DA9F8
039fad94: bl      #0x5beb7f0    ; _ZNSt6__ndk124uniform_int_distributionIiEclINS_23mersenne_twister_engineImLm32ELm624ELm397ELm31ELm2567483615ELm11ELm4294967295ELm7ELm2636928640ELm15ELm4022730752ELm18ELm1812433253EEEEEiRT_RKNS1_10param_typeE @ 0x034616E0
039fade4: bl      #0x5bdc4a0    ; __stack_chk_fail @ 0x00000000
```

### LogicPassword::decodePassword (`0x039FAF90`)

```text
039fafe4: b       #0x39fb0f8
039fafec: bl      #0x5c217c0    ; _ZN13Second_keyXml11getInstanceEv @ 0x04F0A6D8
039faff4: bl      #0x5c217d0    ; _ZNK13Second_keyXml14getCellByIndexEm @ 0x04F0B1D8
039fb014: b       #0x39fb0f8
039fb050: b       #0x39fb060
039fb078: bl      #0x5bdcd30    ; _ZN7cocos2d11StringUtils6formatEPKcz @ 0x0581BB90
039fb098: bl      #0x5be1a90    ; _ZNSt6__ndk112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm @ 0x05B71304
039fb0c8: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fb0f0: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fb0f4: b       #0x39fb054
039fb138: b       #0x39fb17c
039fb168: bl      #0x5bd84ac
039fb170: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fb180: bl      #0x5bdc460    ; _ZdlPv @ 0x05BD4DE8
039fb198: bl      #0x5bdc4a0    ; __stack_chk_fail @ 0x00000000
039fb1c8: bl      #0x5c217e0    ; _ZN25CMSG_PASSWORD_SET_REQUESTC1Ev @ 0x05273B08
039fb1cc: mov     w2, #0x86a0
```

### LogicPassword send-set helper (`0x039FB1A0`)

```text
039fb1c8: bl      #0x5c217e0    ; _ZN25CMSG_PASSWORD_SET_REQUESTC1Ev @ 0x05273B08
039fb1cc: mov     w2, #0x86a0
039fb1d8: bl      #0x5c217a0    ; _ZN13LogicPassword14encodePasswordERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi @ 0x039FAD00
039fb1e8: bl      #0x5c217a0    ; _ZN13LogicPassword14encodePasswordERKNSt6__ndk112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi @ 0x039FAD00
039fb1f0: bl      #0x5bdca50    ; _ZN14MessageSubject9singletonEv @ 0x03B83964
039fb1fc: blr     x8
039fb20c: bl      #0x5c217f0    ; _ZN25CMSG_PASSWORD_SET_REQUEST8packDataER8CIStream @ 0x05273B20
039fb210: bl      #0x5bdca50    ; _ZN14MessageSubject9singletonEv @ 0x03B83964
039fb21c: bl      #0x5bdcd10    ; _ZN14MessageSubject7sendMsgEPKvi @ 0x03B842E4
```

