# Gather (0x0CE8) - Analysis Findings

## What WORKS
- Login (HTTP + Gateway + Game Server) = OK
- World Entry (0x0021) = OK
- Server Key extraction from 0x0038 = OK
- Standard encryption (offset-4) = OK for Train/Build/Research
- Setup packets (0x0840, 0x17D4, 0x0AF2, 0x0245, 0x0834, 0x0709, 0x0A2C, 0x1357, 0x170D) = OK
- 0x0CE8 gather plaintext = MATCHES PCAP byte-for-byte (verified 21 PCAPs)
- 0x1B8B encoding = BYTE-IDENTICAL to PCAP (verified with same inputs)
- Session stays alive WITHOUT 0x1B8B (heartbeats work for 10+ seconds)

## What FAILS
- **0x1B8B always causes server disconnect** (0.2s after sending)
- Without 0x1B8B: slot=2 gets 0x00B8 but no 0x0071 (march doesn't start)
- Without 0x1B8B: slot=1 gets no response at all

## Key Question
If encoding is byte-perfect, WHY does server reject 0x1B8B?

## Hypothesis: Server-side session state
The server may validate 0x1B8B against session state we haven't replicated.
In every PCAP, the C2S sequence before 0x1B8B is:
```
0x001F → 0x0021 → [init flood] → 0x0840 → 0x17D4 → 0x0AF2 → 0x0245 → 0x0834 → 0x0709 → 0x0A2C → [0x1357 → 0x170D] → 0x1B8B
```

Our bot sends this EXACT sequence. But timing differs:
- PCAP: 0x1B8B at ~1.2s after world entry (interleaved with init flood)
- Bot: 0x1B8B at 0.3-10s after world entry (various attempts, ALL fail)

## TODO: Compare 0x00B8 responses
Check if the 0x00B8 we receive (without 0x1B8B) matches the PCAP's 0x00B8.
If different → 0x00B8 contains error info
If same → march should work, maybe timing/ordering issue

## TODO: Try gather with hero=255
Most PCAPs use hero_id=255, not 226. Try both.

## TODO: Analyze 0x00B8 from PCAP
Decrypt and compare with our response.
