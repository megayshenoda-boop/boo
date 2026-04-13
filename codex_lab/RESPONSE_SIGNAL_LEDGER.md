# Response Signal Ledger

Generated from `response_map.json` plus opcode-name hints parsed from test scripts.

| Response opcode | Names from tests | Signal class | Seen from action opcodes | Note |
|---|---|---|---|---|
| `0x0042` | HEARTBEAT | passive | 0x0065, 0x00BF, 0x0CED, 0x0CEE, 0x0CEF | Heartbeat only. Not useful as proof that the tested action succeeded. |
| `0x0076` | MAP_TILE | map_view | 0x0CEB | Map tile data. Strongly consistent with view/map reveal behavior. |
| `0x0077` | MAP_ARMY | map_view | 0x0CEB | Map army data. Supports the interpretation that the opcode triggered world view sync. |
| `0x0078` | MAP_DATA | map_view | 0x0CEB | Map data packet. Strong map-related signal, not a training confirmation. |
| `0x007A` | VIEW_DONE | map_view | 0x0CEB | View done marker in test artifacts. |
| `0x0095` | MAP_BUILD | map_view | 0x0CEB | Map building data. Supports the view/map interpretation. |
| `0x026D` | CHAT_MSG | unknown_but_repeated | 0x009D, 0x0CEB, 0x0CED, 0x0CEE, 0x0CEF | Repeated response across multiple tests. Important to parse, but meaning is still unclear. |
| `0x036C` | SERVER_TICK | passive | 0x009D, 0x0CEE | Server tick or background timing signal. Weak evidence by itself. |
| `0x0773` | - | unknown | 0x0CEB | No manual interpretation added yet. |

## Detailed notes

### 0x0042

- Names from test scripts: `['HEARTBEAT']`
- Signal class: `passive`
- Seen from action opcodes: `['0x0065', '0x00BF', '0x0CED', '0x0CEE', '0x0CEF']`
- Seen from current meanings: `['ITEM_USE', 'OLD_RESEARCH', 'TRAIN in current protocol.py', 'RESEARCH in current protocol.py', 'BUILD in current protocol.py']`
- Seen variants: `['0x0042(8B)']`
- Aggregate count: `5`
- Note: Heartbeat only. Not useful as proof that the tested action succeeded.

### 0x0076

- Names from test scripts: `['MAP_TILE']`
- Signal class: `map_view`
- Seen from action opcodes: `['0x0CEB']`
- Seen from current meanings: `['ENABLE_VIEW in current protocol.py']`
- Seen variants: `['0x0076(166B)']`
- Aggregate count: `1`
- Note: Map tile data. Strongly consistent with view/map reveal behavior.

### 0x0077

- Names from test scripts: `['MAP_ARMY']`
- Signal class: `map_view`
- Seen from action opcodes: `['0x0CEB']`
- Seen from current meanings: `['ENABLE_VIEW in current protocol.py']`
- Seen variants: `['0x0077(222B)']`
- Aggregate count: `1`
- Note: Map army data. Supports the interpretation that the opcode triggered world view sync.

### 0x0078

- Names from test scripts: `['MAP_DATA']`
- Signal class: `map_view`
- Seen from action opcodes: `['0x0CEB']`
- Seen from current meanings: `['ENABLE_VIEW in current protocol.py']`
- Seen variants: `['0x0078(490B)']`
- Aggregate count: `1`
- Note: Map data packet. Strong map-related signal, not a training confirmation.

### 0x007A

- Names from test scripts: `['VIEW_DONE']`
- Signal class: `map_view`
- Seen from action opcodes: `['0x0CEB']`
- Seen from current meanings: `['ENABLE_VIEW in current protocol.py']`
- Seen variants: `['0x007A(0B)']`
- Aggregate count: `1`
- Note: View done marker in test artifacts.

### 0x0095

- Names from test scripts: `['MAP_BUILD']`
- Signal class: `map_view`
- Seen from action opcodes: `['0x0CEB']`
- Seen from current meanings: `['ENABLE_VIEW in current protocol.py']`
- Seen variants: `['0x0095(74B)']`
- Aggregate count: `1`
- Note: Map building data. Supports the view/map interpretation.

### 0x026D

- Names from test scripts: `['CHAT_MSG']`
- Signal class: `unknown_but_repeated`
- Seen from action opcodes: `['0x009D', '0x0CEB', '0x0CED', '0x0CEE', '0x0CEF']`
- Seen from current meanings: `['OLD_BUILD', 'ENABLE_VIEW in current protocol.py', 'TRAIN in current protocol.py', 'RESEARCH in current protocol.py', 'BUILD in current protocol.py']`
- Seen variants: `['0x026D(116B)', '0x026D(130B)', '0x026D(324B)', '0x026D(111B)', '0x026D(151B)', '0x026D(126B)', '0x026D(117B)', '0x026D(124B)', '0x026D(171B)', '0x026D(174B)', '0x026D(337B)', '0x026D(169B)']`
- Aggregate count: `13`
- Note: Repeated response across multiple tests. Important to parse, but meaning is still unclear.

### 0x036C

- Names from test scripts: `['SERVER_TICK']`
- Signal class: `passive`
- Seen from action opcodes: `['0x009D', '0x0CEE']`
- Seen from current meanings: `['OLD_BUILD', 'RESEARCH in current protocol.py']`
- Seen variants: `['0x036C(4B)']`
- Aggregate count: `2`
- Note: Server tick or background timing signal. Weak evidence by itself.

### 0x0773

- Names from test scripts: none
- Signal class: `unknown`
- Seen from action opcodes: `['0x0CEB']`
- Seen from current meanings: `['ENABLE_VIEW in current protocol.py']`
- Seen variants: `['0x0773(70B)']`
- Aggregate count: `1`
- Note: No manual interpretation added yet.
