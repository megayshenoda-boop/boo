# Gather Audit - 2026-03-26

## Scope

Reviewed:

- `D:\CascadeProjects\codex_lab\gather_bot_v3.py`
- `D:\CascadeProjects\codex_lab\audit_gather_logs.py`
- `D:\CascadeProjects\codex_lab\analyze_bot_plaintext.py`
- `D:\CascadeProjects\codex_lab\analyze_real_gather.py`
- `D:\CascadeProjects\codex_lab\analyze_gather_pcap.py`
- all `D:\CascadeProjects\codex_lab\gather_v3_*.log`

## Automated classification

From `python D:\CascadeProjects\codex_lab\audit_gather_logs.py`:

- `legacy_0091_false_positive=4`
- `provisional_00b8_00b9_chain=5`
- `soft_00b8_only=51`
- `strong_opcode_after_0ce8=1`
- `no_accept=92`

This means the gather history is not "all broken" and not "all proven" either.
Most runs reached some post-`0x0CE8` activity, but only one bot log shows a clean strong opcode after
`0x0CE8` without relying on legacy success rules.

## Hard conclusions

### 1. Old `0x0091` successes were false positives

These logs marked gather success even though the only success-like signal after `0x0CE8` was `0x0091`:

- `gather_v3_20260321_075049.log`
- `gather_v3_20260321_075758.log`
- `gather_v3_20260322_040157.log`
- `gather_v3_20260322_041739.log`

They should not be used as proof that gather really started.

### 2. `0x00B8` by itself is common, but not decisive

There are 51 `soft_00b8_only` runs.
That means the server often accepts enough of the packet flow to answer with `0x00B8`, but the flow still
does not reach a later confirm signal that can be trusted.

Operationally:

- `0x0CE8` is often close enough to be acknowledged.
- the missing piece is not "basic connectivity" or "login".
- the remaining gap is post-ack confirmation depth.

### 3. `0x00B8 + 0x00B9` was a temporary heuristic, not ground truth

These logs were accepted by a temporary rule that treated `0x00B8 + 0x00B9` as success:

- `gather_v3_20260323_032835.log`
- `gather_v3_20260323_033702.log`
- `gather_v3_20260323_035530.log`
- `gather_v3_20260323_040314.log`
- `gather_v3_20260323_050920.log`

That rule was later removed. These runs are useful as "near-success" evidence, but they are not clean
proof under the current stricter standard.

### 4. The cleanest bot-side success in the logs is still `20260322_074726`

`gather_v3_20260322_074726.log` is the only bot log currently classified as `strong_opcode_after_0ce8`.

Key evidence in that log:

- hero `244`
- slot `2`
- tile `(644,576)`
- after `Sent 0x0CE8 ...`
- immediate strong response:
  - `SUCCESS 0x076C`

This is the strongest live bot log because it does not depend on:

- legacy `0x0091` logic
- `0x00B8`-only logic
- `0x00B8 + 0x00B9` chain heuristic

### 5. Search mode is not uniformly failing for the same reason

The logs show multiple distinct failure families:

- wrong/occupied/foreign target context during target probe
- `0x00B8` soft accept with no later confirm
- outright no post-`0x0CE8` accept

So "search is broken" is too broad.
What is broken is reliable transition from searched tile context into a strict confirmed gather state.

### 6. Resource search verification is still narrow

In `gather_bot_v3.py`, `build_search_payload()` explicitly marks only wheat (`resource_type=1`) as verified:

- level 1 -> `01040003`
- level 2 -> `02040003`
- level 5 -> `05040003`

Other resource families are still labeled legacy/unverified in code and should not be treated as solved.

### 7. `working_profile` description was misleading

The CLI help string said `working_profile` disables `0x0840` and setup extras.
The actual code enables both.
This mismatch was corrected on 2026-03-26.

## What is actually missing now

The missing proof is not "what is 0x033E" and not "where are tile coordinates in 0x0CE8".
The missing proof is one current, reproducible run that satisfies the strict standard:

- post-`0x0CE8`
- same target tile
- trusted confirm signal, preferably `0x076C` / `0x0071` / `0x007C`

Until that happens, every new tweak should be judged against this standard only.

## Recommended next step

1. Freeze the search problem for a moment.
2. Reproduce the direct/manual path around the strongest reference:
   - `gather_v3_20260322_074726.log`
3. Do not change more than one variable at a time from that baseline.
4. Only after a strict direct success is reproduced again should auto-search be revisited.

This reduces the problem from "whole gather system" to "strict revalidation of one known-good direct path".
