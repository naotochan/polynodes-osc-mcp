"""Tests for osc_registry validation and batch atomicity."""

from pathlib import Path

import pytest

from osc_registry import (
    LEVELS,
    PARAM_NAMES,
    PARAMS,
    all_osc_addresses,
    apply_changes,
    catalog_dict,
    catalog_markdown,
    validate_change,
)

OSC_ADDRESSES_MD = Path(__file__).resolve().parents[1] / "skills/polynodes-guide/reference/osc-addresses.md"


# All addresses from the legacy osc-addresses.md reference
LEGACY_ADDRESSES = {
    "/polynodes/playstartstop",
    "/polynodes/presetslot",
    "/polynodes/seqbpm",
    "/polynodes/MacroGain",
    "/polynodes/MesoGain",
    "/polynodes/MicroGain",
    "/polynodes/DryWet",
    "/polynodes/MacroGainsolo",
    "/polynodes/MesoGainsolo",
    "/polynodes/MicroGainsolo",
    "/polynodes/MacroEnvtime",
    "/polynodes/MesoEnvtime",
    "/polynodes/MicroEnvtime",
    "/polynodes/pbrmacro",
    "/polynodes/pbrmeso",
    "/polynodes/pbrmicro",
    "/polynodes/pbrmacroMR",
    "/polynodes/pbrmesoMR",
    "/polynodes/pbrmicroMR",
    "/polynodes/granusw",
    "/polynodes/granuDur",
    "/polynodes/granuDurMR",
    "/polynodes/filtmacrosw",
    "/polynodes/filtmesosw",
    "/polynodes/filtmicrosw",
    "/polynodes/filtmacro",
    "/polynodes/filtmeso",
    "/polynodes/filtmicro",
    "/polynodes/filtmacroMR",
    "/polynodes/filtmesoMR",
    "/polynodes/filtmicroMR",
    "/polynodes/combmacrosw",
    "/polynodes/combmesosw",
    "/polynodes/combmicrosw",
    "/polynodes/combmacro",
    "/polynodes/combmeso",
    "/polynodes/combmicro",
    "/polynodes/combmacroMR",
    "/polynodes/combmesoMR",
    "/polynodes/combmicroMR",
    "/polynodes/BHsw",
    "/polynodes/BHmacroforce",
    "/polynodes/BHmesoforce",
    "/polynodes/BHmicroforce",
    "/polynodes/WHsw",
    "/polynodes/WHmacroforce",
    "/polynodes/WHmesoforce",
    "/polynodes/WHmicroforce",
    "/polynodes/RMsw",
    "/polynodes/RMmacro",
    "/polynodes/RMmeso",
    "/polynodes/RMmicro",
    "/polynodes/CRSsw",
    "/polynodes/CRSbitLvl",
    "/polynodes/CRSrange",
    "/polynodes/ResoSw",
    "/polynodes/ResoFreqdist",
    "/polynodes/ResoBalance",
    "/polynodes/C1sw",
    "/polynodes/C2sw",
    "/polynodes/C3sw",
    "/polynodes/MacroreturnLvl",
    "/polynodes/MesoreturnLvl",
    "/polynodes/MicroreturnLvl",
    "/polynodes/isomorphsw",
    "/polynodes/isomfreqsw",
    "/polynodes/isomfreqmodr",
    "/polynodes/isomampsw",
    "/polynodes/isomampmodr",
    "/polynodes/isomressw",
    "/polynodes/isomresmodr",
    "/polynodes/isombpcent",
    "/polynodes/navigrndtrig",
    "/polynodes/rearrtrig",
    "/polynodes/polygatessw",
    "/polynodes/tuningpbsw",
    "/polynodes/tuningressw",
    "/polynodes/camzoom",
    "/polynodes/camrotate",
}


def test_catalog_covers_all_legacy_addresses():
    registry_addrs = all_osc_addresses()
    assert LEGACY_ADDRESSES <= registry_addrs


def test_catalog_json_lists_every_address():
    catalog = catalog_dict()
    assert set(catalog["addresses"]) == all_osc_addresses()


def test_address_mapping_gain():
    msg = validate_change({"param": "gain", "level": "macro", "value": 0.0})
    assert msg == {"address": "/polynodes/MacroGain", "value": 0.0}


