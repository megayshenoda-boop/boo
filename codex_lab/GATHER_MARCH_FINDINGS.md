# Gather March Findings

## Scope

This file tracks the live `gather / start march` path with isolated captures, with
special focus on:

- target search / target coordinate resolution
- single-hero selection before march
- `0x0CE8` start-march behavior
- server push packets that confirm gather state

Current baseline below is from one clean operator-controlled capture where:

- one target was searched
- one gather march was sent
- one hero only was intentionally selected by the operator
- no extra hero swaps or second march were mixed into the file

## Isolated single-hero gather capture

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_08_43_35.pcap`

Operator note:

- searched one target
- sent one gather march
- selected one hero only
- operator-identified hero name: `Omar Mukhtar`

## Confirmed chronological flow

The clean sequence in this capture was:

1. target lookup request:
   - `C2S 0x033E payload=01040003`
2. server returned one target position:
   - `S2C 0x033F payload=01aa023a02040003`
3. client sent a map-selection style request on the returned tile:
   - `C2S 0x006E payload=aa023a0201`
4. immediately before march send, the client sent one short hero-related packet:
   - `C2S 0x0323 payload=000100ff000000`
5. the actual gather march was then sent as encrypted:
   - `C2S 0x0CE8 payload=e293247cb529142da94556ad8a78aa33c7efe09549148fde0559dd56ff8d921ab2611ae0663f503eaca2ac79c1eee1954914`
6. immediate server pushes after `0x0CE8` included:
   - `S2C 0x00AA payload=01000000ff000000680000000400bd0105050000000000000000e7040000050000002d9700000a0000000a0000000a0000000a000000191f00000000191e000000001919000000001921000000001925000000001f000000000b0000000400000007000000000000000000000068000000`
   - `S2C 0x00B8 payload=010100000001ff000000`
   - `S2C 0x0071 payload=02d80800b60000000100ed0273220000000001b00300008d023702aa023a024203000000000e003130303032303834393230382c30b600000000000000000000000000000000`
   - `S2C 0x076C payload=010002d80800b60000000100ed0273220000000001b00300008d023702aa023a024203000000000e003130303032303834393230382c3001000100ff000000680005002d970000673c67002d970000040501000000010000000000000000000000000000000000000000000001000000000000000001`
   - `S2C 0x007C payload=380c0000380c0000aa023a02010001000000302a0000`
7. later in the same capture, the march ended / was cleared:
   - `S2C 0x007F payload=02d80800b60000000001000000000000000000`
   - `S2C 0x0070 payload=02d80800b600000000`

## Confirmed conclusions

- `0x0CE8` is the live `start march / gather` action path in this capture.
- The capture contains one accepted gather march, not just screen noise:
  - immediate march-state pushes appeared after `0x0CE8`
  - collect-state push `0x007C` appeared
  - march-end cleanup `0x007F` and `0x0070` appeared later
- The target coordinates returned by the server were:
  - `x = 0x02AA = 682`
  - `y = 0x023A = 570`
- Those same coordinates reappear in later march-state packets:
  - in `0x0071`
  - in `0x076C`
  - in `0x007C`

## Strong hero-related reading

Because the operator intentionally selected one hero only before sending the march,
the strongest current reading for the hero part of the flow is:

- `C2S 0x0323 payload=000100ff000000`
  - this short packet is tightly coupled to the isolated single-hero selection
- `S2C 0x00AA`
  - this does **not** look like the older full-roster `HERO_INFO` dump
  - in this march path it looks like a single-hero or single-context hero sync
- `S2C 0x00B8 payload=010100000001ff000000`
  - this likely echoes expedition / queue hero context for the same selection

The strongest current hero-id mapping from this capture is:

- operator-selected hero `Omar Mukhtar` -> current march-path hero id `255`

Why this is the strongest current reading:

- the selection was isolated to one hero only
- `0x0323` was sent immediately before `0x0CE8`
- `0x00AA` followed immediately after `0x0CE8`
- both `0x00AA` and `0x00B8` contain `ff000000` / `255`

## Strong march-state reading from `0x076C`

The `0x076C` payload is especially useful because it appears to bundle:

- march identity
- target coordinates
- selected hero context
- march type / gather context

From this capture, `0x076C` clearly includes:

- returned target coordinates `aa023a02` -> `(682, 570)`
- selected hero id `ff000000` -> `255`

This means `0x076C` is currently the strongest post-send packet for validating:

- where the march was sent
- which hero context was attached

## What is clear vs not yet clear

### Clear now

- the file contains one real gather march
- `0x0CE8` is the actual send opcode for that gather march
- target coordinate lookup happened before the march send
- the chosen tile was `(682, 570)`
- a single hero context was attached to the march
- the strongest current hero id for that isolated selection is `255`
- the gather path produced:
  - `0x0071`
  - `0x076C`
  - `0x007C`
  - later `0x007F` / `0x0070`

### Not clear yet

- the exact plaintext structure inside this specific `0x0CE8`
  - this capture does not include `0x0038`, so no session server key was captured
- the exact semantic name of `0x0323` in this path
  - legacy opcode maps label it as `HERO_SOLDIER_RECRUIT_REQUEST`
  - but in this flow it behaves like a hero-selection-adjacent packet
- whether `0x00AA` here is:
  - single selected hero sync
  - single march hero sync
  - or a compact hero-state packet with a different field layout than the older roster dump
- whether `0x033E / 0x033F` are truly monster-position only
  - legacy labels call them monster-position request/response
  - in this gather capture they behave like target-coordinate lookup before march

## Practical baseline for next captures

If the goal is to close gather/march cleanly, the next best isolated captures are:

1. same gather flow, but with a different single hero only
2. same gather flow, same target type, but without changing hero
3. one capture that includes fresh login so `0x0038` appears before `0x0CE8`

That combination should settle:

- whether hero id `255` is really the selected hero id
- the exact meaning of `0x0323`
- the decryptable plaintext layout of `0x0CE8`

## Second isolated gather on the same tile with a different single hero

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_09_00_24.pcap`

Operator note:

- same gather target as the previous capture
- same resource/tile path
- one hero only was selected again
- operator-identified hero name: `Mohamed Al-Fatih`

## Confirmed comparison vs the previous capture

This second capture is especially strong because the operator intentionally kept the
target the same and changed only the hero.

Observed hero-adjacent send before march:

- previous capture:
  - `C2S 0x0323 payload=000100ff000000`
- current capture:
  - `C2S 0x0323 payload=000100f4000000`

Observed single-hero sync immediately after `0x0CE8`:

- previous capture:
  - `S2C 0x00AA payload=01000000ff000000...`
  - `S2C 0x00B8 payload=010100000001ff000000`
- current capture:
  - `S2C 0x00AA payload=01000000f4000000...`
  - `S2C 0x00B8 payload=010100000001f4000000`

Observed march-state packet:

- previous capture:
  - `S2C 0x076C ... ff000000 ... aa023a02 ...`
- current capture:
  - `S2C 0x076C ... f4000000 ... aa023a02 ...`

## Confirmed conclusions from the two-capture comparison

- the gather target stayed the same between the two captures:
  - tile bytes stayed `aa023a02`
  - so the target tile remained `(682, 570)`
- the hero id changed cleanly while the target stayed fixed:
  - previous isolated hero id: `255`
  - current isolated hero id: `244`
- this strongly upgrades the hero-id reading:
  - `Omar Mukhtar` -> `255`
  - `Mohamed Al-Fatih` -> `244`

## Strong cross-capture conclusion

Across the two isolated captures on the same tile:

- `0x0323` changed from `ff000000` to `f4000000`
- `0x00AA` changed from `ff000000` to `f4000000`
- `0x00B8` changed from `ff000000` to `f4000000`
- `0x076C` changed from `ff000000` to `f4000000`
- the tile coordinate bytes stayed `aa023a02`

This means the current strongest reading is now:

- hero selection is indeed flowing into the march path
- the changing 32-bit value is the selected hero id
- `0x076C` can be used as a post-send validator for:
  - target tile
  - selected hero id

## Updated practical baseline

For isolated gather captures, the strongest current validation chain is now:

1. optional target lookup:
   - `0x033E`
   - `0x033F`
2. tile selection request:
   - `0x006E`
3. single-hero selection-adjacent send:
   - `0x0323`
4. encrypted gather send:
   - `0x0CE8`
5. validate selected hero id from:
   - `0x00AA`
   - `0x00B8`
   - `0x076C`
6. validate gather tile from:
   - `0x0071`
   - `0x076C`
   - `0x007C`

