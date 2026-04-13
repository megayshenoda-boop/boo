# Gather PCAP Handoff

## Purpose

This file is a clean handoff for a fresh analyst to review the gather captures
from zero without inheriting stale assumptions.

Use this together with:

- `D:\CascadeProjects\codex_lab\GATHER_MARCH_FINDINGS.md`
- `D:\CascadeProjects\codex_lab\EVIDENCE_RULES.md`
- `D:\CascadeProjects\codex_lab\WORKFLOW_METHOD.md`

The goal is to re-evaluate the gather workflow from packet evidence only.

## Canonical Gather Captures

Use these files first. They are the strongest documented gather references so far.

1. `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_08_43_35.pcap`
   - searched target
   - explicit hero change
   - accepted gather
   - hero id observed as `255`
   - target tile `(682, 570)`
2. `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_09_00_24.pcap`
   - same target as previous file
   - explicit hero change
   - accepted gather
   - hero id observed as `244`
   - target tile `(682, 570)`
3. `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_10_36_08.pcap`
   - accepted gather
   - no visible fresh `0x0323`
   - confirms hero state can already be established before send
4. `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_11_00_05.pcap`
   - searched target
   - explicit hero change
   - accepted gather
   - hero id observed as `241`
5. `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_12_18_13.pcap`
   - explicit search path
   - accepted gather
   - confirms `0x033E / 0x033F` search-family behavior
6. `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_15_28_47.pcap`
   - full payload enabled
   - explicit hero change
   - accepted gather
   - hero id observed as `237`
   - target tile `(672, 605)`
7. `D:\CascadeProjects\codex_lab\PCAPdroid_21_Mar_11_05_21.pcap`
   - manual direct gather from map
   - no search
   - no visible `0x0323`
   - accepted gather
   - hero id observed as `255`
   - target tile `(665, 594)`
8. `D:\CascadeProjects\codex_lab\PCAPdroid_21_Mar_11_22_28.pcap`
   - full map-entry to search to accepted gather
   - no visible `0x0323`
   - accepted gather
   - hero id observed as `255`
   - target tile `(638, 568)`

## Stable Packet-Level Facts

These points are repeatedly supported by capture evidence.

- `0x0CE8` is the actual gather send packet in accepted runs.
- Accepted gather runs are validated most strongly by:
  - `0x00B8`
  - `0x0071`
  - `0x076C`
  - `0x007C`
- `0x006E` is consistently tied to tile selection / tile view targeting.
- `0x033E / 0x033F` behave like search request / search response in search-based runs.
- `0x0323` appears when the operator changes hero/formation, but it is not present in
  every accepted gather run.
- Therefore `0x0323` is currently best treated as conditional hero/formation context,
  not a mandatory gather step.
- Multiple accepted `0x0CE8` packets use the same outer encrypted size:
  - encrypted payload `50B`
  - recovered plaintext `46B`
- Several clean accepted gather captures still do not include `0x0038`.

## Strong Comparisons

These comparisons are especially useful and should be reviewed first.

### Same tile, different hero

- `PCAPdroid_20_Mar_08_43_35.pcap`
- `PCAPdroid_20_Mar_09_00_24.pcap`

Why useful:

- same target tile
- different selected hero
- lets the analyst isolate hero-linked changes from tile-linked changes

### Explicit hero change vs already-selected hero

- explicit hero change:
  - `PCAPdroid_20_Mar_08_43_35.pcap`
  - `PCAPdroid_20_Mar_09_00_24.pcap`
  - `PCAPdroid_20_Mar_11_00_05.pcap`
  - `PCAPdroid_20_Mar_15_28_47.pcap`
- no visible fresh hero change:
  - `PCAPdroid_20_Mar_10_36_08.pcap`
  - `PCAPdroid_21_Mar_11_05_21.pcap`
  - `PCAPdroid_21_Mar_11_22_28.pcap`

Why useful:

- tests whether hero state is pushed by a visible packet in that run
- helps separate required flow from already-established client state

### Search-based vs manual direct gather

- search-based:
  - `PCAPdroid_20_Mar_08_43_35.pcap`
  - `PCAPdroid_20_Mar_12_18_13.pcap`
  - `PCAPdroid_21_Mar_11_22_28.pcap`