def test_address_mapping_global():
    msg = validate_change({"param": "dry_wet", "value": 0.5})
    assert msg == {"address": "/polynodes/DryWet", "value": 0.5}


def test_per_layer_range_playback_rate():
    validate_change({"param": "playback_rate", "level": "macro", "value": 10.0})
    validate_change({"param": "playback_rate", "level": "meso", "value": 20.0})
    validate_change({"param": "playback_rate", "level": "micro", "value": 30.0})
    with pytest.raises(ValueError, match="above maximum"):
        validate_change({"param": "playback_rate", "level": "macro", "value": 11.0})
    with pytest.raises(ValueError, match="above maximum"):
        validate_change({"param": "playback_rate", "level": "meso", "value": 21.0})
    with pytest.raises(ValueError, match="above maximum"):
        validate_change({"param": "playback_rate", "level": "micro", "value": 31.0})


def test_per_layer_range_comb_delay():
    validate_change({"param": "comb_delay", "level": "macro", "value": 3000.0})
    validate_change({"param": "comb_delay", "level": "meso", "value": 1000.0})
    validate_change({"param": "comb_delay", "level": "micro", "value": 300.0})
    with pytest.raises(ValueError, match="above maximum"):
        validate_change({"param": "comb_delay", "level": "macro", "value": 3001.0})
    with pytest.raises(ValueError, match="above maximum"):
        validate_change({"param": "comb_delay", "level": "meso", "value": 1001.0})
    with pytest.raises(ValueError, match="above maximum"):
        validate_change({"param": "comb_delay", "level": "micro", "value": 301.0})


def test_switch_accepts_bool():
    msg = validate_change({"param": "play", "value": True})
    assert msg["value"] == 1.0
    msg = validate_change({"param": "play", "value": False})
    assert msg["value"] == 0.0


def test_missing_level_rejected():
    with pytest.raises(ValueError, match="level required"):
        validate_change({"param": "gain", "value": 0.0})


def test_invalid_level_rejected():
    with pytest.raises(ValueError):
        validate_change({"param": "gain", "level": "mega", "value": 0.0})


def test_level_not_allowed_on_global():
    with pytest.raises(ValueError, match="level not allowed"):
        validate_change({"param": "bpm", "level": "macro", "value": 120.0})


def test_unknown_param_rejected():
    with pytest.raises(ValueError):
        validate_change({"param": "not_a_param", "value": 1.0})


def test_out_of_range_rejected():
    with pytest.raises(ValueError, match="above maximum"):
        validate_change({"param": "bpm", "value": 400.0})


def test_batch_validates_all_before_send():
    changes = [
        {"param": "play", "value": 1.0},
        {"param": "bpm", "value": 120.0},
        {"param": "gain", "level": "macro", "value": 0.0},
        {"param": "dry_wet", "value": 0.5},
        {"param": "granulator", "value": True},
    ]
    resolved = apply_changes(changes)
    assert len(resolved) == 5
    assert resolved[0]["address"] == "/polynodes/playstartstop"


def test_batch_first_error_raises():
    changes = [
        {"param": "play", "value": 1.0},
        {"param": "gain", "value": 0.0},  # missing level
    ]
    with pytest.raises(ValueError):
        apply_changes(changes)


def test_osc_addresses_md_matches_registry():
    assert OSC_ADDRESSES_MD.read_text() == catalog_markdown()


def test_every_param_has_spec():
    assert len(PARAMS) == 49
    assert set(PARAMS.keys()) == set(PARAM_NAMES)
    for level in LEVELS:
        validate_change({"param": "gain", "level": level, "value": 0.0})


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf"), "nan", "inf", "-inf"])
def test_non_finite_rejected_for_all_params(bad_value):
    for name in PARAM_NAMES:
        spec = PARAMS[name]
        change: dict[str, object] = {"param": name, "value": bad_value}
        if spec.per_layer:
            change["level"] = "macro"
        with pytest.raises(ValueError):
            validate_change(change)


def test_none_value_raises_value_error():
    with pytest.raises(ValueError, match="missing value"):
        validate_change({"param": "bpm", "value": None})


def test_bool_on_non_switch_raises_value_error():
    with pytest.raises(ValueError, match="bool value only allowed"):
        validate_change({"param": "bpm", "value": True})


def test_nan_string_coerced_and_rejected():
    with pytest.raises(ValueError, match="finite"):
        validate_change({"param": "bpm", "value": "nan"})