## Third gather capture from fresh open with a single gather send

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_10_36_08.pcap`

Operator note:

- fresh open / fresh recording
- one gather only
- no hero swap during the capture
- no second march

## What changed in this third capture

This file is useful because it confirms a second valid gather path shape:

- no `0x033E / 0x033F` search lookup appeared
- no `0x0323` hero-selection-adjacent packet appeared
- no `0x00AA` compact hero packet appeared
- but the actual gather send still happened:
  - `C2S 0x0CE8 payload=a8ba0d9d2f0d6abf03d331bd1625cda65bfd8585d50418ce9949ba46639df50a2e717df0fa0d373030b2cb695dfe8685d504`

Immediately around the send, the clean sequence was:

1. one direct map-selection style request:
   - `C2S 0x006E payload=8d02350201`
2. one accepted gather send:
   - `C2S 0x0CE8 ...`
3. one post-send hero-context echo:
   - `S2C 0x00B8 payload=010100000001ff000000`
4. one gather state packet:
   - `S2C 0x0071 payload=e0d80800b60000000100ed0273220000000001b00300008d0237028d0235026f00000000000e003130303032303930383936342c30b600000000000000000000000000000000`
5. one strong march validation packet:
   - `S2C 0x076C payload=0100e0d80800b60000000100ed0273220000000001b00300008d0237028d0235026f00000000000e003130303032303930383936342c3001000100ff000000680005002d970000673c67002d970000040501000000010000000000000000000000000000`
6. one collect-state packet:
   - `S2C 0x007C payload=380c0000380c00008d023502010001000000302a0000`
7. later cleanup:
   - `S2C 0x007F ...`
   - `S2C 0x0070 ...`

## Confirmed conclusions from the third capture

- a valid gather march can be sent **without** a new visible `0x0323` in the same file
- a valid gather march can also happen **without** `0x00AA`
- the selected hero context still survives into post-send validation packets:
  - `0x00B8` contains `ff000000`
  - `0x076C` contains `ff000000`
- this strongly suggests the selected hero can be reused from existing client state and
  does not have to be re-announced on every gather send

## Target reading in the third capture

The strongest current reading for the actual gather tile in this file is:

- `x = 0x028D = 653`
- `y = 0x0235 = 565`

Why this is the strongest reading:

- the direct tile-selection request was:
  - `0x006E payload=8d02350201`
- the same tile bytes reappear later in:
  - `0x0071`
  - `0x076C`
  - `0x007C`

The extra pair `8d023702` that also appears in `0x0071 / 0x076C` is therefore more
likely to be related to march-state context than the final selected gather tile itself.

## What the third capture upgrades

This third file upgrades the gather model in an important way:

- `0x0323` is **not** strictly required to appear in every valid gather file
- `0x00AA` is **not** strictly required to appear in every valid gather file
- `0x00B8` and especially `0x076C` remain the strongest post-send validators for:
  - selected hero id
  - actual gather tile

The current strongest operational reading is now:

- if a new hero is explicitly changed during the flow:
  - expect `0x0323`
  - often `0x00AA`
- if hero state is already established:
  - gather can still succeed with only:
    - `0x0CE8`
    - `0x00B8`
    - `0x0071`
    - `0x076C`
    - `0x007C`

## Remaining blocker

Even this cleaner fresh capture still does **not** contain `0x0038`.

So the remaining unresolved point is still the same:

- we can validate hero + tile strongly
- but we still cannot decrypt the specific plaintext inside this exact live `0x0CE8`
  from this file alone because no session `server_key` packet was captured here

## Fourth gather capture with explicit formation selection before send

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_11_00_05.pcap`

Operator note:

- target type chosen manually from the resource panel
- client auto-centered on the searched resource tile
- one explicit hero/formation was chosen in the `1..5` formation selector UI
- operator-identified hero used for this run: `Salah ad-Din`

## Confirmed chronological flow in the fourth capture

The clean sequence around the actual send was:

1. map-selection style request on a searched tile:
   - `C2S 0x006E payload=8d02350201`
2. one explicit hero-selection-adjacent send:
   - `C2S 0x0323 payload=000100f1000000`
3. one accepted gather send:
   - `C2S 0x0CE8 payload=2174c33f736ca759efb2f8df4ac0004003005ee789e545acc5a87b243f7c3c687290b492a6e8fa522853020b011f4fe789e5`
4. immediate hero-context sync:
   - `S2C 0x00AA payload=01000000f1000000680000000400bd0105050000000000000000d904000005000000f1a000000a0000000a0000000a0000000a000000192f00000000192100000000191e00000000191900000000191f000000001f00000000000000000a000000020000`
   - `S2C 0x00B8 payload=010100000001f1000000`
5. post-send march validation:
   - `S2C 0x0071 payload=11d90800b60000000100ed0273220000000001290300008d0237028d0235027d01000000000e003130303032303930383936342c30b600000000000000000000000000000000`
   - `S2C 0x076C payload=010011d90800b60000000100ed0273220000000001290300008d0237028d0235027d01000000000e003130303032303930383936342c3001000100f100000068000500f1a000002dcf6b00f1a00000040501000000010000000000000000000000000000`
6. collect-state push:
   - `S2C 0x007C payload=ce060000ce0600008d023502010001000000302a0000`
7. later cleanup:
   - `S2C 0x007F payload=11d90800b60000000001000000000000000000`
   - `S2C 0x0070 payload=11d90800b600000000`

## What this fourth capture proves

This file is the strongest current bridge between the UI flow and the wire flow:

- choosing a formation/hero in the `1..5` selector does produce a visible
  hero-selection-adjacent packet:
  - `0x0323`
- the chosen hero then propagates into all post-send validation packets:
  - `0x00AA`
  - `0x00B8`
  - `0x076C`
- the chosen tile still appears independently in:
  - `0x006E`
  - `0x0071`
  - `0x076C`
  - `0x007C`

## Strongest current hero reading after four captures

The currently strongest isolated march-path hero ids are now:

- `Omar Mukhtar` -> `255`
- `Mohamed Al-Fatih` -> `244`
- `Salah ad-Din` -> `241`

Why the `Salah ad-Din` reading is strong:

- operator explicitly chose the hero through the formation UI in this run
- `0x0323` carried `f1000000`
- `0x00AA` echoed `f1000000`
- `0x00B8` echoed `f1000000`
- `0x076C` echoed `f1000000`

## Updated operational model

The current best model for the gather UI flow is now:

1. choose resource family / level in the search panel
2. client auto-centers on the resulting map tile
3. tile gets selected with:
   - `0x006E`
4. if a new formation/hero choice is made, client sends:
   - `0x0323`
5. client sends gather:
   - `0x0CE8`
6. validate selected hero from:
   - `0x00AA`
   - `0x00B8`
   - `0x076C`
7. validate selected tile from:
   - `0x006E`
   - `0x0071`
   - `0x076C`
   - `0x007C`

## Search-only capture without march send

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_11_27_27.pcap`

Operator note:

- search only
- no hero selection
- no march send

## What actually appeared in the search-only file

This file did **not** contain:

- `0x033E`
- `0x033F`
- `0x0323`
- `0x0CE8`
- `0x00AA`
- `0x00B8`
- `0x076C`
- `0x0071`
- `0x007C`

The visible resource-search activity in this file was instead:

1. map/view setup:
   - `C2S 0x0CEB payload=2577c0b0323071800756335e05df`
2. first tile selection:
   - `C2S 0x006E payload=8d02370201`
3. immediate map refresh around that tile:
   - `S2C 0x0076`
   - `S2C 0x0077`
   - `S2C 0x0078`
   - `S2C 0x007A`
4. later second tile selection:
   - `C2S 0x006E payload=8d02350201`
5. second map refresh:
   - `S2C 0x0076`
   - `S2C 0x0077`
   - `S2C 0x0078`
   - `S2C 0x007A`

## Strong conclusion from the search-only file

This upgrades the search model in an important way:

- `0x033E / 0x033F` are **not guaranteed** to appear in every operator-visible
  "search" flow
- a pure operator-visible search may reduce on the wire to:
  - map/view enable
  - direct tile selection with `0x006E`
  - map sync packets `0x0076 / 0x0077 / 0x0078 / 0x007A`

So the current strongest reading is:

- `0x033E / 0x033F` are still a valid search/lookup family when the client asks
  the server for a fresh target position
- but some "search-only" UI flows can reuse or resolve directly to a selected
  tile without showing `0x033E / 0x033F` in the capture

## Practical update

For gather automation, the most reliable baseline remains:

- treat `0x006E` as the real "selected target tile" signal
- treat `0x0323` as optional hero-selection-adjacent
- treat `0x0CE8` as the actual send

And for search itself:

- do not assume `0x033E / 0x033F` must always exist
- do assume `0x006E` plus map sync can be enough to represent the resolved

## First live replay attempt using the `lords_bot`-style gather payload

Live probe:

- `D:\CascadeProjects\codex_lab\gather_live_wheat2_lordsbot_20260320_073335.log`

Probe settings:

- fresh login through gateway and game server
- extracted live `server_key = 0xF9AB88A9`
- explicit search request:
  - `0x033E payload=02040003`
- explicit tile select:
  - `0x006E payload=69023a0201`
- explicit hero select:
  - `0x0323 payload=000100ff000000`
- gather send used the `lords_bot`-style 62-byte plaintext builder

Observed sequence:

1. login succeeded
2. live session key was captured
3. target lookup response appeared:
   - `TARGET_LOOKUP_RESP count=2 payload=0269023a02040003`
4. client selected the returned tile:
   - `0x006E payload=69023a0201`
5. client selected hero `255`:
   - `0x0323 payload=000100ff000000`
6. client sent encrypted gather:
   - `0x0CE8 payload[lords_bot]=011e62a648170000000000000205c9000000d4000000ce000000d8000000e0000000d30000000200000000000000000000ed027322000000000000000000`
7. no strong gather-success signals appeared afterward

## Conclusion from the live replay attempt

- the surrounding gather flow is valid and understood:
  - login
  - target lookup
  - tile select
  - hero select
- but the direct replay still failed at the actual send step
- this means the remaining blocker is now very narrow:
  - the exact plaintext structure inside `0x0CE8`
- the simpler `lords_bot` builder is therefore **not yet sufficient** for a
  successful live gather replay on this account/session

## Practical status after the live replay attempt

Operationally, gather is now in this state:

- search path: understood
- target tile resolution: understood
- hero-selection propagation: understood
- post-send validation packets: understood
- direct send plaintext inside `0x0CE8`: still unresolved

So the path is close to finished for automation logic, but the actual encrypted
send builder still needs one final breakpoint or clean decrypted capture to
settle the internal `0x0CE8` layout.
  search result on the wire

## Fifth gather capture with explicit wheat level 2 search

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_12_18_13.pcap`

