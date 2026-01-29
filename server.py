#!/usr/bin/env python3
"""
MCP Server for PolyNodes - Spatial Sonic Sculptor by sonicLAB.

Controls PolyNodes application via OSC (Open Sound Control) protocol.
PolyNodes receives OSC messages on port 4799 (default) at 127.0.0.1.
"""

import json
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, field_validator
from mcp.server.fastmcp import FastMCP
from pythonosc import udp_client

# ---------------------------------------------------------------------------
# Server & OSC client setup
# ---------------------------------------------------------------------------

mcp = FastMCP("polynodes_mcp")

# Default OSC connection settings
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4799

_osc_client: Optional[udp_client.SimpleUDPClient] = None


def _get_client(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> udp_client.SimpleUDPClient:
    """Get or create an OSC UDP client."""
    global _osc_client
    if _osc_client is None:
        _osc_client = udp_client.SimpleUDPClient(host, port)
    return _osc_client


def _send_osc(address: str, value: float) -> str:
    """Send a single OSC message and return confirmation."""
    client = _get_client()
    client.send_message(address, value)
    return json.dumps({"status": "sent", "address": address, "value": value})


# ---------------------------------------------------------------------------
# Input Models
# ---------------------------------------------------------------------------

class PlayStopInput(BaseModel):
    """Input for play/stop control."""
    model_config = ConfigDict(str_strip_whitespace=True)
    state: float = Field(..., description="1.0 to play, 0.0 to stop", ge=0.0, le=1.0)


class PresetSlotInput(BaseModel):
    """Input for preset selection."""
    model_config = ConfigDict(str_strip_whitespace=True)
    slot: float = Field(..., description="Preset slot number (1 to 10)", ge=1.0, le=10.0)


class GainInput(BaseModel):
    """Input for gain/volume controls."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="Which level: 'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Gain value in dB (-80.0 to 20.0)", ge=-80.0, le=20.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class DryWetInput(BaseModel):
    """Input for dry/wet balance."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Dry/Wet balance (0.0 = dry, 1.0 = wet)", ge=0.0, le=1.0)


class EnvelopeTimeInput(BaseModel):
    """Input for envelope time."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Envelope time (0.01 to 0.5)", ge=0.01, le=0.5)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class PlaybackRateInput(BaseModel):
    """Input for playback rate."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro' (0.3-10), 'meso' (0.3-20), or 'micro' (0.3-30)")
    value: float = Field(..., description="Playback rate value")

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class PlaybackRateMRInput(BaseModel):
    """Input for playback rate modulation range."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Modulation range (0.0 to 0.75)", ge=0.0, le=0.75)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class SwitchInput(BaseModel):
    """Generic on/off switch input."""
    model_config = ConfigDict(str_strip_whitespace=True)
    state: float = Field(..., description="0.0 = off, 1.0 = on", ge=0.0, le=1.0)


class GranularDurationInput(BaseModel):
    """Input for granular duration."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Duration (10.0 to 1000.0)", ge=10.0, le=1000.0)


