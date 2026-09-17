# PolyNodes OSC Address Reference

Generated from `osc_registry.py`. All OSC messages default to `127.0.0.1:4799` (override with `POLYNODES_OSC_HOST` / `POLYNODES_OSC_PORT`).


## Transport

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `play` | `/polynodes/playstartstop` | Play/Stop | 0.0-1.0 |
| `preset` | `/polynodes/presetslot` | Preset slot | 1.0-10.0 |
| `bpm` | `/polynodes/seqbpm` | Sequencer BPM | 10.0-300.0 |

## Gain

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `gain` (macro) | `/polynodes/MacroGain` | Layer gain dB | -80.0-20.0 |
| `gain` (meso) | `/polynodes/MesoGain` | Layer gain dB | -80.0-20.0 |
| `gain` (micro) | `/polynodes/MicroGain` | Layer gain dB | -80.0-20.0 |
| `dry_wet` | `/polynodes/DryWet` | Dry/Wet balance | 0.0-1.0 |
| `solo` (macro) | `/polynodes/MacroGainsolo` | Layer solo | 0.0-1.0 |
| `solo` (meso) | `/polynodes/MesoGainsolo` | Layer solo | 0.0-1.0 |
| `solo` (micro) | `/polynodes/MicroGainsolo` | Layer solo | 0.0-1.0 |

## Envelope

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `envelope_time` (macro) | `/polynodes/MacroEnvtime` | Envelope time | 0.01-0.5 |
| `envelope_time` (meso) | `/polynodes/MesoEnvtime` | Envelope time | 0.01-0.5 |
| `envelope_time` (micro) | `/polynodes/MicroEnvtime` | Envelope time | 0.01-0.5 |

## Playback Rate

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `playback_rate` (macro) | `/polynodes/pbrmacro` | Playback rate | 0.3-10.0 |
| `playback_rate` (meso) | `/polynodes/pbrmeso` | Playback rate | 0.3-20.0 |
| `playback_rate` (micro) | `/polynodes/pbrmicro` | Playback rate | 0.3-30.0 |
| `playback_rate_mod` (macro) | `/polynodes/pbrmacroMR` | PB rate mod range | 0.0-0.75 |
| `playback_rate_mod` (meso) | `/polynodes/pbrmesoMR` | PB rate mod range | 0.0-0.75 |
| `playback_rate_mod` (micro) | `/polynodes/pbrmicroMR` | PB rate mod range | 0.0-0.75 |

## Granulator

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `granulator` | `/polynodes/granusw` | Granulator switch | 0.0-1.0 |
| `granular_duration` | `/polynodes/granuDur` | Chunk duration | 10.0-1000.0 |
| `granular_duration_mod` | `/polynodes/granuDurMR` | Duration mod range | 0.0-0.75 |

## Bandpass Filter

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `filter` (macro) | `/polynodes/filtmacrosw` | Bandpass filter switch | 0.0-1.0 |
| `filter` (meso) | `/polynodes/filtmesosw` | Bandpass filter switch | 0.0-1.0 |
| `filter` (micro) | `/polynodes/filtmicrosw` | Bandpass filter switch | 0.0-1.0 |
| `filter_freq` (macro) | `/polynodes/filtmacro` | Center frequency Hz | 80.0-8000.0 |
| `filter_freq` (meso) | `/polynodes/filtmeso` | Center frequency Hz | 80.0-8000.0 |
| `filter_freq` (micro) | `/polynodes/filtmicro` | Center frequency Hz | 80.0-8000.0 |
| `filter_mod` (macro) | `/polynodes/filtmacroMR` | Filter mod range | 0.0-0.75 |
| `filter_mod` (meso) | `/polynodes/filtmesoMR` | Filter mod range | 0.0-0.75 |
| `filter_mod` (micro) | `/polynodes/filtmicroMR` | Filter mod range | 0.0-0.75 |

## Comb Filter

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `comb` (macro) | `/polynodes/combmacrosw` | Comb filter switch | 0.0-1.0 |
| `comb` (meso) | `/polynodes/combmesosw` | Comb filter switch | 0.0-1.0 |
| `comb` (micro) | `/polynodes/combmicrosw` | Comb filter switch | 0.0-1.0 |
| `comb_delay` (macro) | `/polynodes/combmacro` | Comb delay | 10.0-3000.0 |
| `comb_delay` (meso) | `/polynodes/combmeso` | Comb delay | 10.0-1000.0 |
| `comb_delay` (micro) | `/polynodes/combmicro` | Comb delay | 10.0-300.0 |
| `comb_mod` (macro) | `/polynodes/combmacroMR` | Comb mod range | 0.0-0.75 |
| `comb_mod` (meso) | `/polynodes/combmesoMR` | Comb mod range | 0.0-0.75 |
| `comb_mod` (micro) | `/polynodes/combmicroMR` | Comb mod range | 0.0-0.75 |

