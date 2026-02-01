# PolyNodes OSC Address Reference

All OSC messages are sent to `127.0.0.1:4799`.

## Transport

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/playstartstop` | Play/Stop | 0.0 or 1.0 |
| `/polynodes/presetslot` | Preset slot | 1-10 |
| `/polynodes/seqbpm` | Sequencer BPM | 10-300 |

## Gain

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/MacroGain` | Macro gain | -80 to 20 dB |
| `/polynodes/MesoGain` | Meso gain | -80 to 20 dB |
| `/polynodes/MicroGain` | Micro gain | -80 to 20 dB |
| `/polynodes/DryWet` | Dry/Wet balance | 0.0-1.0 |
| `/polynodes/MacroGainsolo` | Macro solo | 0/1 |
| `/polynodes/MesoGainsolo` | Meso solo | 0/1 |
| `/polynodes/MicroGainsolo` | Micro solo | 0/1 |

## Envelope

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/MacroEnvtime` | Macro envelope time | 0.01-0.5 |
| `/polynodes/MesoEnvtime` | Meso envelope time | 0.01-0.5 |
| `/polynodes/MicroEnvtime` | Micro envelope time | 0.01-0.5 |

## Playback Rate

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/pbrmacro` | Macro playback rate | 0.3-10 |
| `/polynodes/pbrmeso` | Meso playback rate | 0.3-20 |
| `/polynodes/pbrmicro` | Micro playback rate | 0.3-30 |
| `/polynodes/pbrmacroMR` | Macro PB rate mod range | 0.0-0.75 |
| `/polynodes/pbrmesoMR` | Meso PB rate mod range | 0.0-0.75 |
| `/polynodes/pbrmicroMR` | Micro PB rate mod range | 0.0-0.75 |

## Granulator

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/granusw` | Granulator switch | 0/1 |
| `/polynodes/granuDur` | Chunk duration | 10-1000 |
| `/polynodes/granuDurMR` | Duration mod range | 0.0-0.75 |

## Bandpass Filter

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/filtmacrosw` | Macro filter switch | 0/1 |
| `/polynodes/filtmesosw` | Meso filter switch | 0/1 |
| `/polynodes/filtmicrosw` | Micro filter switch | 0/1 |
| `/polynodes/filtmacro` | Macro center freq | 80-8000 Hz |
| `/polynodes/filtmeso` | Meso center freq | 80-8000 Hz |
| `/polynodes/filtmicro` | Micro center freq | 80-8000 Hz |
| `/polynodes/filtmacroMR` | Macro filter mod range | 0.0-0.75 |
| `/polynodes/filtmesoMR` | Meso filter mod range | 0.0-0.75 |
| `/polynodes/filtmicroMR` | Micro filter mod range | 0.0-0.75 |

## Comb Filter

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/combmacrosw` | Macro comb switch | 0/1 |
| `/polynodes/combmesosw` | Meso comb switch | 0/1 |
| `/polynodes/combmicrosw` | Micro comb switch | 0/1 |
| `/polynodes/combmacro` | Macro comb delay | 10-3000 |
| `/polynodes/combmeso` | Meso comb delay | 10-1000 |
| `/polynodes/combmicro` | Micro comb delay | 10-300 |
| `/polynodes/combmacroMR` | Macro comb mod range | 0.0-0.75 |
| `/polynodes/combmesoMR` | Meso comb mod range | 0.0-0.75 |
| `/polynodes/combmicroMR` | Micro comb mod range | 0.0-0.75 |

## Black Hole

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/BHsw` | Black Hole switch | 0/1 |
| `/polynodes/BHmacroforce` | Macro force | 0.0-1.0 |
| `/polynodes/BHmesoforce` | Meso force | 0.0-1.0 |
| `/polynodes/BHmicroforce` | Micro force | 0.0-1.0 |

## White Hole

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/WHsw` | White Hole switch | 0/1 |
| `/polynodes/WHmacroforce` | Macro force | 0.0-1.0 |
| `/polynodes/WHmesoforce` | Meso force | 0.0-1.0 |
| `/polynodes/WHmicroforce` | Micro force | 0.0-1.0 |

## Ring Modulator

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/RMsw` | Ring Mod switch | 0/1 |
| `/polynodes/RMmacro` | Macro mod freq | 1.0-3.0 |
| `/polynodes/RMmeso` | Meso mod freq | 1.0-3.0 |
| `/polynodes/RMmicro` | Micro mod freq | 1.0-3.0 |

## Bitcrusher

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/CRSsw` | Crusher switch | 0/1 |
| `/polynodes/CRSbitLvl` | Bit depth level | 0.0-1.0 |
| `/polynodes/CRSrange` | Sampling freq range | 0.0-5.0 |

## Resonator

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/ResoSw` | Resonator switch | 0/1 |
| `/polynodes/ResoFreqdist` | Freq distribution | 1.0-3.0 |
| `/polynodes/ResoBalance` | Wet/dry balance | 0.0-0.5 |

## Cuboid FX

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/C1sw` | Cuboid 1 switch | 0/1 |
| `/polynodes/C2sw` | Cuboid 2 switch | 0/1 |
| `/polynodes/C3sw` | Cuboid 3 switch | 0/1 |
| `/polynodes/MacroreturnLvl` | Macro return level | 1.0-80.0 |
| `/polynodes/MesoreturnLvl` | Meso return level | 1.0-80.0 |
| `/polynodes/MicroreturnLvl` | Micro return level | 1.0-80.0 |

## IsoMorph

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/isomorphsw` | IsoMorph switch | 0/1 |
| `/polynodes/isomfreqsw` | Freq mod switch | 0/1 |
| `/polynodes/isomfreqmodr` | Freq mod depth | 0.0-2.0 |
| `/polynodes/isomampsw` | Amp mod switch | 0/1 |
| `/polynodes/isomampmodr` | Amp mod depth | 0.0-2.0 |
| `/polynodes/isomressw` | Res mod switch | 0/1 |
| `/polynodes/isomresmodr` | Res mod depth | 0.0-2.0 |
| `/polynodes/isombpcent` | Bandpass center | 0-5000 |

## Navigation & Misc

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/navigrndtrig` | Random nav trigger | 0/1 |
| `/polynodes/rearrtrig` | Rearrange trigger | 0/1 |
| `/polynodes/polygatessw` | Poly Gates switch | 0/1 |

## Tuning

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/tuningpbsw` | Tuning PB switch | 0/1 |
| `/polynodes/tuningressw` | Tuning Res switch | 0/1 |

## Camera

| Address | Description | Range |
|---------|-------------|-------|
| `/polynodes/camzoom` | Camera zoom | +/- float |
| `/polynodes/camrotate` | Camera rotate | radians |
