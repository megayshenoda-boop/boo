# Password Gate Real Order

This note collapses the current static findings into the smallest clean model of
the password gate, without depending on PCAP timing guesses.

## What The Binary Proves

- `LogicPassword::respPasswordInfo` receives the server-side password-info event.
- Inside that handler, the client immediately does:
  - `delayResetPassword()`
  - `loadLocalPassword()`
- `LogicPassword::loadLocalPassword`:
  - checks a local flag first
  - reads local persisted state from `PlayerDefault`
  - key name: `SecondaryPassword`
  - runs `base64Decode(...)`
  - then builds/sends `CMSG_PASSWORD_CHECK_REQUEST`
- The request builder path is explicit:
  - `CMSG_PASSWORD_CHECK_REQUEST::C1`
  - `LogicPassword::encodePassword(password, 1_000_000)`
  - `CMSG_PASSWORD_CHECK_REQUEST::packData(...)`
  - `MessageSubject::sendMsg(...)`
- `LogicPassword::respCheckPassword` then handles the corresponding return path and
  updates local/UI state:
  - `setSecondaryPasswordErrorCount(0)`
  - `decodePassword(packet_value, 1_000_000)`
  - `saveLocalPassword()`
  - `CMainUI::updateSecondaryPassword()`
  - `SecondaryPasswordInputUI::updateState()`

## Real Local Order

The real order exposed by the client is therefore:

1. Server sends password info.
2. Client records the info flag/state.
3. Client loads local persisted `SecondaryPassword`.
4. Client decodes the local persisted value from base64.
5. Client encodes it through `LogicPassword::encodePassword(..., 1_000_000)`.
6. Client packs and sends `CMSG_PASSWORD_CHECK_REQUEST`.
7. Server returns password-check result.
8. Client decodes the returned value, saves local state again, and updates UI/state.

This is a much tighter model than the old packet-only story. The gate is not just
"a packet that happens before gather"; it is a full local state machine.

## What This Means For Gather Analysis

- This does **not** prove that the gather opcode itself directly calls
  `LogicPassword`.
- It **does** prove that the password-check flow is a first-class local subsystem
  that runs after session setup and before later feature/state updates.
- Since the gather sessions that fully succeed consistently include the password
  check flow before `0x0CE8`, the cleanest current interpretation is:
  - gather is being attempted inside a client/session state that is not fully
    equivalent to the real client unless this password gate has settled correctly.

## What The Binary Does Not Yet Prove

- It does not yet prove which gameplay features are hard-gated by the final
  password state.
- It does not yet show a direct march/gather function calling
  `LogicPassword::respCheckPassword` or `loadLocalPassword`.
- It does not yet expose the resource-decoder layer that unwraps the on-disk `LJS`
  XML assets before `tinyxml2` parses them at runtime.

## Important Corrections

- `second_key.xml` is not uniquely special because of the `LJS` wrapper alone.
  A broader APK scan shows `657/657` files under `assets/resource/xml/*.xml`
  begin with `LJS`.
- Raw 8-byte hits for `LogicPassword` function addresses inside `libgame.so`
  should not automatically be read as dispatch tables; at least some of them are
  ordinary ELF symbol-table metadata.

## Bottom Line

The cleanest static conclusion right now is:

- login/session setup is not the main missing piece
- packet ordering tweaks alone are not the main missing piece
- the strongest remaining difference is a real client-side password state machine
  centered on:
  - `SecondaryPassword`
  - `loadLocalPassword/saveLocalPassword`
  - `encodePassword/decodePassword`
  - `CMSG_PASSWORD_CHECK_REQUEST`

## Related Files

- [PASSWORD_LOCAL_STATE_AUDIT_20260327.md](/D:/CascadeProjects/codex_lab/PASSWORD_LOCAL_STATE_AUDIT_20260327.md)
- [LOGICPASSWORD_CALL_PATHS_20260327.md](/D:/CascadeProjects/codex_lab/LOGICPASSWORD_CALL_PATHS_20260327.md)
- [analyze_logicpassword_paths.py](/D:/CascadeProjects/codex_lab/analyze_logicpassword_paths.py)