Operator note:

- fresh login / fresh recording
- searched `wheat level 2`
- one gather march only
- no second march

## Confirmed chronological flow in the fifth capture

This file cleanly contains:

1. map/view setup:
   - `C2S 0x0CEB payload=1121962f5da52256e8fd6c96664a`
2. one preliminary tile selection during map centering:
   - `C2S 0x006E payload=8d02370201`
3. explicit search lookup request:
   - `C2S 0x033E payload=02040003`
4. explicit search lookup response:
   - `S2C 0x033F payload=0283021802040003`
5. tile selection on the returned search result:
   - `C2S 0x006E payload=8302180201`
6. accepted encrypted gather send:
   - `C2S 0x0CE8 payload=d0b106c4adb8b673b1f99c8d96ed6441df232ab555d849fe19951776e341583aaeadd0c07a139efeb46e6659dd222bb555d8`
7. post-send validation:
   - `S2C 0x00B8 payload=010100000001ff000000`
   - `S2C 0x0071 payload=9dd90800b60000000100ed0273220000000001b00300008d02370283021802dc01000000000e003130303032303737343431332c30b600000000000000000000000000000000`
   - `S2C 0x076C payload=01009dd90800b60000000100ed0273220000000001b00300008d02370283021802dc01000000000e003130303032303737343431332c3001000100ff000000680005002d970000673c67002d970000040501000000010000000000000000000000000000000000000000000001000000000000000001`
   - `S2C 0x007C payload=460f0000460f000083021802010002000000302a0000`
8. later cleanup:
   - `S2C 0x007F payload=9dd90800b60000000001000000000000000000`
   - `S2C 0x0070 payload=9dd90800b600000000`

## Strong conclusions from the fifth capture

- this file confirms the explicit search path:
  - `0x033E` search request
  - `0x033F` search result
  - `0x006E` selection of the returned tile
  - `0x0CE8` actual gather send
- the returned target tile was:
  - `x = 0x0283 = 643`
  - `y = 0x0218 = 536`
- the same tile bytes `83021802` reappear in:
  - `0x006E`
  - `0x0071`
  - `0x076C`
  - `0x007C`
- the selected hero context in this file stayed:
  - `hero id = 255`
  - from `0x00B8` and `0x076C`

## Search request reading upgrade

Comparing explicit-search captures now gives a stronger reading for `0x033E`:

- older explicit search:
  - `0x033E payload=01040003`
- current explicit search:
  - `0x033E payload=02040003`

Because the operator explicitly identified this run as `wheat level 2`, the
strongest current interpretation is:

- the first byte in `0x033E` is very likely the requested target level
- `0x033F` echoes the same trailing request context together with returned
  coordinates

This does **not** yet fully decode every field of `0x033E`, but it upgrades the
model from:

- `0x033E / 0x033F` are search-family packets

to:

- `0x033E / 0x033F` are explicit search lookup packets where level is likely
  encoded directly in the request payload

## Remaining blocker

Even this fresh explicit-search capture still does **not** contain `0x0038`.

So the remaining unresolved point stays the same:

- operationally, gather is already understandable enough to automate
- but exact plaintext inside live encrypted `0x0CE8` still needs one capture that
  includes session key material

## Sixth gather capture with explicit hero selection (`Salah ad-Din`)

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_11_00_05.pcap`

Operator note:

- searched a resource tile, then selected a different hero manually
- the selected hero was identified in the UI as `Salah ad-Din`
- one gather send only

## Confirmed chronological flow in the sixth capture

This file contains the full user-visible sequence:

1. initial map-centering tile select:
   - `C2S 0x006E payload=8d02370201`
2. UI/map refresh burst:
   - `0x099D/0x099E`
   - `0x0767/0x0768`
   - `0x0769/0x076A`
3. final tile select on the actual target:
   - `C2S 0x006E payload=8d02350201`
4. explicit hero/formation selection:
   - `C2S 0x0323 payload=000100f1000000`
5. encrypted gather send:
   - `C2S 0x0CE8 payload=2174c33f736ca759efb2f8df4ac0004003005ee789e545acc5a87b243f7c3c687290b492a6e8fa522853020b011f4fe789e5`
6. post-send validation:
   - `S2C 0x00AA payload=01000000f1000000680000000400bd0105050000000000000000d904000005000000f1a000000a0000000a0000000a0000000a000000192f00000000192100000000191e00000000191900000000191f000000001f00000000000000000a000000020000000c0000000100000068000000`
   - `S2C 0x00B8 payload=010100000001f1000000`
   - `S2C 0x0071 payload=11d90800b60000000100ed0273220000000001290300008d0237028d0235027d01000000000e003130303032303930383936342c30b600000000000000000000000000000000`
   - `S2C 0x076C payload=010011d90800b60000000100ed0273220000000001290300008d0237028d0235027d01000000000e003130303032303930383936342c3001000100f100000068000500f1a000002dcf6b00f1a00000040501000000010000000000000000000000000000000000000000000001000000000000000001`
   - `S2C 0x007F payload=11d90800b60000000001000000000000000000`
   - `S2C 0x0070 payload=11d90800b600000000`
   - `S2C 0x007C payload=ce060000ce0600008d023502010001000000302a0000`

## Strong conclusions from the sixth capture

- this file confirms the visual gameplay sequence directly on the wire:
  - search/map focus
  - target tile selection
  - explicit hero selection
  - gather send
- the selected hero in this file is:
  - `hero id = 241`
  - and it propagates consistently through:
    - `0x0323`
    - `0x00AA`
    - `0x00B8`
    - `0x076C`
- this upgrades the confirmed hero mapping to:
  - `Omar Mukhtar = 255`
  - `Mohamed Al-Fatih = 244`
  - `Salah ad-Din = 241`

## Practical meaning of the sixth capture

This file is the cleanest confirmation so far that gather automation can be
modeled as:

1. select/search a target tile
2. optionally change hero/formation with `0x0323`
3. send the gather command via `0x0CE8`
4. validate success via `0x00B8` and `0x076C`

The remaining unresolved point is still the same narrow blocker:

- the internal plaintext layout of `0x0CE8` itself
- not the surrounding gather workflow

## Seventh gather capture with full payload enabled

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_20_Mar_15_28_47.pcap`

Operator note:

- fresh capture with `PCAP file` + `Full payload`
- one explicit gather flow only
- operator noted this run as `wheat level 2`
- one hero/formation was explicitly chosen before send

## Confirmed chronological flow in the seventh capture

This file contains:

1. initial map-centering tile select:
   - `C2S 0x006E payload=8d02370201`
2. map/UI sync burst:
   - `0x099D/0x099E`
   - `0x0767/0x0768`
   - `0x0769/0x076A`
3. explicit search lookup request:
   - `C2S 0x033E payload=05040003`
4. explicit search lookup response:
   - `S2C 0x033F payload=05a0025d02040003`
5. tile selection on the returned search result:
   - `C2S 0x006E payload=a0025d0201`