## Black Hole

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `blackhole` | `/polynodes/BHsw` | Black Hole switch | 0.0-1.0 |
| `blackhole_force` (macro) | `/polynodes/BHmacroforce` | BH force | 0.0-1.0 |
| `blackhole_force` (meso) | `/polynodes/BHmesoforce` | BH force | 0.0-1.0 |
| `blackhole_force` (micro) | `/polynodes/BHmicroforce` | BH force | 0.0-1.0 |

## White Hole

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `whitehole` | `/polynodes/WHsw` | White Hole switch | 0.0-1.0 |
| `whitehole_force` (macro) | `/polynodes/WHmacroforce` | WH force | 0.0-1.0 |
| `whitehole_force` (meso) | `/polynodes/WHmesoforce` | WH force | 0.0-1.0 |
| `whitehole_force` (micro) | `/polynodes/WHmicroforce` | WH force | 0.0-1.0 |

## Ring Modulator

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `ringmod` | `/polynodes/RMsw` | Ring Mod switch | 0.0-1.0 |
| `ringmod_freq` (macro) | `/polynodes/RMmacro` | Ring mod frequency | 1.0-3.0 |
| `ringmod_freq` (meso) | `/polynodes/RMmeso` | Ring mod frequency | 1.0-3.0 |
| `ringmod_freq` (micro) | `/polynodes/RMmicro` | Ring mod frequency | 1.0-3.0 |

## Bitcrusher

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `crush` | `/polynodes/CRSsw` | Crusher switch | 0.0-1.0 |
| `crush_bit` | `/polynodes/CRSbitLvl` | Bit depth level | 0.0-1.0 |
| `crush_range` | `/polynodes/CRSrange` | Sampling freq range | 0.0-5.0 |

## Resonator

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `resonator` | `/polynodes/ResoSw` | Resonator switch | 0.0-1.0 |
| `resonator_freq_dist` | `/polynodes/ResoFreqdist` | Freq distribution | 1.0-3.0 |
| `resonator_balance` | `/polynodes/ResoBalance` | Wet/dry balance | 0.0-0.5 |

## Cuboid FX

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `cuboid_1` | `/polynodes/C1sw` | Cuboid 1 switch | 0.0-1.0 |
| `cuboid_2` | `/polynodes/C2sw` | Cuboid 2 switch | 0.0-1.0 |
| `cuboid_3` | `/polynodes/C3sw` | Cuboid 3 switch | 0.0-1.0 |
| `cuboid_return` (macro) | `/polynodes/MacroreturnLvl` | Cuboid return level | 1.0-80.0 |
| `cuboid_return` (meso) | `/polynodes/MesoreturnLvl` | Cuboid return level | 1.0-80.0 |
| `cuboid_return` (micro) | `/polynodes/MicroreturnLvl` | Cuboid return level | 1.0-80.0 |

## IsoMorph

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `isomorph` | `/polynodes/isomorphsw` | IsoMorph switch | 0.0-1.0 |
| `isomorph_freq` | `/polynodes/isomfreqsw` | Freq mod switch | 0.0-1.0 |
| `isomorph_amp` | `/polynodes/isomampsw` | Amp mod switch | 0.0-1.0 |
| `isomorph_res` | `/polynodes/isomressw` | Res mod switch | 0.0-1.0 |
| `isomorph_freq_depth` | `/polynodes/isomfreqmodr` | Freq mod depth | 0.0-2.0 |
| `isomorph_amp_depth` | `/polynodes/isomampmodr` | Amp mod depth | 0.0-2.0 |
| `isomorph_res_depth` | `/polynodes/isomresmodr` | Res mod depth | 0.0-2.0 |
| `isomorph_bp_center` | `/polynodes/isombpcent` | Bandpass center | 0.0-5000.0 |

## Navigation & Misc

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `nav_random` | `/polynodes/navigrndtrig` | Random nav trigger | 0.0-1.0 |
| `rearrange` | `/polynodes/rearrtrig` | Rearrange trigger | 0.0-1.0 |
| `poly_gates` | `/polynodes/polygatessw` | Poly Gates switch | 0.0-1.0 |

## Tuning

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `tuning_pb` | `/polynodes/tuningpbsw` | Tuning PB switch | 0.0-1.0 |
| `tuning_res` | `/polynodes/tuningressw` | Tuning Res switch | 0.0-1.0 |

## Camera

| Param | Address | Description | Range |
|-------|---------|-------------|-------|
| `camera_zoom` | `/polynodes/camzoom` | Camera zoom | unbounded |
| `camera_rotate` | `/polynodes/camrotate` | Camera rotate radians | unbounded |
