# ⛩️ Omikuji

日本の「おみくじ」を色々な形で実装したリポジトリです。
A collection of different implementations of "omikuji" (Japanese fortune slips).

| ファイル / File | 内容 / Description |
|---|---|
| `Omikuji.py` | ターミナルで動くシンプル版 / Simple terminal-based version |
| `Omikuji_GUI.py` | Tkinterによる簡易GUI版 / Basic GUI version using Tkinter |
| `Omikuji_AI.py` | **Gemini AIがおみくじ内容を生成するGUI版**(このREADMEで解説) / **GUI version where Gemini AI generates the fortune content** (this README covers this version) |

<br>

## 🇯🇵 日本語 (Omikuji_AI.py について)

### 概要
ボタンを押すと、Gemini AIが「電脳神社の神主」になりきって、クスッと笑えるオリジナルのおみくじ結果を生成します。

### 必要なもの
- Python 3.9 以上 (tkinter が使える環境)
- Gemini APIキー ([Google AI Studio](https://aistudio.google.com/) から無料で取得可能)

### セットアップ

1. リポジトリをクローン
   ```bash
   git clone https://github.com/あなたのユーザー名/リポジトリ名.git
   cd リポジトリ名
   ```

2. 仮想環境を作成して有効化 (推奨)
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windowsの場合: venv\Scripts\activate
   ```

3. 必要なパッケージをインストール
   ```bash
   pip install -r requirements.txt
   ```

4. APIキーを環境変数に設定
   ```bash
   export GEMINI_API_KEY="あなたのAPIキー"
   ```
   (Windowsの場合: `set GEMINI_API_KEY=あなたのAPIキー`)

5. 実行
   ```bash
   python3 Omikuji_AI.py
   ```

### macOSユーザーへの注意
標準のPython(特にpyenvや一部のバージョン)では、Tcl/Tkのバージョンの不整合により、ウィンドウが正しく表示されない・ボタンが反応しないことがあります。その場合は以下を試してください。

```bash
brew install python-tk@3.12
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### このリポジトリのファイル構成
```
.
├── Omikuji.py        # ターミナル版
├── Omikuji_GUI.py     # 簡易GUI版
├── Omikuji_AI.py      # Gemini AI生成版 (このREADMEで解説)
├── requirements.txt
├── README.md
└── .gitignore
```

### ライセンス
このプロジェクトは [MIT License](LICENSE) のもとで公開されています。(必要に応じてLICENSEファイルを追加してください)

<br>

---

<br>

## 🇬🇧 English (about `Omikuji_AI.py`)

### Overview
Press the button, and Gemini AI takes on the role of a "priest at a cyber shrine," generating a unique, playful omikuji (fortune slip) reading.

### Requirements
- Python 3.9+ (with tkinter support)
- A Gemini API key (get one for free at [Google AI Studio](https://aistudio.google.com/))

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set your API key as an environment variable
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```
   (On Windows: `set GEMINI_API_KEY=your-api-key-here`)

5. Run the app
   ```bash
   python3 Omikuji_AI.py
   ```

### Note for macOS users
The system/pyenv-installed Python can sometimes link against a mismatched Tcl/Tk version, causing the window to render incorrectly or the button to not respond. If you run into this, try:

```bash
brew install python-tk@3.12
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Repository structure
```
.
├── Omikuji.py         # Terminal version
├── Omikuji_GUI.py     # Basic GUI version
├── Omikuji_AI.py      # Gemini AI-powered version (covered in this README)
├── requirements.txt
├── README.md
└── .gitignore
```

### License
This project is released under the [MIT License](LICENSE). (Add a LICENSE file if needed.)
