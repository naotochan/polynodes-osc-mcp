#!/usr/bin/env python3
"""MCP server for PolyNodes OSC control — registry-driven 2-tool API."""

import json
import os
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field
from pythonosc import udp_client

from osc_registry import Change, _ensure_finite, apply_changes, catalog_json

mcp = FastMCP("polynodes_mcp")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4799

_osc_client: udp_client.SimpleUDPClient | None = None
_osc_host: str | None = None
_osc_port: int | None = None


def _osc_settings() -> tuple[str, int]:
    host = os.environ.get("POLYNODES_OSC_HOST", DEFAULT_HOST)
    port = int(os.environ.get("POLYNODES_OSC_PORT", str(DEFAULT_PORT)))
    return host, port


def _get_client() -> udp_client.SimpleUDPClient:
    """Return OSC client, recreating when host or port changes."""
    global _osc_client, _osc_host, _osc_port
    host, port = _osc_settings()
    if _osc_client is None or host != _osc_host or port != _osc_port:
        _osc_client = udp_client.SimpleUDPClient(host, port)
        _osc_host = host
        _osc_port = port
    return _osc_client


def _send_osc(address: str, value: float) -> None:
    _get_client().send_message(address, float(value))


def reset_osc_client() -> None:
    """Clear cached client (for tests)."""
    global _osc_client, _osc_host, _osc_port
    _osc_client = None
    _osc_host = None
    _osc_port = None


@mcp.resource(
    "polynodes://catalog",
    mime_type="application/json",
    description="Param names, OSC addresses, ranges, and which params need level.",
)
def polynodes_catalog() -> str:
    return catalog_json()


@mcp.tool(name="polynodes_set", structured_output=False)
def polynodes_set(
    changes: Annotated[list[Change], Field(description="Batch of {param, value, level?}")],
) -> str:
    """Set one or more PolyNodes params in one OSC burst. Read polynodes://catalog for names/ranges. Per-layer params need level=macro|meso|micro. Switches accept 0/1 or bool."""
    resolved = apply_changes(changes)
    sent: list[dict[str, object]] = []
    for msg in resolved:
        _send_osc(msg["address"], msg["value"])
        sent.append({"address": msg["address"], "value": msg["value"]})
    return json.dumps({"ok": True, "sent": sent}, separators=(",", ":"), allow_nan=False)


@mcp.tool(name="polynodes_raw", structured_output=False)
def polynodes_raw(
    address: Annotated[str, Field(description="Full OSC address path")],
    value: Annotated[float, Field(description="Float value to send")],
) -> str:
    """Send a raw OSC message to PolyNodes. Escape hatch for any address."""
    fval = float(value)
    _ensure_finite(fval, "value")
    _send_osc(address, fval)
    return json.dumps(
        {"ok": True, "sent": {"address": address, "value": fval}},
        separators=(",", ":"),
        allow_nan=False,
    )


if __name__ == "__main__":
    mcp.run()
