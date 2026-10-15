import os
import threading
import tkinter as tk
from pathlib import Path

try:
    from google import genai
except ImportError:
    genai = None

# ==========================================
# 1. settings & environment
# ==========================================
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback to load .env if python-dotenv is not installed
    env_file = Path(__file__).resolve().parent / ".env"
    if env_file.is_file():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = val

API_KEY = os.environ.get("GEMINI_API_KEY")


def get_friendly_error_message(error: Exception) -> str:
    """API通信エラーを分かりやすいメッセージに変換する"""
    err_str = str(error)
    if "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
        return "APIキーが無効です。有効なGemini APIキーを設定してください。"
    elif "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
        return "API利用制限(クォータ)に達しました。時間をおいて再試行してください。"
    elif "connection" in err_str.lower() or "timeout" in err_str.lower():
        return "ネットワーク通信エラーが発生しました。接続を確認してください。"
    return f"通信エラー ({type(error).__name__})"


def generate_offline_fallback(reason: str) -> str:
    """APIが利用できない場合に Omikuji.py を利用したオフライン結果を生成する"""
    try:
        from Omikuji import draw_fortune
        luck, message = draw_fortune()
    except Exception:
        luck, message = "吉", "前向きな気持ちで過ごすと良いことがあります。"

    return (
        "⛩️ 【電脳神社・オフラインおみくじ】 ⛩️\n\n"
        "※ AIとの通信ができなかったため、境内の伝統的なおみくじを引きました。\n"
        f"（案内: {reason}）\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"【運勢】{luck}\n"
        f"【お告げ】{message}\n"
        "【電脳神様からのひとこと】\n"
        "「オフラインでも運気は巡っておるぞ。設定を確認してまた参拝するのじゃ。」\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 ヒント: .env ファイルに GEMINI_API_KEY=あなたのキー を設定すると、"
        "AIによるオリジナルおみくじが有効になります。"
    )


def generate_omikuji():
    """
    バックグラウンドスレッドで実行する処理。
    ここでは API 通信を行い、UI の更新は root.after 経由で行う。
    """
    if genai is None:
        fallback = generate_offline_fallback(
            "google-genai パッケージが未インストールです (pip install -r requirements.txt を実行してください)"
        )
        root.after(0, update_result, fallback)
        return

    api_key = os.environ.get("GEMINI_API_KEY") or API_KEY
    if not api_key:
        fallback = generate_offline_fallback(
            "GEMINI_API_KEY が未設定です (.env または環境変数を確認してください)"
        )
        root.after(0, update_result, fallback)
        return

    try:
        client = genai.Client(api_key=api_key)
        prompt = """
        あなたは電脳神社の神主です。引いた人をクスッとさせる、ユニークなおみくじ結果を生成してください。
        以下のフォーマットで、簡潔に出力してください。

        【運勢】(大吉、中吉、凶だけでなく、IT用語を交えた独自の運勢でも可)
        【願事】
        【仕事・学業】
        【恋愛】
        【電脳神様からのひとこと】
        """

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        root.after(0, update_result, response.text)

    except Exception as e:
        reason = get_friendly_error_message(e)
        fallback = generate_offline_fallback(reason)
        root.after(0, update_result, fallback)


def update_result(text):
    """UI更新専用の関数。メインスレッドから呼ばれる。"""
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, text)
    draw_button.config(state=tk.NORMAL)


def on_button_click():
    """ボタンが押されたときの処理(メインスレッドで実行)"""
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "⛩️ 神様(AI)にお伺いを立てています...\n(生成中)")
    draw_button.config(state=tk.DISABLED)

    thread = threading.Thread(target=generate_omikuji, daemon=True)
    thread.start()


# ==========================================
# 2. create the main window and widgets
# ==========================================
root = tk.Tk()
root.title("生成AI おみくじ")
root.geometry("450x600")

# base color for the window
BG_COLOR = "#333333"
root.configure(bg=BG_COLOR)

# Title label
title_label = tk.Label(root, text="⛩️ 生成AI おみくじ ⛩️", font=("Helvetica", 20, "bold"),
                        bg=BG_COLOR, fg="#ffcc00")
title_label.pack(pady=20)

# button
draw_button = tk.Button(root, text="おみくじを引く！", font=("Helvetica", 16, "bold"),
                         command=on_button_click, highlightbackground=BG_COLOR)
draw_button.pack(pady=10)

# frame for the text box and scrollbar
text_frame = tk.Frame(root, bg=BG_COLOR)
text_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# text box for displaying the result
result_text = tk.Text(text_frame, wrap=tk.WORD, font=("Helvetica", 14),
                       bg="#ffffff", fg="#000000",
                       highlightthickness=0,
                       insertbackground="black")
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# add a scrollbar to the text box
scrollbar = tk.Scrollbar(text_frame, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# first message
result_text.insert(tk.END, "ボタンを押すと、ここに結果が表示されます。")

root.update_idletasks()
root.geometry(root.geometry())

if __name__ == "__main__":
    root.mainloop()