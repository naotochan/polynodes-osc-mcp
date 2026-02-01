---
name: polynodes-guide
description: Guide for controlling PolyNodes (sonicLAB) spatial sonic synthesizer via OSC. Covers the 3-layer architecture (Macro/Meso/Micro), DSP effects, and parameter workflows. Use when operating PolyNodes through MCP tools.
version: 0.1.0
---

# PolyNodes Guide

Use this skill when controlling PolyNodes via the MCP OSC tools.

---

## What is PolyNodes?

PolyNodes is a **spatial sonic synthesis** application by [sonicLAB](https://soniclab.net/polynodes/). It decomposes input audio into three temporal layers and spatializes them in 3D space. Control is done via OSC messages on `127.0.0.1:4799`.

---

## Architecture: Three Layers

PolyNodes processes audio through three concurrent layers, each operating at a different temporal scale:

| Layer | Scale | Description |
|-------|-------|-------------|
| **Macro** | Longest | Large-scale structural elements. Slowest playback rates (0.3-10). |
| **Meso** | Medium | Mid-scale textural elements. Medium playback rates (0.3-20). |
| **Micro** | Shortest | Fine-grain detail / particles. Fastest playback rates (0.3-30). |

Each layer has independent control over:
- **Gain** (-80 to 20 dB) and Solo
- **Envelope time** (0.01-0.5)
- **Playback rate** and its stochastic modulation range
- **Bandpass filter** (80-8000 Hz) with modulation range
- **Comb filter** with layer-specific delay ranges

The **Dry/Wet** control (0.0-1.0) blends original input with synthesized output.

---

## DSP Effects (Interactables)

These are global effects that act across all three layers:

### Black Hole
Gravitational attraction — pulls sound nodes inward. Per-layer force (0.0-1.0).

### White Hole
Repulsive reflection — pushes sound nodes outward. Per-layer force (0.0-1.0).

### Ring Modulator
Frequency modulation per layer (1.0-3.0).

### Bitcrusher / Decimater
Bit depth reduction (0.0-1.0) and sampling frequency range (0.0-5.0).

### Resonator
Resonant filter bank with frequency distribution (1.0-3.0) and wet/dry balance (0.0-0.5).

### Cuboid FX
Three spatial cuboid effects (C1/C2/C3). Each can be toggled independently. Return level per layer (1.0-80.0).

### IsoMorph Modulation
Modulates parameters based on spatial isomorphic mapping. Targets: frequency, amplitude, resonance. Depth 0.0-2.0 each. Bandpass center 0-5000 Hz.

---

## Typical Workflows

### Basic Setup
1. Select a preset slot (1-10)
2. Start playback
3. Adjust Dry/Wet balance
4. Set layer gains

### Creating Texture
1. Set playback rates per layer (slower = drone, faster = granular)
2. Enable granulator for micro-level fragmentation
3. Apply bandpass filters to shape frequency content
4. Add comb filters for metallic/resonant coloring

### Adding Movement
1. Enable Black Hole or White Hole for spatial dynamics
2. Use playback rate modulation ranges for stochastic variation
3. Trigger random navigation for evolving spatial patterns
4. Use IsoMorph for parameter modulation tied to spatial position

### Destructive / Glitch Effects
1. Enable Bitcrusher with low bit level
2. Enable Ring Modulator with varied per-layer frequencies
3. Trigger Rearrange mode to shuffle sample chunks
4. Use Poly Gates for rhythmic gating at BPM

---

## Parameter Tips

- **Modulation Range (MR)** parameters (0.0-0.75) add stochastic variation around the base value. Higher = more random.
- **Playback rate** at 1.0 = original speed. Below 1.0 = slower/pitched down. Above 1.0 = faster/pitched up.
- **Envelope time** controls attack/decay of each grain. Shorter = sharper transients. Longer = smoother pads.
- Use `polynodes_list_osc_addresses` to see all available OSC addresses and their ranges.
- Use `polynodes_send_raw_osc` for any address not covered by dedicated tools.

---

## Reference Files

| Topic | File |
|-------|------|
| All OSC addresses and ranges | `reference/osc-addresses.md` |

---

## MCP Tools Available

45+ tools organized by category:

- **Transport**: play/stop, preset slot, BPM
- **Gain**: per-layer gain, dry/wet, solo
- **Envelope**: per-layer envelope time
- **Playback Rate**: per-layer rate and modulation range
- **Granulator**: switch, duration, duration modulation range
- **Bandpass Filter**: per-layer switch, frequency, modulation range
- **Comb Filter**: per-layer switch, delay, modulation range
- **Black Hole / White Hole**: switch, per-layer force
- **Ring Modulator**: switch, per-layer frequency
- **Bitcrusher**: switch, bit level, range
- **Resonator**: switch, frequency distribution, balance
- **Cuboid FX**: per-cuboid switch, per-layer return level
- **IsoMorph**: switch, mod targets, depth, bandpass center
- **Navigation**: random trigger, rearrange, poly gates
- **Tuning**: PB rate and resonator tuning switches
- **Camera**: zoom, rotate
- **Utility**: list all OSC addresses, send raw OSC