6. explicit hero/formation selection:
   - `C2S 0x0323 payload=000100ed000000`
7. encrypted gather send:
   - `C2S 0x0CE8 payload=83c5729cd75705d64bdf82d6ecd87ae7a53522ee2fce3fa56383012d99574661d4bbce9b00e58045ce787802a73435ee2fce`
8. post-send validation:
   - `S2C 0x00AA payload=01000000ed000000650000000440987a01030000000000000000d504000005000000017800000a0000000a0000000a0000000a000000011200000000190c000000001715d8000000011100000000010d000000001f00000000000000000000000000000000000000000000000065000000`
   - `S2C 0x00B8 payload=010100000001ed000000`
   - `S2C 0x0071 payload=2ddb0800b60000000100ed0273220000000001bd0400008d023702a0025d021e00000000000e003130303032303839383133322c30b600000000000000000000000000000000`
   - `S2C 0x076C payload=01002ddb0800b60000000100ed0273220000000001bd0400008d023702a0025d021e00000000000e003130303032303839383133322c3001000100ed0000006500050001780000ad2e300001780000040301000000010000000000000000000000000000000000000000000001000000000000000001`
   - `S2C 0x007C payload=8c1e00008c1e0000a0025d02010005000000302a0000`
9. later cleanup:
   - `S2C 0x007F payload=2ddb0800b60000000001000000000000000000`
   - `S2C 0x0070 payload=2ddb0800b600000000`

## Strong conclusions from the seventh capture

- this is another fully accepted gather march on a new target tile
- the returned target tile was:
  - `x = 0x02A0 = 672`
  - `y = 0x025D = 605`
- the same tile bytes `a0025d02` reappear in:
  - `0x006E`
  - `0x0071`
  - `0x076C`
  - `0x007C`
- this file gives one more clean hero-id confirmation:
  - `hero id = 237`
  - from:
    - `0x0323`
    - `0x00AA`
    - `0x00B8`
    - `0x076C`

## Why this capture is especially useful

- `0x0323` and `0x0CE8` appear back-to-back in the same framed TCP payload
- the full-payload setting did not change the visible gameplay sequence:
  - search
  - tile select
  - hero select
  - encrypted gather send
  - post-send validation
- no `0x0038` appeared in this file either

## Updated practical status

This seventh capture narrows the remaining blocker even further:

- the operational gather chain is now repeatedly confirmed across multiple heroes
  and multiple target tiles
- the unresolved point is still only the internal plaintext layout of `0x0CE8`
- but the outside behavior of gather is now stable enough to summarize as:
  - `0x033E / 0x033F` = search-family lookup
  - `0x006E` = tile selection
  - `0x0323` = hero/formation selection when the client emits a fresh hero change
  - `0x0CE8` = actual gather send
  - `0x00B8` and `0x076C` = strongest post-send hero/target validation packets

## 2026-03-21 direct-send debugging update

Critical implementation bug was found in the local direct-send probes:

- `gather_now.py`
- `gather_smart.py`
- `gather_field0f.py`
- `gather_clean.py`

All four scripts used a simplified `CMsgCodec` header for encrypted packets:

- byte0 was hardcoded as `0x00` (should be checksum low byte)
- byte2 was hardcoded as `0x00` (should be `msg_lo ^ 0xB7`)

This does not match real `CMsgCodec` packets (confirmed by captures, e.g. `b5 -> 02` relation in byte2).

After fixing the codec header generation to match `COMPLETE_BOT.py`:

- `0x0CE8` encrypted payload size remains correct (`50B` payload => `46B` plaintext)
- server behavior changed from immediate generic reject patterns to deeper processing responses
- direct gather is still not fully accepted yet, but encryption-format rejection is no longer the primary blocker

Live probe outcomes after codec fix:

- `gather_clean.py` (03:54 run): returned `0x201A` after `0x0CE8` (no march start)
- `gather_smart.py` (03:55 run): multiple `0x026D` responses after attempts, no `0x0071/0x076C`
- `gather_field0f.py` (03:56 run): repeated `0x026D` responses, no accepted march

Current blocker status:

- encryption wrapper is now aligned
- remaining issue is gather-specific state/layout semantics (hero/session/context fields), not raw packet crypto framing

