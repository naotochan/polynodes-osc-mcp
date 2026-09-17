# ローカル指示書（Cursor）

このリポジトリの MCP サーバーは **手元のマシン** で動かす。クラウドエージェントはクローン先パスも PolyNodes も見えない。インストール・登録・動作確認は全部ローカルでやる。

ホストは **Cursor**。Claude Code は使わない。

---

## パスの区別

| 名前 | 意味 | 例 |
|------|------|-----|
| インストールパス | `server.py` があるクローン先。MCP が起動する場所 | `~/src/polynodes-osc-mcp` |
| 作業パス | 今 Cursor で開いているプロジェクト。cwd はだいたいここ | 別の曲用リポジトリでもよい |
| OSC 先 | PolyNodes の待ち受け。パスではない | `127.0.0.1:4799` |

MCP の `--directory` には **インストールパス** を書く。作業パスを書かない。

---

## 0. 手でサーバーを上げない

`uv run python server.py` をターミナルで常駐させない。stdio MCP は Cursor が起動する。手起動は入力待ちで止まったように見えるだけで、Cursor からは使えない。

---

## 1. クローン

```bash
git clone https://github.com/naotochan/polynodes-osc-mcp.git
cd polynodes-osc-mcp
pwd
```

`pwd` の出力がインストールパス。以降の `/実際のクローン先/polynodes-osc-mcp` をこれに置き換える。

SSH なら:

```bash
git clone git@github.com:naotochan/polynodes-osc-mcp.git
cd polynodes-osc-mcp
pwd
```

すでにクローン済みなら、リポジトリの親ディレクトリから:

```bash
cd polynodes-osc-mcp
git checkout main
git pull origin main
pwd
```

必要なら [uv](https://docs.astral.sh/uv/) を入れておく。`which uv` のパスは後で使う。

---

## 2. PolyNodes

sonicLAB の PolyNodes を起動し、OSC 受信が `127.0.0.1:4799` であること。ここが落ちていると MCP は「送った」と返すだけで音は変わらない。

---

## 3. Cursor に MCP を登録

どのプロジェクトからでも叩くなら **グローバル** `~/.cursor/mcp.json`（Windows は `%USERPROFILE%\.cursor\mcp.json`）。

すでに `mcpServers` があるファイルなら、下のキーを **追加** する。ファイル全体を上書きしない。

```json
{
  "mcpServers": {
    "polynodes-osc-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/実際のクローン先/polynodes-osc-mcp",
        "python",
        "server.py"
      ]
    }
  }
}
```

Dock から起動した Cursor が `uv` を見つけないときは、`command` を `which uv` の絶対パスにする（例: `/Users/you/.local/bin/uv`）。

OSC のホストやポートを変えるときは、シェルの `export` ではなく同じエントリの `env` に書く（Cursor が起こすプロセスにはシェルの環境が届かない）。

```json
"env": {
  "POLYNODES_OSC_HOST": "127.0.0.1",
  "POLYNODES_OSC_PORT": "4799"
}
```

Windows のクローン先は JSON 内でバックスラッシュを二重にする（例: `"C:\\\\Users\\\\you\\\\src\\\\polynodes-osc-mcp"`）。スラッシュ `"C:/Users/you/src/polynodes-osc-mcp"` でもよい。

このリポジトリ自体を Cursor で開いているときだけ、**プロジェクト** `.cursor/mcp.json`（リポジトリ直下）に `${workspaceFolder}` を使ってよい。グローバルな `~/.cursor/mcp.json` には書かない（そこでの workspace は `~/.cursor` になる）。

```json
{
  "mcpServers": {
    "polynodes-osc-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "${workspaceFolder}", "python", "server.py"]
    }
  }
}
```

別プロジェクトを開いた状態で PolyNodes を操作するなら、グローバル＋絶対パスの方。

Cursor の Settings → Tools & MCP で `polynodes-osc-mcp` を有効化し、緑になるまで待つ。だめならエージェント / Cursor を開き直す。

---

## 4. 動作確認

Agent チャットで:

- 「再生して BPM を 120 にして」
- 「ブラックホールをオン、マクロの重力 0.8」
- 「マクロ再生レート 0.5 とドライウェット 0.7 をまとめて」

Cursor が `polynodes_set` を呼ぶ。パラメータ名が不明なら `polynodes://catalog` を読む。

レイヤー付き（`gain` / `playback_rate` / `filter_freq` など）は `level`: `macro` | `meso` | `micro` が必要。

---

## 5. うまくいかないとき

| 症状 | 見るとこ |
|------|----------|
| MCP が赤 / ツールが無い | JSON の文法、クローン先パス、`command` が `uv` の絶対パスか |
| ツールは動くが音が変わらない | PolyNodes 起動と OSC ポート。MCP は UDP を投げるだけで応答は見ない |
| ターミナルで `server.py` が止まったまま | 手起動している。止めて Cursor に任せる |
| `level required` | レイヤー付きパラメータに `macro` / `meso` / `micro` が無い |
| `--directory` にクラウドのパスを書いた | 手元ではない。このマシンで `pwd` した値に直す |

開発用（任意）:

```bash
cd /実際のクローン先/polynodes-osc-mcp
uv sync --extra dev
uv run pytest
```
