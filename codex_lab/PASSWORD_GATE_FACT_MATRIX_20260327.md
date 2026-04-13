# Password Gate Fact Matrix (2026-03-27)

## Purpose

This matrix consolidates the current local evidence around the remaining gather blocker.

It answers four questions:

1. what is proven by live bot runs
2. what is proven by local PCAP references
3. what is proven by local `lords_bot` reverse-engineering references
4. which older explanations are now weaker or ruled out

## A. Proven by live bot runs

### 1. Login is not the current blocker

Proven by repeated current runs such as:

- [gather_v3_20260326_145904.log](/D:/CascadeProjects/codex_lab/gather_v3_20260326_145904.log)
- [gather_v3_20260327_044831.log](/D:/CascadeProjects/codex_lab/gather_v3_20260327_044831.log)

What is proven:

- session opens successfully
- `server_key` is extracted
- search works
- target tile is selected
- `0x0CE8` is sent

So the current blocker is not "cannot log in".

### 2. Current no-`1B8B` flow reaches march send but not real gather

Observed repeatedly in current live runs:

- no valid pre-`0x0CE8` `0x1B8B`
- `0x0CE8` is still sent
- result is either:
  - `no_accept`
  - or `soft-only`

Soft-only means:

- `0x00B8` and sometimes `0x00B9`
- but no `0x0071`
- no `0x076C`
- no `0x007C`
- no visible in-game wheat gather

### 3. Stale/guessed `1B8B` breaks the session family

Observed in:

- [gather_v3_20260326_032120.log](/D:/CascadeProjects/codex_lab/gather_v3_20260326_032120.log)
- [gather_v3_20260326_150025.log](/D:/CascadeProjects/codex_lab/gather_v3_20260326_150025.log)
- [gather_v3_20260326_150027.log](/D:/CascadeProjects/codex_lab/gather_v3_20260326_150027.log)
- [gather_v3_20260326_150029.log](/D:/CascadeProjects/codex_lab/gather_v3_20260326_150029.log)
- [gather_v3_20260326_150031.log](/D:/CascadeProjects/codex_lab/gather_v3_20260326_150031.log)

What is proven:

- random/stale/heuristic `1B8B` does not act like a harmless optional packet
- wrong `1B8B` can abort the session before the gather stage completes

## B. Proven by local PCAP references

### 1. Successful gather references consistently include pre-`0x0CE8` `1B8B`

Supported by:

- [PCAP_20PLUS_AUDIT_20260326.md](/D:/CascadeProjects/codex_lab/PCAP_20PLUS_AUDIT_20260326.md)
- [SUCCESS_PCAP_VS_SOFT_LOGS_20260327.md](/D:/CascadeProjects/codex_lab/SUCCESS_PCAP_VS_SOFT_LOGS_20260327.md)

What is proven:

- from the audited Mar 20 -> Mar 24 window, successful gather references consistently carry `0x1B8B`
- current recent soft-only automation runs do not

### 2. `1B8B` is stronger than many older "must always" assumptions

What the PCAP window weakened:

- direct `0x0023` is not a universal requirement
- `0x01D6` is not a universal requirement
- search is not a universal requirement
- troop count is not universal
- one fixed send-order is not universal

What stayed strong:

- successful references still include `1B8B`
- successful references still end with real post-`0x0CE8` confirmations

### 3. The raw `22B` payload is not best treated as opaque anymore

Supported by:

- [PCAP_1B8B_AUDIT_20260326.md](/D:/CascadeProjects/codex_lab/PCAP_1B8B_AUDIT_20260326.md)
- [PCAP_1B8B_DECODED_AUDIT_20260326.md](/D:/CascadeProjects/codex_lab/PCAP_1B8B_DECODED_AUDIT_20260326.md)

What is proven:

- raw `1B8B` payloads are `22B`
- decoding with the session `CMsgCodec` yields structured `18B` plaintext
- the plaintext has a rigid internal pattern
- the whole plaintext is effectively determined by a smaller `seed32`

What is not proven:

- the live generator of that `seed32`

## C. Proven by local `lords_bot` references

### 1. `1B8B` belongs to a password/security message family

Supported by:

- [constructor_map.txt](/D:/CascadeProjects/lords_bot/constructor_map.txt)
- [opcode_map.txt](/D:/CascadeProjects/lords_bot/opcode_map.txt)
- [PROTOCOL_REFERENCE.txt](/D:/CascadeProjects/lords_bot/PROTOCOL_REFERENCE.txt)
- [LORDS_BOT_PASSWORD_REF_AUDIT_20260327.md](/D:/CascadeProjects/codex_lab/LORDS_BOT_PASSWORD_REF_AUDIT_20260327.md)

What is proven:

- `0x1B8A = CMSG_PASSWORD_INFO`
- `0x1B8B = CMSG_PASSWORD_CHECK_REQUEST`
- `0x1B8C = CMSG_PASSWORD_CHECK_RETURN`
- related request/return family also includes reset/set messages

### 2. The client has explicit password logic and password UI surfaces

Supported by:

- [elf_analysis.txt](/D:/CascadeProjects/lords_bot/elf_analysis.txt)
- [PASSWORD_CLIENT_STATE_AUDIT_20260326.md](/D:/CascadeProjects/codex_lab/PASSWORD_CLIENT_STATE_AUDIT_20260326.md)

What is proven:

- `LogicPassword::encodePassword`
- `LogicPassword::decodePassword`
- `LogicPassword::respCheckPassword`
- `LogicPassword::respPasswordInfo`
- secondary-password UI classes exist in the client resources/symbols

### 3. Local reverse-engineering points to randomized client-side generation

Supported by:

- [PASSWORD_CLIENT_STATE_AUDIT_20260326.md](/D:/CascadeProjects/codex_lab/PASSWORD_CLIENT_STATE_AUDIT_20260326.md)

Current local reading from that audit:

- `LogicPassword::encodePassword` uses `atoi(password_string)`
- plus random values
- plus a high-range multiplier component

Practical implication:

- old `1B8B` replay should fail even when the underlying password state is unchanged

## D. Older explanations that are now weaker

These are weaker because they were tested directly and still ended in soft-only or no-accept:

- send-order alone
- `17A3` presence alone
- `17A4` presence alone
- `0x01D6` alone
- 4 troops vs 5 troops alone
- slot `1` vs fallback slots alone
- heartbeat wait alone

The strongest example is:

- [gather_v3_20260327_044831.log](/D:/CascadeProjects/codex_lab/gather_v3_20260327_044831.log)

That run combined:

- old strong-baseline order
- `0x01D6`
- 4 troops
- slot fallbacks
- heartbeat wait `1.5`

and still stopped at soft-only.

## E. Best current local conclusion

The safest current local conclusion is:

1. current gather failure is not best explained by login failure
2. current gather failure is not best explained by surface order/setup differences alone
3. the strongest surviving difference between real success and current soft-only automation remains valid pre-`0x0CE8` `0x1B8B`
4. local reverse-engineering and local PCAPs both point to a password/security state around that gate

## F. What remains unknown

Still unknown locally:

- the exact live generator for the `seed32` that determines decoded `1B8B`
- whether one more hidden pre-`0x0CE8` state input exists besides the password gate
- whether the current client state depends on runtime-only material not visible in static prefs/files

## G. Operational takeaway

The cleanest next analysis path is no longer broad gather experimentation.

The clean path is:

- keep recent gather runs as proof that non-password deltas were exercised
- treat `1B8B` as the dominant unresolved gate
- keep local notes synchronized so older assumptions do not reopen closed branches