- manual direct from map:
  - `PCAPdroid_21_Mar_11_05_21.pcap`

Why useful:

- confirms search is optional for accepted gather
- narrows what is truly part of the send path vs only part of target discovery

## Current Best Reading

The strongest current outer gather flow is:

1. optional map/UI prep
2. optional search via `0x033E / 0x033F`
3. tile selection via `0x006E`
4. optional hero/formation change via `0x0323`
5. final gather send via `0x0CE8`
6. validate success via `0x00B8`, `0x0071`, `0x076C`, `0x007C`

## What Is Still Open

These points should be treated as unresolved unless the analyst proves them again.

- the exact semantic field layout of plaintext `0x0CE8`
- which plaintext bytes are tied to:
  - current tile
  - current hero
  - session-local state
  - locally prepared UI state
- whether there is one normalized plaintext layout across all accepted runs or
  whether more than one gather variant exists
- whether some values echoed in post-send packets are source-state echoes rather than
  true input fields to the send packet

## Fresh Analyst Rules

- Work evidence-first. Do not start from opcode labels or old guesses.
- Separate:
  - confirmed from packet evidence
  - strong inference
  - unknown
- Do not treat `got response` as `success`.
- Treat accepted gather only when the validation packet family appears after send:
  - `0x00B8`
  - `0x0071`
  - `0x076C`
  - `0x007C`
- Prefer cross-capture comparison over single-capture interpretation.

## Ready Prompt

Use this prompt for a fresh review:

```text
Review the gather PCAPs from zero using evidence-first reasoning only.

Primary references:
- D:\CascadeProjects\codex_lab\GATHER_PCAP_HANDOFF.md
- D:\CascadeProjects\codex_lab\GATHER_MARCH_FINDINGS.md
- D:\CascadeProjects\codex_lab\EVIDENCE_RULES.md

Canonical captures:
- D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_08_43_35.pcap
- D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_09_00_24.pcap
- D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_10_36_08.pcap
- D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_11_00_05.pcap
- D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_12_18_13.pcap
- D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_15_28_47.pcap
- D:\CascadeProjects\codex_lab\PCAPdroid_21_Mar_11_05_21.pcap
- D:\CascadeProjects\codex_lab\PCAPdroid_21_Mar_11_22_28.pcap

Tasks:
1. Reconstruct the chronological packet flow for each accepted gather run.
2. Mark each conclusion as one of:
   - Confirmed
   - Strong inference
   - Unknown
3. Build a comparison matrix for:
   - searched target vs manual direct target
   - explicit hero change vs already-selected hero
   - same tile with different heroes
4. Extract the strongest repeated invariants across accepted runs.
5. Identify the smallest remaining unresolved point in the gather workflow.

Constraints:
- Do not rely on legacy opcode names unless capture evidence supports them.
- Do not assume any field meaning inside `0x0CE8` without cross-capture support.
- Keep the output short, factual, and packet-evidence driven.
```

## Notes From Failed Replay Attempts

These are useful only as negative evidence, not as proof of accepted layout.

- local replay probes reached the correct encrypted size for `0x0CE8`:
  - `50B` encrypted
  - `46B` plaintext
- after codec-header fixes, replay failures shifted away from obvious framing errors
- failed runs produced responses like:
  - `0x201A`
  - `0x026D`
- accepted validation packets did not appear in those failed replay attempts

This means the remaining uncertainty is in gather-specific semantics/state, not merely
outer packet length.

## Extra Negative Evidence

One later live replay test explicitly forced `Hero 244` before the gather send.

Observed outcome:

- server returned `0x026D` after the explicit hero-selection step
- later `0x0CE8` received follow-up responses such as:
  - `0x0091`
  - `0x0080`
  - `0x0082`
- accepted gather validation still did **not** appear:
  - no `0x00B8`
  - no `0x0071`

Why this matters:

- it is another clean reminder that server responses after `0x0CE8` are not enough
  to call the run accepted
- it strengthens the working view that the remaining blocker is state/context
  correctness, not only outer packet framing