class GranularDurationMRInput(BaseModel):
    """Input for granular duration modulation range."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Modulation range (0.0 to 0.75)", ge=0.0, le=0.75)


class FilterInput(BaseModel):
    """Input for bandpass filter frequency."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Center frequency (80.0 to 8000.0 Hz)", ge=80.0, le=8000.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class FilterMRInput(BaseModel):
    """Input for bandpass filter modulation range."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Modulation range (0.0 to 0.75)", ge=0.0, le=0.75)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class FilterSwitchInput(BaseModel):
    """Input for filter on/off per level."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    state: float = Field(..., description="0.0 = off, 1.0 = on", ge=0.0, le=1.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class CombInput(BaseModel):
    """Input for comb filter delay."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro' (10-3000), 'meso' (10-1000), or 'micro' (10-300)")
    value: float = Field(..., description="Comb delay amount")

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class CombMRInput(BaseModel):
    """Input for comb filter modulation range."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Modulation range (0.0 to 0.75)", ge=0.0, le=0.75)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class CombSwitchInput(BaseModel):
    """Input for comb filter on/off per level."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    state: float = Field(..., description="0.0 = off, 1.0 = on", ge=0.0, le=1.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class ForceInput(BaseModel):
    """Input for DSP interactable force (BH / WH)."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Force (0.0 to 1.0)", ge=0.0, le=1.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class RingModInput(BaseModel):
    """Input for ring modulator frequency."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Mod frequency (1.0 to 3.0)", ge=1.0, le=3.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class CubeReturnInput(BaseModel):
    """Input for cuboid FX return level."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    value: float = Field(..., description="Return level (1.0 to 80.0)", ge=1.0, le=80.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class GainSoloInput(BaseModel):
    """Input for gain solo."""
    model_config = ConfigDict(str_strip_whitespace=True)
    level: str = Field(..., description="'macro', 'meso', or 'micro'")
    state: float = Field(..., description="0.0 = off, 1.0 = solo", ge=0.0, le=1.0)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("macro", "meso", "micro"):
            raise ValueError("level must be 'macro', 'meso', or 'micro'")
        return v


class CrushBitInput(BaseModel):
    """Input for bitcrusher bit level."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Bit level (0.0 to 1.0)", ge=0.0, le=1.0)


class CrushRangeInput(BaseModel):
    """Input for bitcrusher range."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Range (0.0 to 5.0)", ge=0.0, le=5.0)


class ResonatorFreqDistInput(BaseModel):
    """Input for resonator frequency distribution."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Frequency distribution (1.0 to 3.0)", ge=1.0, le=3.0)


class ResonatorBalanceInput(BaseModel):
    """Input for resonator balance."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Balance (0.0 to 0.5)", ge=0.0, le=0.5)


class IsomorphModInput(BaseModel):
    """Input for isomorphic modulation depth."""
    model_config = ConfigDict(str_strip_whitespace=True)
    param: str = Field(..., description="'freq', 'amp', or 'res'")
    value: float = Field(..., description="Modulation depth (0.0 to 2.0)", ge=0.0, le=2.0)

    @field_validator("param")
    @classmethod
    def validate_param(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in ("freq", "amp", "res"):
            raise ValueError("param must be 'freq', 'amp', or 'res'")
        return v


class IsomorphBPCenterInput(BaseModel):
    """Input for isomorphic bandpass center."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Bandpass center (0.0 to 5000.0)", ge=0.0, le=5000.0)


class CameraZoomInput(BaseModel):
    """Input for camera zoom."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Zoom amount (positive = in, negative = out)")


class CameraRotateInput(BaseModel):
    """Input for camera rotation."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="Rotation in radians")


class BPMInput(BaseModel):
    """Input for BPM."""
    model_config = ConfigDict(str_strip_whitespace=True)
    value: float = Field(..., description="BPM (10.0 to 300.0)", ge=10.0, le=300.0)


# ---------------------------------------------------------------------------
# Tools - Transport / Playback
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_play_stop",
    annotations={
        "title": "Play/Stop PolyNodes",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_play_stop(params: PlayStopInput) -> str:
    """Start or stop PolyNodes playback.

    Args:
        params: state=1.0 to play, state=0.0 to stop.

    Returns:
        JSON confirmation of the sent OSC message.
    """
    return _send_osc("/polynodes/playstartstop", params.state)


@mcp.tool(
    name="polynodes_preset_slot",
    annotations={
        "title": "Select Preset Slot",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_preset_slot(params: PresetSlotInput) -> str:
    """Select a preset slot (1-10) on PolyNodes.

    Args:
        params: slot number 1-10.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/presetslot", params.slot)


