"""Tests for MCP server tools, resource, and OSC client."""

import asyncio
import json
import os
from unittest.mock import MagicMock, patch

import pytest

import server
from osc_registry import catalog_json


@pytest.fixture(autouse=True)
def _reset_osc_client():
    server.reset_osc_client()
    yield
    server.reset_osc_client()


@pytest.fixture
def mock_send():
    with patch.object(server, "_send_osc") as send:
        yield send


async def _tool_names() -> set[str]:
    tools = await server.mcp.list_tools()
    return {t.name for t in tools}


async def _tools_list_compact_size() -> int:
    tools = await server.mcp.list_tools()
    payload = {"tools": [t.model_dump(by_alias=True, exclude_none=True) for t in tools]}
    return len(json.dumps(payload, separators=(",", ":")))


async def _polynodes_set_schema() -> dict:
    tools = await server.mcp.list_tools()
    for tool in tools:
        if tool.name == "polynodes_set":
            return tool.inputSchema
    raise AssertionError("polynodes_set not found")


def test_tool_count():
    names = asyncio.run(_tool_names())
    assert names == {"polynodes_set", "polynodes_raw"}


def test_tools_list_under_8000_chars():
    size = asyncio.run(_tools_list_compact_size())
    assert size < 8000, f"tools/list compact JSON is {size} chars"


def test_change_schema_requires_param_and_value():
    schema = asyncio.run(_polynodes_set_schema())
    required = schema["$defs"]["Change"]["required"]
    assert "param" in required
    assert "value" in required
    level_prop = schema["$defs"]["Change"]["properties"]["level"]
    assert level_prop["anyOf"][0]["enum"] == ["macro", "meso", "micro"]


def test_list_resources_includes_catalog():
    resources = asyncio.run(server.mcp.list_resources())
    uris = {str(r.uri) for r in resources}
    assert "polynodes://catalog" in uris
    catalog = next(r for r in resources if str(r.uri) == "polynodes://catalog")
    assert catalog.mimeType == "application/json"


def test_read_resource_returns_catalog_json():
    contents = asyncio.run(server.mcp.read_resource("polynodes://catalog"))
    assert len(contents) == 1
    assert contents[0].mime_type == "application/json"
    data = json.loads(contents[0].content)
    assert data == json.loads(catalog_json())
    assert "/polynodes/playstartstop" in data["addresses"]


def test_polynodes_set_batch(mock_send):
    changes = [
        {"param": "play", "value": 1.0},
        {"param": "bpm", "value": 120.0},
        {"param": "gain", "level": "macro", "value": -6.0},
        {"param": "dry_wet", "value": 0.7},
        {"param": "granulator", "value": True},
    ]
    result = json.loads(server.polynodes_set(changes))
    assert result["ok"] is True
    assert len(result["sent"]) == 5
    assert mock_send.call_count == 5


def test_polynodes_set_invalid_sends_nothing(mock_send):
    changes = [
        {"param": "play", "value": 1.0},
        {"param": "gain", "value": 0.0},
    ]
    with pytest.raises(ValueError):
        server.polynodes_set(changes)
    mock_send.assert_not_called()


@pytest.mark.parametrize("bad_value", ["nan", "inf", "-inf"])
def test_polynodes_set_mcp_path_rejects_non_finite(mock_send, bad_value):
    async def _call():
        with pytest.raises(Exception, match="finite"):
            await server.mcp.call_tool(
                "polynodes_set",
                {"changes": [{"param": "bpm", "value": bad_value}]},
            )

    asyncio.run(_call())
    mock_send.assert_not_called()


@pytest.mark.parametrize("bad_value", ["nan", "inf", "-inf"])
def test_polynodes_set_rejects_non_finite_camera(mock_send, bad_value):
    for name in ("camera_zoom", "camera_rotate"):
        with pytest.raises(ValueError, match="finite"):
            server.polynodes_set([{"param": name, "value": bad_value}])
    mock_send.assert_not_called()


def test_polynodes_set_bool_on_non_switch_sends_nothing(mock_send):
    with pytest.raises(ValueError, match="bool value only allowed"):
        server.polynodes_set([{"param": "bpm", "value": True}])
    mock_send.assert_not_called()


def test_polynodes_set_none_value_sends_nothing(mock_send):
    with pytest.raises(ValueError):
        server.polynodes_set([{"param": "bpm", "value": None}])
    mock_send.assert_not_called()


def test_polynodes_set_result_is_valid_json(mock_send):
    result = server.polynodes_set([{"param": "bpm", "value": 120.0}])
    parsed = json.loads(result)
    assert parsed["ok"] is True
    assert parsed["sent"][0]["value"] == 120.0


def test_polynodes_raw(mock_send):
    result = json.loads(server.polynodes_raw("/polynodes/DryWet", 0.5))
    assert result["ok"] is True
    mock_send.assert_called_once_with("/polynodes/DryWet", 0.5)


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_polynodes_raw_rejects_non_finite(mock_send, bad_value):
    with pytest.raises(ValueError, match="finite"):
        server.polynodes_raw("/polynodes/camzoom", bad_value)
    mock_send.assert_not_called()


@pytest.mark.parametrize("bad_value", ["nan", "inf", "-inf"])
def test_polynodes_raw_mcp_path_rejects_non_finite(mock_send, bad_value):
    async def _call():
        with pytest.raises(Exception, match="finite"):
            await server.mcp.call_tool(
                "polynodes_raw",
                {"address": "/polynodes/camzoom", "value": bad_value},
            )

    asyncio.run(_call())
    mock_send.assert_not_called()


def test_osc_client_recreated_on_port_change():
    calls: list[tuple[str, int]] = []

    def fake_client(host: str, port: int) -> MagicMock:
        calls.append((host, port))
        return MagicMock()

    with patch.dict(os.environ, {"POLYNODES_OSC_PORT": "4800"}, clear=False):
        with patch("server.udp_client.SimpleUDPClient", side_effect=fake_client):
            server.reset_osc_client()
            server._get_client()
            assert calls == [("127.0.0.1", 4800)]

            with patch.dict(os.environ, {"POLYNODES_OSC_PORT": "4801"}, clear=False):
                server._get_client()
                assert calls == [
                    ("127.0.0.1", 4800),
                    ("127.0.0.1", 4801),
                ]


def test_catalog_matches_registry_export():
    contents = asyncio.run(server.mcp.read_resource("polynodes://catalog"))
    assert contents[0].content == catalog_json()
