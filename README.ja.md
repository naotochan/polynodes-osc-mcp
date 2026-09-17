# polynodes-osc-mcp

[English](README.md)

sonicLAB の [PolyNodes](https://soniclab.net/polynodes/) を OSC 経由で制御するための MCP (Model Context Protocol) サーバーです。

Claude などの AI アシスタントから、自然言語で PolyNodes の空間音響合成パラメータを操作できます。

## 必要環境

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- PolyNodes が OSC を受信している状態（デフォルト `127.0.0.1:4799`）

## セットアップ

### Claude Code

プロジェクトの MCP サーバーに追加:

```bash
claude mcp add polynodes-osc-mcp -- uv run --directory /path/to/polynodes-osc-mcp python server.py
```

または Claude Code の設定に手動で追加:

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

`claude_desktop_config.json` に追加:

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

### OSC 接続

環境変数でホストとポートを変更できます:

| 変数 | デフォルト | 説明 |
|------|-----------|------|
| `POLYNODES_OSC_HOST` | `127.0.0.1` | PolyNodes OSC ホスト |
| `POLYNODES_OSC_PORT` | `4799` | PolyNodes OSC ポート |

## API (v0.2)

以前のパラメータごとのツール一覧は、2 つのツールと 1 つのリソースに置き換えられました:

| 名前 | 種別 | 説明 |
|------|------|------|
| `polynodes_set` | ツール | 複数パラメータを 1 回の OSC バーストでまとめて設定 |
| `polynodes_raw` | ツール | 任意の OSC アドレス/値を送信（エスケープハッチ） |
| `polynodes://catalog` | リソース | パラメータ名・OSC アドレス・範囲・レイヤー要件の JSON カタログ |

パラメータ名や範囲が不明な場合は `polynodes://catalog` を参照してください。レイヤー単位のパラメータ（`gain`、`playback_rate`、`filter_freq` など）には `level`: `macro` / `meso` / `micro` が必要です。スイッチは `0`/`1` または `bool` を受け付けます。

## 使用例

セットアップ後、自然言語で PolyNodes を操作できます:

- 「再生して BPM を 120 に設定して」
- 「ブラックホールをオンにして、マクロの重力を 0.8 にして」
- 「グラニュレーターを有効にして、デュレーションを 500 にして」
- 「マクロの再生レートを 0.5、メソを 2.0 にまとめて設定して」

`polynodes_set` バッチの例:

```json
[
  {"param": "play", "value": 1},
  {"param": "bpm", "value": 120},
  {"param": "blackhole", "value": true},
  {"param": "blackhole_force", "level": "macro", "value": 0.8}
]
```

## 開発

```bash
uv sync --extra dev
pytest
```

## ライセンス

MIT