## Eighth gather capture: direct manual wheat L1 with one hero

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_21_Mar_11_05_21.pcap`

Operator note:

- manual direct gather from the map
- no search used in this run
- one hero only (`Omar Mukhtar`)
- target was a level 1 wheat node

## Confirmed chronological flow in the eighth capture

This file contains one fully accepted direct gather flow:

1. initial castle/map source select:
   - `C2S 0x006E payload=8d02370201`
2. view enable:
   - `C2S 0x0CEB payload=95bc0bf78f9ff789b8e7b979b660`
3. map/UI sync burst:
   - `C2S 0x099D payloads=93010000, 94010000, 95010000, 96010000, 97010000, 99010000, 9a010000`
   - `S2C 0x099E ...`
   - `C2S 0x0767`
   - `C2S 0x0769`
   - `S2C 0x0768`
   - `S2C 0x076A`
4. repeated manual tile browsing on nearby nodes:
   - `C2S 0x006E payload=8f023c0201`
   - `C2S 0x006E payload=9102410201`
   - `C2S 0x006E payload=96024d0201`
   - `C2S 0x006E payload=9902540201`
   - `C2S 0x006E payload=9b02580201`
   - `C2S 0x006E payload=9a02530201`
5. final accepted gather send:
   - `C2S 0x0CE8 payload=ff79ce7cf8ea6ba974d3cc22c3dd34448a797a1a008219514ccf47d9b61b0895fbf7806f2fa9ceb1e13436f688787b1a0082`
6. post-send validation:
   - `S2C 0x00B8 payload=010100000001ff000000`
   - `S2C 0x0071 payload=66f90800b60000000100ed0273220000000001b00300008d023702990252021a01000000000e003130303032313439323139372c30...`
   - `S2C 0x076C payload=010066f90800b60000000100ed0273220000000001b00300008d023702990252021a01000000000e003130303032313439323139372c30...`
   - `S2C 0x007C payload=380c0000380c000099025202010001000000302a0000`

## Recovered successful plaintext for the eighth capture

Using KPA on the fixed `IGG_ID` bytes inside the encrypted `0x0CE8`, the accepted plaintext is:

- `21a1d99f697300e120ed02732285ffe12084b6e1208404e1208400e1208400e120990252028400e1208400e12084`

Parsed fields:

- hero id = `255`
- target tile = `(665, 594)` from bytes `99025202`
- session byte A = `0xE1`
- session byte B = `0x84`
- byte 13 = `0x85`

## Strong conclusions from the eighth capture

- this is the first clean proof of a fully accepted **manual direct gather without search**
- `0x0323` does **not** appear before the accepted `0x0CE8` in this one-hero flow
- there is **no extra client opcode between the final target-view packets and the accepted `0x0CE8`**
  other than passive `0x0042` heartbeat traffic
- in this scenario, pressing `حملات` does not create a separate wire opcode; it results directly in `0x0CE8`
- the missing piece in failed live replays is therefore not a separate "March button opcode"
  but the exact local state that feeds the final `0x0CE8` plaintext

## Updated practical status after the eighth capture

We now have an accepted manual direct gather sequence that proves:

- `search` is optional for gather
- `0x0323` is optional when the hero is already preselected
- `0x0CE8` remains the real final send opcode
- the remaining direct-send blocker is the session-dependent plaintext composition of `0x0CE8`
  for the currently opened tile and current local hero-selection state

## Ninth gather capture: full map-entry -> search -> gather success

Source capture:

- `D:\CascadeProjects\codex_lab\PCAPdroid_21_Mar_11_22_28.pcap`

Operator note:

- full run from map entry
- search was used
- wheat level 1
- one hero only

## Confirmed chronological flow in the ninth capture

This file contains one fully accepted search-based gather flow:

1. map/UI preparation before search:
   - `C2S 0x0CEB payload=fbd5621b60461d67d57e53df5bf1`
   - `C2S 0x099D payloads=93010000, 94010000, 95010000, 96010000, 97010000, 99010000, 9a010000`
   - `C2S 0x006E payload=8d02370201`
   - `C2S 0x0767`
   - `C2S 0x0769`
   - `S2C 0x099E ...`
   - `S2C 0x0768`
   - `S2C 0x076A`
2. search request:
   - `C2S 0x033E payload=01040003`
3. search response:
   - `S2C 0x033F payload=017e023802040003`
4. target tile selection:
   - `C2S 0x006E payload=7e02380201`
5. final accepted gather send:
   - `C2S 0x0CE8 payload=3fd16601a491c589b89d97059fb26f89d663213d5c9a827610d71cfeea0353b2a7efdb48734b95907d2c6dd1d460203d5c9a`
6. post-send validation:
   - `S2C 0x00B8 payload=010100000001ff000000`
   - `S2C 0x0071 payload=88f90800b60000000100ed0273220000000001b00300008d0237027e0238026903000000000e003130303032313530393732362c30...`
   - `S2C 0x076C payload=010088f90800b60000000100ed0273220000000001b00300008d0237027e0238026903000000000e003130303032313530393732362c30...`
   - `S2C 0x007C payload=380c0000380c00007e023802010001000000302a0000`

## Recovered successful plaintext for the ninth capture

Using KPA on the fixed `IGG_ID` bytes inside the encrypted `0x0CE8`, the accepted plaintext is:

- `210d1e0ce94800cb20ed02732252ffcb204fb6cb204f04cb204f00cb204f00cb207e0238024f00cb204f00cb204f`

Parsed fields:

- hero id = `255`
- target tile = `(638, 568)` from bytes `7e023802`
- session byte A = `0xCB`
- session byte B = `0x4F`
- byte 13 = `0x52`

## Strong conclusions from the ninth capture

- this is the cleanest full proof that **search-based gather can also succeed without `0x0323`**
- the required outer sequence is now directly confirmed as:
  - `0x0CEB`
  - `0x099D/0x099E`
  - `0x006E` source
  - `0x0767/0x0768`
  - `0x0769/0x076A`
  - `0x033E/0x033F`
  - `0x006E` target
  - `0x0CE8`
- `0x0323` is therefore a conditional hero-change packet, not a mandatory gather step
- the accepted `0x0CE8` plaintext still changes per session/run, confirming again that direct send fails because
  we are replaying stale plaintext rather than rebuilding current session state

## 2026-03-22 negative live test: explicit Hero 244 did not establish a march

One later direct live test was run specifically to probe whether forcing
`Hero 244` before the gather send would succeed.

Observed result:

- an explicit hero-selection packet was sent for `Hero 244`
- the server returned `0x026D` immediately after that hero-selection step
- the later `0x0CE8` gather send produced follow-up packets such as:
  - `0x0091`
  - `0x0080`
  - `0x0082`
- but the accepted gather validation chain did **not** appear:
  - no `0x00B8`
  - no `0x0071`

Strong reading from this negative test:

- the failure is not well explained by outer encryption alone
- the server is willing to process the request far enough to return map/info style
  responses, but the gather march still does not become established
- explicit `Hero 244` forcing is therefore not a reliable shortcut to a valid gather
  state in this direct replay path

What this negative result upgrades:

- absence of `0x00B8` and `0x0071` remains the clearest sign that the march did not
  start
- a visible response after `0x0CE8` still does **not** mean accepted gather
- gather failure is more consistent with state / eligibility / context mismatch than
  with a trivial framing-only error

## 2026-03-22 live validation rule upgrade

After repeated live tests, the response families now split into two groups:

Strong gather-start signals:

- `0x00B8`
- `0x0071`
- `0x007C`
- `0x076C`

Weak / ambiguous post-send signals:

- `0x00AA`
- `0x0091`
- `0x0080`
- `0x0082`

Important operational rule:

- `0x0091`, `0x0080`, and `0x0082` can appear even when **no visible gather march**
  appears in the live game client.
- `0x00AA` can also appear without proving that a new gather actually started.
- Therefore live automation must treat gather as **accepted** only when at least one
  strong signal appears, preferably alongside the expected map/march packets.

This is now the validation rule used by `gather_bot_v3.py`:

- weak signals are logged separately
- only strong signals make the final result `success=True`

## 2026-03-22 gather_bot_v3 hardening: no silent template guessing

To avoid accidental replay guesswork in live runs:

- `gather_bot_v3.py` now uses strict template matching by default.
- `0x0CE8` send will abort unless there is an accepted template for the exact `(hero, level)` pair.
- fallback behavior is still available only with explicit CLI flag:
  - `--allow-template-fallback`
- default `--level` was changed to `1` because accepted templates are currently validated mainly for levels `1-2`.

Operational impact:

- this prevents hidden fallback to unrelated templates (a major source of confusing false-negative/false-positive interpretations)
- any remaining failure after this change points more directly to the unresolved session-state part of `0x0CE8`, not template selection ambiguity

## 2026-03-22 new dual-success capture (PCAPdroid_22_Mar_12_31_39.pcap)

Source:

- `D:\CascadeProjects\codex_lab\PCAPdroid_22_Mar_12_31_39.pcap`

Confirmed outcome:

- capture contains **two successful manual gather sends** (wheat level 1)
- both are followed by the strong chain:
  - `0x00B8`
  - `0x0071`
  - `0x076C`
  - `0x007C`

Recovered accepted `0x0CE8` plaintexts (KPA with IGG bytes + target tile bytes):

1. hero `255`:
   - `217ce0f5697000b320ed027322a6ffb320a7b6b320a704b320a700b320a700b3208a024002a700b320a700b320a7`
   - target tile `(650,576)` from `8a024002`
2. hero `244`:
   - `218d00f2a96200b320ed02732278f4b32079b6b3207904b3207900b3207900b320840240027900b3207900b32079`
   - target tile `(644,576)` from `84024002`

Notable field pattern from this capture:

- both successful sends share `VA=0xB3`
- `VB` differs by hero/path (`0xA7` for hero255, `0x79` for hero244)
- `b13` remains close to `VB` (`0xA6`, `0x78`)

Operational update:

- these two plaintexts were added to `gather_bot_v3.py` template set as:
  - `hero255_lvl1_22mar_1231`
  - `hero244_lvl1_22mar_1231`

## 2026-03-22 live replay attempts on fresh code (still negative)

After adding direct target override and matching the 22-Mar packet order more closely,
multiple direct runs were executed against the recovered successful tiles:

- hero255 -> target `(650,576)`
- hero244 -> target `(644,576)`

Code-level updates used in these tests:

- direct tile override CLI (`--target-x/--target-y`) to bypass empty `0x033F`
- default `0x099D` troop list switched to latest successful set:
  - `403,405,406,407,411`
- source `0x006E` moved to **after** `0x0CEB` (matching latest success trace)
- optional full setup extras added:
  - `0x0709`, `0x0A2C`, `0x17A3`

Observed result in all replay attempts:

- no strong success chain (`0x00B8/0x0071/0x076C/0x007C`) appeared
- only map/march noise (`0x0076/0x0077/0x0078/0x007A`) and side updates

Interpretation:

- the remaining blocker is still dynamic `0x0CE8` acceptance context/state
  (not weak-signal misclassification, and not missing static template inventory)
- stale/fixed `0x1B8B` replay can even abort the connection, so it cannot be
  blindly reused across sessions

## 2026-03-22 new single-run capture (PCAPdroid_22_Mar_12_57_05.pcap)

Source:

- `D:\CascadeProjects\codex_lab\PCAPdroid_22_Mar_12_57_05.pcap`

Confirmed outcome:

- contains one successful gather send on tile `(650,576)`
- strong chain present after `0x0CE8`:
  - `0x00B8`
  - `0x0071`
  - `0x076C`
  - `0x007C`

Recovered accepted `0x0CE8` plaintext (KPA with IGG+tile anchors):

- hero `255`:
  - `2180e099698400b320ed02732296ffb3209bb6b3209b04b3209b00b3209b00b3208a0240029b00b3209b00b3209b`

New sequencing observation from this capture:

- one valid path shows:
  - `0x0245/0x0834/0x0709/0x0A2C/0x17A3/0x1B8B`
  - `0x099D x5`
  - `0x0767 + 0x0769`
  - `0x0CEB`
  - `0x006E` source then `0x006E` target
  - `0x0CE8`
- i.e. `0x0CEB` can appear **after** troop/sync in a successful run.

Operational impact:

- `gather_bot_v3.py` was extended with alternate ordering mode:
  - `--prelude-after-troops`
- stale replay of `0x1B8B` payload from another session still causes immediate
  connection abort (`WinError 10053`), confirming that `0x1B8B` is session-bound.

## 2026-03-22 full-session diff upgrade (why gather is harder)

Reassembled C2S sequence from latest successful captures (`12:31` and `12:57`)
showed two critical facts:

1. Canonical successful setup order (latest baseline):

- `0x0840 -> 0x0245 -> 0x0834 -> 0x0709 -> 0x0A2C -> 0x17A3 -> 0x1B8B`
- then troops/sync (`0x099D x5`, `0x0767`, `0x0769`)
- then `0x0CEB`, source `0x006E`, target `0x006E`, **`0x0042` heartbeat**
- then `0x0CE8`

2. The successful traces do **not** require an early target `0x006E` during setup.

Bot updates made from this diff:

- removed setup-target `0x006E` from default flow (kept as legacy toggle)
- removed unconditional preselect `0x006E` before gather flow (now optional)
- added explicit pre-`0x0CE8` heartbeat option:
  - `--send-pre-0ce8-heartbeat`

Live result after this upgrade:

- flow got closer and now can return weak `0x0091` after `0x0CE8`
- but still no strong chain (`0x00B8/0x0071/0x076C/0x007C`) in bot replay

## 2026-03-22 dataset result for `0x1B8B` (71 pairs)

A cross-PCAP dataset was extracted: `(0023 token, 1B8B payload)` from 71 sessions.

Observed:

- same token can appear across multiple captures with completely different `0x1B8B`
- random `0x1B8B` or stale replay `0x1B8B` usually causes fast connection abort
  (`WinError 10053`)

Inference:

- `0x1B8B` is not static and not token-only; it is bound to additional dynamic
  session state (challenge/nonce/time-derived context)
- this dynamic state is currently the main blocker for turning weak replay into
  strong gather-start acceptance

## 2026-03-22 correction after direct decode (root cause fixed)

A direct decode pass over strong-success PCAPs found that the previous KPA-derived
`0x0CE8` templates had field positions shifted.

Verified real `0x0CE8` layout in successful captures:

- `[9:11] = tile_x`
- `[11:13] = tile_y`
- `[14] = hero`
- `[18] = kingdom`
- `[33:37] = igg_id`

Root bug in `gather_bot_v3.py` before fix:

- code patched tile bytes at offset `33` (overwriting igg field) instead of offset `9`
- templates were based on shifted KPA plaintexts (`21...`) instead of direct codec decode
  (`01...`)

Implemented fix:

- replaced gather templates with verified direct-decoded successful plaintexts
- patched builder to set dynamic fields at correct offsets:
  - slot `[0]`
  - tile `[9:13]`
  - hero `[14]`
  - kingdom `[18]`
  - igg_id `[33:37]`

Live validation:

- log: `gather_v3_20260322_072639.log`
- command profile:
  - setup extras (`0x0709/0x0A2C/0x17A3`)
  - prelude after troops
  - source then target `0x006E`
  - pre-`0x0CE8` heartbeat
- result:
  - strong signal received: `0x00B8`
  - bot printed `GATHER STARTED (strong signal)`

Practical note:

- repeated immediate replays on the same target can return only weak `0x0091`
  (target/slot state dependent after a successful start), so evaluation should
  use fresh tile/slot context when re-testing.

## 2026-03-22 end-of-day lock (what is now confirmed)

### 1. Confirmed working gather profile

Strong accept (`0x00B8`) was reproduced multiple times today with:

- full setup extras enabled (`0x0709/0x0A2C/0x17A3`)
- `0x099D x5` then `0x0767 + 0x0769`
- `0x0CEB` then source `0x006E` then target `0x006E`
- pre-`0x0CE8` heartbeat
- corrected direct-decoded `0x0CE8` template builder

Representative successful logs:

- `gather_v3_20260322_072639.log` (hero255)
- `gather_v3_20260322_073825.log` (hero255)
- `gather_v3_20260322_074311.log` (hero244)
- `gather_v3_20260322_074802.log` (hero244)
- `gather_v3_20260322_075051.log` (hero255, search mode + level2 + template fallback)

## 2026-03-23 search regression isolated and corrected

Root cause of the new regression was in the **auto-search path**, not in the
already-fixed `0x0CE8` field offsets.

What had regressed in `gather_bot_v3.py`:

- `0x033E` was being built as:
  - `[resource_type, resource_level, 0x00, 0x03]`
- for wheat level 2 that produced:
  - `01020003`
- but successful captures prove the real wheat search payload is:
  - level 1 -> `01040003`
  - level 2 -> `02040003`
  - level 5 -> `05040003`
- so for wheat:
  - first byte = requested level
  - second byte = wheat search family `0x04`

The second regression was **ordering**:

- auto-search was being sent too early in `main()`, before the proven
  gather-prelude / troop-sync sequence
- successful search-based captures place the search later in the flow, after
  prelude/sync and before the final target `0x006E`

Code fix applied:

- added explicit search payload builder for wheat:
  - `build_search_payload()`
- moved auto-search resolution out of `main()` and into `do_gather()`
- auto-search now runs in-flow:
  - setup
  - troops/sync
  - `0x0CEB`
  - source `0x006E`
  - `0x033E / 0x033F`
  - target `0x006E`
  - heartbeat
  - `0x0CE8`

Live validation after this fix:

- log: `gather_v3_20260323_014312.log`
- confirmed on wire:
  - `Sent 0x033E search payload=02040003`
  - search happened **after** `0x099D/0x0767/0x0769/0x0CEB/source 0x006E`
  - `Recv 0x033F ... tile=(663,558)`
  - final target select:
    - `0x006E payload=97022e0201`

Result of this validation:

- search path is now back on the proven wire shape
- but the final gather still did **not** receive strong validation in that run
- so the remaining blocker is now narrowed again to **post-search gather
  acceptance**:
  - current template fallback for level 2
  - and/or session-bound march state around final `0x0CE8`

Practical conclusion:

- the current failure is **no longer because we are searching with the wrong
  packet or in the wrong place in the flow**
- the remaining work is the exact accepted `0x0CE8`/hero-state combination for
  search-based wheat level 2

## 2026-03-23 follow-up search replay probes after fixing `0x033E`

After fixing the search payload and moving auto-search into the in-flow gather
sequence, several tighter probes were run to match the successful search
captures as closely as possible.

### 1. Search-specific pre-send order was updated

Auto-search path now uses:

- `0x0CEB`
- `0x099D ...`
- source `0x006E`
- `0x0767 + 0x0769`
- wait for sync replies:
  - `0x099E`
  - `0x0768`
  - `0x076A`
- `0x033E / 0x033F`
- target `0x006E`
- optional heartbeat / `0x0323`
- `0x0CE8`

This matches the older successful search capture shape much more closely than
the previous direct-baseline reuse.

### 2. Level 2 search probe with corrected order

- log: `gather_v3_20260323_015206.log`
- confirmed:
  - `0x033E payload=02040003`
  - in-flow search after prelude/troops/source/sync
- result:
  - no strong accept after `0x0CE8`

### 3. Level 1 search probe with corrected order

- log: `gather_v3_20260323_015235.log`
- confirmed:
  - `0x033E payload=01040003`
  - search returned tile `(645,542)`
- result:
  - no strong accept after `0x0CE8`

### 4. Level 1 probe with explicit hero select

- log: `gather_v3_20260323_015348.log`
- extra step:
  - `0x0323 payload=000100ff000000`
- result:
  - still no strong accept

### 5. Level 1 probe using the older 7-troop search capture set

- log: `gather_v3_20260323_015417.log`
- troop IDs used:
  - `403,404,405,406,407,409,410`
- result:
  - still no strong accept

### 6. Level 1 probe with no pre-`0x0CE8` heartbeat

- log: `gather_v3_20260323_015454.log`
- settings:
  - no heartbeat before `0x0CE8`
  - 7-troop search set
- result:
  - weak `0x0080`
  - no `0x00B8 / 0x0071 / 0x076C / 0x007C`

### Narrowed conclusion

At this point the following are now directly ruled out as the main blocker:

- wrong `0x033E` payload for wheat
- wrong placement of auto-search in the flow
- missing sync wait before search
- missing `0x0323` in the tested hero255 path
- wrong 5-vs-7 troop selection set alone
- pre-`0x0CE8` heartbeat as the only blocker

The remaining blocker is therefore still centered on the final accepted
`0x0CE8` state composition after search, not the search-family wire protocol
itself.

## 2026-03-23 slot-state upgrade

A new live finding changed the diagnosis materially: **march slot state**
changes the result even when tile, hero, and payload family stay the same.

### Manual direct on the same tile: slot 1 vs slot 2

Using the same target tile `(644,564)` and the same hero/profile:

- `slot 1`
  - log: `gather_v3_20260323_020328.log`
  - result:
    - no `0x00B8`
    - no strong chain
- `slot 2`
  - log: `gather_v3_20260323_020524.log`
  - result:
    - repeated `0x00B8`
    - plus follow-up `0x0033` and `0x00B9`
    - but still no target-matched `0x0071/0x076C/0x007C`

This is important because it proves the problem is not just:

- search packet shape
- target tile
- or hero id alone

It also depends on **which march slot is used at that moment**.

### Search path with slot fallback

Search run with automatic retry from `slot 1` to `slot 2`:

- log: `gather_v3_20260323_020910.log`
- behavior:
  - `slot 1`:
    - no `0x00B8`
  - `slot 2`:
    - `0x00B8`
    - `0x0033`
    - `0x00B9`
    - no strong chain

Search run with soft-accept enabled:

- log: `gather_v3_20260323_021005.log`
- flags:
  - `--slot-fallbacks 2`
  - `--accept-soft-00b8`
- result:
  - `slot 1` failed
  - `slot 2` produced `0x00B8`
  - bot marked this as provisional / soft success and saved the tile

### Code update

`gather_bot_v3.py` now supports:

- `--slot-fallbacks`
  - retry on alternate march slots after the primary one
- `--accept-soft-00b8`
  - treat `0x00B8`-only acceptance as provisional success

### Practical reading

At minimum, the earlier “why did it stop behaving like yesterday?” question now
has a concrete partial answer:

- one major difference was **slot state**
- `slot 1` can fail silently while `slot 2` returns the same `0x00B8` pattern
  that older “successful” live runs showed

### 2. Hero IDs validated in live gather

- hero `255` = Mokhtar (validated by successful strong runs)
- hero `244` = Mohamed Al-Fatih (validated by successful strong runs)

### 3. Search mode vs manual target

- manual mode (`--target-x/--target-y`) is still supported for deterministic replay tests
- search mode is now confirmed working in live run:
  - level1 can return `count=0` depending on map state
  - level2 search returned valid targets and succeeded with strong accept

### 4. New anti-repeat search cache (implemented)

`gather_bot_v3.py` now has tile de-dup for auto-search runs:

- default behavior avoids recently used tiles
- recent tile cache file:
  - `D:\CascadeProjects\codex_lab\gather_recent_tiles.json`
- key options:
  - `--allow-repeat-target`
  - `--recent-tiles-file`
  - `--recent-tiles-ttl-minutes`
  - `--recent-tiles-max`
  - `--max-search-attempts`
  - `--search-retry-delay`
  - `--clear-recent-tiles`

Important behavior:

- de-dup applies to auto-search mode
- if override target is explicitly passed, script warns if repeated but still executes

### 5. Current safe run command (search mode, no manual coordinates)

```powershell
python D:\CascadeProjects\codex_lab\gather_bot_v3.py --hero 255 --resource 1 --level 2 --working-profile --allow-template-fallback --max-template-attempts 1 --max-search-attempts 10 --troops 403,405,406,407,411 --source-x 653 --source-y 567 --pre-0ce8-heartbeat-wait 1.5
```

---

## Next session checklist (requested for tomorrow)

1. Gather resource types coverage:
   - wheat / wood / stone / ore / gold
   - confirm per-type search and accept chain
2. Remaining hero IDs mapping:
   - identify and validate all gather-usable heroes beyond `244` and `255`
3. Rebel kill flow:
   - isolate op sequence and acceptance signals for maverick/rebel attack
4. Multi-march concurrency:
   - verify up to 5 simultaneous gather marches
   - confirm slot handling and per-slot success evidence
5. Multi-hero in single march:
   - validate packet behavior for selecting more than one hero in one campaign
   - map required opcodes/fields and acceptance criteria

## 2026-03-23 new proof: two separate gather marches in one capture

Source:

- `D:\CascadeProjects\codex_lab\PCAPdroid_23_Mar_07_17_11.pcap`

Confirmed from timeline and direct decode:

- two separate C2S `0x0CE8` sends exist in the same session
- both are strongly accepted (each followed by strong chain)

Decoded gathers:

1. First gather (`0x0CE8`):
   - hero: `255` (Mokhtar)
   - tile: `(644,564)`
   - plaintext:
     - `01f4c9c949170000008402340201ff000000b60000000400000000000000000000ed027322000000000000000000`
   - strong responses:
     - `0x00B8`, `0x0071`, `0x076C`, `0x007C`

2. Second gather (`0x0CE8`):
   - hero: `244` (Mohamed Al-Fatih)
   - tile: `(647,560)`
   - plaintext:
     - `01fcb9ca49170000008702300201f4000000b60000000400000000000000000000ed027322000000000000000000`
   - strong responses:
     - `0x00B8`, `0x0071`, `0x076C`, `0x007C`

Extra evidence:

- second `0x00B8` payload is larger (`19B`):
  - `020100000001ff0000000200000001f4000000`
- inference: this likely reflects multi-march state (two active marches in response context).

Impact:

- multi-march (at least 2 concurrent gather marches) is now confirmed in real traffic.
- this reduces risk for tomorrow's "up to 5 marches" expansion test, since base behavior is proven.

## 2026-03-23 live bot send: two campaigns with delay (verified)

Objective:

- send two gather campaigns from bot with a short gap and avoid repeated target tiles.

Runs executed:

1. `gather_v3_20260323_012633.log`
   - hero `244`, slot `2`
   - auto-searched tile `(632,542)`
   - strong accept: `0x00B8` -> `GATHER STARTED`
2. `gather_v3_20260323_012650.log`
   - hero `255`, slot `3`
   - auto-searched tile `(621,594)`
   - strong accept: `0x00B8` -> `GATHER STARTED`

Notes:

- there was one earlier failed probe at `01:26:02` (no strong accept), then two successful starts.
- successful campaigns used different tiles and different slots, matching the anti-repeat intent.

## 2026-03-23 false-positive fix: prevent rebel/non-gather misclassification

Issue reproduced in live runs:

- `0x00B8` can appear even when run is not confirmed as real resource gather.
- user-observed case: bot path could still end up as non-gather action (e.g., rebel/other march),
  while old logic marked success too early.

Root cause in bot logic:

- success was allowed on first strong opcode in `{0x00B8, 0x0071, 0x076C, 0x007C}`.
- this made `0x00B8` alone sufficient, which is too weak as gather proof.

Fix applied in `gather_bot_v3.py`:

- gather final success now requires **target-matched confirmation** from:
  - `0x0071` or `0x076C` or `0x007C`
  - and payload must contain the sent target tile marker (`<tile_x,tile_y>` LE bytes)
- `0x00B8` is now treated as intermediate signal only; never final by itself.

Validation run after fix:

- log: `gather_v3_20260323_013031.log`
- observed:
  - `0x00B8` received
  - no target-matched `0x0071/0x076C/0x007C`
- final result:
  - `success=False` (correctly rejected false positive)

## 2026-03-23 live bot double-send check (with spacing + anti-repeat)

Direct live execution from `gather_bot_v3.py` (search mode, no manual coords):

- first attempt in this batch failed (no strong)
  - `gather_v3_20260323_012149.log`
- then two strong accepted sends were achieved with spacing and different tiles:
  1. `gather_v3_20260323_012224.log`
     - hero `244`, slot `2`, tile `(696,537)`
     - strong: `0x00B8`
  2. `gather_v3_20260323_012326.log`
     - hero `244`, slot `3`, tile `(668,578)`
     - strong: `0x00B8`

Notes:

- tiles were different between accepted sends
- anti-repeat cache remained active (search mode; no manual target override)

## 2026-03-23 sequencing correction from search-success PCAP

Reference capture revisited:

- `D:\CascadeProjects\codex_lab\PCAPdroid_21_Mar_11_22_28.pcap`

Key chronological proof around accepted `0x0CE8`:

1. `0x0245`
2. `0x0834`
3. `0x099D` x7 (`193,194,195,196,197,199,19A`)
4. `0x0CEB`
5. source `0x006E` (`653,567`)
6. `0x0767` + `0x0769`
7. `0x033E` / `0x033F`
8. target `0x006E`
9. `0x0042` heartbeat + echo
10. `0x0CE8`
11. strong chain: `0x00B8` + `0x0071` + `0x076C` + `0x007C`

Important nuance:

- byte 0 in `0x033F` behaves as level echo in these captures, not a reliable "count" field.

### Bot updates applied in `gather_bot_v3.py`

- Added search-capture troop profile:
  - `SEARCH_CAPTURE_TROOPS = [403,404,405,406,407,409,410]`
- Working profile now defaults to:
  - no `0x0840`
  - no setup extras (`0x0709/0x0A2C/0x17A3`)
  - `prelude_after_troops=True`
  - `send_source_first=True`
  - pre-`0x0CE8` heartbeat enabled
- Added `--send-0840` opt-in flag.
- Auto-search pre-send order corrected to:
  - `troops -> 0x0CEB -> source -> sync`
- Fallback slot behavior corrected:
  - each fallback slot now forces fresh auto-search tile instead of reusing previous target.
- Search log wording updated:
  - `Recv 0x033F level_echo=... tile=(x,y)`.

### Live validation after these fixes

Runs:

- `gather_v3_20260323_022522.log` (level 1, slots 1->2->3 fallback)
- `gather_v3_20260323_022619.log` (level 2, slots 1->2->3 fallback)

Observed:

- corrected sequence is now present on wire (order and troop IDs align with capture model)
- fallback now searches new tiles (non-reuse verified in logs)
- still no final strong chain (`0x0071/0x076C/0x007C`) in these runs
- repeated pattern remains mostly `0x00B8`-only (or weak only), therefore still not confirmed gather start

## 2026-03-23 target-probe hardening (no new capture required)

Problem addressed:

- auto-search frequently returned tiles that produced weak/non-gather context before `0x0CE8`
  (especially `0x0091` / `0x0080`) and wasted attempts.

Code hardening in `gather_bot_v3.py`:

- added target probe after searched `0x006E` and before `0x0CE8`
- if weak pre-send context appears (`0x0091/0x0080/0x0082`), tile is rejected
- auto-search immediately retries on a new tile (blocked tile set + non-repeating search)
- `0x033F` zero tile `(0,0)` is now treated invalid and retried

Live validation:

- `gather_v3_20260323_025007.log`
  - tile `(619,539)` rejected due to weak `0x0091`
  - tile `(619,542)` rejected due to weak `0x0091`
  - tile `(614,589)` rejected due to weak `0x0080`
  - moved to tile `(624,600)` and attempted `0x0CE8`
  - no strong confirmation chain
- `gather_v3_20260323_025037.log`
  - tile `(664,550)` rejected due to weak `0x0091`
  - retried on `(631,551)` automatically
  - no strong confirmation chain

Conclusion of this hardening:

- search path is now safer (filters obvious wrong targets before final send)
- remaining blocker is still final accepted gather state after search
- direct/manual path remains separately validated; search-path final acceptance remains unresolved

## 2026-03-23 late-night probes: KPA template + expanded slot sweep

### 1) KPA-derived probe template test

Template added for isolated testing:

- name: `kpa_search_l1_probe_21mar`
- plaintext base:
  - `210d1e0ce94800cb20ed02732252ffcb204fb6cb204f04cb204f00cb204f00cb207e0238024f00cb204f00cb204f`
- metadata:
  - `tile_offset=33`
  - `igg_offset=9`
  - `patch_slot=False`

Result in live run:

- log: `gather_v3_20260323_025433.log`
- server produced no strong or soft acceptance after this template
- practical reading:
  - this KPA form is not replay-ready as a drop-in replacement in current live state

### 2) Multi-template search run on one resolved tile

- log: `gather_v3_20260323_025511.log`
- tested 6 templates sequentially on same tile after search+probe path
- no `0x00B8`, no `0x0071/0x076C/0x007C`

### 3) Expanded slot sweep in one session (`2,3,4,5`)

- log: `gather_v3_20260323_025831.log`
- behavior:
  - slot 2: no acceptance
  - slot 3/4/5: `0x00B8` appears on some attempts
  - still no target-confirm chain (`0x0071/0x076C/0x007C`)

Net state after these probes:

- search + target filtering + slot fallback is functioning technically
- accepted gather confirmation chain is still absent in search mode in current live conditions

## 2026-03-23 slot-fix + wheat-only auto-search sanity run

Code fix applied in `gather_bot_v3.py`:

- template selector now excludes all `probe_only` templates from every automatic/fallback path
- `probe_only` templates can still be used only if explicitly forced by `--template-name`
- purpose: prevent slot/state corruption from probe payloads in normal gather runs

Live run after fix (`hero=255`, wheat search, auto target, forced real gather template):

- command profile used `--working-profile --resource 1 --level 1 --template-name hero255_lvl1_cap_22mar`
- log: `gather_v3_20260323_031001.log`
- observed:
  - slot plan executed as expected (`[1,2,3,4,5]`)
  - slot 1 and 2 failed to accept
  - slot 3 produced `0x00B8` soft acceptance
  - `0x0CE8` payload clearly patched slot byte to `03` (`march_slot=3`)
  - no target-confirm chain (`0x0071/0x076C/0x007C`) in that attempt window

Operational takeaway:

- slot routing bug is fixed at bot layer (slot patching and slot fallback are working)
- remaining gap is confirmation depth after `0x00B8` on search path, not slot assignment

## 2026-03-23 correction: 0x00B8+0x00B9 is not enough for real gather

Correction after revalidation:

- the temporary rule (`0x00B8 + 0x00B9` => strong) produced false positives
- before/after march-state checks showed no confirmed in-game gather despite that chain
- strict confirmation remains:
  - `0x0071/0x076C/0x007C` with target match (or explicit march-state evidence)

Code status:

- fallback strong-by-ack logic was removed from `gather_bot_v3.py`
- `0x00B9` is kept as observed telemetry only, not as success proof

## 2026-03-26 correction: search target probe is observational, not a rejection gate

Re-reading the Mar20+ successful PCAP window shows that the old search-probe rejection rule was
too aggressive.

Confirmed from successful search-based sessions:

- `0x0076 / 0x0077 / 0x0078 / 0x007A` can appear between searched target select and `0x0CE8`
- `0x0091` can also appear in that same pre-`0x0CE8` window
- `0x0080 / 0x0082` can also appear in that same pre-`0x0CE8` window

Concrete proof:

- `PCAPdroid_20_Mar_15_28_47.pcap` shows
  `0x0076 + 0x0077 + 0x0091 + 0x0078 + 0x0080 + 0x0082 + 0x007A`
  after target `0x006E`
- the same session still succeeds with:
  `0x00B8 + 0x0071 + 0x076C + 0x007C`

Meaning:

- `0x0091 / 0x0080 / 0x0082` remain weak or ambiguous as post-send success proof
- but they are **not** reliable pre-send tile-rejection signals in auto-search

Bot implication:

- target probe should log these packets
- but should not discard the searched tile based on them alone

## 2026-03-30 stability update: sync-first baseline + guarded accept chain

Applied in `gather_bot_v3.py`:

- `--working-profile` now also forces `--auto-search-sync-first`
  (order: troops -> sync -> prelude -> source) to match the stronger baseline.
- Added guarded strong-accept promotion when all of the following occur in one attempt:
  - `0x00B8` seen
  - `0x00B9` seen
  - at least one march/progress signal observed (`0x0076/0x0077/0x0078/0x007A` or `0x0033/0x0037`)
  - no error opcode

Reason:

- several recent live logs show repeated `0x00B8 + 0x00B9` chains without `0x0071/0x076C/0x007C`
  inside the short wait window, which caused unnecessary slot retries.
- guarded chain promotion is intended to reduce false-negative retries while still requiring
  more than weak/ambiguous opcodes.

## 2026-03-30 live retest after stability update

Live command executed via runner:

- `python D:\CascadeProjects\codex_lab\test_gather.py --no-log-session-candidates --slot-fallbacks 2,3 --pre-0ce8-heartbeat-wait 1.5`

Result:

- log: `gather_v3_20260330_144548.log`
- slot 1: no acceptance
- slot 2: received `0x00B8`, progress (`0x0037` + `0x0033`), and ack `0x00B9`
- chain-promoted strong accept triggered:
  - `CONFIRM strong accept via chain 0x00B8 + 0x00B9 (march_seen=0 progress_seen=2)`
- final status:
  - `GATHER STARTED (strong signal) via slot 2`

## 2026-03-30 correction after in-game verification

User-side live check reported no real gather in game for the above run.
So the interim chain rule was tightened again.

Updated rule in `gather_bot_v3.py`:

- removed promotion based on `0x0033/0x0037` progress packets
- guarded promotion now requires all of:
  - `0x00B8`
  - `0x00B9`
  - at least one post-send march packet (`0x0076/0x0077/0x0078/0x007A`)
  - target marker match inside that march packet payload
  - no error opcode

Practical effect:

- avoids false positives where `0x00B8+0x00B9` appears without real target-bound march state.

## 2026-03-30 1B8B structured probe (label sweep)

Probe command:

- `python D:\CascadeProjects\codex_lab\test_gather.py --no-log-session-candidates --slot-fallbacks 2,3 --pre-0ce8-heartbeat-wait 1.5 --probe-session-labels session_tail_le,session_head_le,server_key,crc32_session_bytes`

Observed behavior:

- each run sent `0x1B8B` structured in setup stage
- all tested seed-label variants disconnected quickly (`WinError 10053`) before gather completion
- probe logs:
  - `gather_v3_20260330_145456.log`
  - `gather_v3_20260330_145458.log`
  - `gather_v3_20260330_145500.log`
  - `gather_v3_20260330_145503.log`

Conclusion:

- current `build_1b8b_plain(seed32)` formulation is not accepted by server in live sessions
- keep `send_1b8b=no` for production gather path until lib-level derivation is exact
- `gather_bot_v3.py` setup send path now catches socket-abort errors and exits cleanly (no hard traceback crash)

lib evidence captured on 2026-03-30:

- `LogicPassword::encodePassword (0x039FAD00)` uses:
  - `atoi`
  - `RandomHelper::getEngine`
  - `uniform_int_distribution` (twice)
- This confirms current `seed32`-only 1B8B builder is oversimplified and can disconnect sessions.
