# Network-Only `0x1B8B` Derivation Audit

This note records the direct output of the older offline derivation attempts:

- [crack_1b8b_full.py](/D:/CascadeProjects/codex_lab/crack_1b8b_full.py)
- [crack_1b8b_v3.py](/D:/CascadeProjects/codex_lab/crack_1b8b_v3.py)

The goal is narrow:

- answer whether the already captured network fields are enough to derive
  session-valid `0x1B8B`
- separate "not enough data in the capture" from
  "we tried simple network-only transforms and they failed"

## 1. Raw command outputs

Saved command outputs:

- [\_tmp_crack_1b8b_full.out](/D:/CascadeProjects/codex_lab/_tmp_crack_1b8b_full.out)
- [\_tmp_crack_1b8b_v3.out](/D:/CascadeProjects/codex_lab/_tmp_crack_1b8b_v3.out)

These were generated with Scapy cache redirected into the project workspace so
the scripts could run cleanly.

## 2. What `crack_1b8b_full.py` proved

The "full" scanner walked the late local PCAP set and found three sessions with
visible `0x1B8B`:

- `PCAPdroid_25_Mar_07_05_12.pcap`
- `PCAPdroid_25_Mar_07_29_40.pcap`
- `PCAPdroid_27_Mar_09_17_04.pcap`

For those three sessions it extracted:

- visible `0x1B8B`
- server key
- constant `0x1B8A`

But it did **not** recover a usable pair of:

- `access_key`
- and `session_token`

in the same extracted testable records.

So its own summary was:

- sessions with `0x1B8B`: `3`
- sessions with full derivation inputs: `0`

Meaning:

- the late PCAP subset does not, by itself, provide enough visible network
  material for a direct "derive `1B8B` from the wire" attempt

## 3. What `crack_1b8b_v3.py` proved

The older `v3` script found `2` sessions where the network view was richer:

- `PCAPdroid_20_Mar_00_53_10.pcap`
- `PCAPdroid_21_Mar_09_01_57.pcap`

For these it had:

- `0x1B8B`
- session token from `0x001F`
- server key from `0x0038`
- gateway `0x000B`
- and a per-session access key recovered from `0x000B`

So unlike the late scanner, this script did reach the "network-only derivation"
stage with actual candidate inputs.

It then tried families including:

- RC4 with:
  - access key
  - gateway token
  - session token
  - server key bytes
  - combined key material
- direct hashes:
  - `md5`
  - `sha1`
  - `sha256`
- HMACs over combinations of:
  - access key
  - gateway token
  - session token
  - server key bytes
  - IGG ID bytes

The output showed no match for either session.

Practical reading:

- when enough wire-visible fields *are* present, simple network-only transforms
  still do not reproduce `0x1B8B`

## 4. Combined reading

Taken together, the two outputs support a cleaner statement than before:

1. many captures do not expose enough network fields in one place to attempt a
   direct derivation at all
2. in the captures that *do* expose the obvious network inputs, simple
   network-only derivations still fail

So the remaining unknown is not well explained by:

- a trivial hash of session token
- a trivial hash of access key
- a simple access-key/session-key/server-key HMAC
- RC4 with obvious candidate keys
- or a visible fixed transform of the constant `0x1B8A`

## 5. What this means for the current gather diagnosis

This does **not** prove that a derivation from runtime state is the only
possible explanation in the universe.

It does support the current local ranking:

- `0x1B8B` remains the last hard delta in the bot baseline
- and the network captures do not currently support a simple wire-only
  reconstruction of the session-valid value

That fits the binary-backed path already documented in:

- [LOGICPASSWORD_STATE_LAYOUT_20260327.md](/D:/CascadeProjects/codex_lab/LOGICPASSWORD_STATE_LAYOUT_20260327.md)
- [LAST_DELTA_1B8B_BUNDLE_20260327.md](/D:/CascadeProjects/codex_lab/LAST_DELTA_1B8B_BUNDLE_20260327.md)

## 6. Bottom line

The current offline evidence says:

- late PCAPs often do not expose enough wire material to derive `0x1B8B`
- earlier richer PCAPs do expose enough obvious inputs to test simple ideas
- and those simple wire-only derivations still fail

So "just derive it from the PCAP" is no longer the best-supported working model.
