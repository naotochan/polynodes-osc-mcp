# polynodes-osc-mcp

[English](README.md)

sonicLAB の [PolyNodes](https://soniclab.net/polynodes/) を OSC 経由で制御するための MCP (Model Context Protocol) サーバーです。

Cursor から、自然言語で PolyNodes の空間音響合成パラメータを操作できます。

**手元での入れ方・パスの話は [LOCAL.md](LOCAL.md)（Cursor 前提の指示書）です。** クラウド側にはクローン先パスが見えないので、MCP 登録はローカルで行ってください。

## 必要環境

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- PolyNodes が OSC を受信している状態（デフォルト `127.0.0.1:4799`）
- Cursor（MCP ホスト。`server.py` は手起動しない）

## セットアップ

手順の本体は [LOCAL.md](LOCAL.md)。要点だけ:

1. このリポジトリを手元にクローンする（`pwd` がインストールパス）
2. PolyNodes を起動する
3. クローン先を `--directory` にしたエントリを `~/.cursor/mcp.json` に追加する（JSON の形は [LOCAL.md](LOCAL.md)）
4. Cursor の Settings → Tools & MCP で緑になるのを確認する
5. Agent チャットで「再生して BPM を 120 にして」などと頼む

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
