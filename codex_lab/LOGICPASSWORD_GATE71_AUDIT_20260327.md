# LogicPassword Gate71 Access Audit

This note tracks explicit reads/writes of `this + 0x71` in the known local password flow regions.

## respPasswordInfo (`0x039FA2A0`)

- `0x039FA2C4`: `strb w9, [x0, #0x71]`

## respCheckPassword (`0x039FA52C`)

- No direct `#0x71` access in the scanned region.

## respUpdatePassword (`0x039FA85C`)

- `0x039FA88C`: `strb w9, [x0, #0x71]`

## respResetPassword (`0x039FABCC`)

- No direct `#0x71` access in the scanned region.

## loadLocalPassword (`0x039FB2C8`)

- `0x039FB2EC`: `ldrb w8, [x0, #0x71]`

## saveLocalPassword (`0x039FC4E4`)

- No direct `#0x71` access in the scanned region.

## wrapper_before_send (`0x039FAC34`)

- No direct `#0x71` access in the scanned region.

## send_check_helper (`0x039FAC60`)

- No direct `#0x71` access in the scanned region.

## Reading

- Direct `#0x71` accesses were found only in the regions listed above.
- This helps separate the true gate readers/writers from nearby UI/update helpers.
- The write sites are not equivalent:
  - `respPasswordInfo` writes `this+0x71` from a decoded object byte loaded by
    `ldrb w9, [x1, #4]`
  - `respUpdatePassword` writes `this+0x71 = 1` directly

## Key Micro-Disassembly

### `respPasswordInfo`

```text
039fa2ac: ldrb    w9, [x1, #4]
039fa2b8: strb    w8, [x0, #0x70]
039fa2c4: strb    w9, [x0, #0x71]
```

### `respUpdatePassword`

```text
039fa878: mov     w9, #1
039fa88c: strb    w9, [x0, #0x71]
```

## Notes

- This is a local disassembly audit only.
- It does not prove runtime values by itself.