# ---------------------------------------------------------------------------
# Tools - Gain
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_set_gain",
    annotations={
        "title": "Set Layer Gain",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_gain(params: GainInput) -> str:
    """Set gain for a macro/meso/micro layer (-80 to 20 dB).

    Args:
        params: level ('macro','meso','micro') and value in dB.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/MacroGain",
        "meso": "/polynodes/MesoGain",
        "micro": "/polynodes/MicroGain",
    }
    return _send_osc(addr_map[params.level], params.value)


@mcp.tool(
    name="polynodes_set_dry_wet",
    annotations={
        "title": "Set Dry/Wet Balance",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_dry_wet(params: DryWetInput) -> str:
    """Set the dry/wet balance (0.0=dry original, 1.0=wet synthesis).

    Args:
        params: value 0.0-1.0.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/DryWet", params.value)


@mcp.tool(
    name="polynodes_gain_solo",
    annotations={
        "title": "Solo Layer Gain",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_gain_solo(params: GainSoloInput) -> str:
    """Solo a specific layer (macro/meso/micro).

    Args:
        params: level and state (1.0=solo, 0.0=unsolo).

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/MacroGainsolo",
        "meso": "/polynodes/MesoGainsolo",
        "micro": "/polynodes/MicroGainsolo",
    }
    return _send_osc(addr_map[params.level], params.state)


# ---------------------------------------------------------------------------
# Tools - Envelope
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_set_envelope_time",
    annotations={
        "title": "Set Envelope Time",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_envelope_time(params: EnvelopeTimeInput) -> str:
    """Set attack/decay envelope time for macro/meso/micro agents (0.01-0.5).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/MacroEnvtime",
        "meso": "/polynodes/MesoEnvtime",
        "micro": "/polynodes/MicroEnvtime",
    }
    return _send_osc(addr_map[params.level], params.value)


# ---------------------------------------------------------------------------
# Tools - Playback Rate
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_set_playback_rate",
    annotations={
        "title": "Set Playback Rate",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_playback_rate(params: PlaybackRateInput) -> str:
    """Set playback rate for agents. Macro: 0.3-10, Meso: 0.3-20, Micro: 0.3-30.

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/pbrmacro",
        "meso": "/polynodes/pbrmeso",
        "micro": "/polynodes/pbrmicro",
    }
    return _send_osc(addr_map[params.level], params.value)


@mcp.tool(
    name="polynodes_set_playback_rate_mod_range",
    annotations={
        "title": "Set PB Rate Modulation Range",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_playback_rate_mod_range(params: PlaybackRateMRInput) -> str:
    """Set the stochastic modulation range for playback rate (0.0-0.75).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/pbrmacroMR",
        "meso": "/polynodes/pbrmesoMR",
        "micro": "/polynodes/pbrmicroMR",
    }
    return _send_osc(addr_map[params.level], params.value)


# ---------------------------------------------------------------------------
# Tools - Granulator
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_granular_switch",
    annotations={
        "title": "Granulator On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_granular_switch(params: SwitchInput) -> str:
    """Turn the granulator on or off.

    Args:
        params: state 1.0=on, 0.0=off.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/granusw", params.state)


@mcp.tool(
    name="polynodes_granular_duration",
    annotations={
        "title": "Set Granular Duration",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_granular_duration(params: GranularDurationInput) -> str:
    """Set granular chunk duration (10-1000).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/granuDur", params.value)


@mcp.tool(
    name="polynodes_granular_duration_mod_range",
    annotations={
        "title": "Set Granular Duration Mod Range",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_granular_duration_mod_range(params: GranularDurationMRInput) -> str:
    """Set granular duration modulation range (0.0-0.75).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/granuDurMR", params.value)


# ---------------------------------------------------------------------------
# Tools - Bandpass Filter
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_filter_switch",
    annotations={
        "title": "Bandpass Filter On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_filter_switch(params: FilterSwitchInput) -> str:
    """Turn bandpass filter on/off for a layer.

    Args:
        params: level and state.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/filtmacrosw",
        "meso": "/polynodes/filtmesosw",
        "micro": "/polynodes/filtmicrosw",
    }
    return _send_osc(addr_map[params.level], params.state)


@mcp.tool(
    name="polynodes_set_filter_freq",
    annotations={
        "title": "Set Filter Frequency",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_filter_freq(params: FilterInput) -> str:
    """Set bandpass filter center frequency (80-8000 Hz).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/filtmacro",
        "meso": "/polynodes/filtmeso",
        "micro": "/polynodes/filtmicro",
    }
    return _send_osc(addr_map[params.level], params.value)


@mcp.tool(
    name="polynodes_set_filter_mod_range",
    annotations={
        "title": "Set Filter Modulation Range",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_filter_mod_range(params: FilterMRInput) -> str:
    """Set bandpass filter modulation range (0.0-0.75).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/filtmacroMR",
        "meso": "/polynodes/filtmesoMR",
        "micro": "/polynodes/filtmicroMR",
    }
    return _send_osc(addr_map[params.level], params.value)


# ---------------------------------------------------------------------------
# Tools - Comb Filter
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_comb_switch",
    annotations={
        "title": "Comb Filter On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_comb_switch(params: CombSwitchInput) -> str:
    """Turn comb filter on/off for a layer.

    Args:
        params: level and state.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/combmacrosw",
        "meso": "/polynodes/combmesosw",
        "micro": "/polynodes/combmicrosw",
    }
    return _send_osc(addr_map[params.level], params.state)


@mcp.tool(
    name="polynodes_set_comb_delay",
    annotations={
        "title": "Set Comb Delay",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_comb_delay(params: CombInput) -> str:
    """Set comb filter delay. Macro: 10-3000, Meso: 10-1000, Micro: 10-300.

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/combmacro",
        "meso": "/polynodes/combmeso",
        "micro": "/polynodes/combmicro",
    }
    return _send_osc(addr_map[params.level], params.value)


@mcp.tool(
    name="polynodes_set_comb_mod_range",
    annotations={
        "title": "Set Comb Modulation Range",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_comb_mod_range(params: CombMRInput) -> str:
    """Set comb filter modulation range (0.0-0.75).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/combmacroMR",
        "meso": "/polynodes/combmesoMR",
        "micro": "/polynodes/combmicroMR",
    }
    return _send_osc(addr_map[params.level], params.value)


# ---------------------------------------------------------------------------
# Tools - DSP Interactables (Black Hole, White Hole, Ring Mod, Crusher, Resonator)
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_blackhole_switch",
    annotations={
        "title": "Black Hole On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_blackhole_switch(params: SwitchInput) -> str:
    """Turn the Black Hole DSP interactable on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/BHsw", params.state)


@mcp.tool(
    name="polynodes_blackhole_force",
    annotations={
        "title": "Set Black Hole Force",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_blackhole_force(params: ForceInput) -> str:
    """Set Black Hole gravitational force per layer (0.0-1.0).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/BHmacroforce",
        "meso": "/polynodes/BHmesoforce",
        "micro": "/polynodes/BHmicroforce",
    }
    return _send_osc(addr_map[params.level], params.value)


@mcp.tool(
    name="polynodes_whitehole_switch",
    annotations={
        "title": "White Hole On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_whitehole_switch(params: SwitchInput) -> str:
    """Turn the White Hole DSP interactable on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/WHsw", params.state)


@mcp.tool(
    name="polynodes_whitehole_force",
    annotations={
        "title": "Set White Hole Force",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_whitehole_force(params: ForceInput) -> str:
    """Set White Hole reflection force per layer (0.0-1.0).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/WHmacroforce",
        "meso": "/polynodes/WHmesoforce",
        "micro": "/polynodes/WHmicroforce",
    }
    return _send_osc(addr_map[params.level], params.value)


@mcp.tool(
    name="polynodes_ringmod_switch",
    annotations={
        "title": "Ring Modulator On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_ringmod_switch(params: SwitchInput) -> str:
    """Turn Ring Modulator on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/RMsw", params.state)


@mcp.tool(
    name="polynodes_ringmod_freq",
    annotations={
        "title": "Set Ring Mod Frequency",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_ringmod_freq(params: RingModInput) -> str:
    """Set ring modulator center frequency per layer (1.0-3.0).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/RMmacro",
        "meso": "/polynodes/RMmeso",
        "micro": "/polynodes/RMmicro",
    }
    return _send_osc(addr_map[params.level], params.value)


@mcp.tool(
    name="polynodes_crush_switch",
    annotations={
        "title": "Bitcrusher On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_crush_switch(params: SwitchInput) -> str:
    """Turn Bitcrusher/Decimater on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/CRSsw", params.state)


@mcp.tool(
    name="polynodes_crush_bit_level",
    annotations={
        "title": "Set Crush Bit Level",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_crush_bit_level(params: CrushBitInput) -> str:
    """Set bitcrusher bit depth level (0.0-1.0).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/CRSbitLvl", params.value)


@mcp.tool(
    name="polynodes_crush_range",
    annotations={
        "title": "Set Crush Range",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_crush_range(params: CrushRangeInput) -> str:
    """Set bitcrusher sampling frequency range (0.0-5.0).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/CRSrange", params.value)


@mcp.tool(
    name="polynodes_resonator_switch",
    annotations={
        "title": "Resonator On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_resonator_switch(params: SwitchInput) -> str:
    """Turn Resonator on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/ResoSw", params.state)


@mcp.tool(
    name="polynodes_resonator_freq_dist",
    annotations={
        "title": "Set Resonator Freq Distribution",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_resonator_freq_dist(params: ResonatorFreqDistInput) -> str:
    """Set resonator frequency distribution (1.0-3.0).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/ResoFreqdist", params.value)


@mcp.tool(
    name="polynodes_resonator_balance",
    annotations={
        "title": "Set Resonator Balance",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_resonator_balance(params: ResonatorBalanceInput) -> str:
    """Set resonator wet/dry balance (0.0-0.5).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/ResoBalance", params.value)


# ---------------------------------------------------------------------------
# Tools - Cuboid FX
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_cuboid_switch",
    annotations={
        "title": "Cuboid Switch",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_cuboid_switch(cube: int = Field(..., description="Cuboid number: 1, 2, or 3", ge=1, le=3), state: float = Field(..., description="0.0=off, 1.0=on", ge=0.0, le=1.0)) -> str:
    """Turn a cuboid (C1/C2/C3) on or off.

    Args:
        cube: 1, 2, or 3.
        state: 0.0=off, 1.0=on.

    Returns:
        JSON confirmation.
    """
    return _send_osc(f"/polynodes/C{cube}sw", state)


@mcp.tool(
    name="polynodes_cuboid_return_level",
    annotations={
        "title": "Set Cuboid Return Level",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_cuboid_return_level(params: CubeReturnInput) -> str:
    """Set cuboid FX return level per layer (1.0-80.0).

    Args:
        params: level and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "macro": "/polynodes/MacroreturnLvl",
        "meso": "/polynodes/MesoreturnLvl",
        "micro": "/polynodes/MicroreturnLvl",
    }
    return _send_osc(addr_map[params.level], params.value)


# ---------------------------------------------------------------------------
# Tools - Isomorphic Modulation
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_isomorph_switch",
    annotations={
        "title": "IsoMorph On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_isomorph_switch(params: SwitchInput) -> str:
    """Turn IsoMorph modulation on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/isomorphsw", params.state)


@mcp.tool(
    name="polynodes_isomorph_mod_switch",
    annotations={
        "title": "IsoMorph Modulation Target Switch",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_isomorph_mod_switch(param: str = Field(..., description="'freq', 'amp', or 'res'"), state: float = Field(..., description="0.0=off, 1.0=on", ge=0.0, le=1.0)) -> str:
    """Turn on/off a specific isomorphic modulation target (freq/amp/res).

    Args:
        param: 'freq', 'amp', or 'res'.
        state: 0.0 or 1.0.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "freq": "/polynodes/isomfreqsw",
        "amp": "/polynodes/isomampsw",
        "res": "/polynodes/isomressw",
    }
    param = param.lower().strip()
    if param not in addr_map:
        return json.dumps({"error": "param must be 'freq', 'amp', or 'res'"})
    return _send_osc(addr_map[param], state)


@mcp.tool(
    name="polynodes_isomorph_mod_depth",
    annotations={
        "title": "Set IsoMorph Mod Depth",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_isomorph_mod_depth(params: IsomorphModInput) -> str:
    """Set isomorphic modulation depth for freq/amp/res (0.0-2.0).

    Args:
        params: param and value.

    Returns:
        JSON confirmation.
    """
    addr_map = {
        "freq": "/polynodes/isomfreqmodr",
        "amp": "/polynodes/isomampmodr",
        "res": "/polynodes/isomresmodr",
    }
    return _send_osc(addr_map[params.param], params.value)


@mcp.tool(
    name="polynodes_isomorph_bp_center",
    annotations={
        "title": "Set IsoMorph BP Center",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_isomorph_bp_center(params: IsomorphBPCenterInput) -> str:
    """Set isomorphic bandpass center frequency (0-5000).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/isombpcent", params.value)


# ---------------------------------------------------------------------------
# Tools - Navigation & Misc
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_navigation_random_trigger",
    annotations={
        "title": "Navigation Random Trigger",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_navigation_random_trigger(params: SwitchInput) -> str:
    """Trigger random navigation mode changes.

    Args:
        params: state 1.0=on.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/navigrndtrig", params.state)


@mcp.tool(
    name="polynodes_rearrange_trigger",
    annotations={
        "title": "Rearrange Trigger",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_rearrange_trigger(params: SwitchInput) -> str:
    """Trigger Re-Arr mode (rearranges input sample chunks).

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/rearrtrig", params.state)


@mcp.tool(
    name="polynodes_poly_gates_switch",
    annotations={
        "title": "Poly Gates On/Off",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_poly_gates_switch(params: SwitchInput) -> str:
    """Turn Poly Gates on or off (BPM-synced layer gating).

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/polygatessw", params.state)


@mcp.tool(
    name="polynodes_tuning_pb_switch",
    annotations={
        "title": "Tuning PB Switch",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_tuning_pb_switch(params: SwitchInput) -> str:
    """Turn tuning scale application on PB rate on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/tuningpbsw", params.state)


@mcp.tool(
    name="polynodes_tuning_res_switch",
    annotations={
        "title": "Tuning Res Switch",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_tuning_res_switch(params: SwitchInput) -> str:
    """Turn tuning scale application on resonator filter on or off.

    Args:
        params: state.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/tuningressw", params.state)


# ---------------------------------------------------------------------------
# Tools - Camera
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_camera_zoom",
    annotations={
        "title": "Camera Zoom",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_camera_zoom(params: CameraZoomInput) -> str:
    """Zoom the 3D camera (positive=in, negative=out).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/camzoom", params.value)


@mcp.tool(
    name="polynodes_camera_rotate",
    annotations={
        "title": "Camera Rotate",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_camera_rotate(params: CameraRotateInput) -> str:
    """Rotate the 3D camera (value in radians).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/camrotate", params.value)


# ---------------------------------------------------------------------------
# Tools - BPM
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_set_bpm",
    annotations={
        "title": "Set BPM",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_set_bpm(params: BPMInput) -> str:
    """Set the sequencer BPM (10-300).

    Args:
        params: value.

    Returns:
        JSON confirmation.
    """
    return _send_osc("/polynodes/seqbpm", params.value)


# ---------------------------------------------------------------------------
# Tools - Convenience / Composite
# ---------------------------------------------------------------------------

@mcp.tool(
    name="polynodes_list_osc_addresses",
    annotations={
        "title": "List All OSC Addresses",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def polynodes_list_osc_addresses() -> str:
    """List all available PolyNodes OSC addresses and their parameter ranges.

    Returns:
        JSON with all OSC addresses grouped by category.
    """
    addresses = {
        "transport": {
            "/polynodes/playstartstop": "Play/Stop (0.0 or 1.0)",
            "/polynodes/presetslot": "Preset Slot (1-10)",
            "/polynodes/seqbpm": "BPM (10-300)",
        },
        "gain": {
            "/polynodes/MacroGain": "Macro Gain dB (-80 to 20)",
            "/polynodes/MesoGain": "Meso Gain dB (-80 to 20)",
            "/polynodes/MicroGain": "Micro Gain dB (-80 to 20)",
            "/polynodes/DryWet": "Dry/Wet (0.0-1.0)",
            "/polynodes/MacroGainsolo": "Macro Solo (0/1)",
            "/polynodes/MesoGainsolo": "Meso Solo (0/1)",
            "/polynodes/MicroGainsolo": "Micro Solo (0/1)",
        },
        "envelope": {
            "/polynodes/MacroEnvtime": "Macro Env Time (0.01-0.5)",
            "/polynodes/MesoEnvtime": "Meso Env Time (0.01-0.5)",
            "/polynodes/MicroEnvtime": "Micro Env Time (0.01-0.5)",
        },
        "playback_rate": {
            "/polynodes/pbrmacro": "Macro PBR (0.3-10)",
            "/polynodes/pbrmeso": "Meso PBR (0.3-20)",
            "/polynodes/pbrmicro": "Micro PBR (0.3-30)",
            "/polynodes/pbrmacroMR": "Macro PBR ModRange (0-0.75)",
            "/polynodes/pbrmesoMR": "Meso PBR ModRange (0-0.75)",
            "/polynodes/pbrmicroMR": "Micro PBR ModRange (0-0.75)",
        },
        "granulator": {
            "/polynodes/granusw": "Granulator Switch (0/1)",
            "/polynodes/granuDur": "Duration (10-1000)",
            "/polynodes/granuDurMR": "Duration ModRange (0-0.75)",
        },
        "bandpass_filter": {
            "/polynodes/filtmacrosw": "Macro Filter Switch (0/1)",
            "/polynodes/filtmesosw": "Meso Filter Switch (0/1)",
            "/polynodes/filtmicrosw": "Micro Filter Switch (0/1)",
            "/polynodes/filtmacro": "Macro Freq (80-8000)",
            "/polynodes/filtmeso": "Meso Freq (80-8000)",
            "/polynodes/filtmicro": "Micro Freq (80-8000)",
            "/polynodes/filtmacroMR": "Macro Filter ModRange (0-0.75)",
            "/polynodes/filtmesoMR": "Meso Filter ModRange (0-0.75)",
            "/polynodes/filtmicroMR": "Micro Filter ModRange (0-0.75)",
        },
        "comb_filter": {
            "/polynodes/combmacrosw": "Macro Comb Switch (0/1)",
            "/polynodes/combmesosw": "Meso Comb Switch (0/1)",
            "/polynodes/combmicrosw": "Micro Comb Switch (0/1)",
            "/polynodes/combmacro": "Macro Comb (10-3000)",
            "/polynodes/combmeso": "Meso Comb (10-1000)",
            "/polynodes/combmicro": "Micro Comb (10-300)",
            "/polynodes/combmacroMR": "Macro Comb ModRange (0-0.75)",
            "/polynodes/combmesoMR": "Meso Comb ModRange (0-0.75)",
            "/polynodes/combmicroMR": "Micro Comb ModRange (0-0.75)",
        },
        "blackhole": {
            "/polynodes/BHsw": "BH Switch (0/1)",
            "/polynodes/BHmacroforce": "BH Macro Force (0-1)",
            "/polynodes/BHmesoforce": "BH Meso Force (0-1)",
            "/polynodes/BHmicroforce": "BH Micro Force (0-1)",
        },
        "whitehole": {
            "/polynodes/WHsw": "WH Switch (0/1)",
            "/polynodes/WHmacroforce": "WH Macro Force (0-1)",
            "/polynodes/WHmesoforce": "WH Meso Force (0-1)",
            "/polynodes/WHmicroforce": "WH Micro Force (0-1)",
        },
        "ring_modulator": {
            "/polynodes/RMsw": "RM Switch (0/1)",
            "/polynodes/RMmacro": "RM Macro (1-3)",
            "/polynodes/RMmeso": "RM Meso (1-3)",
            "/polynodes/RMmicro": "RM Micro (1-3)",
        },
        "bitcrusher": {
            "/polynodes/CRSsw": "Crush Switch (0/1)",
            "/polynodes/CRSbitLvl": "Bit Level (0-1)",
            "/polynodes/CRSrange": "Range (0-5)",
        },
        "resonator": {
            "/polynodes/ResoSw": "Resonator Switch (0/1)",
            "/polynodes/ResoFreqdist": "Freq Distribution (1-3)",
            "/polynodes/ResoBalance": "Balance (0-0.5)",
        },
        "cuboid_fx": {
            "/polynodes/C1sw": "Cuboid 1 Switch (0/1)",
            "/polynodes/C2sw": "Cuboid 2 Switch (0/1)",
            "/polynodes/C3sw": "Cuboid 3 Switch (0/1)",
            "/polynodes/MacroreturnLvl": "Macro Return (1-80)",
            "/polynodes/MesoreturnLvl": "Meso Return (1-80)",
            "/polynodes/MicroreturnLvl": "Micro Return (1-80)",
        },
        "isomorph": {
            "/polynodes/isomorphsw": "IsoMorph Switch (0/1)",
            "/polynodes/isomfreqsw": "Freq Mod Switch (0/1)",
            "/polynodes/isomfreqmodr": "Freq Mod Depth (0-2)",
            "/polynodes/isomampsw": "Amp Mod Switch (0/1)",
            "/polynodes/isomampmodr": "Amp Mod Depth (0-2)",
            "/polynodes/isomressw": "Res Mod Switch (0/1)",
            "/polynodes/isomresmodr": "Res Mod Depth (0-2)",
            "/polynodes/isombpcent": "BP Center (0-5000)",
        },
        "navigation": {
            "/polynodes/navigrndtrig": "Nav Random Trigger (0/1)",
            "/polynodes/rearrtrig": "Rearrange Trigger (0/1)",
            "/polynodes/polygatessw": "Poly Gates Switch (0/1)",
        },
        "tuning": {
            "/polynodes/tuningpbsw": "Tuning PB Switch (0/1)",
            "/polynodes/tuningressw": "Tuning Res Switch (0/1)",
        },
        "camera": {
            "/polynodes/camzoom": "Camera Zoom (+/- float)",
            "/polynodes/camrotate": "Camera Rotate (radians)",
        },
    }
    return json.dumps(addresses, indent=2)


@mcp.tool(
    name="polynodes_send_raw_osc",
    annotations={
        "title": "Send Raw OSC Message",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def polynodes_send_raw_osc(address: str = Field(..., description="OSC address (e.g. '/polynodes/DryWet')"), value: float = Field(..., description="Float value to send")) -> str:
    """Send a raw OSC message to PolyNodes. Use this for any OSC address.

    Args:
        address: Full OSC address path.
        value: Float value.

    Returns:
        JSON confirmation.
    """
    return _send_osc(address, value)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
