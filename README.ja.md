# polynodes-osc-mcp

[English](README.md)

sonicLAB の [PolyNodes](https://soniclab.net/polynodes/) を OSC 経由で制御するための MCP (Model Context Protocol) サーバーです。

Claude などの AI アシスタントから、自然言語で PolyNodes の空間音響合成パラメータを操作できます。

## 必要環境

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- PolyNodes が `127.0.0.1:4799` で OSC を受信している状態

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

## 利用可能なツール (全45種)

| カテゴリ | ツール |
|---|---|
| **トランスポート** | 再生/停止、プリセットスロット (1-10)、BPM (10-300) |
| **ゲイン** | Macro/Meso/Micro ゲイン (-80〜20 dB)、Dry/Wet、ソロ |
| **エンベロープ** | レイヤーごとのアタック/ディケイ時間 (0.01-0.5) |
| **再生レート** | レイヤーごとのレート + 確率的変調範囲 |
| **グラニュレーター** | On/Off、チャンク長 (10-1000)、変調範囲 |
| **バンドパスフィルター** | On/Off、中心周波数 (80-8000 Hz)、レイヤーごとの変調 |
| **コムフィルター** | On/Off、ディレイ、レイヤーごとの変調 |
| **ブラックホール** | On/Off、レイヤーごとの重力 (0-1) |
| **ホワイトホール** | On/Off、レイヤーごとの反射力 (0-1) |
| **リングモジュレーター** | On/Off、レイヤーごとの周波数 (1-3) |
| **ビットクラッシャー** | On/Off、ビット深度 (0-1)、サンプリング範囲 (0-5) |
| **レゾネーター** | On/Off、周波数分布 (1-3)、バランス (0-0.5) |
| **Cuboid FX** | 3つの Cuboid On/Off、レイヤーごとのリターンレベル (1-80) |
| **IsoMorph** | On/Off、freq/amp/res 変調ターゲットと深度 |
| **ナビゲーション** | ランダムトリガー、再配置、Poly Gates |
| **チューニング** | 再生レートとレゾネーターのチューニングスケール切替 |
| **カメラ** | ズーム、回転 |
| **Raw OSC** | 任意の OSC メッセージを直接送信 |

## 使用例

セットアップ後、自然言語で PolyNodes を操作できます:

- 「再生して BPM を 120 に設定して」
- 「ブラックホールをオンにして、マクロの重力を 0.8 にして」
- 「グラニュレーターを有効にして、デュレーションを 500 にして」
- 「全パラメータをランダマイズして」
- 「遅い再生レートと深いリバーブでダークアンビエントなテクスチャを作って」

## ライセンス

MIT
