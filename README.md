# polynodes-osc-mcp

[日本語](README.ja.md)

MCP (Model Context Protocol) server for controlling [PolyNodes](https://soniclab.net/polynodes/) by sonicLAB via OSC.

This server lets [Cursor](https://cursor.com) control PolyNodes' spatial sonic synthesis parameters through natural language.

**Local install and path notes live in [LOCAL.md](LOCAL.md)** (Cursor-first). Cloud agents cannot see your clone path; register the MCP on the machine that runs PolyNodes.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- PolyNodes running and receiving OSC (default `127.0.0.1:4799`)
- Cursor as the MCP host (do not start `server.py` by hand)

## Setup

Follow [LOCAL.md](LOCAL.md). Short version:

1. Clone this repo locally (`pwd` is the install path)
2. Start PolyNodes
3. クローン先を `--directory` にしたエントリを `~/.cursor/mcp.json` に追加する（JSON の形は [LOCAL.md](LOCAL.md)）
4. Enable it in Cursor Settings → Tools & MCP until it shows green
5. In Agent chat: "Play and set BPM to 120"

### OSC connection

Override the default host and port with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `POLYNODES_OSC_HOST` | `127.0.0.1` | PolyNodes OSC host |
| `POLYNODES_OSC_PORT` | `4799` | PolyNodes OSC port |

## API (v0.2)

Two tools and one resource replace the previous per-parameter tool list:

| Name | Type | Description |
|------|------|-------------|
| `polynodes_set` | tool | Batch-set one or more params in a single OSC burst |
| `polynodes_raw` | tool | Send any OSC address/value (escape hatch) |
| `polynodes://catalog` | resource | JSON catalog of param names, OSC addresses, ranges, and per-layer requirements |

Read `polynodes://catalog` when unsure of param names or valid ranges. Per-layer params (`gain`, `playback_rate`, `filter_freq`, etc.) require `level`: `macro`, `meso`, or `micro`. Switches accept `0`/`1` or `bool`.

Param categories include transport, gain, envelope, playback rate, granulator, filters, DSP interactables (Black Hole, White Hole, Ring Mod, Crusher, Resonator), Cuboid FX, IsoMorph, navigation, tuning, and camera.

## Usage Examples

Once configured, you can control PolyNodes with natural language:

- "Play and set BPM to 120"
- "Turn on the Black Hole and set macro force to 0.8"
- "Enable the granulator with duration 500"
- "Set macro playback rate to 0.5 and meso to 2.0 in one batch"

Example `polynodes_set` batch:

```json
[
  {"param": "play", "value": 1},
  {"param": "bpm", "value": 120},
  {"param": "blackhole", "value": true},
  {"param": "blackhole_force", "level": "macro", "value": 0.8}
]
```

## Development

```bash
uv sync --extra dev
pytest
```

## License

MIT
