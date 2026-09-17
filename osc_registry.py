"""OSC parameter registry for PolyNodes — single source of truth."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Literal, Mapping, TypedDict

from pydantic import BaseModel, ConfigDict

Level = Literal["macro", "meso", "micro"]
LEVELS: tuple[Level, ...] = ("macro", "meso", "micro")

ParamName = Literal[
    "play",
    "preset",
    "bpm",
    "gain",
    "dry_wet",
    "solo",
    "envelope_time",
    "playback_rate",
    "playback_rate_mod",
    "granulator",
    "granular_duration",
    "granular_duration_mod",
    "filter",
    "filter_freq",
    "filter_mod",
    "comb",
    "comb_delay",
    "comb_mod",
    "blackhole",
    "blackhole_force",
    "whitehole",
    "whitehole_force",
    "ringmod",
    "ringmod_freq",
    "crush",
    "crush_bit",
    "crush_range",
    "resonator",
    "resonator_freq_dist",
    "resonator_balance",
    "cuboid_1",
    "cuboid_2",
    "cuboid_3",
    "cuboid_return",
    "isomorph",
    "isomorph_freq",
    "isomorph_amp",
    "isomorph_res",
    "isomorph_freq_depth",
    "isomorph_amp_depth",
    "isomorph_res_depth",
    "isomorph_bp_center",
    "nav_random",
    "rearrange",
    "poly_gates",
    "tuning_pb",
    "tuning_res",
    "camera_zoom",
    "camera_rotate",
]

PARAM_NAMES: tuple[ParamName, ...] = (
    "play",
    "preset",
    "bpm",
    "gain",
    "dry_wet",
    "solo",
    "envelope_time",
    "playback_rate",
    "playback_rate_mod",
    "granulator",
    "granular_duration",
    "granular_duration_mod",
    "filter",
    "filter_freq",
    "filter_mod",
    "comb",
    "comb_delay",
    "comb_mod",
    "blackhole",
    "blackhole_force",
    "whitehole",
    "whitehole_force",
    "ringmod",
    "ringmod_freq",
    "crush",
    "crush_bit",
    "crush_range",
    "resonator",
    "resonator_freq_dist",
    "resonator_balance",
    "cuboid_1",
    "cuboid_2",
    "cuboid_3",
    "cuboid_return",
    "isomorph",
    "isomorph_freq",
    "isomorph_amp",
    "isomorph_res",
    "isomorph_freq_depth",
    "isomorph_amp_depth",
    "isomorph_res_depth",
    "isomorph_bp_center",
    "nav_random",
    "rearrange",
    "poly_gates",
    "tuning_pb",
    "tuning_res",
    "camera_zoom",
    "camera_rotate",
)


@dataclass(frozen=True)
class RangeSpec:
    min: float | None = None
    max: float | None = None

    def check(self, value: float, label: str) -> None:
        _ensure_finite(value, label)
        if self.min is not None and value < self.min:
            raise ValueError(f"{label}: value {value} below minimum {self.min}")
        if self.max is not None and value > self.max:
            raise ValueError(f"{label}: value {value} above maximum {self.max}")


@dataclass(frozen=True)
class ParamSpec:
    name: str
    category: str
    description: str
    per_layer: bool = False
    switch: bool = False
    address: str | None = None
    addresses: dict[str, str] | None = None
    range: RangeSpec | None = None
    level_ranges: dict[str, RangeSpec] | None = None

    def all_addresses(self) -> list[str]:
        if self.address:
            return [self.address]
        if self.addresses:
            return list(self.addresses.values())
        return []

    def resolve_address(self, level: str | None) -> str:
        if self.per_layer:
            if level is None:
                raise ValueError(f"{self.name}: level required (macro|meso|micro)")
            lvl = _normalize_level(level)
            if self.addresses is None or lvl not in self.addresses:
                raise ValueError(f"{self.name}: invalid level '{level}'")
            return self.addresses[lvl]
        if level is not None:
            raise ValueError(f"{self.name}: level not allowed")
        if self.address is None:
            raise ValueError(f"{self.name}: no address configured")
        return self.address

    def range_for(self, level: str | None) -> RangeSpec | None:
        if self.level_ranges and level is not None:
            lvl = _normalize_level(level)
            if lvl in self.level_ranges:
                return self.level_ranges[lvl]
        return self.range


def _normalize_level(level: str) -> Level:
    lvl = level.lower().strip()
    if lvl not in LEVELS:
        raise ValueError(f"level must be 'macro', 'meso', or 'micro', got '{level}'")
    return lvl  # type: ignore[return-value]


def _ensure_finite(value: float, label: str) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{label}: value must be finite, got {value}")


def _coerce_value(value: Any, switch: bool, label: str = "value") -> float:
    if value is None:
        raise ValueError("missing value")
    if isinstance(value, bool):
        if not switch:
            raise ValueError("bool value only allowed for switch params")
        return 1.0 if value else 0.0
    try:
        fval = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label}: invalid numeric value {value!r}") from exc
    _ensure_finite(fval, label)
    if switch and fval not in (0.0, 1.0):
        raise ValueError(f"switch value must be 0, 1, or bool, got {value}")
    return fval


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_LAYER_GAIN = {
    "macro": "/polynodes/MacroGain",
    "meso": "/polynodes/MesoGain",
    "micro": "/polynodes/MicroGain",
}
_LAYER_SOLO = {
    "macro": "/polynodes/MacroGainsolo",
    "meso": "/polynodes/MesoGainsolo",
    "micro": "/polynodes/MicroGainsolo",
}
_LAYER_ENV = {
    "macro": "/polynodes/MacroEnvtime",
    "meso": "/polynodes/MesoEnvtime",
    "micro": "/polynodes/MicroEnvtime",
}
_LAYER_PBR = {
    "macro": "/polynodes/pbrmacro",
    "meso": "/polynodes/pbrmeso",
    "micro": "/polynodes/pbrmicro",
}
_LAYER_PBR_MR = {
    "macro": "/polynodes/pbrmacroMR",
    "meso": "/polynodes/pbrmesoMR",
    "micro": "/polynodes/pbrmicroMR",
}
_LAYER_FILT_SW = {
    "macro": "/polynodes/filtmacrosw",
    "meso": "/polynodes/filtmesosw",
    "micro": "/polynodes/filtmicrosw",
}
_LAYER_FILT = {
    "macro": "/polynodes/filtmacro",
    "meso": "/polynodes/filtmeso",
    "micro": "/polynodes/filtmicro",
}
_LAYER_FILT_MR = {
    "macro": "/polynodes/filtmacroMR",
    "meso": "/polynodes/filtmesoMR",
    "micro": "/polynodes/filtmicroMR",
}
_LAYER_COMB_SW = {
    "macro": "/polynodes/combmacrosw",
    "meso": "/polynodes/combmesosw",
    "micro": "/polynodes/combmicrosw",
}
_LAYER_COMB = {
    "macro": "/polynodes/combmacro",
    "meso": "/polynodes/combmeso",
    "micro": "/polynodes/combmicro",
}
_LAYER_COMB_MR = {
    "macro": "/polynodes/combmacroMR",
    "meso": "/polynodes/combmesoMR",
    "micro": "/polynodes/combmicroMR",
}
_LAYER_BH_FORCE = {
    "macro": "/polynodes/BHmacroforce",
    "meso": "/polynodes/BHmesoforce",
    "micro": "/polynodes/BHmicroforce",
}
_LAYER_WH_FORCE = {
    "macro": "/polynodes/WHmacroforce",
    "meso": "/polynodes/WHmesoforce",
    "micro": "/polynodes/WHmicroforce",
}
_LAYER_RM = {
    "macro": "/polynodes/RMmacro",
    "meso": "/polynodes/RMmeso",
    "micro": "/polynodes/RMmicro",
}
_LAYER_RETURN = {
    "macro": "/polynodes/MacroreturnLvl",
    "meso": "/polynodes/MesoreturnLvl",
    "micro": "/polynodes/MicroreturnLvl",
}

_MR_RANGE = RangeSpec(0.0, 0.75)

PARAMS: dict[str, ParamSpec] = {
    "play": ParamSpec("play", "transport", "Play/Stop", switch=True, address="/polynodes/playstartstop", range=RangeSpec(0.0, 1.0)),
    "preset": ParamSpec("preset", "transport", "Preset slot", address="/polynodes/presetslot", range=RangeSpec(1.0, 10.0)),
    "bpm": ParamSpec("bpm", "transport", "Sequencer BPM", address="/polynodes/seqbpm", range=RangeSpec(10.0, 300.0)),
    "gain": ParamSpec("gain", "gain", "Layer gain dB", per_layer=True, addresses=_LAYER_GAIN, range=RangeSpec(-80.0, 20.0)),
    "dry_wet": ParamSpec("dry_wet", "gain", "Dry/Wet balance", address="/polynodes/DryWet", range=RangeSpec(0.0, 1.0)),
    "solo": ParamSpec("solo", "gain", "Layer solo", per_layer=True, switch=True, addresses=_LAYER_SOLO, range=RangeSpec(0.0, 1.0)),
    "envelope_time": ParamSpec("envelope_time", "envelope", "Envelope time", per_layer=True, addresses=_LAYER_ENV, range=RangeSpec(0.01, 0.5)),
    "playback_rate": ParamSpec(
        "playback_rate",
        "playback_rate",
        "Playback rate",
        per_layer=True,
        addresses=_LAYER_PBR,
        level_ranges={
            "macro": RangeSpec(0.3, 10.0),
            "meso": RangeSpec(0.3, 20.0),
            "micro": RangeSpec(0.3, 30.0),
        },
    ),
    "playback_rate_mod": ParamSpec("playback_rate_mod", "playback_rate", "PB rate mod range", per_layer=True, addresses=_LAYER_PBR_MR, range=_MR_RANGE),
    "granulator": ParamSpec("granulator", "granulator", "Granulator switch", switch=True, address="/polynodes/granusw", range=RangeSpec(0.0, 1.0)),
    "granular_duration": ParamSpec("granular_duration", "granulator", "Chunk duration", address="/polynodes/granuDur", range=RangeSpec(10.0, 1000.0)),
    "granular_duration_mod": ParamSpec("granular_duration_mod", "granulator", "Duration mod range", address="/polynodes/granuDurMR", range=_MR_RANGE),
    "filter": ParamSpec("filter", "bandpass_filter", "Bandpass filter switch", per_layer=True, switch=True, addresses=_LAYER_FILT_SW, range=RangeSpec(0.0, 1.0)),
    "filter_freq": ParamSpec("filter_freq", "bandpass_filter", "Center frequency Hz", per_layer=True, addresses=_LAYER_FILT, range=RangeSpec(80.0, 8000.0)),
    "filter_mod": ParamSpec("filter_mod", "bandpass_filter", "Filter mod range", per_layer=True, addresses=_LAYER_FILT_MR, range=_MR_RANGE),
    "comb": ParamSpec("comb", "comb_filter", "Comb filter switch", per_layer=True, switch=True, addresses=_LAYER_COMB_SW, range=RangeSpec(0.0, 1.0)),
    "comb_delay": ParamSpec(
        "comb_delay",
        "comb_filter",
        "Comb delay",
        per_layer=True,
        addresses=_LAYER_COMB,
        level_ranges={
            "macro": RangeSpec(10.0, 3000.0),
            "meso": RangeSpec(10.0, 1000.0),
            "micro": RangeSpec(10.0, 300.0),
        },
    ),
    "comb_mod": ParamSpec("comb_mod", "comb_filter", "Comb mod range", per_layer=True, addresses=_LAYER_COMB_MR, range=_MR_RANGE),
    "blackhole": ParamSpec("blackhole", "blackhole", "Black Hole switch", switch=True, address="/polynodes/BHsw", range=RangeSpec(0.0, 1.0)),
    "blackhole_force": ParamSpec("blackhole_force", "blackhole", "BH force", per_layer=True, addresses=_LAYER_BH_FORCE, range=RangeSpec(0.0, 1.0)),
    "whitehole": ParamSpec("whitehole", "whitehole", "White Hole switch", switch=True, address="/polynodes/WHsw", range=RangeSpec(0.0, 1.0)),
    "whitehole_force": ParamSpec("whitehole_force", "whitehole", "WH force", per_layer=True, addresses=_LAYER_WH_FORCE, range=RangeSpec(0.0, 1.0)),
    "ringmod": ParamSpec("ringmod", "ring_modulator", "Ring Mod switch", switch=True, address="/polynodes/RMsw", range=RangeSpec(0.0, 1.0)),
    "ringmod_freq": ParamSpec("ringmod_freq", "ring_modulator", "Ring mod frequency", per_layer=True, addresses=_LAYER_RM, range=RangeSpec(1.0, 3.0)),
    "crush": ParamSpec("crush", "bitcrusher", "Crusher switch", switch=True, address="/polynodes/CRSsw", range=RangeSpec(0.0, 1.0)),
    "crush_bit": ParamSpec("crush_bit", "bitcrusher", "Bit depth level", address="/polynodes/CRSbitLvl", range=RangeSpec(0.0, 1.0)),
    "crush_range": ParamSpec("crush_range", "bitcrusher", "Sampling freq range", address="/polynodes/CRSrange", range=RangeSpec(0.0, 5.0)),
    "resonator": ParamSpec("resonator", "resonator", "Resonator switch", switch=True, address="/polynodes/ResoSw", range=RangeSpec(0.0, 1.0)),
    "resonator_freq_dist": ParamSpec("resonator_freq_dist", "resonator", "Freq distribution", address="/polynodes/ResoFreqdist", range=RangeSpec(1.0, 3.0)),
    "resonator_balance": ParamSpec("resonator_balance", "resonator", "Wet/dry balance", address="/polynodes/ResoBalance", range=RangeSpec(0.0, 0.5)),
    "cuboid_1": ParamSpec("cuboid_1", "cuboid_fx", "Cuboid 1 switch", switch=True, address="/polynodes/C1sw", range=RangeSpec(0.0, 1.0)),
    "cuboid_2": ParamSpec("cuboid_2", "cuboid_fx", "Cuboid 2 switch", switch=True, address="/polynodes/C2sw", range=RangeSpec(0.0, 1.0)),
    "cuboid_3": ParamSpec("cuboid_3", "cuboid_fx", "Cuboid 3 switch", switch=True, address="/polynodes/C3sw", range=RangeSpec(0.0, 1.0)),
    "cuboid_return": ParamSpec("cuboid_return", "cuboid_fx", "Cuboid return level", per_layer=True, addresses=_LAYER_RETURN, range=RangeSpec(1.0, 80.0)),
    "isomorph": ParamSpec("isomorph", "isomorph", "IsoMorph switch", switch=True, address="/polynodes/isomorphsw", range=RangeSpec(0.0, 1.0)),
    "isomorph_freq": ParamSpec("isomorph_freq", "isomorph", "Freq mod switch", switch=True, address="/polynodes/isomfreqsw", range=RangeSpec(0.0, 1.0)),
    "isomorph_amp": ParamSpec("isomorph_amp", "isomorph", "Amp mod switch", switch=True, address="/polynodes/isomampsw", range=RangeSpec(0.0, 1.0)),
    "isomorph_res": ParamSpec("isomorph_res", "isomorph", "Res mod switch", switch=True, address="/polynodes/isomressw", range=RangeSpec(0.0, 1.0)),
    "isomorph_freq_depth": ParamSpec("isomorph_freq_depth", "isomorph", "Freq mod depth", address="/polynodes/isomfreqmodr", range=RangeSpec(0.0, 2.0)),
    "isomorph_amp_depth": ParamSpec("isomorph_amp_depth", "isomorph", "Amp mod depth", address="/polynodes/isomampmodr", range=RangeSpec(0.0, 2.0)),
    "isomorph_res_depth": ParamSpec("isomorph_res_depth", "isomorph", "Res mod depth", address="/polynodes/isomresmodr", range=RangeSpec(0.0, 2.0)),
    "isomorph_bp_center": ParamSpec("isomorph_bp_center", "isomorph", "Bandpass center", address="/polynodes/isombpcent", range=RangeSpec(0.0, 5000.0)),
    "nav_random": ParamSpec("nav_random", "navigation", "Random nav trigger", switch=True, address="/polynodes/navigrndtrig", range=RangeSpec(0.0, 1.0)),
    "rearrange": ParamSpec("rearrange", "navigation", "Rearrange trigger", switch=True, address="/polynodes/rearrtrig", range=RangeSpec(0.0, 1.0)),
    "poly_gates": ParamSpec("poly_gates", "navigation", "Poly Gates switch", switch=True, address="/polynodes/polygatessw", range=RangeSpec(0.0, 1.0)),
    "tuning_pb": ParamSpec("tuning_pb", "tuning", "Tuning PB switch", switch=True, address="/polynodes/tuningpbsw", range=RangeSpec(0.0, 1.0)),
    "tuning_res": ParamSpec("tuning_res", "tuning", "Tuning Res switch", switch=True, address="/polynodes/tuningressw", range=RangeSpec(0.0, 1.0)),
    "camera_zoom": ParamSpec("camera_zoom", "camera", "Camera zoom", address="/polynodes/camzoom"),
    "camera_rotate": ParamSpec("camera_rotate", "camera", "Camera rotate radians", address="/polynodes/camrotate"),
}


class Change(BaseModel):
    model_config = ConfigDict(extra="forbid")

    param: ParamName
    value: float | bool | int
    level: Level | None = None


class ResolvedMessage(TypedDict):
    address: str
    value: float


def _range_label(rng: RangeSpec | None) -> str:
    if rng is None:
        return "unbounded"
    if rng.min is not None and rng.max is not None:
        return f"{rng.min}-{rng.max}"
    if rng.min is not None:
        return f">={rng.min}"
    if rng.max is not None:
        return f"<={rng.max}"
    return "unbounded"


def _as_change(change: Change | Mapping[str, Any]) -> Change:
    if isinstance(change, Change):
        return change
    if change.get("value") is None:
        raise ValueError("missing value")
    try:
        return Change.model_validate(change)
    except Exception as exc:
        raise ValueError(str(exc)) from exc


def validate_change(change: Change | Mapping[str, Any]) -> ResolvedMessage:
    """Validate one change; raise ValueError on failure."""
    item = _as_change(change)
    name = item.param
    if name not in PARAMS:
        raise ValueError(f"unknown param '{name}'")

    spec = PARAMS[name]
    level: str | None = None
    if item.level is not None:
        level = _normalize_level(item.level)

    fval = _coerce_value(item.value, spec.switch, name)
    address = spec.resolve_address(level)

    rng = spec.range_for(level)
    if rng is not None:
        rng.check(fval, name)

    return {"address": address, "value": fval}


def apply_changes(changes: list[Change | Mapping[str, Any]]) -> list[ResolvedMessage]:
    """Validate all changes first; send nothing if any fail."""
    resolved: list[ResolvedMessage] = []
    for change in changes:
        resolved.append(validate_change(change))
    return resolved


def all_osc_addresses() -> set[str]:
    addrs: set[str] = set()
    for spec in PARAMS.values():
        addrs.update(spec.all_addresses())
    return addrs


def _param_catalog_entry(spec: ParamSpec) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "name": spec.name,
        "category": spec.category,
        "description": spec.description,
        "per_layer": spec.per_layer,
        "switch": spec.switch,
    }
    if spec.per_layer:
        entry["addresses"] = dict(spec.addresses or {})
        if spec.level_ranges:
            entry["level_ranges"] = {k: _range_label(v) for k, v in spec.level_ranges.items()}
        elif spec.range:
            entry["range"] = _range_label(spec.range)
    else:
        entry["address"] = spec.address
        if spec.range:
            entry["range"] = _range_label(spec.range)
        else:
            entry["range"] = "unbounded"
    return entry


def catalog_dict() -> dict[str, Any]:
    by_category: dict[str, list[dict[str, Any]]] = {}
    for spec in PARAMS.values():
        by_category.setdefault(spec.category, []).append(_param_catalog_entry(spec))
    return {
        "params": [_param_catalog_entry(PARAMS[n]) for n in PARAM_NAMES],
        "by_category": by_category,
        "addresses": sorted(all_osc_addresses()),
    }


def catalog_json() -> str:
    return json.dumps(catalog_dict(), separators=(",", ":"))


def catalog_markdown() -> str:
    """Generate osc-addresses.md content from the registry."""
    lines = [
        "# PolyNodes OSC Address Reference",
        "",
        "Generated from `osc_registry.py`. All OSC messages default to `127.0.0.1:4799` "
        "(override with `POLYNODES_OSC_HOST` / `POLYNODES_OSC_PORT`).",
        "",
    ]

    category_titles = {
        "transport": "Transport",
        "gain": "Gain",
        "envelope": "Envelope",
        "playback_rate": "Playback Rate",
        "granulator": "Granulator",
        "bandpass_filter": "Bandpass Filter",
        "comb_filter": "Comb Filter",
        "blackhole": "Black Hole",
        "whitehole": "White Hole",
        "ring_modulator": "Ring Modulator",
        "bitcrusher": "Bitcrusher",
        "resonator": "Resonator",
        "cuboid_fx": "Cuboid FX",
        "isomorph": "IsoMorph",
        "navigation": "Navigation & Misc",
        "tuning": "Tuning",
        "camera": "Camera",
    }

    seen_categories: list[str] = []
    for name in PARAM_NAMES:
        spec = PARAMS[name]
        if spec.category not in seen_categories:
            seen_categories.append(spec.category)
            title = category_titles.get(spec.category, spec.category)
            lines.extend(["", f"## {title}", "", "| Param | Address | Description | Range |", "|-------|---------|-------------|-------|"])

        if spec.per_layer and spec.addresses:
            for lvl in LEVELS:
                addr = spec.addresses[lvl]
                rng = spec.range_for(lvl)
                range_str = _range_label(rng)
                lines.append(f"| `{spec.name}` ({lvl}) | `{addr}` | {spec.description} | {range_str} |")
        else:
            rng = spec.range_for(None)
            range_str = _range_label(rng)
            lines.append(f"| `{spec.name}` | `{spec.address}` | {spec.description} | {range_str} |")

    lines.append("")
    return "\n".join(lines)
