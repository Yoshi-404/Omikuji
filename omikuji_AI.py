import tkinter as tk
import threading
from google import genai

# ==========================================
# 1. settings
# ==========================================
API_KEY = "GEMINI_API_KEY"
client = genai.Client(api_key=API_KEY)


def generate_omikuji():
    """
    バックグラウンドスレッドで実行する処理。
    ここでは API 通信のみを行い、UI の更新は行わない
    (Tkinter は別スレッドから直接 UI をいじると Mac で不安定になるため)。
    """
    # print("[DEBUG] generate_omikuji が呼ばれました")  # for debugging
    try:
        prompt = """
        あなたは電脳神社の神主です。引いた人をクスッとさせる、ユニークなおみくじ結果を生成してください。
        以下のフォーマットで、簡潔に出力してください。

        【運勢】(大吉、中吉、凶だけでなく、IT用語を交えた独自の運勢でも可)
        【願事】
        【仕事・学業】
        【恋愛】
        【電脳神様からのひとこと】
        """

        # print("[DEBUG] API呼び出し開始")  # for debugging
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        # print("[DEBUG] API呼び出し成功:", response.text[:50])  # for debugging
        root.after(0, update_result, response.text)

    except Exception as e:
        # print("[DEBUG] エラー発生:", e)  # for debugging
        root.after(0, update_result, f"エラーが発生しました。\n{e}")


def update_result(text):
    """
    UI更新専用の関数。必ずメインスレッド(root.after経由)から呼ばれる。
    """
    # print("[DEBUG] update_result が呼ばれました")  # for debugging
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, text)
    draw_button.config(state=tk.NORMAL)


def on_button_click():
    """ボタンが押されたときの処理(メインスレッドで実行)"""
    # print("[DEBUG] ボタンがクリックされました")  # for debugging
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
                        bg=BG_COLOR, fg="#ffcc00")  # color: gold
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
                       bg="#ffffff", fg="#000000",       # white background, black text
                       highlightthickness=0,             # correct highlight thickness for Mac
                       insertbackground="black")         # cursor color
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# add a scrollbar to the text box
scrollbar = tk.Scrollbar(text_frame, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# first message
result_text.insert(tk.END, "ボタンを押すと、ここに結果が表示されます。")

# correct the highlight thickness for Mac
root.update_idletasks()
root.geometry(root.geometry())  # reset the geometry to apply the highlight thickness correction

# print("[DEBUG] mainloop開始直前")  # for debugging

# launch the Tkinter event loop
root.mainloop()