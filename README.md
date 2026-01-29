# polynodes-osc-mcp

MCP (Model Context Protocol) server for controlling [PolyNodes](https://soniclab.net/polynodes/) by sonicLAB via OSC.

This server enables AI assistants like Claude to control PolyNodes' spatial sonic synthesis parameters through natural language.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- PolyNodes running and receiving OSC on `127.0.0.1:4799`

## Setup

### Claude Code

Add to your project's MCP servers:

```bash
claude mcp add polynodes-osc-mcp -- uv run --directory /path/to/polynodes-osc-mcp python server.py
```

Or manually add to your Claude Code settings:

```json
{
  "mcpServers": {
    "polynodes-osc-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "/path/to/polynodes-osc-mcp", "python", "server.py"]
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "polynodes-osc-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/polynodes-osc-mcp", "python", "server.py"]
    }
  }
}
```

## Available Tools (45 total)

| Category | Tools |
|---|---|
| **Transport** | Play/Stop, Preset Slot (1-10), BPM (10-300) |
| **Gain** | Macro/Meso/Micro gain (-80 to 20 dB), Dry/Wet, Solo |
| **Envelope** | Attack/Decay time per layer (0.01-0.5) |
| **Playback Rate** | Rate per layer + stochastic modulation range |
| **Granulator** | On/Off, chunk duration (10-1000), modulation range |
| **Bandpass Filter** | On/Off, center frequency (80-8000 Hz), modulation per layer |
| **Comb Filter** | On/Off, delay, modulation per layer |
| **Black Hole** | On/Off, gravitational force per layer (0-1) |
| **White Hole** | On/Off, reflection force per layer (0-1) |
| **Ring Modulator** | On/Off, frequency per layer (1-3) |
| **Bitcrusher** | On/Off, bit depth (0-1), sampling range (0-5) |
| **Resonator** | On/Off, frequency distribution (1-3), balance (0-0.5) |
| **Cuboid FX** | 3 cuboids On/Off, return level per layer (1-80) |
| **IsoMorph** | On/Off, freq/amp/res modulation targets and depth |
| **Navigation** | Random trigger, Rearrange, Poly Gates |
| **Tuning** | PB rate and resonator tuning scale switches |
| **Camera** | Zoom, Rotate |
| **Raw OSC** | Send any OSC message directly |

## Usage Examples

Once configured, you can control PolyNodes with natural language:

- "Play and set BPM to 120"
- "Turn on the Black Hole and set macro force to 0.8"
- "Enable the granulator with duration 500"
- "Randomize all parameters"
- "Set a dark ambient texture with slow playback rates and high reverb"

## License

MIT
